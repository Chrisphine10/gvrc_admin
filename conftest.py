"""
Shared pytest fixtures for the Hodi Admin test suite.

All fixtures are transaction-isolated: pytest-django wraps each test in a
database rollback, so objects created in one test are never visible to another.
"""

import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def test_user(db):
    User = get_user_model()
    return User.objects.create_user(
        email="test@example.com",
        full_name="Test User",
        phone_number="+254700000000",
        password="testpass123",
    )


@pytest.fixture
def superuser(db):
    User = get_user_model()
    return User.objects.create_superuser(
        email="admin@hodi.ke",
        full_name="Admin User",
        phone_number="+254700000001",
        password="adminpass123",
    )


@pytest.fixture
def county(db):
    from apps.geography.models import County
    return County.objects.create(county_name="Test County", county_code="TC001")


@pytest.fixture
def constituency(db, county):
    from apps.geography.models import Constituency
    return Constituency.objects.create(
        constituency_name="Test Constituency",
        constituency_code="TC001",
        county=county,
    )


@pytest.fixture
def ward(db, constituency):
    from apps.geography.models import Ward
    return Ward.objects.create(
        ward_name="Test Ward",
        ward_code="TW001",
        constituency=constituency,
    )


@pytest.fixture
def operational_status(db):
    from apps.lookups.models import OperationalStatus
    return OperationalStatus.objects.create(
        status_name="Operational",
        description="Fully operational facility",
        sort_order=1,
    )


@pytest.fixture
def contact_type(db):
    from apps.lookups.models import ContactType
    return ContactType.objects.create(type_name="Phone")


@pytest.fixture
def service_category(db):
    from apps.lookups.models import ServiceCategory
    return ServiceCategory.objects.create(category_name="Health Services")


@pytest.fixture
def facility(db, ward, operational_status, test_user):
    from apps.facilities.models import Facility
    return Facility.objects.create(
        facility_name="Test Facility",
        facility_code="TF001",
        registration_number="REG001",
        operational_status=operational_status,
        ward=ward,
        address_line_1="123 Test Street",
        is_active=True,
        created_by=test_user,
    )


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    return api_client
