# Hodi Admin - Multi-Institutional GBV Response Platform

**A comprehensive Django-based system for managing all facilities and institutions involved in Gender-Based Violence (GBV) response in Kenya, including police stations, hospitals, NGOs, safe houses, legal aid centers, and community organizations.**

## 🎯 Multi-Institutional GBV Response System

This platform serves as a **centralized directory and coordination hub** for all institutions involved in GBV response, enabling seamless inter-agency coordination and survivor support across different sectors.

### 🏢 Supported Institution Types

#### **Health Sector**
- 🏥 **Hospitals** - Emergency care, medical examination, treatment
- 🏥 **Health Centers** - Primary healthcare, counseling referrals
- 🏥 **Clinics** - Specialized care, mental health services

#### **Law Enforcement & Security**
- 👮 **Police Stations** - Crime reporting, investigation, protection
- 👮 **Police Posts** - Community policing, first response
- 🛡️ **Security Facilities** - Witness protection, safe transportation

#### **NGOs & Civil Society**
- 🤝 **Non-Governmental Organizations** - Advocacy, support services
- 🏘️ **Community-Based Organizations (CBOs)** - Local support, awareness
- ⛪ **Faith-Based Organizations** - Spiritual support, shelter

#### **Specialized GBV Services**
- 🏠 **Safe Houses** - Emergency accommodation, protection
- ⚖️ **Legal Aid Centers** - Legal representation, court support
- 📞 **Gender Desks** - Specialized GBV units within institutions
- 🧠 **Counseling Centers** - Psychological support, therapy

### 🎯 GBV Service Categories

The system categorizes GBV response services into four main areas:

1. **🤜 Physical Violence** - Medical care, forensic examination, treatment
2. **💔 Sexual Violence** - Post-exposure prophylaxis, counseling, legal support
3. **🧠 Emotional/Psychological Violence** - Mental health services, therapy, support groups
4. **💰 Economic Violence** - Financial literacy, economic empowerment, legal aid

### 🏢 Institutional Ownership Models

- **🏛️ Public** - Government hospitals, police stations, public health facilities
- **🏢 Private** - Private hospitals, clinics, security companies
- **⛪ Faith-Based** - Church-run hospitals, religious shelter organizations
- **🤝 NGO** - International and local NGOs providing GBV services
- **🏘️ Community-Owned** - Community-managed safe houses, support centers

---

## 🚀 Quick Start (local)

Python 3.15 (3.12+ works). Local development uses SQLite; never point local
tools at a production database.

```bash
uv venv --python 3.15.2 venv          # or: python -m venv venv
venv/Scripts/python -m pip install -r requirements-dev.txt   # Linux/macOS: venv/bin/python
venv/Scripts/python run_local.py migrate
venv/Scripts/python run_local.py runserver 127.0.0.1:8000
```

* Web: http://127.0.0.1:8000/ (landing page), staff dashboard at `/dashboard/`
* API docs: `/swagger/`
* Staff accounts are created by an administrator (`createsuperuser`, then
  Users in the dashboard). Self-registration is off unless
  `ALLOW_SELF_REGISTRATION=true`.

### Tests

```bash
venv/Scripts/python -m pytest -q --no-cov      # ~1,300 tests, settings core.settings.test (in-memory SQLite)
venv/Scripts/python manage.py check_data       # read-only data consistency report
```

### Production

See [DEPLOY.md](./DEPLOY.md): server layout, routine update, rollback.

---

## 🗂️ Project layout

```
apps/
  authentication/  users, roles and permissions (custom RBAC), login, password reset (email + SMS)
  facilities/      facilities, contacts, services, map; manage.py repair_contacts
  geography/       counties / constituencies / wards
  lookups/         reference lists (contact types, GBV categories, ...)
  chat/            help chats between the app and staff (+ SMS alerts)
  mobile/, mobile_sessions/  the mobile app API (/mobile/...)
  api/             REST API (/api/...)
  sms/             bulk SMS and chat alerts through Bonga (Intelli-Wealth)
  common/          application settings, map settings, check_data
  documents/, music/, analytics/, monitoring/, home/
  templates/, static/   web UI (Argon/Bootstrap + assets/css/hodi-theme.css)
core/              settings (dev/prod/test), urls, errors.py (error pages + API errors), storage
tests/             pytest suite
docs/              design notes and older documentation
scripts/           one-off tools (not collected by pytest)
systemd/           hodi-sms service + timer
```

