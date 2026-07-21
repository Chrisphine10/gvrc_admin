# GVRC Admin Permission System Documentation

## Overview

The GVRC Admin system implements a comprehensive role-based access control (RBAC) system that allows fine-grained control over user permissions across different modules. The system is built on Django's authentication framework and includes custom models, decorators, and utility functions.

## System Architecture

### Core Models

#### 1. User Model (`apps.authentication.models.User`)
- Extends Django's `AbstractBaseUser` and `PermissionsMixin`
- Custom fields: `user_id`, `full_name`, `email`, `phone_number`
- Django standard fields: `is_staff`, `is_superuser`, `is_active`

#### 2. UserRole Model (`apps.authentication.models.UserRole`)
- Defines available roles in the system
- Fields: `role_id`, `role_name`, `description`, `is_system_role`, `created_at`
- Example roles: Super Admin, Facility Manager, Data Analyst, etc.

#### 3. Permission Model (`apps.authentication.models.Permission`)
- Defines granular permissions
- Fields: `permission_id`, `permission_name`, `resource_name`, `action_name`, `description`
- Example: `view_facilities`, `add_users`, `change_roles`

#### 4. RolePermission Model (`apps.authentication.models.RolePermission`)
- Many-to-many relationship between roles and permissions
- Fields: `role`, `permission`, `granted_at`, `granted_by`

#### 5. UserRoleAssignment Model (`apps.authentication.models.UserRoleAssignment`)
- Many-to-many relationship between users and roles
- Fields: `user`, `role`, `assigned_at`, `assigned_by`, `expires_at`

## Permission System Features

### 1. Predefined Roles

The system includes the following predefined roles:

- **Super Admin**: Full system access with all permissions
- **System Administrator**: User and role management permissions
- **Facility Manager**: Facility management permissions
- **Data Analyst**: Analytics and reporting permissions
- **Regular User**: Basic view permissions
- **Content Manager**: Document management permissions

### 2. Permission Categories

Permissions are organized by resource and action:

#### User Management
- `view_users` - View user list and details
- `add_users` - Create new users
- `change_users` - Edit user information
- `delete_users` - Delete users

#### Role Management
- `view_roles` - View roles and permissions
- `add_roles` - Create new roles
- `change_roles` - Edit roles and permissions
- `delete_roles` - Delete roles

#### Facility Management
- `view_facilities` - View facilities
- `add_facilities` - Create new facilities
- `change_facilities` - Edit facilities
- `delete_facilities` - Delete facilities

#### Analytics
- `view_analytics` - View analytics and reports
- `export_analytics` - Export analytics data

#### Content Management
- `view_documents` - View documents
- `add_documents` - Upload documents
- `change_documents` - Edit documents
- `delete_documents` - Delete documents

#### System Administration
- `access_admin` - Access Django admin panel
- `manage_system` - Manage system settings

## Usage Guide

### 1. Permission Checking Functions

#### `has_permission(user, permission_name)`
Check if a user has a specific permission through their roles.

```python
from apps.authentication.permissions import has_permission

if has_permission(request.user, 'view_facilities'):
    # User can view facilities
    pass
```

#### `has_role(user, role_name)`
Check if a user has a specific role.

```python
from apps.authentication.permissions import has_role

if has_role(request.user, 'Facility Manager'):
    # User is a facility manager
    pass
```

#### `has_any_role(user, role_names)`
Check if a user has any of the specified roles.

```python
from apps.authentication.permissions import has_any_role

if has_any_role(request.user, ['Facility Manager', 'System Administrator']):
    # User is either a facility manager or system administrator
    pass
```

### 2. View Decorators

#### `@permission_required(permission_name)`
Require a specific permission for a view.

```python
from apps.authentication.permissions import permission_required

@permission_required('view_facilities')
def facility_list(request):
    # Only users with 'view_facilities' permission can access
    pass
```

#### `@role_required(role_name)`
Require a specific role for a view.

```python
from apps.authentication.permissions import role_required

@role_required('Facility Manager')
def facility_create(request):
    # Only facility managers can access
    pass
```

#### `@any_role_required(role_names)`
Require any of the specified roles for a view.

```python
from apps.authentication.permissions import any_role_required

@any_role_required(['Facility Manager', 'System Administrator'])
def facility_edit(request):
    # Either facility managers or system administrators can access
    pass
```

#### `@staff_required()`
Require staff status for a view.

```python
from apps.authentication.permissions import staff_required

@staff_required()
def admin_panel(request):
    # Only staff members can access
    pass
```

#### `@superuser_required()`
Require superuser status for a view.

```python
from apps.authentication.permissions import superuser_required

@superuser_required()
def system_settings(request):
    # Only superusers can access
    pass
```

### 3. AJAX Permission Decorators

For AJAX views that return JSON responses:

#### `@ajax_permission_required(permission_name)`
```python
from apps.authentication.permissions import ajax_permission_required

@ajax_permission_required('change_roles')
def assign_permission_to_role(request, role_id):
    # Returns JSON error if permission denied
    pass
```

