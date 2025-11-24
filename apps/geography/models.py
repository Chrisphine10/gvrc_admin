# -*- encoding: utf-8 -*-
"""
Geographic administrative division models for GVRC Admin
"""

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class County(models.Model):
    """County model for administrative divisions"""
    county_id = models.AutoField(primary_key=True)
    county_name = models.CharField(max_length=100, null=False)
    county_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    
    def __str__(self):
        return self.county_name
    
    def has_facilities(self):
        """Check if county has facilities connected through constituencies and wards"""
        try:
            # Check if any ward in this county has facilities
            return self.constituency_set.filter(ward__facility__isnull=False).exists()
        except:
            return False
    
    def can_delete(self):
        """Check if county can be safely deleted"""
        return not self.has_facilities() and not self.constituency_set.exists()
    
    def clean(self):
        """Validate county data"""
        if not self.county_name or not self.county_name.strip():
            raise ValidationError('County name is required')
        if not self.county_code or not self.county_code.strip():
            raise ValidationError('County code is required')
    
    class Meta:
        verbose_name_plural = "Counties"
        db_table = 'counties'
        indexes = [
            models.Index(fields=['county_name']),
            models.Index(fields=['county_code']),
        ]


class Constituency(models.Model):
    """Constituency model for administrative divisions"""
    constituency_id = models.AutoField(primary_key=True)
    constituency_name = models.CharField(max_length=100, null=False)
    county = models.ForeignKey(County, on_delete=models.CASCADE, db_column='county_id', null=False)
    constituency_code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    
    def __str__(self):
        return f"{self.constituency_name} - {self.county.county_name}"
    
    def has_facilities(self):
        """Check if constituency has facilities connected through wards"""
        try:
            # Check if any ward in this constituency has facilities
            return self.ward_set.filter(facility__isnull=False).exists()
        except:
            return False
    
    def can_delete(self):
        """Check if constituency can be safely deleted"""
        return not self.has_facilities() and not self.ward_set.exists()
    
    def clean(self):
        """Validate constituency data"""
        if not self.constituency_name or not self.constituency_name.strip():
            raise ValidationError('Constituency name is required')
        if not self.constituency_code or not self.constituency_code.strip():
            raise ValidationError('Constituency code is required')
        if not self.county:
            raise ValidationError('County is required')
    
    class Meta:
        verbose_name_plural = "Constituencies"
        db_table = 'constituencies'
        indexes = [
            models.Index(fields=['county']),
            models.Index(fields=['constituency_name']),
            models.Index(fields=['constituency_code']),
        ]


class Ward(models.Model):
    """Ward model for administrative divisions"""
    ward_id = models.AutoField(primary_key=True)
    ward_name = models.CharField(max_length=100, null=False)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, db_column='constituency_id', null=False)
    ward_code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    
    def __str__(self):
        return f"{self.ward_name} - {self.constituency.constituency_name}"
    
    def has_facilities(self):
        """Check if ward has facilities connected"""
        try:
            # Check if this ward has facilities
            return hasattr(self, 'facility_set') and self.facility_set.exists()
        except:
            return False
    
    def can_delete(self):
        """Check if ward can be safely deleted"""
        return not self.has_facilities()
    
    def clean(self):
        """Validate ward data"""
        if not self.ward_name or not self.ward_name.strip():
            raise ValidationError('Ward name is required')
        if not self.ward_code or not self.ward_code.strip():
            raise ValidationError('Ward code is required')
        if not self.constituency:
            raise ValidationError('Constituency is required')
    
    class Meta:
        verbose_name_plural = "Wards"
        db_table = 'wards'
        indexes = [
            models.Index(fields=['constituency']),
            models.Index(fields=['ward_name']),
            models.Index(fields=['ward_code']),
        ]