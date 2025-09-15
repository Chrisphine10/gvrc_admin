DUMthe # Database Schema Documentation

## Overview

This document describes the complete database schema for the Hodi Admin system, which has been restructured to align with the specified requirements.

## Database Structure

### 1. Geographical Entities

#### Counties
- **Table**: `counties`
- **Purpose**: Administrative divisions at the county level
- **Key Fields**: `county_id` (PK), `county_name`

#### Constituencies
- **Table**: `constituencies`
- **Purpose**: Administrative divisions within counties
- **Key Fields**: `constituency_id` (PK), `constituency_name`, `county_id` (FK)
- **Indexes**: `county_id`

#### Wards
- **Table**: `wards`
- **Purpose**: Administrative divisions within constituencies
- **Key Fields**: `ward_id` (PK), `ward_name`, `constituency_id` (FK)
- **Indexes**: `constituency_id`

### 2. Lookup Tables

#### Operational Statuses
- **Table**: `operational_statuses`
- **Purpose**: Available operational statuses for facilities
- **Key Fields**: `operational_status_id` (PK), `status_name`

#### Contact Types
- **Table**: `contact_types`
- **Purpose**: Types of contact information
- **Key Fields**: `contact_type_id` (PK), `type_name`

#### Service Categories
- **Table**: `service_categories`
- **Purpose**: Categories of services offered by facilities
- **Key Fields**: `service_category_id` (PK), `category_name`

#### Owner Types
- **Table**: `owner_types`
- **Purpose**: Types of facility ownership
- **Key Fields**: `owner_type_id` (PK), `type_name`

#### GBV Categories
- **Table**: `gbv_categories`
- **Purpose**: Categories of Gender-Based Violence services
- **Key Fields**: `gbv_category_id` (PK), `category_name`, `description`

#### Document Types
- **Table**: `document_types`
- **Purpose**: Types of documents in the system
- **Key Fields**: `document_type_id` (PK), `type_name`, `description`

### 3. Facilities

#### Main Facility Table
- **Table**: `facilities`
- **Purpose**: Core facility information
- **Key Fields**: 
  - `facility_id` (PK)
  - `facility_name`
  - `registration_number` (unique)
  - `operational_status_id` (FK)
  - `ward_id` (FK)
  - `active_status`
  - `created_at`, `updated_at`
  - `created_by`, `updated_by`
- **Indexes**: `ward_id`

#### Facility Contacts
- **Table**: `facility_contacts`
- **Purpose**: Contact information for facilities
- **Key Fields**: 
  - `contact_id` (PK)
  - `facility_id` (FK)
  - `contact_type_id` (FK)
  - `contact_value`
  - `active_status`
  - `created_at`, `updated_at`
  - `created_by`, `updated_by`

#### Facility Coordinates
- **Table**: `facility_coordinates`
- **Purpose**: Geographical coordinates for facilities
- **Key Fields**: 
  - `coordinate_id` (PK)
  - `facility_id` (FK)
  - `latitude`, `longitude`
  - `coordinates_string`
  - `collection_date`
  - `data_source`, `collection_method`
  - `active_status`
  - `created_at`, `updated_at`
  - `created_by`, `updated_by`

#### Facility Services
- **Table**: `facility_services`
- **Purpose**: Services offered by facilities
- **Key Fields**: 
  - `service_id` (PK)
  - `facility_id` (FK)
  - `service_category_id` (FK)
  - `service_description`
  - `active_status`
  - `created_at`, `updated_at`
  - `created_by`, `updated_by`

#### Facility Owners
- **Table**: `facility_owners`
- **Purpose**: Ownership information for facilities
- **Key Fields**: 
  - `owner_id` (PK)
  - `facility_id` (FK)
  - `owner_name`
  - `owner_type_id` (FK)
  - `active_status`
  - `created_at`, `updated_at`
  - `created_by`, `updated_by`

#### Facility GBV Categories
- **Table**: `facility_gbv_categories`
- **Purpose**: Many-to-many relationship between facilities and GBV categories
- **Key Fields**: `facility_id` (FK), `gbv_category_id` (FK)
- **Constraints**: Unique together on both fields

### 4. Users and Authentication

#### Users
- **Table**: `users`
- **Purpose**: System users
- **Key Fields**: 
  - `user_id` (PK)
  - `full_name`
  - `email` (unique)
  - `phone_number` (unique)
  - `password_hash`
  - `is_active`
  - `facility_id` (FK)
  - `created_at`, `updated_at`