### Errors

Clients never see exception text. The app and API get JSON
(`{"error": "...", "detail": ...}`), browsers get the branded 403/404/500 pages,
and the real exception is logged with its traceback (`core/errors.py`).

### Technology stack
- **Backend**: Django 6.1, Django REST Framework 3.18, Python 3.15
- **Database**: SQLite (production and local), PostgreSQL supported (`DJANGO_ENV=postgres`)
- **Web UI**: Argon Dashboard (Bootstrap 4.6) with the Hodi theme; Leaflet/OpenStreetMap or Google Maps
- **SMS**: Bonga SMS (Intelli-Wealth account)
- **Serving**: gunicorn 27 behind nginx

---

## 📱 Comprehensive API Documentation for Mobile Integration

### 🚀 **Base URL & Authentication**
```
Base URL: https://your-domain.com/api/
Documentation: https://your-domain.com/swagger/
```

**Authentication Methods:**
```bash
# Token Authentication (Recommended)
Authorization: Token <your_token_here>

# Session Authentication (Web)
X-CSRFToken: <csrf_token_here>
```

---

### 🏥 **Core Facility Endpoints**

#### **1. List All Facilities** `GET /api/facilities/`
```bash
# Advanced filtering and search
curl "http://localhost:8000/api/facilities/?search=hospital&county=1&status=1&has_coordinates=true" \
     -H "Authorization: Token YOUR_TOKEN"
```

**Query Parameters:**
- `search` - Search by name, registration, location
- `county` - Filter by county ID  
- `constituency` - Filter by constituency ID
- `ward` - Filter by ward ID
- `status` - Filter by operational status ID
- `service_category` - Filter by service category ID
- `has_coordinates` - Only facilities with GPS (`true`/`false`)
- `page` - Page number (default: 1)
- `page_size` - Items per page (max 100, default: 20)

#### **2. Facility Details** `GET /api/facilities/{id}/`
```bash
# Get complete facility information with all related data
curl "http://localhost:8000/api/facilities/123/" \
     -H "Authorization: Token YOUR_TOKEN"
```

**Response includes:**
- Complete facility information
- All contact details (phone, email, WhatsApp, emergency)
- Services offered with categories
- GPS coordinates and location data
- Ownership information
- GBV service categories
- Operational status

#### **3. Advanced Facility Search** `POST /api/facilities/search/`
```bash
# Complex search with multiple criteria
curl -X POST "http://localhost:8000/api/facilities/search/" \
     -H "Authorization: Token YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "search": "health center",
       "county": 1,
       "service_category": 1,
       "has_coordinates": true,
       "page_size": 10
     }'
```

#### **4. Map View Facilities** `GET /api/facilities/map/`
```bash
# Get facilities with GPS coordinates for map display
curl "http://localhost:8000/api/facilities/map/?county=1" \
     -H "Authorization: Token YOUR_TOKEN"
```

---

### 🎯 **Specialized GBV Response Endpoints**

#### **1. Emergency SOS Services** `POST /api/facilities/emergency/`
```bash
# Find nearest emergency services with 24/7 availability
curl -X POST "http://localhost:8000/api/facilities/emergency/" \
     -H "Authorization: Token YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "latitude": -1.2921,
       "longitude": 36.8219,
       "radius_km": 10,
       "service_types": ["Emergency Services", "Security Services"],
       "urgent": true
     }'
```

**🚨 SOS Button Integration:**
```javascript
// Emergency SOS button implementation
const handleSOSPress = async (userLocation) => {
  try {
    const emergencyServices = await fetch('/api/facilities/emergency/', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${userToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        latitude: userLocation.latitude,
        longitude: userLocation.longitude,
        radius_km: 5,
        service_types: ["Emergency Services", "Security Services"],
        urgent: true
      })
    });
    
    const services = await emergencyServices.json();
    
    // Auto-dial first available emergency contact
    if (services.results.length > 0) {
      const emergencyContact = services.results[0].emergency_contact;
      Linking.openURL(`tel:${emergencyContact}`);
    }
  } catch (error) {
    // Fallback to national emergency numbers
    Linking.openURL('tel:999'); // Kenya Police Emergency
  }
};
```

