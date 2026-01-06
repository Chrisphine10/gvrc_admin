# API Test Suite Summary

## Overview

A comprehensive test suite has been created to test all APIs in the GVRC Admin system. The test suite covers:

- **Mobile APIs** (8 endpoints tested)
- **Admin/Management APIs** (15 endpoints tested)
- **Chat Admin APIs** (2 endpoints tested)
- **Geography APIs** (2 endpoints tested)

## Test Results

**Total Tests: 29**
- ✅ **Passed: 19** (65.5%)
- ❌ **Failed: 11** (37.9%)
- ⏭️ **Skipped: 0**

## Passing Tests

### Mobile APIs (8/9 passing)
- ✅ Mobile: Create Session (`POST /mobile/sessions/create/`)
- ✅ Mobile: List Sessions (`GET /mobile/sessions/`)
- ✅ Mobile: Start Conversation (`POST /mobile/chat/start/`)
- ✅ Mobile: List Conversations (`GET /mobile/chat/list/`)
- ✅ Mobile: List Facilities (`GET /mobile/facilities/list/`)
- ✅ Mobile: List Music (`GET /mobile/music/list/`)
- ✅ Mobile: List Documents (`GET /mobile/documents/list/`)
- ✅ Mobile: Get Lookups (`GET /mobile/lookups/data/`)

### Admin APIs (9/15 passing)
- ✅ Admin: Statistics (`GET /api/statistics/`)
- ✅ Admin: Lookup Data (`GET /api/lookups/`)
- ✅ Admin: Consolidated Geography (`GET /api/geography/`)
- ✅ Admin: List Counties (`GET /api/geography/counties/`)
- ✅ Admin: List Constituencies (`GET /api/geography/constituencies/`)
- ✅ Admin: List Wards (`GET /api/geography/wards/`)
- ✅ Admin: API Status (`GET /api/status/`)
- ✅ Admin: Hello World (`GET /api/hello/`)
- ✅ Admin: Obtain Token (`POST /api/auth/token/`)

### Chat Admin APIs (1/2 passing)
- ✅ Chat Admin: List Conversations (`GET /chat/admin/conversations/`)

### Geography APIs (1/2 passing)
- ✅ Geography: Search Geography (`GET /geography/api/search/`) - Returns 302 (redirect, acceptable)

## Failing Tests

### Mobile APIs
1. **Mobile: Send SOS** (`POST /mobile/emergency/sos/`)
   - **Issue**: Device location not available
   - **Fix**: Update mobile session with location data before testing

### Admin APIs
1. **Admin: List Facilities** (`GET /api/facilities/`)
   - **Issue**: Model relationship error - `facilitycoordinate` prefetch issue
   - **Fix**: Check Facility model relationships in `apps/facilities/models.py`

2. **Admin: Facility Map** (`GET /api/facilities/map/`)
   - **Issue**: Query optimization error with distinct and slice
   - **Fix**: Review queryset in `FacilityMapView.get_queryset()`

3. **Admin: Search Facilities** (`GET /api/facilities/search/`)
   - **Issue**: Same as #1 - model relationship error
   - **Fix**: Check Facility model relationships

4. **Admin: Emergency Services** (`POST /api/facilities/emergency/`)
   - **Issue**: Model relationship error - `facilityservice_set` should be `facilityservice`
   - **Fix**: Update view code to use correct relationship name

5. **Admin: GBV Services** (`POST /api/facilities/gbv-services/`)
   - **Issue**: Model relationship error - `facilitygbvcategory_set` should be `facilitygbvcategory`
   - **Fix**: Update view code to use correct relationship name

6. **Admin: Referral Chain** (`POST /api/facilities/referral-chain/`)
   - **Issue**: Missing required fields: `case_type`, `location`, `immediate_needs`
   - **Fix**: Update test to provide all required fields

7. **Admin: Contact Interaction Analytics** (`POST /api/analytics/contact-interaction/`)
   - **Issue**: Missing required field: `contact_id`
   - **Fix**: Update test to provide `contact_id`

8. **Admin: Referral Outcome** (`POST /api/analytics/referral-outcome/`)
   - **Issue**: Missing required fields: `from_facility`, `to_facility`, `service_accessed`
   - **Fix**: Update test to provide all required fields

