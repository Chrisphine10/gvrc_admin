# -*- encoding: utf-8 -*-
"""
Facility models for GVRC Admin
"""

from django.db import models
from django.contrib.auth.models import User
from apps.common.models import TimeStampedModel


class Facility(TimeStampedModel):
    """Community-based facility model"""
    FACILITY_TYPES = [
        # Health facilities
        ('hospital', 'Hospital'),
        ('clinic', 'Clinic'),
        ('dispensary', 'Dispensary'),
        ('health_center', 'Health Center'),
        ('laboratory', 'Laboratory'),
        ('pharmacy', 'Pharmacy'),
        # Police and security
        ('police_station', 'Police Station'),
        ('police_post', 'Police Post'),
        ('security_office', 'Security Office'),
        # Community organizations
        ('cbo', 'Community-Based Organization (CBO)'),
        ('ngo', 'Non-Governmental Organization (NGO)'),
        ('faith_based', 'Faith-Based Organization'),
        # Support services
        ('safe_house', 'Safe House'),
        ('shelter', 'Shelter'),
        ('legal_aid', 'Legal Aid Center'),
        ('gender_desk', 'Gender Desk'),
        ('counseling_center', 'Counseling Center'),
        ('rehabilitation_center', 'Rehabilitation Center'),
        # Other community facilities
        ('community_center', 'Community Center'),
        ('youth_center', 'Youth Center'),
        ('women_center', 'Women Center'),
        ('elderly_center', 'Elderly Center'),
        ('disability_center', 'Disability Center'),
    ]
    
    OWNERSHIP_TYPES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('faith_based', 'Faith-based'),
        ('ngo', 'NGO'),
        ('community', 'Community-owned'),
        ('government', 'Government'),
    ]
    
    name = models.CharField(max_length=200)
    facility_type = models.CharField(max_length=30, choices=FACILITY_TYPES)
    ownership = models.CharField(max_length=20, choices=OWNERSHIP_TYPES)
    county = models.CharField(max_length=100)
    ward = models.CharField(max_length=100)
    location = models.CharField(max_length=200, help_text="Street address or general location description")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="Latitude coordinate (e.g., -1.2921)")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="Longitude coordinate (e.g., 36.8219)")
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    registration_number = models.CharField(max_length=50, unique=True)
    
    # Additional fields for community facilities
    target_population = models.CharField(max_length=200, blank=True, help_text="Primary target population served")
    services_offered = models.TextField(blank=True, help_text="Brief description of main services")
    operating_hours = models.CharField(max_length=100, blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_facility_type_display()}"
    
    def get_coordinates(self):
        """Return coordinates as a tuple if both lat and lon are available"""
        if self.latitude and self.longitude:
            return (float(self.latitude), float(self.longitude))
        return None
    
    def get_location_display(self):
        """Return formatted location information"""
        location_parts = []
        if self.county:
            location_parts.append(f"County: {self.county}")
        if self.ward:
            location_parts.append(f"Ward: {self.ward}")
        if self.location:
            location_parts.append(f"Address: {self.location}")
        if self.latitude and self.longitude:
            location_parts.append(f"Coordinates: {self.latitude}, {self.longitude}")
        
        return " | ".join(location_parts) if location_parts else "Location not specified"
    
    class Meta:
        verbose_name_plural = "Facilities"


class Facility_Services(TimeStampedModel):
    """Services offered by facilities"""
    SERVICE_CATEGORIES = [
        # Health services
        ('curative', 'Curative Services'),
        ('preventive', 'Preventive Services'),
        ('diagnostic', 'Diagnostic Services'),
        ('rehabilitative', 'Rehabilitative Services'),
        ('support', 'Support Services'),
        # Security and legal services
        ('security', 'Security Services'),
        ('legal', 'Legal Services'),
        ('counseling', 'Counseling Services'),
        ('protection', 'Protection Services'),
        # Community services
        ('education', 'Education Services'),
        ('training', 'Training Services'),
        ('advocacy', 'Advocacy Services'),
        ('emergency', 'Emergency Services'),
        ('referral', 'Referral Services'),
    ]
    
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='services')
    service_name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=SERVICE_CATEGORIES)
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.facility.name} - {self.service_name}"
    
    class Meta:
        verbose_name_plural = "Facility Services"


class Facility_HumanResources(TimeStampedModel):
    """Human resources at facilities"""
    STAFF_CATEGORIES = [
        # Health staff
        ('medical', 'Medical Staff'),
        ('nursing', 'Nursing Staff'),
        ('pharmacy', 'Pharmacy Staff'),
        ('laboratory', 'Laboratory Staff'),
        # Security staff
        ('police', 'Police Officers'),
        ('security', 'Security Personnel'),
        # Legal and support staff
        ('legal', 'Legal Staff'),
        ('counselor', 'Counselors'),
        ('social_worker', 'Social Workers'),
        ('psychologist', 'Psychologists'),
        # Administrative staff
        ('administrative', 'Administrative Staff'),
        ('support', 'Support Staff'),
        ('volunteer', 'Volunteers'),
    ]
    
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='staff')
    staff_category = models.CharField(max_length=20, choices=STAFF_CATEGORIES)
    position = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200, blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.facility.name} - {self.full_name} ({self.position})"
    
    class Meta:
        verbose_name_plural = "Facility Human Resources"


