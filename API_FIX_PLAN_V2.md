# API Test Failures - Comprehensive Fix Plan v2.0
## Data Engineering Best Practices Edition

## Overview
This document outlines a comprehensive, reversible, and auditable approach to fixing 11 failing API tests. All changes follow data engineering best practices including version control, backup strategies, rollback procedures, and object storage integration.

---

## 🎯 Core Principles

1. **Reversibility**: Every change must be reversible
2. **Auditability**: All changes tracked and logged
3. **Data Safety**: No data loss or corruption
4. **Version Control**: All changes in Git with proper commits
5. **Testing**: Comprehensive testing before and after changes
6. **Monitoring**: Observability for all changes
7. **Documentation**: Complete documentation of all changes

---

## 📋 Pre-Implementation Checklist

### Phase 0: Preparation & Safety (MUST COMPLETE FIRST)

#### 0.1 Version Control & Backup
- [ ] **Create feature branch**: `git checkout -b fix/api-test-failures-v2`
- [ ] **Verify clean working directory**: `git status`
- [ ] **Create backup tag**: `git tag backup-pre-api-fixes-$(date +%Y%m%d-%H%M%S)`
- [ ] **Database backup** (if using PostgreSQL):
  ```bash
  # PostgreSQL backup
  pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > backups/db_backup_$(date +%Y%m%d_%H%M%S).sql
  
  # SQLite backup (if applicable)
  cp db.sqlite3 backups/db_backup_$(date +%Y%m%d_%H%M%S).sqlite3
  ```
- [ ] **Media files backup** (if any):
  ```bash
  tar -czf backups/media_backup_$(date +%Y%m%d_%H%M%S).tar.gz media/
  ```

#### 0.2 Change Tracking Setup
- [ ] **Create change log file**: `CHANGES_API_FIXES_$(date +%Y%m%d).md`
- [ ] **Initialize audit trail**: Document all planned changes
- [ ] **Set up rollback scripts directory**: `mkdir -p scripts/rollback/`

#### 0.3 Environment Verification
- [ ] **Verify test environment**: Ensure test database is separate from production
- [ ] **Check Django migrations status**: `python manage.py showmigrations`
- [ ] **Verify dependencies**: `pip list > requirements_backup_$(date +%Y%m%d).txt`
- [ ] **Document current state**: Create baseline test results

#### 0.4 Object Storage Preparation (Optional but Recommended)
- [ ] **Configure object storage** (S3/Azure Blob/GCS) for:
  - Large query result caching
  - Analytics data export
  - Test data snapshots
  - Backup storage
- [ ] **Set up storage credentials** (use environment variables, never hardcode)
- [ ] **Create storage buckets/containers**:
  - `gvrc-api-cache` - Query result cache
  - `gvrc-api-backups` - Automated backups
  - `gvrc-api-exports` - Data exports

---

## 🔧 Implementation Plan

### Phase 1: Database & Model Analysis (Data Engineering Best Practices)

#### 1.1 Relationship Name Verification
**Objective**: Verify actual Django relationship names before making changes

**Steps**:
1. **Create verification script**: `scripts/verify_relationships.py`
   ```python
   #!/usr/bin/env python
   """Verify Django model relationships"""
   import os
   import django
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')
   django.setup()
   
   from apps.facilities.models import Facility
   from django.db import models
   
   # Get all related objects
   related_objects = []
   for field in Facility._meta.get_fields():
       if field.one_to_many or field.many_to_many:
           related_objects.append({
               'name': field.name,
               'related_name': getattr(field, 'related_name', None),
               'accessor_name': getattr(field, 'get_accessor_name', lambda: None)()
           })
   
   print("Facility Model Relationships:")
   for rel in related_objects:
       print(f"  - {rel}")
   ```

2. **Run verification**: `python scripts/verify_relationships.py > logs/relationship_verification.log`

3. **Document findings**: Update fix plan with actual relationship names

**Rollback**: No database changes, script only

---

### Phase 2: Code Changes with Reversibility

#### 2.1 Create Reversible Change Scripts

**For each fix, create:**
1. **Forward migration script**: `scripts/fixes/fix_<issue_number>.py`
2. **Rollback script**: `scripts/rollback/rollback_<issue_number>.py`
3. **Verification script**: `scripts/verify/fix_<issue_number>_verify.py`

