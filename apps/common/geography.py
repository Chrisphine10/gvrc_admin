# -*- encoding: utf-8 -*-
"""
Geographical models for administrative divisions
"""

from django.db import models


class County(models.Model):
    """County model for administrative divisions"""
    county_id = models.AutoField(primary_key=True)
    county_name = models.CharField(max_length=100, unique=True, null=False)
    
    def __str__(self):
        return self.county_name
    
    class Meta:
        verbose_name_plural = "Counties"
        db_table = 'counties'


class Constituency(models.Model):
    """Constituency model for administrative divisions"""
    constituency_id = models.AutoField(primary_key=True)
    constituency_name = models.CharField(max_length=100, null=False)
    county = models.ForeignKey(County, on_delete=models.CASCADE, db_column='county_id')
    
    def __str__(self):
        return f"{self.constituency_name} - {self.county.county_name}"
    
    class Meta:
        verbose_name_plural = "Constituencies"
        db_table = 'constituencies'
        indexes = [
            models.Index(fields=['county']),
        ]


class Ward(models.Model):
    """Ward model for administrative divisions"""
    ward_id = models.AutoField(primary_key=True)
    ward_name = models.CharField(max_length=100, null=False)
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, db_column='constituency_id')
    
    def __str__(self):
        return f"{self.ward_name} - {self.constituency.constituency_name}"
    
    class Meta:
        verbose_name_plural = "Wards"
        db_table = 'wards'
        indexes = [
            models.Index(fields=['constituency']),
        ]
