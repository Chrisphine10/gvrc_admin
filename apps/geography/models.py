# -*- encoding: utf-8 -*-
"""
Geographic administrative division models for GVRC Admin
"""

from django.db import models
from django.utils import timezone


class County(models.Model):
    """County model for administrative divisions"""
    county_id = models.AutoField(primary_key=True)
    county_name = models.CharField(max_length=100, null=False)
    county_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    
    def __str__(self):
        return self.county_name
    
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
    
    class Meta:
        verbose_name_plural = "Wards"
        db_table = 'wards'
        indexes = [
            models.Index(fields=['constituency']),
            models.Index(fields=['ward_name']),
            models.Index(fields=['ward_code']),
        ]