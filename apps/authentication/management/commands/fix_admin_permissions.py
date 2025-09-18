# -*- encoding: utf-8 -*-
"""
Management command to fix admin user permissions
"""

from django.core.management.base import BaseCommand
from apps.authentication.models import UserRole, Permission, RolePermission, UserRoleAssignment
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Fix admin user permissions by creating roles/permissions and assigning Super Admin role'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default='admin@hodi.ke',
            help='Email of the admin user to fix (default: admin@hodi.ke)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreation of roles and permissions',
        )

    def handle(self, *args, **options):
        email = options['email']
        force = options['force']
        
        self.stdout.write('🔧 Fixing admin user permissions...')
        
        try:
            # Step 1: Create roles if they don't exist
            self.stdout.write('📋 Creating system roles...')
            roles_data = [
                {'role_name': 'Super Admin', 'description': 'Full system access with all permissions', 'is_system_role': True},
                {'role_name': 'System Administrator', 'description': 'System administration with user and role management', 'is_system_role': True},
                {'role_name': 'Facility Manager', 'description': 'Can manage facilities and related data', 'is_system_role': True},
                {'role_name': 'Data Analyst', 'description': 'Can view analytics and reports', 'is_system_role': True},
                {'role_name': 'Regular User', 'description': 'Basic user access to view data', 'is_system_role': True},
                {'role_name': 'Content Manager', 'description': 'Can manage documents and content', 'is_system_role': True}
            ]
            
            roles_created = 0
            for role_data in roles_data:
                if force:
                    UserRole.objects.filter(role_name=role_data['role_name']).delete()
                
                role, created = UserRole.objects.get_or_create(
                    role_name=role_data['role_name'],
                    defaults=role_data
                )
                if created:
                    roles_created += 1
                    self.stdout.write(f'  ✅ Created role: {role.role_name}')
                else:
                    self.stdout.write(f'  ℹ️  Role already exists: {role.role_name}')
            
            self.stdout.write(f'📋 Created {roles_created} new roles')
            
            # Step 2: Create permissions if they don't exist
            self.stdout.write('🔐 Creating system permissions...')
            permissions_data = [
                {'permission_name': 'view_users', 'resource_name': 'users', 'action_name': 'view', 'description': 'Can view user list and details'},
                {'permission_name': 'add_users', 'resource_name': 'users', 'action_name': 'add', 'description': 'Can create new users'},
                {'permission_name': 'change_users', 'resource_name': 'users', 'action_name': 'change', 'description': 'Can edit user information'},
                {'permission_name': 'delete_users', 'resource_name': 'users', 'action_name': 'delete', 'description': 'Can delete users'},
                {'permission_name': 'view_roles', 'resource_name': 'roles', 'action_name': 'view', 'description': 'Can view roles and permissions'},
                {'permission_name': 'add_roles', 'resource_name': 'roles', 'action_name': 'add', 'description': 'Can create new roles'},
                {'permission_name': 'change_roles', 'resource_name': 'roles', 'action_name': 'change', 'description': 'Can edit roles and permissions'},
                {'permission_name': 'delete_roles', 'resource_name': 'roles', 'action_name': 'delete', 'description': 'Can delete roles'},
                {'permission_name': 'view_facilities', 'resource_name': 'facilities', 'action_name': 'view', 'description': 'Can view facilities'},
                {'permission_name': 'add_facilities', 'resource_name': 'facilities', 'action_name': 'add', 'description': 'Can create new facilities'},
                {'permission_name': 'change_facilities', 'resource_name': 'facilities', 'action_name': 'change', 'description': 'Can edit facility information'},
                {'permission_name': 'delete_facilities', 'resource_name': 'facilities', 'action_name': 'delete', 'description': 'Can delete facilities'},
                {'permission_name': 'view_analytics', 'resource_name': 'analytics', 'action_name': 'view', 'description': 'Can view analytics and reports'},
                {'permission_name': 'view_documents', 'resource_name': 'documents', 'action_name': 'view', 'description': 'Can view documents'},
                {'permission_name': 'add_documents', 'resource_name': 'documents', 'action_name': 'add', 'description': 'Can upload documents'},
                {'permission_name': 'change_documents', 'resource_name': 'documents', 'action_name': 'change', 'description': 'Can edit documents'},
                {'permission_name': 'delete_documents', 'resource_name': 'documents', 'action_name': 'delete', 'description': 'Can delete documents'},
                {'permission_name': 'view_admin', 'resource_name': 'admin', 'action_name': 'view', 'description': 'Can access admin interface'},
                {'permission_name': 'manage_system', 'resource_name': 'system', 'action_name': 'manage', 'description': 'Can manage system settings'},
            ]
            
            permissions_created = 0
            for perm_data in permissions_data:
                if force:
                    Permission.objects.filter(permission_name=perm_data['permission_name']).delete()
                
                permission, created = Permission.objects.get_or_create(
                    permission_name=perm_data['permission_name'],
                    defaults=perm_data
                )
                if created:
                    permissions_created += 1
                    self.stdout.write(f'  ✅ Created permission: {permission.permission_name}')
                else:
                    self.stdout.write(f'  ℹ️  Permission already exists: {permission.permission_name}')
            
            self.stdout.write(f'🔐 Created {permissions_created} new permissions')
            
            # Step 3: Assign all permissions to Super Admin role
            self.stdout.write('🔗 Assigning permissions to Super Admin role...')
            super_admin_role = UserRole.objects.get(role_name='Super Admin')
            all_permissions = Permission.objects.all()
            role_perms_created = 0
            
            # Get admin user for granting permissions
            admin_user = User.objects.filter(email=email).first()
            if not admin_user:
                admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                admin_user = User.objects.first()  # Fallback
            
            if not admin_user:
                self.stdout.write(self.style.ERROR('❌ No admin user found to grant permissions'))
                return
            
            for permission in all_permissions:
                role_perm, created = RolePermission.objects.get_or_create(
                    role=super_admin_role,
                    permission=permission,
                    defaults={'granted_by': admin_user}
                )
                if created:
                    role_perms_created += 1
            
            self.stdout.write(f'🔗 Assigned {role_perms_created} permissions to Super Admin role')
            
            # Step 4: Find and assign Super Admin role to admin user
            self.stdout.write(f'👤 Assigning Super Admin role to {email}...')
            admin_user = User.objects.filter(email=email).first()
            
            if not admin_user:
                self.stdout.write(self.style.ERROR(f'❌ Admin user ({email}) not found!'))
                self.stdout.write('Available users:')
                for user in User.objects.all():
                    self.stdout.write(f'  - {user.email} (ID: {user.user_id})')
                return
            
            self.stdout.write(f'👤 Found admin user: {admin_user.email}')
            
            # Assign Super Admin role to admin user
            user_role_assignment, created = UserRoleAssignment.objects.get_or_create(
                user=admin_user,
                role=super_admin_role,
                defaults={'assigned_by': admin_user}
            )
            
            if created:
                self.stdout.write(f'✅ Assigned Super Admin role to {admin_user.email}')
            else:
                self.stdout.write(f'ℹ️  {admin_user.email} already has Super Admin role')
            
            # Step 5: Ensure admin user is superuser
            if not admin_user.is_superuser:
                admin_user.is_superuser = True
                admin_user.is_staff = True
                admin_user.save()
                self.stdout.write(f'✅ Made {admin_user.email} a superuser and staff member')
            else:
                self.stdout.write(f'ℹ️  {admin_user.email} is already a superuser')
            
            self.stdout.write(self.style.SUCCESS('\n🎉 SUCCESS! Admin user permissions fixed!'))
            self.stdout.write(f'📊 Summary:')
            self.stdout.write(f'  - Roles: {UserRole.objects.count()}')
            self.stdout.write(f'  - Permissions: {Permission.objects.count()}')
            self.stdout.write(f'  - Role-Permissions: {RolePermission.objects.count()}')
            self.stdout.write(f'  - Admin user has Super Admin role: ✅')
            self.stdout.write(f'  - Admin user is superuser: {"✅" if admin_user.is_superuser else "❌"}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
            import traceback
            traceback.print_exc()