class Facility_Infrastructure(TimeStampedModel):
    """Infrastructure and operational equipment for community facilities"""
    EQUIPMENT_CATEGORIES = [
        # Emergency and medical vehicles
        ('ambulance', 'Ambulance'),
        ('emergency_vehicle', 'Emergency Vehicle'),
        ('medical_transport', 'Medical Transport Vehicle'),
        ('police_vehicle', 'Police Vehicle'),
        ('security_vehicle', 'Security Vehicle'),
        # Medical equipment
        ('medical_equipment', 'Medical Equipment'),
        ('diagnostic_equipment', 'Diagnostic Equipment'),
        ('emergency_equipment', 'Emergency Equipment'),
        ('first_aid_equipment', 'First Aid Equipment'),
        # Communication equipment
        ('communication_equipment', 'Communication Equipment'),
        ('radio_equipment', 'Radio Equipment'),
        ('emergency_communication', 'Emergency Communication'),
        # Security equipment
        ('security_equipment', 'Security Equipment'),
        ('surveillance_equipment', 'Surveillance Equipment'),
        ('safety_equipment', 'Safety Equipment'),
        # IT and office equipment
        ('it_equipment', 'IT Equipment'),
        ('office_equipment', 'Office Equipment'),
        ('data_management', 'Data Management Equipment'),
        # Utilities and infrastructure
        ('power_equipment', 'Power Equipment'),
        ('water_equipment', 'Water Equipment'),
        ('generator', 'Generator'),
        ('backup_systems', 'Backup Systems'),
        # Other operational equipment
        ('furniture', 'Furniture'),
        ('storage_equipment', 'Storage Equipment'),
        ('maintenance_equipment', 'Maintenance Equipment'),
    ]
    
    EQUIPMENT_CONDITIONS = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('non_functional', 'Non-Functional'),
        ('under_maintenance', 'Under Maintenance'),
    ]
    
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='infrastructure')
    equipment_name = models.CharField(max_length=200, help_text="Name of the equipment or vehicle (e.g., Ambulance, Emergency Radio)")
    category = models.CharField(max_length=30, choices=EQUIPMENT_CATEGORIES)
    quantity = models.PositiveIntegerField(default=1, help_text="Number of units available")
    condition = models.CharField(max_length=20, choices=EQUIPMENT_CONDITIONS, default='good')
    registration_number = models.CharField(max_length=50, blank=True, help_text="Vehicle registration number if applicable")
    model_year = models.PositiveIntegerField(null=True, blank=True, help_text="Year of manufacture")
    last_maintenance = models.DateField(null=True, blank=True)
    next_maintenance = models.DateField(null=True, blank=True)
    insurance_expiry = models.DateField(null=True, blank=True, help_text="Insurance expiry date for vehicles")
    fuel_type = models.CharField(max_length=20, blank=True, help_text="Fuel type for vehicles (e.g., Petrol, Diesel, Electric)")
    capacity = models.CharField(max_length=50, blank=True, help_text="Capacity or specifications (e.g., 4 passengers, 1000W)")
    is_operational = models.BooleanField(default=True, help_text="Whether the equipment is currently operational")
    notes = models.TextField(blank=True, help_text="Additional notes about the equipment")
    
    def __str__(self):
        return f"{self.facility.name} - {self.equipment_name}"
    
    def is_vehicle(self):
        """Check if this is a vehicle type equipment"""
        vehicle_categories = ['ambulance', 'emergency_vehicle', 'medical_transport', 'police_vehicle', 'security_vehicle']
        return self.category in vehicle_categories
    
    def needs_maintenance(self):
        """Check if equipment needs maintenance based on last maintenance date"""
        if self.last_maintenance:
            from datetime import date, timedelta
            # Suggest maintenance every 6 months for vehicles, 12 months for other equipment
            maintenance_interval = timedelta(days=180 if self.is_vehicle() else 365)
            return date.today() - self.last_maintenance > maintenance_interval
        return False
    
    def get_operational_status(self):
        """Get operational status with color coding"""
        if not self.is_operational:
            return "Non-Operational"
        elif self.condition == 'poor' or self.condition == 'non_functional':
            return "Needs Attention"
        elif self.needs_maintenance():
            return "Needs Maintenance"
        else:
            return "Operational"
    
    class Meta:
        verbose_name_plural = "Facility Infrastructure"
