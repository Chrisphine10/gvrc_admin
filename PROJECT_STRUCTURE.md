# Django Project Structure - Professional Organization

## 📁 Current Project Structure

```
gvrc_dmin/
│
├── manage.py
├── requirements.txt
├── .env.example                 ← Environment variables template
├── PROJECT_STRUCTURE.md         ← This file
│
├── core/                        ← Main settings package
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py          ← Imports dev.py by default
│   │   ├── base.py              ← Base settings
│   │   ├── dev.py               ← Development settings
│   │   └── prod.py              ← Production settings
│   ├── urls.py                  ← Global URLConf with Swagger
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/                        ← All Django apps live here
│   ├── __init__.py
│   ├── common/                  ← Shared logic/utilities
│   │   ├── __init__.py
│   │   ├── models.py            ← Abstract base classes
│   │   └── utils.py             ← Helper functions
│   ├── home/                    ← Home/landing page app
│   │   ├── __init__.py
│   │   ├── urls.py              ← Home URLs with namespacing
│   │   ├── views.py             ← Professional view naming
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── migrations/
│   └── api/                     ← API endpoints
│       ├── __init__.py
│       ├── apps.py
│       ├── urls.py              ← API URLs
│       ├── views.py             ← API views
│       └── serializers.py       ← DRF serializers
│
├── static/                      ← Static files
├── media/                       ← Media uploads (to be created)
├── templates/                   ← Global templates
└── helpers/                     ← Legacy helpers (kept for compatibility)
```

## 🚀 Key Improvements Made

### 1. **Settings Organization**
- Split settings into `base.py`, `dev.py`, and `prod.py`
- Environment-specific configurations
- Secure production settings

### 2. **App Structure**
- Moved `home` app to `apps/home/`
- Created `apps/api/` for API endpoints
- Created `apps/common/` for shared utilities
- Added proper app namespacing

### 3. **API Integration**
- Added Django REST Framework
- Integrated Swagger/OpenAPI documentation
- Created sample API endpoints

### 4. **Professional Routing**
- Organized URLs with proper namespacing
- Added API versioning structure
- Integrated Swagger UI at `/swagger/`

## 🔧 Usage Instructions

### Environment Setup
1. Copy `.env.example` to `.env`
2. Update environment variables as needed

### API Documentation
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

### Sample API Endpoints
- `GET /api/hello/` - Hello world endpoint
- `GET /api/status/` - API status check

### Settings Management
- Development: Uses `core.settings.dev` (default)
- Production: Set `DJANGO_SETTINGS_MODULE=core.settings.prod`

## 📦 New Dependencies Added
- `djangorestframework` - REST API framework
- `drf-yasg` - Swagger/OpenAPI integration
- `python-decouple` - Environment variable management

## 🔄 Backward Compatibility
- Old URLs still work (home page)
- Legacy helper functions maintained
- Existing models and admin unchanged

## 🎯 Next Steps
1. Run `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Create superuser: `python manage.py createsuperuser`
4. Start development server: `python manage.py runserver`
5. Visit `/swagger/` to explore the API documentation