#### `@ajax_role_required(role_name)`
```python
from apps.authentication.permissions import ajax_role_required

@ajax_role_required('Facility Manager')
def facility_ajax_action(request):
    # Returns JSON error if role denied
    pass
```

### 4. REST Framework Permission Classes

For DRF viewsets and API views:

```python
from apps.authentication.permissions import HasPermissionPermission, HasRolePermission

class FacilityViewSet(viewsets.ModelViewSet):
    permission_classes = [HasPermissionPermission('view_facilities')]

class AdminViewSet(viewsets.ModelViewSet):
    permission_classes = [HasRolePermission('System Administrator')]
```

### 5. Template Context

The permission system provides template context variables:

```html
<!-- Check if user has permission -->
{% if user_permissions and 'view_facilities' in user_permissions %}
    <a href="{% url 'facility_list' %}">View Facilities</a>
{% endif %}

<!-- Check if user has role -->
{% if 'Facility Manager' in user_roles %}
    <a href="{% url 'facility_create' %}">Create Facility</a>
{% endif %}

<!-- Use permission checking functions -->
{% if has_permission user 'add_facilities' %}
    <button>Add Facility</button>
{% endif %}
```

## Implementation Examples

### 1. Facility Views with Permissions

```python
from apps.authentication.permissions import permission_required

@permission_required('view_facilities')
def facility_list(request):
    """List facilities - requires view_facilities permission"""
    # Implementation
    pass

@permission_required('add_facilities')
def facility_create(request):
    """Create facility - requires add_facilities permission"""
    # Implementation
    pass

@permission_required('change_facilities')
def facility_update(request, facility_id):
    """Update facility - requires change_facilities permission"""
    # Implementation
    pass
```

### 2. Role-Based Access Control

```python
from apps.authentication.permissions import role_required, any_role_required

@role_required('Facility Manager')
def facility_management(request):
    """Only facility managers can access"""
    pass

@any_role_required(['Facility Manager', 'System Administrator'])
def facility_advanced_settings(request):
    """Either facility managers or system administrators"""
    pass
```

### 3. API Views with Permissions

```python
from rest_framework import viewsets
from apps.authentication.permissions import HasPermissionPermission

class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    permission_classes = [HasPermissionPermission('view_facilities')]
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [HasPermissionPermission('add_facilities')]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [HasPermissionPermission('change_facilities')]
        elif self.action == 'destroy':
            permission_classes = [HasPermissionPermission('delete_facilities')]
        else:
            permission_classes = [HasPermissionPermission('view_facilities')]
        
        return [permission() for permission in permission_classes]
```

## Management Commands

### Setup User Roles and Permissions

```bash
python manage.py setup_user_roles
```

This command:
- Creates system roles
- Creates system permissions
- Assigns permissions to roles
- Ensures admin user has superuser privileges
- Assigns Super Admin role to admin user

### Fix User Permissions

```bash
python manage.py fix_user_permissions --email admin@example.com
python manage.py fix_user_permissions --all-superusers
```

## Testing

The system includes comprehensive testing capabilities:

```bash
python test_permissions.py
```

This test script verifies:
- Role and permission models exist
- Role-permission assignments are correct
- User-role assignments are working
- Permission checking functions work correctly
- Decorators can be applied to functions

## Security Considerations

1. **Permission Inheritance**: Superusers automatically have all permissions
2. **Role Expiration**: User roles can have expiration dates
3. **Audit Trail**: All role and permission assignments are tracked with timestamps and grantors
4. **Granular Control**: Permissions are resource and action specific
5. **Template Security**: Template context provides safe permission checking

## Best Practices

1. **Use Specific Permissions**: Prefer specific permissions over broad roles when possible
2. **Check Permissions in Views**: Always check permissions in view logic, not just templates
3. **Use Decorators**: Apply permission decorators consistently across views
4. **Test Permissions**: Regularly test permission assignments and access control
5. **Document Access Requirements**: Clearly document which roles and permissions are required for each feature

## Troubleshooting

### Common Issues

1. **Permission Denied Errors**: Check if user has the required role and permission
2. **Template Permission Checks**: Ensure context processor is enabled in settings
3. **AJAX Permission Errors**: Use appropriate AJAX decorators for JSON responses
4. **Role Assignment Issues**: Verify role assignments are not expired

### Debug Commands

```python
# Check user permissions
from apps.authentication.permissions import get_user_permissions, get_user_roles

user = User.objects.get(email='user@example.com')
permissions = get_user_permissions(user)
roles = get_user_roles(user)
```

## Future Enhancements

1. **Permission Groups**: Group related permissions for easier management
2. **Dynamic Permissions**: Runtime permission creation and assignment
3. **Permission Inheritance**: Hierarchical permission inheritance
4. **Audit Logging**: Detailed audit logs for permission changes
5. **API Permissions**: Enhanced API-level permission checking