#### User Locations
- **Table**: `user_locations`
- **Purpose**: Track user locations
- **Key Fields**: 
  - `location_id` (PK)
  - `user_id` (FK)
  - `ward_id` (FK)
  - `captured_at`
  - `created_at`, `updated_at`

#### Authentication Methods
- **Table**: `authentication_methods`
- **Purpose**: Available authentication methods
- **Key Fields**: `auth_id` (PK), `method_name`, `description`

#### User Authentication Methods
- **Table**: `user_auth_methods`
- **Purpose**: Many-to-many relationship between users and authentication methods
- **Key Fields**: `user_id` (FK), `auth_id` (FK)
- **Constraints**: Unique together on both fields

#### Access Levels
- **Table**: `access_levels`
- **Purpose**: Available access levels
- **Key Fields**: `access_id` (PK), `level_name`, `description`

#### User Access Levels
- **Table**: `user_access_levels`
- **Purpose**: Many-to-many relationship between users and access levels
- **Key Fields**: `user_id` (FK), `access_id` (FK)
- **Constraints**: Unique together on both fields

### 5. Sessions and Tokens

#### User Sessions
- **Table**: `user_sessions`
- **Purpose**: Track user sessions
- **Key Fields**: 
  - `session_id` (PK)
  - `user_id` (FK)
  - `latitude`, `longitude`
  - `ip_address`
  - `created_at`, `expires_at`

#### API Tokens
- **Table**: `api_tokens`
- **Purpose**: API access tokens
- **Key Fields**: 
  - `token_id` (PK)
  - `session_id` (FK)
  - `token_hash`
  - `created_at`, `expires_at`

#### Reset Tokens
- **Table**: `reset_tokens`
- **Purpose**: Password reset tokens
- **Key Fields**: 
  - `reset_id` (PK)
  - `user_id` (FK)
  - `token_hash`
  - `created_at`, `expires_at`
  - `used`

### 6. Click Tracking

#### Contact Clicks
- **Table**: `contact_clicks`
- **Purpose**: Track when users click on facility contacts
- **Key Fields**: 
  - `click_id` (PK)
  - `session_id` (FK)
  - `user_id` (FK)
  - `facility_id` (FK)
  - `contact_id` (FK)
  - `clicked_at`
  - `helpful`
  - `followup_at`

### 7. Documents

#### Documents
- **Table**: `documents`
- **Purpose**: Document management
- **Key Fields**: 
  - `document_id` (PK)
  - `title`
  - `description`
  - `file_url`
  - `facility_id` (FK)
  - `gbv_category_id` (FK)
  - `document_type_id` (FK)
  - `uploaded_by` (FK)
  - `uploaded_at`

## Abstract Base Classes

### TimeStampedModel
- Provides `created_at` and `updated_at` fields
- Used by most models for audit trail

### UserTrackedModel
- Extends TimeStampedModel
- Adds `created_by` and `updated_by` fields
- Tracks which user created/modified records

### ActiveStatusModel
- Extends UserTrackedModel
- Adds `active_status` field
- Provides soft delete functionality

## Relationships

### Hierarchical Structure
```
County → Constituency → Ward → Facility
```

### Facility Relationships
- Each facility belongs to one ward
- Each facility can have multiple contacts, coordinates, services, and owners
- Facilities can be associated with multiple GBV categories

### User Relationships
- Users can be associated with facilities
- Users can have multiple authentication methods and access levels
- User sessions track location and activity

## Indexes

The following indexes are created for performance:
- `counties.county_name` (unique)
- `constituencies.county_id`
- `wards.constituency_id`
- `facilities.ward_id`
- `facility_contacts.facility_id`
- `facility_coordinates.facility_id`
- `facility_services.facility_id`
- `facility_owners.facility_id`

## Data Integrity

### Foreign Key Constraints
- All relationships are properly constrained with CASCADE or SET_NULL as appropriate
- Many-to-many relationships use junction tables with unique constraints

### Unique Constraints
- County names are unique
- Facility registration numbers are unique
- User emails and phone numbers are unique
- Contact type names, service category names, etc. are unique

## Usage

### Running Migrations
```bash
python manage.py migrate
```

### Loading Initial Data
```bash
python manage.py load_initial_data
```

### Creating Superuser
```bash
python manage.py createsuperuser
```

## Admin Interface

All models are registered in the Django admin with appropriate:
- List displays
- Search fields
- Filters
- Read-only fields
- Optimized querysets with select_related

## API Endpoints

The system includes REST API endpoints for:
- Facilities and related data
- User management
- Authentication
- Document management

## Security Features

- Password hashing
- Session management
- Access level controls
- API token authentication
- User activity tracking