**Template Structure**:
```python
# scripts/fixes/fix_01_facility_list_view.py
"""
Fix Issue 1: Admin List Facilities - Relationship Name
Reversible: Yes
Rollback: scripts/rollback/rollback_01_facility_list_view.py
"""
import os
import django
import shutil
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')
django.setup()

def apply_fix():
    """Apply the fix"""
    file_path = 'apps/api/views.py'
    backup_path = f'backups/views_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.py'
    
    # Create backup
    shutil.copy2(file_path, backup_path)
    print(f"✓ Backup created: {backup_path}")
    
    # Read file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Apply fix
    old_string = "Prefetch('facilitycoordinate',"
    new_string = "Prefetch('facilitycoordinate_set',"
    
    if old_string in content:
        content = content.replace(old_string, new_string)
        
        # Write back
        with open(file_path, 'w') as f:
            f.write(content)
        
        # Log change
        with open('CHANGES_API_FIXES.log', 'a') as log:
            log.write(f"{datetime.now()}: Fixed Issue 1 - facilitycoordinate -> facilitycoordinate_set\n")
        
        print("✓ Fix applied successfully")
        return True
    else:
        print("✗ Fix pattern not found")
        return False

def rollback():
    """Rollback the fix"""
    # Implementation in rollback script
    pass

if __name__ == '__main__':
    apply_fix()
```

---

### Phase 3: Database Migration Safety

#### 3.1 Create Safe Migration Strategy

**For any model changes** (if needed):
1. **Create migration**: `python manage.py makemigrations --name api_fixes_<issue>`
2. **Review migration**: Check generated SQL
3. **Test migration on copy**: Use test database first
4. **Create rollback migration**: Document reverse operations
5. **Add data validation**: Verify data integrity after migration

**Migration Template**:
```python
# apps/api/migrations/XXXX_api_fixes_relationship_names.py
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('api', 'previous_migration'),
    ]

    operations = [
        # Only if model changes needed
        # Otherwise, this is code-only fix
    ]
    
    # Rollback operations
    def rollback(self, apps, schema_editor):
        # Document reverse operations
        pass
```

---

### Phase 4: Object Storage Integration (Optional Enhancement)

#### 4.1 Query Result Caching
**Objective**: Cache expensive queries to object storage for better performance

**Implementation**:
```python
# apps/api/utils/storage_cache.py
import json
import hashlib
from django.core.cache import cache
from django.conf import settings
import boto3  # or azure-storage-blob, google-cloud-storage

class ObjectStorageCache:
    """Cache query results to object storage"""
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket = settings.AWS_CACHE_BUCKET
    
    def get_cache_key(self, query_params):
        """Generate cache key from query parameters"""
        key_string = json.dumps(query_params, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, cache_key):
        """Retrieve from object storage"""
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket,
                Key=f'query_cache/{cache_key}.json'
            )
            return json.loads(response['Body'].read())
        except:
            return None
    
    def set(self, cache_key, data, ttl=3600):
        """Store in object storage"""
        self.s3_client.put_object(
            Bucket=self.bucket,
            Key=f'query_cache/{cache_key}.json',
            Body=json.dumps(data),
            Metadata={'ttl': str(ttl)}
        )
```

**Usage in Views**:
```python
# In FacilityListView
from apps.api.utils.storage_cache import ObjectStorageCache

def get_queryset(self):
    cache = ObjectStorageCache()
    cache_key = cache.get_cache_key(self.request.query_params)
    
    # Try cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result
    
    # Execute query
    queryset = Facility.objects.select_related(...)
    # ... query logic ...
    
    # Cache result
    cache.set(cache_key, list(queryset.values()), ttl=3600)
    
    return queryset
```

#### 4.2 Analytics Data Export
**Objective**: Export large analytics datasets to object storage

**Implementation**:
```python
# apps/api/utils/data_export.py
class AnalyticsExporter:
    """Export analytics data to object storage"""
    
    def export_contact_interactions(self, start_date, end_date):
        """Export contact interactions to S3"""
        data = ContactInteraction.objects.filter(
            created_at__range=[start_date, end_date]
        ).values()
        
        # Export to S3
        export_key = f'exports/contact_interactions_{start_date}_{end_date}.json'
        self.s3_client.put_object(
            Bucket=settings.AWS_EXPORT_BUCKET,
            Key=export_key,
            Body=json.dumps(list(data), default=str)
        )
        
        return export_key
```

---

## 📝 Detailed Fix Implementation

### Issue 1: Admin: List Facilities
**Category**: Model Relationship Fix

**Implementation Steps**:
1. **Verify relationship name** (Phase 1.1)
2. **Create backup** of `apps/api/views.py`
3. **Apply fix** using reversible script
4. **Test locally** before committing
5. **Document change** in CHANGES log