#### **2. GBV-Specific Service Search** `POST /api/facilities/gbv-services/`
```bash
# Find facilities by GBV service category
curl -X POST "http://localhost:8000/api/facilities/gbv-services/" \
     -H "Authorization: Token YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "gbv_category": "Sexual Violence",
       "service_types": ["Health Services", "Legal Services"],
       "county": 1,
       "available_24_7": true
     }'
```

#### **3. Multi-Service Referral Chain** `POST /api/facilities/referral-chain/`
```bash
# Get recommended service pathway for GBV cases
curl -X POST "http://localhost:8000/api/facilities/referral-chain/" \
     -H "Authorization: Token YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "case_type": "Sexual Violence",
       "location": {"county": 1, "ward": 15},
       "immediate_needs": ["Medical Care", "Police Report", "Safe House"],
       "followup_needs": ["Legal Aid", "Counseling"]
     }'
```

---

### 🔗 **Interconnected Data Endpoints**

#### **1. Facility with All Relations** `GET /api/facilities/{id}/complete/`
```bash
# Get facility with all interconnected data in single request
curl "http://localhost:8000/api/facilities/123/complete/" \
     -H "Authorization: Token YOUR_TOKEN"
```

**Includes:**
- Facility details
- All contacts (with click tracking)
- All services offered
- GPS coordinates
- Owner information
- GBV categories
- Recent activity/analytics

#### **2. Cross-Reference Services** `GET /api/services/cross-reference/`
```bash
# Find facilities offering multiple complementary services
curl "http://localhost:8000/api/services/cross-reference/?services=1,3,5&county=1" \
     -H "Authorization: Token YOUR_TOKEN"
```

#### **3. Contact Network** `GET /api/contacts/network/{facility_id}/`
```bash
# Get contact network including partner organizations
curl "http://localhost:8000/api/contacts/network/123/" \
     -H "Authorization: Token YOUR_TOKEN"
```

#### **4. Geographic Service Coverage** `GET /api/geography/coverage/`
```bash
# Analyze service coverage by geographic area
curl "http://localhost:8000/api/geography/coverage/?county=1&service_type=1" \
     -H "Authorization: Token YOUR_TOKEN"
```

---

### 📊 **Analytics & Tracking Endpoints**

#### **1. Contact Click Tracking** `POST /api/analytics/contact-click/`
```bash
# Track when users contact a facility
curl -X POST "http://localhost:8000/api/analytics/contact-click/" \
     -H "Authorization: Token YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "facility_id": 123,
       "contact_id": 456,
       "contact_type": "Phone",
       "helpful": true,
       "user_location": {"latitude": -1.2921, "longitude": 36.8219}
     }'
```

#### **2. Referral Success Tracking** `POST /api/analytics/referral-outcome/`
```bash
# Track referral outcomes between facilities
curl -X POST "http://localhost:8000/api/analytics/referral-outcome/" \
     -H "Authorization: Token YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "from_facility": 123,
       "to_facility": 456,
       "service_accessed": true,
       "satisfaction_rating": 4,
       "case_type": "Sexual Violence"
     }'
```

#### **3. Usage Statistics** `GET /api/statistics/`
```bash
# Comprehensive system statistics
curl "http://localhost:8000/api/statistics/" \
     -H "Authorization: Token YOUR_TOKEN"
```

---

### 📱 **Mobile API Endpoints**

The system provides dedicated mobile-optimized endpoints designed specifically for mobile applications and field workers. **Mobile apps use session-based authentication - no user login required.**

#### **1. Mobile Facilities** `GET /api/mobile/facilities/`
```bash
# Get facilities optimized for mobile consumption
curl "http://localhost:8000/api/mobile/facilities/?device_id=mobile_device_123&page=1&page_size=20"
```

**Note**: `device_id` passed as query parameter for mobile session authentication.

**Mobile Optimizations:**
- Reduced payload size
- Essential fields only
- Efficient pagination
- GPS coordinate prioritization

#### **2. Mobile Emergency SOS** `POST /api/mobile/emergency-sos/`
```bash
# Find nearest emergency facilities using mobile session location
curl -X POST "http://localhost:8000/api/mobile/emergency-sos/" \
     -H "Content-Type: application/json" \
     -d '{
       "device_id": "mobile_device_123",
       "emergency_type": "Medical",
       "radius_km": 5
     }'
```

**Note**: Location automatically retrieved from mobile session, no need to provide coordinates.

