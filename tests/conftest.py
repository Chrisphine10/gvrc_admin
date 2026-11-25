"""
Shared fixtures and factories for the top-level test suite.

How access works in this app (learned from apps/authentication):

* Dashboard views are gated by ``permission_required('<action>_<resource>')``
  (apps/authentication/permissions.py). ``has_permission`` returns True for a
  superuser, otherwise it looks for a RolePermission on a role the user holds
  through a UserRoleAssignment whose ``expires_at`` is NULL.
* Migration 0005_seed_rbac seeds the Permission catalogue. It only creates the
  roles when a user already exists, so on the empty test database there are
  permissions but no roles. ``grant()`` below builds a role on the fly.
* A view that fails the permission check redirects to /dashboard/ (302), which
  is why a plain logged-in user gets 302 instead of 200 on the facility map.
* The mobile API authenticates a *device*, not a user: POST
  /mobile/sessions/create/ with a device_id creates a MobileSession, and every
  protected mobile endpoint then needs ``device_id`` (query string for GET,
  query string or body for POST/PUT). See MobileSessionPermission in
  apps/mobile/views.py.

Nothing here touches the network: an autouse fixture makes any real HTTP call
through ``requests`` fail loudly.
"""

import datetime
import itertools

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.utils import timezone

_seq = itertools.count(1)


def _n():
    return next(_seq)


# ---------------------------------------------------------------------------
# Safety nets
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _no_network(monkeypatch):
    """Any un-mocked HTTP request through requests is a test bug."""
    import requests

    def _blocked(self, method, url, *args, **kwargs):  # pragma: no cover
        raise RuntimeError(f"Network access attempted in tests: {method} {url}")

    monkeypatch.setattr(requests.sessions.Session, "request", _blocked)


@pytest.fixture(autouse=True)
def _clear_cache():
    """Several views cache_page() their output; never leak between tests."""
    from django.core.cache import cache
    cache.clear()
    yield
    cache.clear()


@pytest.fixture(autouse=True)
def _media_root(settings, tmp_path):
    """Uploaded files go to a throwaway folder, never the real media/."""
    settings.MEDIA_ROOT = str(tmp_path / "media")


@pytest.fixture(autouse=True)
def _fast_clients(settings):
    """WhiteNoise rescans every static file (~6,000 here) each time a new test
    Client builds its middleware chain - about 3 s per Client on Windows. It
    only serves /static/, which no test requests, so drop it for the suite."""
    settings.MIDDLEWARE = [m for m in settings.MIDDLEWARE if "whitenoise" not in m.lower()]


# ---------------------------------------------------------------------------
# Users and RBAC
# ---------------------------------------------------------------------------

def make_user(password="pass12345!", **kwargs):
    User = get_user_model()
    n = _n()
    defaults = {
        "email": f"user{n}@example.com",
        "full_name": f"User Number{n}",
        "phone_number": f"+2547100{n:05d}",
    }
    defaults.update(kwargs)
    return User.objects.create_user(password=password, **defaults)


def grant(user, *permission_names, role_name=None, expires_at=None):
    """Give ``user`` a fresh role holding exactly ``permission_names``."""
    from apps.authentication.models import (
        Permission, RolePermission, UserRole, UserRoleAssignment,
    )
    role = UserRole.objects.create(role_name=role_name or f"Role {_n()}")
    for name in permission_names:
        action, _, resource = name.partition("_")
        perm, _ = Permission.objects.get_or_create(
            permission_name=name,
            defaults={"resource_name": resource or name, "action_name": action},
        )
        RolePermission.objects.create(role=role, permission=perm, granted_by=user)
    UserRoleAssignment.objects.create(
        user=user, role=role, assigned_by=user, expires_at=expires_at,
    )
    return role


@pytest.fixture
def password():
    return "pass12345!"


@pytest.fixture
def staff_user(db, password):
    """Staff flag set, but no RBAC role at all."""
    return make_user(password=password, is_staff=True, full_name="Staff NoRole")


@pytest.fixture
def plain_user(db, password):
    """Not staff, no role (what /register/ produces)."""
    return make_user(password=password, full_name="Plain Person")


@pytest.fixture
def admin_user(db, password):
    return get_user_model().objects.create_superuser(
        email="root@example.com", full_name="Root Admin",
        phone_number="+254799999999", password=password,
    )


@pytest.fixture
def user_factory(db):
    return make_user


@pytest.fixture
def grant_perms():
    return grant


def logged_in_client(user):
    c = Client()
    c.force_login(user)
    return c


@pytest.fixture
def client_for():
    return logged_in_client


@pytest.fixture
def anon_client():
    return Client()


@pytest.fixture
def staff_client(staff_user):
    return logged_in_client(staff_user)


@pytest.fixture
def admin_client_(admin_user):
    return logged_in_client(admin_user)


# ---------------------------------------------------------------------------
# Domain objects
# ---------------------------------------------------------------------------

@pytest.fixture
def geo(db):
    from apps.geography.models import Constituency, County, Ward
    county = County.objects.create(county_name="Nairobi", county_code="047")
    constituency = Constituency.objects.create(
        constituency_name="Westlands", constituency_code="047-01", county=county,
    )
    ward = Ward.objects.create(
        ward_name="Parklands", ward_code="047-01-01", constituency=constituency,
    )
    return {"county": county, "constituency": constituency, "ward": ward}