**Fix Code**:
```python
# apps/api/views.py - Line 133
# BEFORE:
Prefetch(
    'facilitycoordinate',  # ❌
    queryset=FacilityCoordinate.objects.filter(),
    to_attr='active_coordinates'
),

# AFTER:
Prefetch(
    'facilitycoordinate_set',  # ✅
    queryset=FacilityCoordinate.objects.filter(is_active=True),
    to_attr='active_coordinates'
),
```

**Rollback**:
```python
# scripts/rollback/rollback_01_facility_list_view.py
# Restore from backup file
shutil.copy2('backups/views_backup_YYYYMMDD_HHMMSS.py', 'apps/api/views.py')
```

**Verification**:
```python
# scripts/verify/fix_01_verify.py
# Run API test and verify it passes
```

---

### Issue 2: Admin: Facility Map
**Category**: Query Optimization Fix

**Implementation Steps**:
1. **Analyze query performance** before fix
2. **Create performance baseline**
3. **Apply fix** with distinct() before slice
4. **Measure performance improvement**
5. **Add query result caching** (optional, Phase 4.1)

**Fix Code**:
```python
# apps/api/views.py - FacilityMapView.get_queryset()
# BEFORE:
if zoom_level <= 5:
    queryset = queryset.filter(...)[:1000]
elif zoom_level <= 8:
    queryset = queryset[:5000]
else:
    queryset = queryset[:10000]
return queryset.distinct()  # ❌

# AFTER:
queryset = queryset.distinct()  # ✅ Move distinct() before slice
if zoom_level <= 5:
    queryset = queryset.filter(...)[:1000]
elif zoom_level <= 8:
    queryset = queryset[:5000]
else:
    queryset = queryset[:10000]
return queryset
```

**Performance Monitoring**:
```python
# Add query timing
import time
start_time = time.time()
queryset = self.get_queryset()
execution_time = time.time() - start_time

# Log to monitoring system
logger.info(f"FacilityMapView query time: {execution_time}s")
```

---

### Issue 3: Admin: Search Facilities
**Category**: Model Relationship Fix

**Same approach as Issue 1**

---

### Issue 4: Admin: Emergency Services
**Category**: Model Relationship Fix

**Implementation Steps**:
1. **Verify relationship name** (may need to check model for related_name)
2. **Apply fix** based on verification
3. **Add query caching** for emergency queries (critical for performance)

**Fix Code** (after verification):
```python
# apps/api/views.py - EmergencyServicesView.post()
# Verify actual relationship name first, then apply:
queryset = Facility.objects.select_related(
    'ward__constituency__county',
    'operational_status'
).prefetch_related(
    'facilityservice__service_category',  # ✅ or 'facilityservice_set__service_category'
    'facilitycontact__contact_type'  # ✅ or 'facilitycontact_set__contact_type'
).filter(
    is_active=True,
    operational_status__status_name='Operational',
    facilityservice__service_category__category_name__in=service_types,  # ✅
    facilitycoordinate__latitude__isnull=False,
    facilitycoordinate__longitude__isnull=False
)
```

---

### Issue 5: Admin: GBV Services
**Category**: Model Relationship Fix

**Same approach as Issue 4**

---

### Issue 6: Mobile: Send SOS
**Category**: Test Data Fix

**Implementation Steps**:
1. **Update test setup** to include location data
2. **Add data validation** to ensure location is set
3. **Add error handling** for missing location

**Fix Code**:
```python
# test_all_apis.py - setup_test_data()
# AFTER creating mobile_session:
self.mobile_session.latitude = -1.2921  # Nairobi coordinates
self.mobile_session.longitude = 36.8219
self.mobile_session.location_updated_at = timezone.now()
self.mobile_session.location_permission_granted = True
self.mobile_session.save()

# Verify location was saved
assert self.mobile_session.latitude is not None
assert self.mobile_session.longitude is not None
```

---

### Issue 7-9: Test Data Fixes
**Category**: Test Data Enhancement

**Implementation Steps**:
1. **Create test data fixtures** (reusable)
2. **Use factories** for test data generation
3. **Add data validation** in tests
4. **Document test data requirements**

**Fix Code** (Issue 7 - Referral Chain):
```python
# test_all_apis.py - test_admin_apis()
# Create reusable test data
test_referral_data = {
    'case_type': 'sexual_violence',
    'location': {
        'county': 'Nairobi',
        'ward': 'Westlands'
    },
    'immediate_needs': ['medical_care', 'counseling'],
    'followup_needs': ['legal_support']
}

self.test_endpoint('POST', '/api/facilities/referral-chain/', 
                 'Admin: Referral Chain', 
                 data=test_referral_data, 
                 requires_auth=True)
```