#### **3. Mobile Contact Interaction** `POST /api/mobile/contact-interaction/`
```bash
# Track contact interactions from mobile devices
curl -X POST "http://localhost:8000/api/mobile/contact-interaction/" \
     -H "Content-Type: application/json" \
     -d '{
       "contact_id": 123,
       "device_id": "mobile_device_123",
       "is_helpful": true
     }'
```

**Note**: `device_id` is required in request body to identify mobile session, location automatically retrieved from mobile session.

**Mobile-Specific Features:**
- Device ID tracking for mobile analytics
- GPS coordinate capture
- Simplified response format
- Mobile-optimized error handling

#### **4. Mobile Sessions** `POST /api/mobile/sessions/`
```bash
# Create mobile device sessions (no authentication required)
curl -X POST "http://localhost:8000/api/mobile/sessions/" \
     -H "Content-Type: application/json" \
     -d '{
       "device_id": "mobile_device_abc123",
       "device_type": "Android",
       "app_version": "1.0.0",
       "latitude": -1.2921,
       "longitude": 36.8219
     }'
```

#### **4a. End Mobile Session** `POST /api/mobile/sessions/end/`
```bash
# End mobile device session
curl -X POST "http://localhost:8000/api/mobile/sessions/end/" \
     -H "Content-Type: application/json" \
     -d '{
       "device_id": "mobile_device_123"
     }'
```

**Note**: Session end requires `device_id` in request body for validation.

#### **5. Mobile Documents** `GET /api/mobile/documents/`
```bash
# Access documents optimized for mobile viewing
curl "http://localhost:8000/api/mobile/documents/?device_id=mobile_device_123"
```

**Note**: `device_id` passed as query parameter for mobile session authentication.

#### **6. Mobile Music** `GET /api/mobile/music/`
```bash
# Access music content for mobile applications
curl "http://localhost:8000/api/mobile/music/?device_id=mobile_device_123"
```

**Note**: `device_id` passed as query parameter for mobile session authentication.

**Mobile API Benefits:**
- **Anonymous Access**: No user registration or login required
- **Session-Based Auth**: Mobile session acts as authentication mechanism
- **Device Tracking**: Built-in mobile device session management
- **Location Awareness**: GPS coordinates automatically available from session
- **Performance**: Optimized queries and response formats
- **User Privacy**: No personal information required for basic functionality

### 🔐 **Mobile Session Authentication**
Mobile apps create anonymous sessions using device IDs and location data:
1. **Create Session**: `POST /api/mobile/sessions/` with device_id and location
2. **Use APIs**: All mobile endpoints automatically validate the session
3. **No Login**: Traditional user authentication not required
4. **Location Services**: GPS coordinates stored in session for location-based features

---

### 🗂️ **Lookup Data Endpoints**

#### **1. All Lookup Data** `GET /api/lookups/`
```bash
# Get all reference data for forms and filters
curl "http://localhost:8000/api/lookups/" \
     -H "Authorization: Token YOUR_TOKEN"
```

#### **2. Geography Hierarchy** 
```bash
# Counties
GET /api/geography/counties/

# Constituencies by county
GET /api/geography/constituencies/?county=1

# Wards by constituency  
GET /api/geography/wards/?constituency=1
```

---

### 📱 **Mobile App Integration Examples**

#### **React Native Implementation**
```javascript
// Emergency SOS Component
const SOSButton = () => {
  const handleEmergencyPress = async () => {
    const location = await getCurrentLocation();
    
    const emergencyServices = await fetchEmergencyServices({
      latitude: location.latitude,
      longitude: location.longitude,
      radius_km: 10,
      urgent: true
    });
    
    // Show emergency options modal
    showEmergencyModal(emergencyServices);
  };

  return (
    <TouchableOpacity 
      style={styles.sosButton}
      onPress={handleEmergencyPress}
    >
      <Text>🚨 SOS</Text>
    </TouchableOpacity>
  );
};

// Service Finder Hook
const useGBVServices = () => {
  const findNearbyServices = async (serviceType, location) => {
    return await fetch('/api/facilities/search/', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${userToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        county: location.county,
        service_category: serviceType,
        has_coordinates: true,
        page_size: 20
      })
    }).then(res => res.json());
  };

  return { findNearbyServices };
};
```

