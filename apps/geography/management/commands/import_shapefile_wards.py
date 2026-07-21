"""
Import ward data from a Kenya wards ESRI Shapefile (.dbf attribute table).

Usage:
    python manage.py import_shapefile_wards --dbf /path/to/kenya_wards.dbf

The command reads the DBF file without any GIS/GDAL dependency, matches each
record to existing County and Constituency rows using normalised name lookup,
then creates or updates Ward rows.  Unmatched records are reported at the end.

Shapefile field → model mapping
  county    → County.county_name   (case-insensitive)
  subcounty → Constituency.constituency_name (case-insensitive; "Sub County"
               suffix is stripped before matching)
  ward      → Ward.ward_name
  uid       → Ward.ward_code       (unique key used for upsert)
"""
import struct
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.geography.models import County, Constituency, Ward


# ---------------------------------------------------------------------------
# DBF reader (pure Python — no external deps)
# ---------------------------------------------------------------------------

def _read_dbf(path: str):
    """Yield dicts for each non-deleted record in a dBASE III/IV .dbf file."""
    with open(path, "rb") as f:
        f.read(4)                                           # version + date
        num_records = struct.unpack("<I", f.read(4))[0]
        header_size = struct.unpack("<H", f.read(2))[0]
        record_size = struct.unpack("<H", f.read(2))[0]
        f.read(20)                                          # reserved

        fields = []
        while True:
            chunk = f.read(32)
            if chunk[0:1] == b"\r":
                break
            name = chunk[0:11].split(b"\x00")[0].decode("utf-8", errors="replace")
            length = chunk[16]
            fields.append((name, length))

        f.seek(header_size)
        for _ in range(num_records):
            raw = f.read(record_size)
            if raw[0:1] == b"*":        # deleted record
                continue
            offset = 1
            row = {}
            for name, length in fields:
                row[name] = raw[offset : offset + length].decode(
                    "utf-8", errors="replace"
                ).strip()
                offset += length
            yield row


# ---------------------------------------------------------------------------
# Name normalisation helpers
# ---------------------------------------------------------------------------

_SUBCOUNTY_SUFFIXES = (
    " sub county", " subcounty", " sub-county",
    " constituency", " division",
)


# County name aliases: shapefile spelling → canonical DB spelling
# Add more entries here if new mismatches are found.
COUNTY_ALIASES: dict[str, str] = {
    "elgeyo-marakwet": "elgeyo marakwet",
    "tharaka-nithi":   "tharaka nithi",
    "muranga":         "murang'a",
    "taita-taveta":    "taita taveta",
    "homa-bay":        "homa bay",
    "uasin-gishu":     "uasin gishu",
    "trans-nzoia":     "trans nzoia",
    "west-pokot":      "west pokot",
}


def _norm(text: str) -> str:
    """Lowercase + collapse whitespace."""
    return " ".join(text.lower().split())


def _norm_county(text: str) -> str:
    """Normalise county name, resolving known aliases."""
    n = _norm(text)
    return COUNTY_ALIASES.get(n, n)


def _norm_subcounty(text: str) -> str:
    s = _norm(text)
    for suffix in _SUBCOUNTY_SUFFIXES:
        if s.endswith(suffix):
            s = s[: -len(suffix)].strip()
    return s


# ---------------------------------------------------------------------------
# Management command
# ---------------------------------------------------------------------------

class Command(BaseCommand):
    help = "Import/upsert ward data from a Kenya wards shapefile (.dbf)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dbf",
            default="/home/seven/Downloads/kenya_wards/Kenya_Wards/kenya_wards.dbf",
            help="Path to the kenya_wards.dbf file",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and report without writing to the database",
        )

    def handle(self, *args, **options):
        dbf_path = options["dbf"]
        dry_run = options["dry_run"]

        if not os.path.exists(dbf_path):
            raise CommandError(f"DBF file not found: {dbf_path}")

        self.stdout.write(f"Reading {dbf_path} …")

        # Build look-up indices from DB (case-insensitive)
        county_map = {_norm(c.county_name): c for c in County.objects.all()}
        # constituency_map keyed by (normalised_name, county_pk) → Constituency
        const_map: dict[tuple, Constituency] = {}
        for con in Constituency.objects.select_related("county").all():
            key = (_norm(con.constituency_name), con.county_id)
            const_map[key] = con
            # also index stripped version
            stripped = _norm_subcounty(con.constituency_name)
            const_map[(_norm(stripped), con.county_id)] = con

        created = updated = skipped = 0
        unmatched_counties: set[str] = set()
        unmatched_constituencies: set[str] = set()

        records = list(_read_dbf(dbf_path))
        self.stdout.write(f"Loaded {len(records)} records from shapefile.")

        with transaction.atomic():
            for row in records:
                county_raw = row.get("county", "")
                subcounty_raw = row.get("subcounty", "")
                ward_raw = row.get("ward", "")
                uid = row.get("uid", "")

                if not ward_raw or not uid:
                    skipped += 1
                    continue

                # --- match county ---
                county = county_map.get(_norm_county(county_raw))
                if county is None:
                    unmatched_counties.add(county_raw)
                    skipped += 1
                    continue

                # --- match constituency (try raw name, then stripped) ---
                const_key_raw = (_norm(subcounty_raw), county.county_id)
                const_key_stripped = (_norm_subcounty(subcounty_raw), county.county_id)
                constituency = const_map.get(const_key_raw) or const_map.get(const_key_stripped)

                if constituency is None:
                    unmatched_constituencies.add(f"{subcounty_raw} (in {county_raw})")
                    skipped += 1
                    continue

                # --- upsert ward ---
                if not dry_run:
                    ward, was_created = Ward.objects.update_or_create(
                        ward_code=uid,
                        defaults={
                            "ward_name": ward_raw.title(),
                            "constituency": constituency,
                        },
                    )
                    if was_created:
                        created += 1
                    else:
                        updated += 1
                else:
                    created += 1   # count as "would create" in dry-run

        # --- summary ---
        mode = "DRY RUN — " if dry_run else ""
        self.stdout.write(self.style.SUCCESS(
            f"\n{mode}Done!"
            f"\n  Created : {created}"
            f"\n  Updated : {updated}"
            f"\n  Skipped : {skipped}"
        ))

        if unmatched_counties:
            self.stdout.write(self.style.WARNING(
                f"\nUnmatched counties ({len(unmatched_counties)}):"
            ))
            for name in sorted(unmatched_counties):
                self.stdout.write(f"  - {name}")

        if unmatched_constituencies:
            self.stdout.write(self.style.WARNING(
                f"\nUnmatched constituencies ({len(unmatched_constituencies)}) — "
                "these wards were skipped:"
            ))
            for name in sorted(unmatched_constituencies)[:30]:
                self.stdout.write(f"  - {name}")
            if len(unmatched_constituencies) > 30:
                self.stdout.write(
                    f"  … and {len(unmatched_constituencies) - 30} more"
                )
