"""repair_contacts: the real broken values found in production (Nov 2026)."""

from io import StringIO

import pytest
from django.core.management import call_command

from apps.facilities.management.commands.repair_contacts import plan_for


@pytest.mark.parametrize("value,expected", [
    ("5", ("drop", [])),
    ("1-5", ("drop", [])),
    ("051320040721350043", ("split", ["05132004", "0721350043"])),
    ("0202222220721337999", ("split", ["020222222", "0721337999"])),
    ("04021210721350039", ("split", ["0402121", "0721350039"])),
    ("(20) – 6763481 Fax: (20) – 6763482 Mobile: 0722203884", ("extract", ["0722203884"])),
    ("2223247 Mobile: 0722-206424", ("extract", ["0722206424"])),
    ("mchospital@wanachi.com", ("email", ["mchospital@wanachi.com"])),
])
def test_plans_for_real_broken_values(value, expected):
    assert plan_for(value) == expected


@pytest.mark.parametrize("value", ["0712345678", "+254 712 345 678", "020 2222222", "999", "1195", "0800 720 565"])
def test_good_numbers_are_left_alone(value):
    assert plan_for(value) is None


@pytest.mark.django_db
def test_dry_run_changes_nothing_and_apply_repairs(world):
    from apps.facilities.models import Facility, FacilityContact
    from apps.lookups.models import ContactType

    fac = Facility.objects.first()
    phone, _ = ContactType.objects.get_or_create(type_name="Phone")
    ContactType.objects.get_or_create(type_name="Email")
    user = fac.created_by
    junk = FacilityContact.objects.create(facility=fac, contact_type=phone, contact_value="7", created_by=user)
    glued = FacilityContact.objects.create(facility=fac, contact_type=phone, contact_value="051320040721350043", created_by=user)
    mail = FacilityContact.objects.create(facility=fac, contact_type=phone, contact_value="info@clinic.org", created_by=user)

    out = StringIO()
    call_command("repair_contacts", stdout=out)
    assert "Dry run" in out.getvalue()
    assert FacilityContact.objects.filter(pk__in=[junk.pk, glued.pk, mail.pk], is_active=True).count() == 3

    call_command("repair_contacts", "--apply", stdout=StringIO())
    assert not FacilityContact.objects.filter(pk__in=[junk.pk, glued.pk, mail.pk], is_active=True).exists()
    active = set(FacilityContact.objects.filter(facility=fac, is_active=True).values_list("contact_value", "contact_type__type_name"))
    assert ("0721350043", "Phone") in active and ("05132004", "Phone") in active
    assert ("info@clinic.org", "Email") in active
    # running again finds nothing left to do
    out = StringIO()
    call_command("repair_contacts", stdout=out)
    assert "0 contacts to repair" in out.getvalue()
