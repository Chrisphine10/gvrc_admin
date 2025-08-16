# -*- encoding: utf-8 -*-
"""
Document management models
"""

from django.db import models
from apps.facilities.models import Facility
from apps.common.lookups import GBVCategory, DocumentType
from apps.authentication.models import User


class Document(models.Model):
    """Document management model"""
    document_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file_url = models.URLField()
    facility = models.ForeignKey('facilities.Facility', on_delete=models.CASCADE, db_column='facility_id', null=True, blank=True)
    gbv_category = models.ForeignKey('common.GBVCategory', on_delete=models.CASCADE, db_column='gbv_category_id', null=True, blank=True)
    document_type = models.ForeignKey('common.DocumentType', on_delete=models.CASCADE, db_column='document_type_id', null=True, blank=True)
    uploaded_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, db_column='uploaded_by', null=True, blank=True)
    uploaded_at = models.DateTimeField()
    
    def __str__(self):
        return f"{self.title} - {self.facility.facility_name}"
    
    class Meta:
        db_table = 'documents'
