# Facility Management API Documentation

## Overview
This API provides endpoints for managing facilities, users, locations, and related data. It follows REST principles and uses token-based authentication.

## Authentication

### Login
- **POST** `/auth/login/`
- Authenticate a user and receive a token
- Request body: `{ "email": "user@example.com", "password": "password123" }`
- Response: `{ "token": "auth_token", "user": {...}, "message": "Login successful" }`

### Register
- **POST** `/auth/register/`
- Register a new user
- Request body: `{ "full_name": "John Doe", "email": "john@example.com", "password": "password123", "password_confirm": "password123" }`
- Response: `{ "token": "auth_token", "user": {...}, "message": "Registration successful" }`

### Logout
- **POST** `/auth/logout/`
- Invalidate the user's authentication token
- Response: `{ "message": "Logout successful" }`

## Users

### List/Create Users
- **GET** `/users/`
- List all users with filtering and search capabilities
- Query parameters: `is_active`, `facility`, `search`, `ordering`

- **POST** `/users/`
- Create a new user
- Request body: `{ "full_name": "John Doe", "email": "john@example.com", "password": "password123", "facility": 1 }`

### User Detail
- **GET** `/users/{user_id}/`
- Retrieve details of a specific user

- **PUT** `/users/{user_id}/`
- Update a specific user

- **DELETE** `/users/{user_id}/`
- Delete a specific user

### User Profile
- **GET** `/users/profile/`
- Retrieve the authenticated user's profile

- **PUT** `/users/profile/`
- Update the authenticated user's profile

## Facilities

### List/Create Facilities
- **GET** `/facilities/`
- List all facilities with filtering and search capabilities
- Query parameters: `operational_status`, `ward`, `county`, `constituency`, `search`, `ordering`

- **POST** `/facilities/`
- Create a new facility
- Request body: `{ "facility_name": "Health Center", "registration_number": "HC123", "operational_status": 1, "ward": 5 }`

### Facility Detail
- **GET** `/facilities/{facility_id}/`
- Retrieve details of a specific facility

- **PUT** `/facilities/{facility_id}/`
- Update a specific facility

- **DELETE** `/facilities/{facility_id}/`
- Delete a specific facility

### Facility Search
- **GET** `/facilities/search/`
- Search facilities by various criteria
- Query parameters: `q`, `county`, `constituency`, `ward`, `service_category`

## Facility Related Data

### Facility Contacts
- **GET** `/facilities/{facility_id}/contacts/`
- List all contacts for a specific facility

- **POST** `/facilities/{facility_id}/contacts/`
- Create a new contact for a facility

- **GET** `/facility-contacts/{contact_id}/`
- Retrieve details of a specific contact

- **PUT** `/facility-contacts/{contact_id}/`
- Update a specific contact

- **DELETE** `/facility-contacts/{contact_id}/`
- Delete a specific contact

### Facility Coordinates
- **GET** `/facilities/{facility_id}/coordinates/`
- Retrieve coordinates for a specific facility

- **PUT** `/facilities/{facility_id}/coordinates/`
- Update coordinates for a specific facility

### Facility Services
- **GET** `/facilities/{facility_id}/services/`
- List all services for a specific facility

- **POST** `/facilities/{facility_id}/services/`
- Create a new service for a facility

- **GET** `/facility-services/{service_id}/`
- Retrieve details of a specific service

- **PUT** `/facility-services/{service_id}/`
- Update a specific service

- **DELETE** `/facility-services/{service_id}/`
- Delete a specific service

### Facility Owners
- **GET** `/facilities/{facility_id}/owners/`
- List all owners for a specific facility

- **POST** `/facilities/{facility_id}/owners/`
- Create a new owner for a facility

- **GET** `/facility-owners/{owner_id}/`
- Retrieve details of a specific owner

- **PUT** `/facility-owners/{owner_id}/`
- Update a specific owner

- **DELETE** `/facility-owners/{owner_id}/`
- Delete a specific owner

## Locations

### Counties
- **GET** `/counties/`
- List all counties

### Constituencies
- **GET** `/constituencies/`
- List all constituencies
- Query parameters: `county`

### Wards
- **GET** `/wards/`
- List all wards
- Query parameters: `constituency`, `county`

## Lookup Data

### Operational Statuses
- **GET** `/operational-statuses/`
- List all operational statuses

### Contact Types
- **GET** `/contact-types/`
- List all contact types

### Service Categories
- **GET** `/service-categories/`
- List all service categories

### Owner Types
- **GET** `/owner-types/`
- List all owner types

## User Locations

### List/Create User Locations
- **GET** `/user-locations/`
- List all locations for the authenticated user

- **POST** `/user-locations/`
- Create a new location for the authenticated user

### User Location Detail
- **GET** `/user-locations/{location_id}/`
- Retrieve details of a specific user location

- **PUT** `/user-locations/{location_id}/`
- Update a specific user location

- **DELETE** `/user-locations/{location_id}/`
- Delete a specific user location

## Sessions

### User Sessions
- **GET** `/user-sessions/`
- List all sessions for the authenticated user

## Dashboard

### Dashboard Statistics
- **GET** `/dashboard/stats/`
- Retrieve dashboard statistics including total facilities, users, and recent facilities

### Nearby Facilities
- **GET** `/facilities/nearby/`
- Find facilities near a specific location
- Query parameters: `lat`, `lng`, `radius`