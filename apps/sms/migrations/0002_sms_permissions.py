"""
Add the SMS permissions to the RBAC catalogue seeded by
authentication.0005_seed_rbac, and grant them to the roles that run the
platform.

* view_sms   - see broadcasts and delivery results
* send_sms   - send bulk SMS (costs money on the Intelli-Wealth account)
* change_sms - edit the SMS account settings and send a test SMS

Super Admin and System Administrator get all three. Other roles get none: an
operator can grant them per role from the Roles page. Idempotent; never removes
a grant an operator made.
"""

from django.db import migrations
from django.utils import timezone

PERMISSIONS = [
    ("view_sms", "view", "View bulk SMS broadcasts and delivery results"),
    ("send_sms", "send", "Send bulk SMS (billed to the SMS account)"),
    ("change_sms", "change", "Change SMS account settings and send test SMS"),
]
GRANT_TO = ("Super Admin", "System Administrator")


def add_permissions(apps, schema_editor):
    Permission = apps.get_model("authentication", "Permission")
    UserRole = apps.get_model("authentication", "UserRole")
    RolePermission = apps.get_model("authentication", "RolePermission")
    User = apps.get_model("authentication", "User")

    perms = []
    for name, action, description in PERMISSIONS:
        perm, _ = Permission.objects.get_or_create(
            permission_name=name,
            defaults={"resource_name": "sms", "action_name": action, "description": description},
        )
        perms.append(perm)

    actor = User.objects.filter(is_superuser=True).order_by("user_id").first() or \
        User.objects.order_by("user_id").first()
    if actor is None:
        return  # empty database: nothing to grant yet; superusers pass every check anyway

    for role in UserRole.objects.filter(role_name__in=GRANT_TO):
        for perm in perms:
            RolePermission.objects.get_or_create(
                role=role, permission=perm,
                defaults={"granted_by": actor, "granted_at": timezone.now()},
            )


def noop(apps, schema_editor):
    return


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0001_initial"),
        ("authentication", "0005_seed_rbac"),
    ]

    operations = [migrations.RunPython(add_permissions, noop)]
