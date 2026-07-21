# -*- encoding: utf-8 -*-
"""
Management command to set up initial user roles and permissions
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.authentication.models import UserRole, Permission, RolePermission, UserRoleAssignment
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = 'Set up initial user roles and permissions system'

    def handle(self, *args, **options):
        self.stdout.write('Setting up user roles and permissions system...')
        
        # Create system roles
        roles_created = self.create_system_roles()
        
        # Create system permissions
        permissions_created = self.create_system_permissions()
        
        # Assign permissions to roles
        role_permissions_created = self.assign_permissions_to_roles()
        
        # Ensure admin user is super admin
        admin_updated = self.ensure_admin_superuser()
        
        # Create admin role assignment
        admin_role_assigned = self.assign_admin_role()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Setup complete! Created {roles_created} roles, {permissions_created} permissions, '
                f'{role_permissions_created} role-permission assignments, updated admin user, '
                f'and assigned admin role.'
            )
        )

    def create_system_roles(self):
        """Create the initial system roles"""
        roles_data = [
            {
                'role_name': 'Super Admin',
                'description': 'Full system access with all permissions',
                'is_system_role': True
            },
            {
                'role_name': 'System Administrator',
                'description': 'System administration with user and role management',
                'is_system_role': True
            },
            {
                'role_name': 'Facility Manager',
                'description': 'Can manage facilities and related data',
                'is_system_role': True
            },
            {
                'role_name': 'Data Analyst',
                'description': 'Can view analytics and reports',
                'is_system_role': True
            },
            {
                'role_name': 'Regular User',
                'description': 'Basic user access to view data',
                'is_system_role': True
            },
            {
                'role_name': 'Content Manager',
                'description': 'Can manage documents and content',
                'is_system_role': True
            }
        ]
        
        roles_created = 0
        for role_data in roles_data:
            role, created = UserRole.objects.get_or_create(
                role_name=role_data['role_name'],
                defaults=role_data
            )
            if created:
                roles_created += 1
                self.stdout.write(f'Created role: {role.role_name}')
        
        return roles_created

    def create_system_permissions(self):
        """Create the initial system permissions"""
        permissions_data = [
            # User management permissions
            {'permission_name': 'view_users', 'resource_name': 'users', 'action_name': 'view', 'description': 'Can view user list and details'},
            {'permission_name': 'add_users', 'resource_name': 'users', 'action_name': 'add', 'description': 'Can create new users'},
            {'permission_name': 'change_users', 'resource_name': 'users', 'action_name': 'change', 'description': 'Can edit user information'},
            {'permission_name': 'delete_users', 'resource_name': 'users', 'action_name': 'delete', 'description': 'Can delete users'},
            
            # Role management permissions
            {'permission_name': 'view_roles', 'resource_name': 'roles', 'action_name': 'view', 'description': 'Can view roles and permissions'},
            {'permission_name': 'add_roles', 'resource_name': 'roles', 'action_name': 'add', 'description': 'Can create new roles'},
            {'permission_name': 'change_roles', 'resource_name': 'roles', 'action_name': 'change', 'description': 'Can edit roles and permissions'},
            {'permission_name': 'delete_roles', 'resource_name': 'roles', 'action_name': 'delete', 'description': 'Can delete roles'},
            
            # Facility management permissions
            {'permission_name': 'view_facilities', 'resource_name': 'facilities', 'action_name': 'view', 'description': 'Can view facilities'},
            {'permission_name': 'add_facilities', 'resource_name': 'facilities', 'action_name': 'add', 'description': 'Can create new facilities'},
            {'permission_name': 'change_facilities', 'resource_name': 'facilities', 'action_name': 'change', 'description': 'Can edit facilities'},
            {'permission_name': 'delete_facilities', 'resource_name': 'facilities', 'action_name': 'delete', 'description': 'Can delete facilities'},
            
            # Analytics permissions
            {'permission_name': 'view_analytics', 'resource_name': 'analytics', 'action_name': 'view', 'description': 'Can view analytics and reports'},
            {'permission_name': 'export_analytics', 'resource_name': 'analytics', 'action_name': 'export', 'description': 'Can export analytics data'},
            
            # Content management permissions
            {'permission_name': 'view_documents', 'resource_name': 'documents', 'action_name': 'view', 'description': 'Can view documents'},
            {'permission_name': 'add_documents', 'resource_name': 'documents', 'action_name': 'add', 'description': 'Can upload documents'},
            {'permission_name': 'change_documents', 'resource_name': 'documents', 'action_name': 'change', 'description': 'Can edit documents'},
            {'permission_name': 'delete_documents', 'resource_name': 'documents', 'action_name': 'delete', 'description': 'Can delete documents'},
            
            # System administration permissions
            {'permission_name': 'access_admin', 'resource_name': 'admin', 'action_name': 'access', 'description': 'Can access Django admin panel'},
            {'permission_name': 'manage_system', 'resource_name': 'system', 'action_name': 'manage', 'description': 'Can manage system settings'},
        ]
        
        permissions_created = 0
        for perm_data in permissions_data:
            permission, created = Permission.objects.get_or_create(
                permission_name=perm_data['permission_name'],
                defaults=perm_data
            )
            if created:
                permissions_created += 1
                self.stdout.write(f'Created permission: {permission.permission_name}')
        
        return permissions_created

    def assign_permissions_to_roles(self):
        """Assign permissions to appropriate roles"""
        role_permissions_created = 0
        
        # Get roles
        super_admin_role = UserRole.objects.get(role_name='Super Admin')
        system_admin_role = UserRole.objects.get(role_name='System Administrator')
        facility_manager_role = UserRole.objects.get(role_name='Facility Manager')
        data_analyst_role = UserRole.objects.get(role_name='Data Analyst')
        regular_user_role = UserRole.objects.get(role_name='Regular User')
        content_manager_role = UserRole.objects.get(role_name='Content Manager')
        
        # Get admin user for granting permissions
        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                admin_user = User.objects.filter(email='admin@gvrc.com').first()
            if not admin_user:
                admin_user = User.objects.first()  # Fallback to first user
        except:
            admin_user = None
        
        if not admin_user:
            self.stdout.write(self.style.WARNING('No admin user found to grant permissions'))
            return 0
        
        # Super Admin gets all permissions
        all_permissions = Permission.objects.all()
        for permission in all_permissions:
            role_perm, created = RolePermission.objects.get_or_create(
                role=super_admin_role,
                permission=permission,
                defaults={'granted_by': admin_user}
            )
            if created:
                role_permissions_created += 1
        
        # System Administrator gets user and role management permissions
        system_admin_permissions = Permission.objects.filter(
            resource_name__in=['users', 'roles', 'admin', 'system']
        )
        for permission in system_admin_permissions:
            role_perm, created = RolePermission.objects.get_or_create(
                role=system_admin_role,
                permission=permission,
                defaults={'granted_by': admin_user}
            )
            if created:
                role_permissions_created += 1
        
        # Facility Manager gets facility management permissions
        facility_permissions = Permission.objects.filter(
            resource_name='facilities'
        )
        for permission in facility_permissions:
            role_perm, created = RolePermission.objects.get_or_create(
                role=facility_manager_role,
                permission=permission,
                defaults={'granted_by': admin_user}
            )
            if created:
                role_permissions_created += 1
        
        # Data Analyst gets analytics permissions
        analytics_permissions = Permission.objects.filter(
            resource_name='analytics'
        )
        for permission in analytics_permissions:
            role_perm, created = RolePermission.objects.get_or_create(
                role=data_analyst_role,
                permission=permission,
                defaults={'granted_by': admin_user}
            )
            if created:
                role_permissions_created += 1
        
        # Content Manager gets document permissions
        document_permissions = Permission.objects.filter(
            resource_name='documents'
        )
        for permission in document_permissions:
            role_perm, created = RolePermission.objects.get_or_create(
                role=content_manager_role,
                permission=permission,
                defaults={'granted_by': admin_user}
            )
            if created:
                role_permissions_created += 1
        
        # Regular User gets basic view permissions
        view_permissions = Permission.objects.filter(
            action_name='view'
        )
        for permission in view_permissions:
            role_perm, created = RolePermission.objects.get_or_create(
                role=regular_user_role,
                permission=permission,
                defaults={'granted_by': admin_user}
            )
            if created:
                role_permissions_created += 1
        
        return role_permissions_created

    def ensure_admin_superuser(self):
        """Ensure the admin user has superuser privileges"""
        try:
            admin_user = User.objects.filter(email='admin@gvrc.com').first()
            if admin_user:
                if not admin_user.is_superuser:
                    admin_user.is_superuser = True
                    admin_user.is_staff = True
                    admin_user.verified = True
                    admin_user.save()
                    self.stdout.write('Updated admin user to superuser')
                    return True
                else:
                    self.stdout.write('Admin user already has superuser privileges')
                    return False
            else:
                self.stdout.write(self.style.WARNING('No admin user found with email admin@gvrc.com'))
                return False
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating admin user: {e}'))
            return False

    def assign_admin_role(self):
        """Assign the Super Admin role to the admin user"""
        try:
            admin_user = User.objects.filter(email='admin@gvrc.com').first()
            if not admin_user:
                admin_user = User.objects.filter(is_superuser=True).first()
            
            if admin_user:
                super_admin_role = UserRole.objects.get(role_name='Super Admin')
                
                # Check if role is already assigned
                existing_assignment = UserRoleAssignment.objects.filter(
                    user=admin_user,
                    role=super_admin_role
                ).first()
                
                if not existing_assignment:
                    UserRoleAssignment.objects.create(
                        user=admin_user,
                        role=super_admin_role,
                        assigned_by=admin_user,  # Admin assigns to themselves
                        expires_at=None  # Never expires
                    )
                    self.stdout.write('Assigned Super Admin role to admin user')
                    return True
                else:
                    self.stdout.write('Admin user already has Super Admin role')
                    return False
            else:
                self.stdout.write(self.style.WARNING('No admin user found to assign role'))
                return False
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error assigning admin role: {e}'))
            return False
