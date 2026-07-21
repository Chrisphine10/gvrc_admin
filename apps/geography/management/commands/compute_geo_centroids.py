"""
Populate centroid_lat, centroid_lng, bbox_north/south/east/west on Ward,
Constituency, and County from the Kenya wards shapefile.

Three passes:
  Pass 1 — Wards: read per-record bounding boxes from .shp, match by
           ward_code == uid from .dbf, bulk_update matched rows.
  Pass 2 — Constituencies: ORM aggregation over their wards.
  Pass 3 — Counties: ORM aggregation over their constituencies.

Usage:
    python manage.py compute_geo_centroids
    python manage.py compute_geo_centroids --shp /path/to/kenya_wards.shp
    python manage.py compute_geo_centroids --wards-only
    python manage.py compute_geo_centroids --dry-run
"""
import struct
import os
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Avg, Min, Max

from apps.geography.models import County, Constituency, Ward

DEFAULT_SHP = "/home/seven/Downloads/kenya_wards/Kenya_Wards/kenya_wards.shp"
DEFAULT_DBF = "/home/seven/Downloads/kenya_wards/Kenya_Wards/kenya_wards.dbf"


# ---------------------------------------------------------------------------
# Pure-Python shapefile readers (no GIS dependencies needed)
# ---------------------------------------------------------------------------

def _read_dbf_uid_map(dbf_path: str) -> dict[int, str]:
    """Return {record_index: uid} from the DBF attribute table."""
    with open(dbf_path, "rb") as f:
        f.read(4)
        num_records = struct.unpack("<I", f.read(4))[0]
        header_size = struct.unpack("<H", f.read(2))[0]
        record_size = struct.unpack("<H", f.read(2))[0]
        f.read(20)

        fields = []
        while True:
            chunk = f.read(32)
            if chunk[0:1] == b"\r":
                break
            name = chunk[0:11].split(b"\x00")[0].decode("utf-8", errors="replace")
            length = chunk[16]
            fields.append((name, length))

        uid_idx = next(
            (i for i, (n, _) in enumerate(fields) if n == "uid"), None
        )
        if uid_idx is None:
            raise CommandError("DBF has no 'uid' field — wrong shapefile?")

        f.seek(header_size)
        uid_map: dict[int, str] = {}
        for rec_idx in range(num_records):
            raw = f.read(record_size)
            if raw[0:1] == b"*":        # deleted
                continue
            offset = 1
            for i, (name, length) in enumerate(fields):
                val = raw[offset : offset + length].decode(
                    "utf-8", errors="replace"
                ).strip()
                if i == uid_idx:
                    uid_map[rec_idx] = val
                    break
                offset += length
        return uid_map


def _read_shp_bboxes(shp_path: str) -> list[tuple | None]:
    """
    Return a list of (xmin, ymin, xmax, ymax) per record (None for nulls).
    Reads only the per-record bounding box — no polygon vertex parsing needed.
    """
    bboxes: list[tuple | None] = []
    with open(shp_path, "rb") as f:
        f.read(100)                     # skip 100-byte file header
        while True:
            hdr = f.read(8)
            if len(hdr) < 8:
                break
            content_len = struct.unpack(">I", hdr[4:8])[0]
            content = f.read(content_len * 2)
            shape_type = struct.unpack("<I", content[0:4])[0]
            if shape_type == 5:         # Polygon
                bbox = struct.unpack("<4d", content[4:36])
                bboxes.append(bbox)     # (xmin, ymin, xmax, ymax)
            else:
                bboxes.append(None)
    return bboxes


# ---------------------------------------------------------------------------
# Command
# ---------------------------------------------------------------------------

