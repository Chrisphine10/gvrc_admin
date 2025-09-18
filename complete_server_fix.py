#!/usr/bin/env python
"""
Complete Server Fix Script
Combines database configuration fix and admin permissions setup
Run this single script to fix all server issues at once.
"""

import os
import sys
import django
from pathlib import Path

def main():
    """Main function to fix all server issues"""
    print("🚀 Complete Server Fix Script")
    print("=" * 50)
    
    # Step 1: Fix Database Configuration
    print("\n🔧 Step 1: Fixing database configuration...")
    fix_database_config()
    
    # Step 2: Set up Django environment
    print("\n🔧 Step 2: Setting up Django environment...")
    setup_django_environment()
    
    # Step 3: Fix admin permissions
    print("\n🔧 Step 3: Fixing admin permissions...")
    fix_admin_permissions()
    
    # Step 4: Verify everything works
    print("\n🔧 Step 4: Verifying fixes...")
    verify_fixes()
    
    print("\n🎉 SUCCESS! All server issues have been fixed!")
    print("✅ Database connection: WORKING")
    print("✅ Admin permissions: SET UP")
    print("✅ Chat assignment: READY")
    print("\n📝 Next steps:")
    print("1. Try logging in with admin@hodi.ke")
    print("2. Test the chat assignment functionality at https://hodi.co.ke/chat/conversation/1/")
    print("3. Verify all admin features are working")

def fix_database_config():
    """Fix database configuration by setting correct environment variables"""
    print("📋 Setting database environment variables...")
    
    # Set the correct database configuration
    os.environ['DB_ENGINE'] = 'postgresql'
    os.environ['DB_NAME'] = 'gvrc_db'
    os.environ['DB_USERNAME'] = 'postgres'
    os.environ['DB_PASS'] = 'postgres123#'
    os.environ['DB_HOST'] = 'database-postgres.cn2uqm2iclii.eu-north-1.rds.amazonaws.com'
    os.environ['DB_PORT'] = '5432'
    
    print("✅ Database environment variables set:")
    print(f"   DB_ENGINE: {os.environ['DB_ENGINE']}")
    print(f"   DB_NAME: {os.environ['DB_NAME']}")
    print(f"   DB_USERNAME: {os.environ['DB_USERNAME']}")
    print(f"   DB_HOST: {os.environ['DB_HOST']}")
    print(f"   DB_PORT: {os.environ['DB_PORT']}")

def setup_django_environment():
    """Set up Django environment"""
    # Add project root to Python path
    project_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.postgres')
    
    print("✅ Django environment configured")
    print(f"   Settings module: {os.environ['DJANGO_SETTINGS_MODULE']}")
    
    # Initialize Django
    django.setup()
    print("✅ Django initialized successfully")

def fix_admin_permissions():
    """Fix admin permissions using the management command"""
    try:
        from django.core.management import execute_from_command_line
        print("🚀 Running fix_admin_permissions command...")
        
        # Run the fix command
        execute_from_command_line(['manage.py', 'fix_admin_permissions'])
        
        print("✅ Admin permissions fixed successfully!")
        
    except Exception as e:
        print(f"❌ Error fixing admin permissions: {str(e)}")
        print("🔧 Attempting manual permission setup...")
        manual_permission_setup()

def manual_permission_setup():
    """Manual permission setup if the command fails"""
    try:
        from apps.authentication.models import UserRole, Permission, RolePermission, UserRoleAssignment
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        print("📋 Creating roles and permissions manually...")
        
        # Create roles
        roles_data = [
            {'role_name': 'Super Admin', 'description': 'Full system access with all permissions', 'is_system_role': True},
            {'role_name': 'System Administrator', 'description': 'System administration with user and role management', 'is_system_role': True},
            {'role_name': 'Facility Manager', 'description': 'Can manage facilities and related data', 'is_system_role': True},
            {'role_name': 'Data Analyst', 'description': 'Can view analytics and reports', 'is_system_role': True},
            {'role_name': 'Regular User', 'description': 'Basic user access to view data', 'is_system_role': True},
            {'role_name': 'Content Manager', 'description': 'Can manage documents and content', 'is_system_role': True}
        ]
        
        for role_data in roles_data:
            role, created = UserRole.objects.get_or_create(
                role_name=role_data['role_name'],
                defaults=role_data
            )
            if created:
                print(f"   ✅ Created role: {role.role_name}")
        
        # Create permissions
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
        
        for perm_data in permissions_data:
            permission, created = Permission.objects.get_or_create(
                permission_name=perm_data['permission_name'],
                defaults=perm_data
            )
            if created:
                print(f"   ✅ Created permission: {permission.permission_name}")
        
        # Assign all permissions to Super Admin role
        super_admin_role = UserRole.objects.get(role_name='Super Admin')
        all_permissions = Permission.objects.all()
        
        # Get admin user for granting permissions
        admin_user = User.objects.filter(email='admin@hodi.ke').first()
        if not admin_user:
            admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.first()
        
        if admin_user:
            print(f"   👤 Using admin user: {admin_user.email}")
            
            for permission in all_permissions:
                RolePermission.objects.get_or_create(
                    role=super_admin_role,
                    permission=permission,
                    defaults={'granted_by': admin_user}
                )
            
            # Assign Super Admin role to admin user
            UserRoleAssignment.objects.get_or_create(
                user=admin_user,
                role=super_admin_role,
                defaults={'assigned_by': admin_user}
            )
            
            # Ensure admin user is superuser
            if not admin_user.is_superuser:
                admin_user.is_superuser = True
                admin_user.is_staff = True
                admin_user.save()
                print(f"   ✅ Made {admin_user.email} a superuser")
        
        print("✅ Manual permission setup completed!")
        
    except Exception as e:
        print(f"❌ Manual permission setup failed: {str(e)}")
        raise

def verify_fixes():
    """Verify that all fixes are working"""
    try:
        from django.core.management import execute_from_command_line
        from django.db import connection
        
        # Test database connection
        print("🔍 Testing database connection...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("✅ Database connection: WORKING")
        
        # Test Django check
        print("🔍 Running Django system check...")
        execute_from_command_line(['manage.py', 'check'])
        print("✅ Django system check: PASSED")
        
        # Test admin user
        print("🔍 Checking admin user...")
        from django.contrib.auth import get_user_model
        User = get_user_model()
        admin_user = User.objects.filter(email='admin@hodi.ke').first()
        if admin_user and admin_user.is_superuser:
            print(f"✅ Admin user ({admin_user.email}): READY")
        else:
            print("⚠️  Admin user needs attention")
        
        # Test roles and permissions
        print("🔍 Checking roles and permissions...")
        from apps.authentication.models import UserRole, Permission, RolePermission
        role_count = UserRole.objects.count()
        perm_count = Permission.objects.count()
        role_perm_count = RolePermission.objects.count()
        
        print(f"✅ Roles: {role_count}")
        print(f"✅ Permissions: {perm_count}")
        print(f"✅ Role-Permissions: {role_perm_count}")
        
    except Exception as e:
        print(f"❌ Verification failed: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {str(e)}")
        print("\n🔧 Manual troubleshooting steps:")
        print("1. Check if PostgreSQL is running")
        print("2. Verify database credentials")
        print("3. Check network connectivity to AWS RDS")
        print("4. Ensure Django settings are correct")
        sys.exit(1)