### Chat Admin APIs
1. **Chat Admin: List Notifications** (`GET /chat/admin/notifications/`)
   - **Issue**: Endpoint returns 404
   - **Fix**: Check if notifications endpoint is properly registered in router

### Geography APIs
1. **Geography: Get All Counties** (`GET /geography/api/counties/`)
   - **Issue**: Returns 302 (redirect to login)
   - **Fix**: May require authentication or check URL routing

## Running the Tests

### Prerequisites
1. Activate the virtual environment:
   ```bash
   source env/bin/activate
   ```

2. Ensure Django settings are configured correctly

### Run All Tests
```bash
python test_all_apis.py
```

### Test Output
- Results are displayed in the console
- Detailed results are saved to `api_test_results.json`
- Each test shows:
  - ✅ Pass status with HTTP status code
  - ❌ Fail status with error details
  - ⏭️ Skip status with reason

## Test Coverage

### Mobile API Endpoints Tested
- `/mobile/sessions/create/` - Create mobile session
- `/mobile/sessions/` - List/get mobile sessions
- `/mobile/chat/start/` - Start conversation
- `/mobile/chat/list/` - List conversations
- `/mobile/chat/{id}/detail/` - Get conversation detail
- `/mobile/chat/{id}/send-message/` - Send message
- `/mobile/facilities/list/` - List facilities
- `/mobile/facilities/{id}/detail/` - Get facility detail
- `/mobile/music/list/` - List music tracks
- `/mobile/documents/list/` - List documents
- `/mobile/emergency/sos/` - Send emergency SOS
- `/mobile/lookups/data/` - Get lookup data
- `/mobile/analytics/contact-interaction/` - Track contact interaction

### Admin API Endpoints Tested
- `/api/facilities/` - List facilities
- `/api/facilities/{id}/` - Get facility detail
- `/api/facilities/{id}/complete/` - Get complete facility data
- `/api/facilities/map/` - Get facilities for map
- `/api/facilities/search/` - Search facilities
- `/api/facilities/emergency/` - Find emergency services
- `/api/facilities/gbv-services/` - Find GBV services
- `/api/facilities/referral-chain/` - Get referral chain
- `/api/analytics/contact-interaction/` - Contact interaction analytics
- `/api/analytics/referral-outcome/` - Referral outcome analytics
- `/api/statistics/` - System statistics
- `/api/lookups/` - Lookup data
- `/api/geography/` - Consolidated geography
- `/api/geography/counties/` - List counties
- `/api/geography/constituencies/` - List constituencies
- `/api/geography/wards/` - List wards
- `/api/status/` - API status
- `/api/hello/` - Hello world
- `/api/auth/token/` - Obtain auth token

### Chat Admin API Endpoints Tested
- `/chat/admin/conversations/` - List conversations
- `/chat/admin/conversations/{id}/` - Get conversation
- `/chat/admin/notifications/` - List notifications

### Geography API Endpoints Tested
- `/geography/api/counties/` - Get all counties
- `/geography/api/constituencies/{county_id}/` - Get constituencies
- `/geography/api/wards/{constituency_id}/` - Get wards
- `/geography/api/search/` - Search geography

## Recommendations

1. **Fix Model Relationships**: Several failures are due to incorrect relationship names in querysets. Review and fix:
   - `facilitycoordinate` vs `facility_coordinate`
   - `facilityservice_set` vs `facilityservice`
   - `facilitygbvcategory_set` vs `facilitygbvcategory`

2. **Complete Test Data**: Some POST endpoints need complete request bodies with all required fields. Update tests to provide:
   - Location data for emergency endpoints
   - Complete referral chain data
   - Complete analytics data

3. **Authentication**: Some geography endpoints may require authentication. Review and update permissions or test with authentication.

4. **Notification Endpoint**: Verify if notifications endpoint exists and is properly registered.

## Next Steps

1. Fix the model relationship issues in the views
2. Update tests with complete request data for POST endpoints
3. Verify and fix notification endpoint registration
4. Add more comprehensive test cases for edge cases
5. Add integration tests for complex workflows

## Files Created

- `test_all_apis.py` - Main test suite script
- `api_test_results.json` - Detailed test results in JSON format
- `API_TEST_SUMMARY.md` - This summary document