class Command(BaseCommand):
    help = (
        "Compute centroid lat/lng and bounding boxes for Ward, Constituency, "
        "and County from the Kenya wards shapefile."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--shp",
            default=DEFAULT_SHP,
            help="Path to kenya_wards.shp (default: %(default)s)",
        )
        parser.add_argument(
            "--dbf",
            default=DEFAULT_DBF,
            help="Path to kenya_wards.dbf (default: %(default)s)",
        )
        parser.add_argument(
            "--wards-only",
            action="store_true",
            help="Only update wards; skip constituency/county roll-up.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and report counts without writing to the database.",
        )

    # ------------------------------------------------------------------

    def handle(self, *args, **options):
        shp_path = options["shp"]
        dbf_path = options["dbf"]
        dry_run = options["dry_run"]
        wards_only = options["wards_only"]

        for path in (shp_path, dbf_path):
            if not os.path.exists(path):
                raise CommandError(f"File not found: {path}")

        self.stdout.write(f"Reading shapefile …  {shp_path}")

        uid_map = _read_dbf_uid_map(dbf_path)
        bboxes = _read_shp_bboxes(shp_path)

        if len(uid_map) != len(bboxes):
            self.stdout.write(
                self.style.WARNING(
                    f"DBF rows ({len(uid_map)}) ≠ SHP records ({len(bboxes)}); "
                    "processing min(both)."
                )
            )

        # Build uid → (centroid_lat, centroid_lng, bbox_*) lookup
        uid_to_geo: dict[str, dict] = {}
        for rec_idx, uid in uid_map.items():
            if rec_idx >= len(bboxes):
                continue
            bbox = bboxes[rec_idx]
            if bbox is None or not uid:
                continue
            xmin, ymin, xmax, ymax = bbox
            uid_to_geo[uid] = {
                "centroid_lat": Decimal(str(round((ymin + ymax) / 2, 7))),
                "centroid_lng": Decimal(str(round((xmin + xmax) / 2, 7))),
                "bbox_north":   Decimal(str(round(ymax, 7))),
                "bbox_south":   Decimal(str(round(ymin, 7))),
                "bbox_east":    Decimal(str(round(xmax, 7))),
                "bbox_west":    Decimal(str(round(xmin, 7))),
            }

        self.stdout.write(f"Shapefile has {len(uid_to_geo)} usable ward records.")

        # --- Pass 1: update wards ---
        ward_qs = Ward.objects.filter(ward_code__in=uid_to_geo.keys())
        wards_to_update = []
        for ward in ward_qs:
            geo = uid_to_geo[ward.ward_code]
            for field, value in geo.items():
                setattr(ward, field, value)
            wards_to_update.append(ward)

        geo_fields = [
            "centroid_lat", "centroid_lng",
            "bbox_north", "bbox_south", "bbox_east", "bbox_west",
        ]

        if not dry_run:
            with transaction.atomic():
                Ward.objects.bulk_update(wards_to_update, geo_fields, batch_size=500)
        self.stdout.write(
            self.style.SUCCESS(
                f"Pass 1 — {'Would update' if dry_run else 'Updated'} "
                f"{len(wards_to_update)} wards."
            )
        )

        if wards_only:
            self.stdout.write("--wards-only set; skipping constituency/county roll-up.")
            return

        if dry_run:
            self.stdout.write(
                "Pass 2/3 — dry-run: would aggregate constituencies and counties."
            )
            return

        # --- Pass 2: constituencies aggregated from their wards ---
        const_qs = Constituency.objects.filter(
            ward__centroid_lat__isnull=False
        ).distinct().annotate(
            _clat=Avg("ward__centroid_lat"),
            _clng=Avg("ward__centroid_lng"),
            _bn=Max("ward__bbox_north"),
            _bs=Min("ward__bbox_south"),
            _be=Max("ward__bbox_east"),
            _bw=Min("ward__bbox_west"),
        )

        consts_to_update = []
        for con in const_qs:
            con.centroid_lat = Decimal(str(round(float(con._clat), 7)))
            con.centroid_lng = Decimal(str(round(float(con._clng), 7)))
            con.bbox_north   = Decimal(str(round(float(con._bn), 7)))
            con.bbox_south   = Decimal(str(round(float(con._bs), 7)))
            con.bbox_east    = Decimal(str(round(float(con._be), 7)))
            con.bbox_west    = Decimal(str(round(float(con._bw), 7)))
            consts_to_update.append(con)

        with transaction.atomic():
            Constituency.objects.bulk_update(consts_to_update, geo_fields, batch_size=200)
        self.stdout.write(
            self.style.SUCCESS(
                f"Pass 2 — Updated {len(consts_to_update)} constituencies."
            )
        )

        # --- Pass 3: counties aggregated from their constituencies ---
        county_qs = County.objects.filter(
            constituency__centroid_lat__isnull=False
        ).distinct().annotate(
            _clat=Avg("constituency__centroid_lat"),
            _clng=Avg("constituency__centroid_lng"),
            _bn=Max("constituency__bbox_north"),
            _bs=Min("constituency__bbox_south"),
            _be=Max("constituency__bbox_east"),
            _bw=Min("constituency__bbox_west"),
        )

        counties_to_update = []
        for county in county_qs:
            county.centroid_lat = Decimal(str(round(float(county._clat), 7)))
            county.centroid_lng = Decimal(str(round(float(county._clng), 7)))
            county.bbox_north   = Decimal(str(round(float(county._bn), 7)))
            county.bbox_south   = Decimal(str(round(float(county._bs), 7)))
            county.bbox_east    = Decimal(str(round(float(county._be), 7)))
            county.bbox_west    = Decimal(str(round(float(county._bw), 7)))
            counties_to_update.append(county)

        with transaction.atomic():
            County.objects.bulk_update(counties_to_update, geo_fields, batch_size=50)
        self.stdout.write(
            self.style.SUCCESS(
                f"Pass 3 — Updated {len(counties_to_update)} counties."
            )
        )

        self.stdout.write(self.style.SUCCESS("\nAll done!"))
