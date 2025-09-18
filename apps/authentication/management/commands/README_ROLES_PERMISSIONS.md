# Roles and Permissions Management Commands

## Create Default Roles and Permissions

Use this command to set up the default roles and permissions system:

```bash
python manage.py create_default_roles_permissions
```

### Options

- `--force`: Force recreation even if roles/permissions already exist
- `--verbose`: Show detailed output

### Examples

```bash
# Basic usage
python manage.py create_default_roles_permissions

# Force recreation with detailed output
python manage.py create_default_roles_permissions --force --verbose

# Show detailed output without force
python manage.py create_default_roles_permissions --verbose
```

### What It Creates

**Roles (6):**
- Super Admin
- System Administrator  
- Facility Manager
- Data Analyst
- Regular User
- Content Manager

**Permissions (18):**
- User management: view, add, change, delete users
- Role management: view, add, change, delete roles
- Facility management: view, add, change, delete facilities
- Analytics: view analytics
- Document management: view, add, change, delete documents
- Admin: view admin interface, manage system

**Role-Permission Assignments:**
- Super Admin: All permissions
- System Administrator: User, role, admin, system permissions
- Facility Manager: Facility management permissions
- Data Analyst: View permissions
- Regular User: Basic view permissions (facilities, documents)
- Content Manager: Document management permissions

### Related Commands

- `python manage.py create_admin_user --password <password>` - Create admin user
- `python manage.py make_superuser <email>` - Make user a superuser
