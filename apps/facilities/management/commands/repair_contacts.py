"""Repair facility phone contacts broken by imports.

    python manage.py repair_contacts            # dry run: show what would change
    python manage.py repair_contacts --apply    # make the changes

What it fixes (only active contacts whose type is a phone kind):

* junk values such as "5" or "1-5" (shifted spreadsheet columns) -> switched off;
* a landline and a mobile glued together, e.g. "051320040721350043"
  -> switched off, replaced by "05132004" and "0721350043";
* text with labels, e.g. "(20) 6763481 Fax: ... Mobile: 0722203884"
  -> switched off, replaced by the mobile number(s) found;
* an email address stored as a phone -> switched off, replaced by an Email contact.

Nothing is deleted: a bad row is set is_active=False, so the original value
stays for audit and the change can be undone by switching it back on.
"""

import re

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

PHONE_WORDS = ("phone", "mobile", "tel", "hotline", "whatsapp", "sms", "emergency")
EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[A-Za-z]{2,}")
MOBILE_RE = re.compile(r"(?<!\d)(?:\+?254|0)?(7\d{2}|1\d{2})[\s-]?(\d{3})[\s-]?(\d{3})(?!\d)")


def plan_for(value: str):
    """Return (action, new_values) for one contact value, or None if it is fine."""
    raw = (value or "").strip()
    digits = re.sub(r"\D", "", raw)
    if EMAIL_RE.fullmatch(raw):
        return ("email", [raw.lower()])
    if 3 <= len(digits) <= 13 and not re.search(r"[A-Za-z]", raw):
        return None  # a plausible number (or short code like 999 / 1195)
    if len(digits) <= 2 or re.fullmatch(r"[\d\s-]{1,4}", raw):
        return ("drop", [])
    if re.fullmatch(r"\d{15,20}", digits) and not re.search(r"[A-Za-z]", raw):
        tail = digits[-10:]
        head = digits[:-10]
        if re.fullmatch(r"0[17]\d{8}", tail):
            out = []
            if re.fullmatch(r"0\d{6,9}", head):
                out.append(head)
            out.append(tail)
            return ("split", out)
    mobiles = ["0" + "".join(m.groups()) for m in MOBILE_RE.finditer(raw)]
    if mobiles:
        return ("extract", list(dict.fromkeys(mobiles)))
    return ("drop", [])


class Command(BaseCommand):
    help = "Repair facility phone contacts broken by imports (dry run unless --apply)."

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true", help="Make the changes (default: only report).")

    def handle(self, *args, apply=False, **opts):
        from apps.facilities.models import FacilityContact
        from apps.lookups.models import ContactType

        email_type = ContactType.objects.filter(type_name__iexact="Email").first()
        rows = (FacilityContact.objects.filter(is_active=True).select_related("contact_type", "facility")
                .order_by("pk"))
        plans = []
        for c in rows:
            kind = (c.contact_type.type_name or "").lower()
            if not any(w in kind for w in PHONE_WORDS):
                continue
            plan = plan_for(c.contact_value)
            if plan:
                plans.append((c, *plan))

        counts = {}
        for c, action, values in plans:
            counts[action] = counts.get(action, 0) + 1
            shown = ", ".join(values) if values else "-"
            self.stdout.write(f"  contact {c.pk} (facility {c.facility_id}): {c.contact_value!r} -> {action}: {shown}")
        self.stdout.write(f"{len(plans)} contacts to repair: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))

        if not apply:
            self.stdout.write("Dry run: nothing changed. Re-run with --apply to make these changes.")
            return

        created = 0
        with transaction.atomic():
            for c, action, values in plans:
                existing = set(FacilityContact.objects.filter(facility=c.facility, is_active=True)
                               .exclude(pk=c.pk).values_list("contact_value", flat=True))
                for v in values:
                    ctype = email_type if action == "email" else c.contact_type
                    if ctype is None or v in existing:
                        continue
                    FacilityContact.objects.create(
                        facility=c.facility, contact_type=ctype, contact_value=v,
                        contact_person_name=c.contact_person_name, is_primary=False, is_active=True,
                        created_by=c.created_by,
                    )
                    existing.add(v)
                    created += 1
                c.is_active = False
                c.updated_at = timezone.now()
                c.save(update_fields=["is_active", "updated_at"])
        self.stdout.write(self.style.SUCCESS(f"Applied: {len(plans)} contacts switched off, {created} clean contacts added."))