#### **Flutter Implementation**
```dart
class GBVServicesAPI {
  static const String baseUrl = 'https://your-domain.com/api';
  
  // Emergency SOS functionality
  static Future<List<Facility>> getEmergencyServices({
    required double latitude,
    required double longitude,
    int radiusKm = 10,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/facilities/emergency/'),
      headers: {
        'Authorization': 'Token $userToken',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'latitude': latitude,
        'longitude': longitude,
        'radius_km': radiusKm,
        'service_types': ['Emergency Services', 'Security Services'],
        'urgent': true
      }),
    );
    
    if (response.statusCode == 200) {
      return Facility.fromJsonList(jsonDecode(response.body)['results']);
    } else {
      throw Exception('Failed to load emergency services');
    }
  }
  
  // Track contact interaction
  static Future<void> trackContactClick({
    required int facilityId,
    required int contactId,
    required String contactType,
    bool helpful = true,
  }) async {
    await http.post(
      Uri.parse('$baseUrl/analytics/contact-click/'),
      headers: {
        'Authorization': 'Token $userToken',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'facility_id': facilityId,
        'contact_id': contactId,
        'contact_type': contactType,
        'helpful': helpful,
      }),
    );
  }
}
```

---

### 🔗 **Quick Reference Links**

#### **📖 Complete API Documentation**
- **Swagger UI**: `https://your-domain.com/swagger/` - Interactive API testing
- **ReDoc**: `https://your-domain.com/redoc/` - Beautiful API documentation
- **Postman Collection**: Available for download

#### **🚨 Emergency Contacts Integration**
```bash
# National Emergency Numbers (Kenya)
Police: 999, 112
Ambulance: 999, 112  
Fire: 999, 112
Gender Violence Recovery Centre: 116
```

#### **📊 Rate Limiting & Performance**
- **Rate Limit**: 1000 requests/hour per user
- **Pagination**: Max 100 items per request
- **Caching**: Statistics cached 5 minutes, lookups 10 minutes
- **Response Time**: <200ms for standard queries

---

## 🔧 Development

### Add New Feature
1. Create model in appropriate app
2. Add API serializer and view
3. Configure admin interface
4. Add URL routing
5. Update documentation

### Testing
```bash
python manage.py test                    # Run tests
curl http://localhost:8000/api/status/   # Test API
```

### Database Commands
```bash
python manage.py makemigrations          # Create migrations
python manage.py migrate                 # Apply migrations
python manage.py load_initial_data       # Load sample data
python manage.py create_test_user        # Create test user
```

---

## 🚀 Deployment

### Docker
```bash
docker-compose up --build
```

### Render.com
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn core.wsgi:application`
4. Configure environment variables

### Environment Variables
```env
DJANGO_SETTINGS_MODULE=core.settings.prod
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:pass@host:5432/dbname
ALLOWED_HOSTS=your-domain.com
```

---

## 📊 Current Status

✅ **Multi-Institutional GBV Platform** - Complete system supporting all GBV response sectors  
✅ **Cross-Sector Database** - Police, hospitals, NGOs, legal centers, safe houses  
✅ **GBV Service Categories** - Physical, sexual, emotional, economic violence support  
✅ **Inter-Agency API** - REST API optimized for cross-sector coordination  
✅ **Field Worker Mobile Support** - Optimized for emergency response and referrals  
✅ **Referral Tracking** - Analytics for inter-agency coordination effectiveness  
✅ **Comprehensive Documentation** - Multi-institutional setup and usage guides  

### 🎯 GBV Response Coverage
- **👮 Law Enforcement** - Police stations and security facilities registered
- **🏥 Health Sector** - Hospitals, clinics, and health centers with GBV services  
- **🤝 NGO Sector** - CBOs, faith-based organizations, and NGOs providing GBV support
- **⚖️ Legal Services** - Legal aid centers and gender desks for survivor support
- **🏠 Safe Houses** - Emergency accommodation and protection facilities  

---

## 🆘 Support

- **📖 Documentation**: [Complete Guide](./docs/GVRC_ADMIN_COMPLETE_DOCUMENTATION.md)
- **🔧 Troubleshooting**: [Common Issues](./docs/GVRC_ADMIN_COMPLETE_DOCUMENTATION.md#troubleshooting)
- **📧 Email**: admin@gvrc.com
- **🐛 Issues**: Create issue in repository

---

## 📝 License

This project is for internal use by Hodi Admin system. See documentation for full terms.

---

**Built with ❤️ using Django and Django REST Framework**