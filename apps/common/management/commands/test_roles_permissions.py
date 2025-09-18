# -*- encoding: utf-8 -*-
"""
Management command to test roles and permissions creation
"""

from django.core.management.base import BaseCommand
from apps.authentication.models import UserRole, Permission, RolePermission


class Command(BaseCommand):
    help = 'Test roles and permissions creation'

    def handle(self, *args, **options):
        self.stdout.write('Testing roles and permissions creation...')
        
        # Check current counts
        roles_count = UserRole.objects.count()
        permissions_count = Permission.objects.count()
        role_permissions_count = RolePermission.objects.count()
        
        self.stdout.write(f'Current counts:')
        self.stdout.write(f'  Roles: {roles_count}')
        self.stdout.write(f'  Permissions: {permissions_count}')
        self.stdout.write(f'  Role-Permissions: {role_permissions_count}')
        
        # List existing roles
        self.stdout.write('\nExisting roles:')
        for role in UserRole.objects.all():
            self.stdout.write(f'  - {role.role_name}')
        
        # List existing permissions
        self.stdout.write('\nExisting permissions:')
        for perm in Permission.objects.all()[:10]:  # Show first 10
            self.stdout.write(f'  - {perm.permission_name}')
        
        if permissions_count > 10:
            self.stdout.write(f'  ... and {permissions_count - 10} more')
        
        # Check if Super Admin role has permissions
        try:
            super_admin = UserRole.objects.get(role_name='Super Admin')
            super_admin_perms = RolePermission.objects.filter(role=super_admin).count()
            self.stdout.write(f'\nSuper Admin role has {super_admin_perms} permissions assigned')
        except UserRole.DoesNotExist:
            self.stdout.write('\nSuper Admin role does not exist')
        
        self.stdout.write('\nTest complete!')