**Test Data Factory** (Best Practice):
```python
# tests/factories.py
import factory
from apps.facilities.models import Facility, FacilityContact

class FacilityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Facility
    
    facility_name = factory.Sequence(lambda n: f"Test Facility {n}")
    # ... other fields

class FacilityContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FacilityContact
    
    facility = factory.SubFactory(FacilityFactory)
    # ... other fields
```

---

### Issue 10: Chat Admin: List Notifications
**Category**: Endpoint URL Fix

**Implementation Steps**:
1. **Update test** to use correct URL
2. **OR add list method** to ViewSet (if needed)
3. **Document endpoint behavior**

**Fix Code**:
```python
# test_all_apis.py - test_chat_admin_apis()
self.test_endpoint('GET', '/chat/admin/notifications/unread/', 
                 'Chat Admin: List Unread Notifications', 
                 requires_auth=True)
```

---

### Issue 11: Geography: Get All Counties
**Category**: Authentication Fix

**Implementation Steps**:
1. **Update test** to use authenticated client
2. **OR update view** to use API authentication (if appropriate)
3. **Document authentication requirements**

**Fix Code**:
```python
# test_all_apis.py - test_geography_apis()
self.test_endpoint('GET', '/geography/api/counties/', 
                 'Geography: Get All Counties', 
                 requires_auth=True)  # ✅ Add authentication
```

---

## 🔄 Rollback Procedures

### Complete Rollback Strategy

#### Step 1: Code Rollback
```bash
# Restore from Git
git checkout backup-pre-api-fixes-YYYYMMDD-HHMMSS
# OR
git revert <commit-hash>
```

#### Step 2: Database Rollback (if migrations applied)
```bash
# Rollback migrations
python manage.py migrate api <previous_migration_number>
```

#### Step 3: Restore Backups
```bash
# Restore database
psql -h $DB_HOST -U $DB_USER -d $DB_NAME < backups/db_backup_YYYYMMDD_HHMMSS.sql

# Restore media files
tar -xzf backups/media_backup_YYYYMMDD_HHMMSS.tar.gz
```

#### Step 4: Verify Rollback
```bash
# Run tests to verify
python test_all_apis.py
```

---

## 📊 Monitoring & Observability

### 1. Change Tracking
**File**: `CHANGES_API_FIXES_YYYYMMDD.md`
```markdown
# API Fixes Change Log - YYYY-MM-DD

## Issue 1: Admin List Facilities
- **Time**: 2024-11-26 10:00:00
- **Change**: Updated relationship name from 'facilitycoordinate' to 'facilitycoordinate_set'
- **File**: apps/api/views.py:133
- **Rollback**: scripts/rollback/rollback_01_facility_list_view.py
- **Verified**: Yes
- **Test Result**: PASS
```

### 2. Performance Monitoring
**Add to views**:
```python
import time
import logging

logger = logging.getLogger(__name__)

class FacilityListView(generics.ListAPIView):
    def get_queryset(self):
        start_time = time.time()
        queryset = super().get_queryset()
        execution_time = time.time() - start_time
        
        logger.info(f"FacilityListView query executed in {execution_time:.3f}s")
        
        # Alert if query is slow
        if execution_time > 1.0:
            logger.warning(f"Slow query detected: {execution_time:.3f}s")
        
        return queryset
```

### 3. Error Tracking
**Add exception logging**:
```python
import logging
from sentry_sdk import capture_exception  # If using Sentry

try:
    queryset = Facility.objects.select_related(...)
except Exception as e:
    logger.error(f"Error in FacilityListView: {str(e)}", exc_info=True)
    capture_exception(e)  # Send to error tracking
    raise
```

---

## ✅ Testing Strategy

### 1. Pre-Implementation Testing
- [ ] Run current test suite: `python test_all_apis.py`
- [ ] Document baseline: Save results to `test_results_baseline.json`
- [ ] Verify test environment isolation

### 2. Incremental Testing
- [ ] Test each fix individually
- [ ] Verify no regression in passing tests
- [ ] Test edge cases
- [ ] Performance testing for query optimizations

### 3. Post-Implementation Testing
- [ ] Run full test suite
- [ ] Compare results with baseline
- [ ] Integration testing
- [ ] Load testing (if applicable)

