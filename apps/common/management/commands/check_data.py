"""Read-only consistency report for the Hodi database.

    python manage.py check_data              # report
    python manage.py check_data --examples 10
    python manage.py check_data --strict     # exit 1 when any ERROR is found

Nothing is changed. ERROR = data that breaks a page or the app; WARN = data a
person should look at; INFO = numbers worth knowing.
"""

import os
import re
from collections import Counter

from django.core.management.base import BaseCommand
from django.db.models import Count, Q
from django.utils import timezone

# Kenya's bounding box with a small margin. A coordinate outside it puts the
# facility in the sea or another country on the map.
KENYA_LAT = (-4.9, 5.1)
KENYA_LNG = (33.8, 42.0)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Command(BaseCommand):
    help = "Report data consistency problems (read-only)."

    def add_arguments(self, parser):
        parser.add_argument("--examples", type=int, default=5, help="Example ids to show per finding.")
        parser.add_argument("--strict", action="store_true", help="Exit with status 1 if any ERROR is found.")

    def handle(self, *args, examples=5, strict=False, **opts):
        self.n = examples
        self.errors = 0
        self.warnings = 0
        for section in (self.geography, self.facilities, self.coordinates, self.contacts,
                        self.users, self.files, self.settings_rows, self.sms):
            section()
        self.stdout.write("")
        self.stdout.write(f"Summary: {self.errors} error(s), {self.warnings} warning(s).")
        if strict and self.errors:
            raise SystemExit(1)

    # ------------------------------------------------------------- output
    def head(self, title):
        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING(title))

    def report(self, level, text, ids=()):
        ids = list(ids)
        tail = f"  e.g. {', '.join(str(i) for i in ids[: self.n])}" if ids else ""
        if level == "ERROR":
            self.errors += 1
            self.stdout.write(self.style.ERROR(f"  ERROR {text}{tail}"))
        elif level == "WARN":
            self.warnings += 1
            self.stdout.write(self.style.WARNING(f"  WARN  {text}{tail}"))
        else:
            self.stdout.write(f"  INFO  {text}{tail}")

    def dupes(self, qs, fields, label, level="WARN"):
        rows = list(qs.values(*fields).annotate(n=Count("pk")).filter(n__gt=1).order_by("-n"))
        if rows:
            extra = sum(r["n"] - 1 for r in rows)
            sample = [" / ".join(str(r[f]) for f in fields) + f" x{r['n']}" for r in rows]
            self.report(level, f"{len(rows)} {label} appear more than once ({extra} extra rows)", sample)

    # ------------------------------------------------------------ sections
    def geography(self):
        from apps.geography.models import Constituency, County, Ward

        self.head("Geography")
        self.report("INFO", f"{County.objects.count()} counties, {Constituency.objects.count()} constituencies, "
                            f"{Ward.objects.count()} wards (Kenya has 47 / 290 / 1,450)")
        self.dupes(County.objects.all(), ["county_name"], "county names")
        self.dupes(Constituency.objects.all(), ["county__county_name", "constituency_name"],
                   "constituency names within a county")
        self.dupes(Ward.objects.all(), ["constituency__constituency_name", "ward_name"],
                   "ward names within a constituency")
        unused_wards = Ward.objects.filter(facility__isnull=True).count()
        self.report("INFO", f"{unused_wards} wards have no facility")

    def facilities(self):
        from apps.facilities.models import Facility

        self.head("Facilities")
        qs = Facility.objects.all()
        total = qs.count()
        active = qs.filter(is_active=True).count()
        self.report("INFO", f"{total} facilities, {active} active")
        blank_code = qs.filter(facility_code="").values_list("pk", flat=True)
        if blank_code:
            self.report("ERROR", f"{len(blank_code)} facilities have an empty-string facility_code "
                                 "(must be NULL; migration facilities.0005 fixes this)", blank_code)
        self.dupes(qs.filter(is_active=True), ["ward__ward_name", "facility_name"],
                   "active facility names within the same ward")
        for rel, label in (("facilitycoordinate", "a map location"),
                           ("facilitycontact", "a contact"),
                           ("facilityservice", "a service"),
                           ("facilitygbvcategory", "a GBV category")):
            ids = qs.filter(is_active=True).filter(**{f"{rel}__isnull": True}).values_list("pk", flat=True)
            if ids:
                level = "WARN" if rel in ("facilitycoordinate", "facilitygbvcategory") else "INFO"
                self.report(level, f"{len(ids)} active facilities have no {label}", ids)

    def coordinates(self):
        from apps.facilities.models import FacilityCoordinate

        self.head("Map locations")
        qs = FacilityCoordinate.objects.filter(is_active=True)
        outside = qs.exclude(latitude__range=KENYA_LAT, longitude__range=KENYA_LNG)
        zero = qs.filter(latitude=0, longitude=0)
        swapped = outside.filter(latitude__range=KENYA_LNG, longitude__range=KENYA_LAT)
        if zero.exists():
            self.report("ERROR", f"{zero.count()} locations are 0,0 (the Gulf of Guinea)",
                        zero.values_list("facility_id", flat=True))
        if swapped.exists():
            self.report("ERROR", f"{swapped.count()} locations look like latitude and longitude swapped",
                        swapped.values_list("facility_id", flat=True))
        rest = outside.exclude(pk__in=zero.values("pk")).exclude(pk__in=swapped.values("pk"))
        if rest.exists():
            self.report("ERROR", f"{rest.count()} locations fall outside Kenya",
                        rest.values_list("facility_id", flat=True))
        multi = (qs.values("facility_id").annotate(n=Count("pk")).filter(n__gt=1)
                 .values_list("facility_id", flat=True))
        if multi:
            self.report("WARN", f"{len(multi)} facilities have more than one active location "
                                "(the map shows the first)", multi)
        stacked = list(qs.values("latitude", "longitude").annotate(n=Count("facility", distinct=True))
                       .filter(n__gt=1).order_by("-n")[:50])
        if stacked:
            sample = [f"{r['latitude']},{r['longitude']} x{r['n']}" for r in stacked]
            self.report("INFO", f"{len(stacked)}{'+' if len(stacked) == 50 else ''} points hold several "
                                "facilities (shared building or a placeholder location)", sample)

    def contacts(self):
        from apps.facilities.models import FacilityContact
        from apps.sms.services import is_sendable_phone

        self.head("Facility contacts")
        qs = FacilityContact.objects.filter(is_active=True).select_related("contact_type")
        kinds = Counter()
        bad_phone, bad_email, mobiles = [], [], 0
        for c in qs.iterator():
            kind = (c.contact_type.type_name or "").lower()
            value = (c.contact_value or "").strip()
            kinds[c.contact_type.type_name] += 1
            if "mail" in kind:
                if not EMAIL_RE.match(value):
                    bad_email.append(c.pk)
            elif any(w in kind for w in ("phone", "mobile", "tel", "hotline", "whatsapp", "sms")):
                digits = re.sub(r"\D", "", value)
                if not 3 <= len(digits) <= 13:  # 3-digit short codes such as 999 / 1195 are valid
                    bad_phone.append(c.pk)
                elif is_sendable_phone(value):
                    mobiles += 1
        self.report("INFO", f"{sum(kinds.values())} active contacts: "
                            + ", ".join(f"{k} {v}" for k, v in kinds.most_common()))
        self.report("INFO", f"{mobiles} are Kenyan mobile numbers that bulk SMS can reach")
        if bad_phone:
            self.report("WARN", f"{len(bad_phone)} phone contacts are not a usable number", bad_phone)
        if bad_email:
            self.report("WARN", f"{len(bad_email)} email contacts are not a valid address", bad_email)
        self.dupes(qs, ["facility_id", "contact_type__type_name", "contact_value"],
                   "identical contacts on the same facility")
        multi_primary = (qs.filter(is_primary=True).values("facility_id").annotate(n=Count("pk"))
                         .filter(n__gt=1).values_list("facility_id", flat=True))
        if multi_primary:
            self.report("INFO", f"{len(multi_primary)} facilities have more than one primary contact", multi_primary)

    def users(self):
        from apps.authentication.models import User, UserRoleAssignment

        self.head("Users and roles")
        now = timezone.now()
        users = User.objects.all()
        self.report("INFO", f"{users.count()} users, {users.filter(is_active=True).count()} active, "
                            f"{users.filter(is_superuser=True).count()} superusers")
        live = Q(userroleassignment__expires_at__isnull=True) | Q(userroleassignment__expires_at__gt=now)
        no_role = (users.filter(is_active=True, is_superuser=False).exclude(live)
                   .values_list("email", flat=True))
        if no_role:
            self.report("WARN", f"{len(no_role)} active non-superusers have no current role "
                                "(they can sign in but see almost nothing)", no_role)
        expired = UserRoleAssignment.objects.filter(expires_at__lte=now).count()
        if expired:
            self.report("INFO", f"{expired} role assignments have expired")
        from apps.sms.services import normalize_phone
        bad = [u.email for u in users.filter(is_active=True) if not re.fullmatch(r"254\d{9}", normalize_phone(u.phone_number or ""))]
        if bad:
            self.report("WARN", f"{len(bad)} active users have a phone number SMS alerts cannot reach", bad)

    def files(self):
        from apps.documents.models import Document
        from apps.music.models import Music

        self.head("Uploaded files")
        for model, field, label in ((Document, "file", "documents"), (Music, "music_file", "music tracks")):
            missing = []
            rows = model.objects.exclude(**{f"{field}": ""}).exclude(**{f"{field}__isnull": True})
            for obj in rows.iterator():
                f = getattr(obj, field)
                try:
                    if not os.path.exists(f.path):
                        missing.append(obj.pk)
                except (ValueError, NotImplementedError):
                    pass
            self.report("INFO", f"{rows.count()} {label} with an uploaded file")
            if missing:
                self.report("ERROR", f"{len(missing)} {label} point at a file that is not on disk", missing)

    def settings_rows(self):
        from apps.common.models import ApplicationSettings

        self.head("Settings")
        n = ApplicationSettings.objects.count()
        if n != 1:
            self.report("WARN" if n == 0 else "ERROR", f"{n} application settings rows (expected 1)")
        else:
            s = ApplicationSettings.objects.get()
            self.report("INFO", f"map provider: {s.effective_map_provider()}")

    def sms(self):
        from apps.sms.services import credential_sources, resolve_credentials

        self.head("SMS (Bonga)")
        creds = resolve_credentials()
        missing = [k for k in ("client_id", "api_key", "api_secret", "service_id") if not creds.get(k)]
        if missing:
            self.report("WARN", f"Bonga SMS is not configured; missing: {', '.join(missing)}")
        else:
            sources = credential_sources()
            self.report("INFO", "Bonga SMS credentials present ("
                                + ", ".join(f"{k}: {v}" for k, v in sources.items()) + ")")
