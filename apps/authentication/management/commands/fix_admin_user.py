# -*- encoding: utf-8 -*-
"""
Management command to fix admin@hodi.ke user permissions
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.authentication.models import User, UserRole, UserRoleAssignment
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = 'Fix admin@hodi.ke user permissions and ensure access to chat functionality'

    def handle(self, *args, **options):
        self.stdout.write('Fixing admin@hodi.ke user permissions...')
        
        try:
            # Get the admin user
            admin_user = User.objects.get(email='admin@hodi.ke')
            
            # Fix user permissions
            changes_made = self.fix_user_permissions(admin_user)
            
            # Ensure user has proper role assignments
            role_assigned = self.assign_admin_role(admin_user)
            
            # Verify chat access permissions
            chat_access = self.verify_chat_access(admin_user)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully fixed admin@hodi.ke user!'
                )
            )
            
            if changes_made:
                self.stdout.write(f'Changes made: {", ".join(changes_made)}')
            
            if role_assigned:
                self.stdout.write('Admin role assigned successfully')
            
            if chat_access:
                self.stdout.write('Chat access verified successfully')
                
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('User admin@hodi.ke not found. Please create the user first.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error fixing admin user: {e}')
            )

    def fix_user_permissions(self, user):
        """Fix permissions for the admin user"""
        changes_made = []
        
        # Ensure user is active
        if not user.is_active:
            user.is_active = True
            changes_made.append('is_active=True')
        
        # Ensure user is staff (required for Django admin and chat access)
        if not user.is_staff:
            user.is_staff = True
            changes_made.append('is_staff=True')
        
        # Ensure user is superuser (optional, but recommended for admin)
        if not user.is_superuser:
            user.is_superuser = True
            changes_made.append('is_superuser=True')
        
        # Ensure user is verified
        if not user.verified:
            user.verified = True
            changes_made.append('verified=True')
        
        if changes_made:
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Updated user {user.email} permissions: {", ".join(changes_made)}'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'User {user.email} already has correct permissions'
                )
            )
        
        return changes_made

    def assign_admin_role(self, user):
        """Assign the Super Admin role to the user"""
        try:
            # Get or create Super Admin role
            super_admin_role, created = UserRole.objects.get_or_create(
                role_name='Super Admin',
                defaults={
                    'description': 'Full system access with all permissions',
                    'is_system_role': True
                }
            )
            
            if created:
                self.stdout.write('Created Super Admin role')
            
            # Check if role is already assigned
            existing_assignment = UserRoleAssignment.objects.filter(
                user=user,
                role=super_admin_role
            ).first()
            
            if not existing_assignment:
                UserRoleAssignment.objects.create(
                    user=user,
                    role=super_admin_role,
                    assigned_by=user,  # User assigns to themselves
                    expires_at=None  # Never expires
                )
                self.stdout.write('Assigned Super Admin role to user')
                return True
            else:
                self.stdout.write('User already has Super Admin role')
                return False
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error assigning admin role: {e}')
            )
            return False

    def verify_chat_access(self, user):
        """Verify that the user has access to chat functionality"""
        try:
            # Check if user can access chat views
            from django.contrib.auth.models import Permission
            from django.contrib.contenttypes.models import ContentType
            
            # Get chat app content type
            chat_content_type = ContentType.objects.get(app_label='chat')
            
            # Check for basic chat permissions
            chat_permissions = Permission.objects.filter(
                content_type=chat_content_type
            )
            
            if chat_permissions.exists():
                self.stdout.write(f'Found {chat_permissions.count()} chat permissions')
                
                # Ensure user has at least view permission
                view_permission = chat_permissions.filter(codename='view_conversation').first()
                if view_permission:
                    if not user.has_perm('chat.view_conversation'):
                        # Add the permission directly to user
                        user.user_permissions.add(view_permission)
                        self.stdout.write('Added chat view permission to user')
                    else:
                        self.stdout.write('User already has chat view permission')
                else:
                    self.stdout.write('Chat view permission not found')
            else:
                self.stdout.write('No chat permissions found in system')
            
            return True
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error verifying chat access: {e}')
            )
            return False