### 4. Rollback Testing
- [ ] Test rollback procedures
- [ ] Verify data integrity after rollback
- [ ] Document rollback test results

---

## 📦 Deployment Strategy

### 1. Staging Deployment
```bash
# Deploy to staging
git push origin fix/api-test-failures-v2
# Run tests on staging
# Verify all fixes work
```

### 2. Production Deployment
```bash
# Create release branch
git checkout -b release/api-fixes-v2.0
# Merge fixes
git merge fix/api-test-failures-v2
# Tag release
git tag -a v2.0.0 -m "API fixes with data engineering best practices"
# Deploy to production
```

### 3. Post-Deployment Monitoring
- [ ] Monitor error rates
- [ ] Monitor query performance
- [ ] Monitor API response times
- [ ] Check logs for issues

---

## 📚 Documentation Updates

### Files to Update:
1. **API_TEST_SUMMARY.md** - Update with new results
2. **CHANGELOG.md** - Document all changes
3. **API_FIX_PLAN_V2.md** - This document (mark as completed)
4. **README.md** - Update if needed
5. **DATABASE_SCHEMA.md** - Update if model changes made

---

## 🎯 Success Criteria

### Must Have:
- [ ] All 11 failing tests now pass
- [ ] No new test failures introduced
- [ ] All changes documented
- [ ] Rollback procedures tested and working
- [ ] Performance maintained or improved
- [ ] No data loss or corruption

### Nice to Have:
- [ ] Query result caching implemented
- [ ] Object storage integration for large datasets
- [ ] Performance improvements measured
- [ ] Monitoring and alerting set up

---

## 📋 Implementation Checklist

### Phase 0: Preparation
- [ ] Create feature branch
- [ ] Create backups (database, media, code)
- [ ] Set up change tracking
- [ ] Verify environment
- [ ] Set up object storage (optional)

### Phase 1: Analysis
- [ ] Verify relationship names
- [ ] Document findings
- [ ] Create baseline metrics

### Phase 2: Implementation
- [ ] Fix Issue 1 (List Facilities)
- [ ] Fix Issue 2 (Facility Map)
- [ ] Fix Issue 3 (Search Facilities)
- [ ] Fix Issue 4 (Emergency Services)
- [ ] Fix Issue 5 (GBV Services)
- [ ] Fix Issue 6 (Mobile SOS)
- [ ] Fix Issue 7 (Referral Chain)
- [ ] Fix Issue 8 (Contact Analytics)
- [ ] Fix Issue 9 (Referral Outcome)
- [ ] Fix Issue 10 (Notifications)
- [ ] Fix Issue 11 (Geography)

### Phase 3: Testing
- [ ] Run individual tests
- [ ] Run full test suite
- [ ] Performance testing
- [ ] Rollback testing

### Phase 4: Deployment
- [ ] Deploy to staging
- [ ] Verify on staging
- [ ] Deploy to production
- [ ] Monitor post-deployment

### Phase 5: Documentation
- [ ] Update all documentation
- [ ] Create change log
- [ ] Document lessons learned

---

## 🔐 Security Considerations

1. **Credentials**: Never hardcode credentials, use environment variables
2. **Object Storage**: Use IAM roles and bucket policies
3. **Backups**: Encrypt backups at rest
4. **Audit Logs**: Secure audit log storage
5. **Access Control**: Limit who can rollback changes

---

## 📞 Support & Escalation

### If Issues Arise:
1. **Check logs**: Review application and error logs
2. **Verify backups**: Ensure backups are accessible
3. **Test rollback**: Verify rollback procedures work
4. **Contact team**: Escalate if needed

### Emergency Rollback:
```bash
# Quick rollback script
./scripts/emergency_rollback.sh
```

---

## 📅 Timeline Estimate

- **Phase 0 (Preparation)**: 1-2 hours
- **Phase 1 (Analysis)**: 1 hour
- **Phase 2 (Implementation)**: 3-4 hours
- **Phase 3 (Testing)**: 2-3 hours
- **Phase 4 (Deployment)**: 1-2 hours
- **Phase 5 (Documentation)**: 1 hour

**Total Estimated Time**: 9-13 hours

---

## ✅ Final Approval Checklist

- [ ] All team members reviewed plan
- [ ] Backups created and verified
- [ ] Rollback procedures tested
- [ ] Object storage configured (if applicable)
- [ ] Monitoring set up
- [ ] Documentation complete
- [ ] Ready to proceed

---

**Created**: 2024-11-26  
**Version**: 2.0  
**Status**: Awaiting Approval  
**Next Steps**: Review and approve before implementation



