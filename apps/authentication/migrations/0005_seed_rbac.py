# -*- encoding: utf-8 -*-
"""
Seed the role/permission catalogue, and make sure nobody is left unassigned.

There was already a create_default_roles_permissions management command, and
it had never been run: on a fresh database the permissions table was empty.
That is worse than having no RBAC at all, because has_permission() returns
False for everyone except superusers - so the handful of views that did carry
@permission_required were closed to every ordinary staff account, while the
hundred-odd views without a decorator stayed wide open to any logged-in user.

Seeding belongs in a migration rather than a command someone has to remember.
The deploy already runs migrate, so the catalogue now exists before any view
can ask about it.

Everything here is idempotent. It never deletes a role and never moves a user
who already has an assignment - an operator's deliberate choices outrank this
file. The one exception is that for the system roles defined below, this file
is authoritative about which permissions they hold, so stale over-grants get
pruned rather than accumulating.
"""

from django.db import migrations
from django.utils import timezone


# resource -> actions. The first five already existed; music, geography,
# monitoring, chat and settings are new, and are exactly the areas whose
# write views had no authorisation check at all.
RESOURCES = {
    'facilities': ['view', 'add', 'change', 'delete'],
    'users': ['view', 'add', 'change', 'delete'],
    'roles': ['view', 'add', 'change', 'delete'],
    'documents': ['view', 'add', 'change', 'delete'],
    'music': ['view', 'add', 'change', 'delete'],
    'geography': ['view', 'add', 'change', 'delete'],
    # The reference tables behind facilities and documents: operational
    # status, contact type, service category, owner type, GBV category,
    # infrastructure type, condition status, document type. Editing one
    # reshapes data everywhere it is used, and every one of these views was
    # reachable by any logged-in account.
    'lookups': ['view', 'add', 'change', 'delete'],
    'monitoring': ['view', 'change'],
    'chat': ['view', 'change'],
    'settings': ['view', 'change'],
    'analytics': ['view'],
    'admin': ['view'],
    'system': ['manage'],
}


def _name(action, resource):
    return '{0}_{1}'.format(action, resource)


ROLES = {
    'Super Admin': {
        'description': 'Full access to everything, including roles and system settings.',
        'permissions': '*',
    },
    'System Administrator': {
        'description': 'Runs the platform day to day. No role or permission editing.',
        'permissions': [
            _name(a, r) for r, acts in RESOURCES.items() for a in acts
            if r not in ('roles', 'system')
        ],
    },
    'Facility Manager': {
        'description': 'Maintains the facility directory and its geography.',
        'permissions': [
            'view_facilities', 'add_facilities', 'change_facilities',
            'view_geography', 'add_geography', 'change_geography',
            'view_lookups', 'add_lookups', 'change_lookups',
            'view_analytics', 'view_admin',
        ],
    },
    'Content Manager': {
        'description': 'Maintains resources and the music library.',
        'permissions': [
            'view_documents', 'add_documents', 'change_documents',
            'view_music', 'add_music', 'change_music',
            'view_lookups', 'change_lookups',
            'view_admin',
        ],
    },
    'Data Analyst': {
        'description': 'Read-only across the platform, plus analytics.',
        'permissions': [
            'view_facilities', 'view_documents', 'view_music',
            'view_geography', 'view_monitoring', 'view_analytics',
            'view_lookups', 'view_admin',
        ],
    },
    'Regular User': {
        'description': 'Can sign in and see the dashboard. Nothing else.',
        'permissions': ['view_admin'],
    },
}


def seed(apps, schema_editor):
    UserRole = apps.get_model('authentication', 'UserRole')
    Permission = apps.get_model('authentication', 'Permission')
    RolePermission = apps.get_model('authentication', 'RolePermission')
    UserRoleAssignment = apps.get_model('authentication', 'UserRoleAssignment')
    User = apps.get_model('authentication', 'User')

    # granted_by / assigned_by are NOT NULL, so the bookkeeping needs a user to
    # point at. Prefer a real superuser; if the database has no users at all
    # there is nothing to assign either, and we return early.
    actor = User.objects.filter(is_superuser=True).order_by('user_id').first()
    if actor is None:
        actor = User.objects.order_by('user_id').first()

    perms = {}
    for resource, actions in RESOURCES.items():
        for action in actions:
            name = _name(action, resource)
            obj, _ = Permission.objects.get_or_create(
                permission_name=name,
                defaults={
                    'resource_name': resource,
                    'action_name': action,
                    'description': '{0} {1}'.format(action, resource),
                },
            )
            perms[name] = obj

    if actor is None:
        return

    for role_name, spec in ROLES.items():
        role, _ = UserRole.objects.get_or_create(
            role_name=role_name,
            defaults={
                'description': spec['description'],
                'is_system_role': True,
                'created_at': timezone.now(),
            },
        )
        wanted = set(perms.keys()) if spec['permissions'] == '*' \
            else set(spec['permissions'])
        for perm_name in wanted:
            perm = perms.get(perm_name)
            if perm is None:
                continue
            RolePermission.objects.get_or_create(
                role=role, permission=perm,
                defaults={'granted_by': actor, 'granted_at': timezone.now()},
            )

        # For the roles defined here, this file is the source of truth: drop
        # grants that are not in the list. The old management command had
        # already given System Administrator add/change/delete_roles and
        # manage_system, so an additive-only pass left an account that is
        # meant to run the platform able to rewrite the permission system
        # itself. Silent privilege drift is the thing being fixed, so leaving
        # it would defeat the point.
        #
        # Only roles this migration owns are touched. A role an operator
        # created (is_system_role=False) is never pruned.
        if role.is_system_role:
            RolePermission.objects.filter(role=role).exclude(
                permission__permission_name__in=wanted
            ).delete()

    # Nobody gets locked out. Until now any authenticated user could reach
    # every unprotected view, so applying decorators without this step would
    # take the admin away from real staff mid-deploy. Existing accounts keep
    # roughly the access they had; new accounts start at Regular User.
    roles_by_name = {r.role_name: r for r in UserRole.objects.all()}
    for user in User.objects.all():
        if UserRoleAssignment.objects.filter(user=user).exists():
            continue
        if user.is_superuser:
            role = roles_by_name.get('Super Admin')
        elif user.is_staff:
            role = roles_by_name.get('System Administrator')
        else:
            role = roles_by_name.get('Regular User')
        if role is None:
            continue
        UserRoleAssignment.objects.get_or_create(
            user=user, role=role,
            defaults={'assigned_by': actor, 'assigned_at': timezone.now()},
        )


def unseed(apps, schema_editor):
    """Deliberately does nothing.

    Reversing would mean deleting roles and assignments an operator may have
    edited since. Rolling back a schema change should not quietly strip
    people's access.
    """
    return


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_userprofile_avatar_url'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