@pytest.fixture
def lookups(db):
    from apps.lookups import models as L
    return {
        "status": L.OperationalStatus.objects.create(status_name="Operational", sort_order=1),
        "status_closed": L.OperationalStatus.objects.create(status_name="Closed", sort_order=2),
        "contact_type": L.ContactType.objects.create(type_name="Phone"),
        "email_type": L.ContactType.objects.create(type_name="Email"),
        "service_category": L.ServiceCategory.objects.create(category_name="Medical"),
        "owner_type": L.OwnerType.objects.create(type_name="Government"),
        "gbv_category": L.GBVCategory.objects.create(category_name="Physical Violence"),
        "infra_type": L.InfrastructureType.objects.create(type_name="Shelter"),
        "condition": L.ConditionStatus.objects.create(status_name="Good"),
        "doc_type": L.DocumentType.objects.create(
            type_name="PDF", allowed_extensions='["pdf"]', max_file_size_mb=10,
        ),
    }


def make_facility(geo, lookups, user, name=None, lat=-1.2640, lng=36.8030,
                  with_related=True, **kwargs):
    from apps.facilities.models import (
        Facility, FacilityContact, FacilityCoordinate, FacilityGBVCategory,
        FacilityInfrastructure, FacilityOwner, FacilityService,
    )
    n = _n()
    facility = Facility.objects.create(
        facility_name=name or f"Facility {n}",
        facility_code=f"FC{n:04d}",
        registration_number=f"REG-{n:04d}",
        operational_status=kwargs.pop("operational_status", lookups["status"]),
        ward=kwargs.pop("ward", geo["ward"]),
        address_line_1="1 Test Road",
        created_by=user,
        **kwargs,
    )
    if lat is not None and lng is not None:
        FacilityCoordinate.objects.create(
            facility=facility, latitude=lat, longitude=lng,
            collection_date=datetime.date(2024, 1, 1), created_by=user,
        )
    if with_related:
        FacilityContact.objects.create(
            facility=facility, contact_type=lookups["contact_type"],
            contact_value="+254700111222", is_primary=True, created_by=user,
        )
        FacilityService.objects.create(
            facility=facility, service_category=lookups["service_category"],
            service_name="Counselling", is_free=True,
        )
        FacilityOwner.objects.create(
            facility=facility, owner_name="County Government",
            owner_type=lookups["owner_type"], created_by=user,
        )
        FacilityInfrastructure.objects.create(
            facility=facility, infrastructure_type=lookups["infra_type"],
            condition_status=lookups["condition"], capacity=10, created_by=user,
        )
        FacilityGBVCategory.objects.create(
            facility=facility, gbv_category=lookups["gbv_category"], created_by=user,
        )
    return facility


@pytest.fixture
def facility_factory(geo, lookups):
    def _make(user, **kwargs):
        return make_facility(geo, lookups, user, **kwargs)
    return _make


@pytest.fixture
def mobile_session(db):
    from apps.mobile_sessions.models import MobileSession
    return MobileSession.objects.create(
        device_id="device-test-0001", latitude=-1.2650, longitude=36.8040,
    )


@pytest.fixture
def world(db, geo, lookups, admin_user, staff_user, plain_user, mobile_session):
    """One of everything, for URL smoke tests and API shape checks."""
    from apps.authentication.models import Permission, UserRole
    from apps.chat.models import ChatNotification, Conversation, Message
    from apps.documents.models import Document
    from apps.music.models import Music, MusicPlay

    facility = make_facility(geo, lookups, admin_user, name="Parklands GBV Centre")
    conversation = Conversation.objects.create(
        mobile_session=mobile_session, subject="Need help", assigned_admin=admin_user,
    )
    message = Message.objects.create(
        conversation=conversation, sender_type="mobile", content="Hello, I need help",
    )
    notification = ChatNotification.objects.create(
        user=admin_user, notification_type="new_message",
        conversation=conversation, message=message,
    ) if _has_field(ChatNotification, "message") else ChatNotification.objects.create(
        user=admin_user, notification_type="new_message", conversation=conversation,
    )
    document = Document.objects.create(
        title="Know your rights", description="Guide", content="Text",
        document_type=lookups["doc_type"], gbv_category=lookups["gbv_category"],
        is_public=True, uploaded_by=admin_user, external_url="https://example.org/doc",
    )
    music = Music.objects.create(
        name="Calm", artist="Hodi", link="https://example.org/calm.mp3",
        created_by=admin_user,
    )
    MusicPlay.objects.create(music=music, user=admin_user)
    role = UserRole.objects.create(role_name="Smoke Role", description="for tests")
    permission = Permission.objects.order_by("permission_id").first()
    return {
        **geo,
        **lookups,
        "facility": facility,
        "contact": facility.facilitycontact_set.first(),
        "conversation": conversation,
        "message": message,
        "notification": notification,
        "document": document,
        "music": music,
        "role": role,
        "permission": permission,
        "mobile_session": mobile_session,
        "admin": admin_user,
        "staff": staff_user,
        "plain": plain_user,
    }


def _has_field(model, name):
    return any(f.name == name for f in model._meta.get_fields())


@pytest.fixture
def now():
    return timezone.now()
