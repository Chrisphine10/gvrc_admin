# -*- encoding: utf-8 -*-
"""
Document management models for GVRC Admin
"""

from django.db import models
from django.utils import timezone


class Document(models.Model):
    """Document model for file and content management"""
    document_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True)
    file_url = models.CharField(max_length=500, blank=True)
    file_name = models.CharField(max_length=255, blank=True)
    file_size_bytes = models.BigIntegerField(blank=True, null=True)
    content = models.TextField(blank=True)
    gbv_category = models.ForeignKey('lookups.GBVCategory', on_delete=models.SET_NULL, blank=True, null=True, db_column='gbv_category')
    image_url = models.CharField(max_length=500, blank=True)
    external_url = models.CharField(max_length=500, blank=True)
    document_type = models.ForeignKey('lookups.DocumentType', on_delete=models.CASCADE, db_column='document_type_id', null=False)
    is_public = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=True, null=False)
    uploaded_at = models.DateTimeField(default=timezone.now, null=False)
    uploaded_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='documents_uploaded', db_column='uploaded_by', null=False)
    
    def __str__(self):
        return f"{self.title} - {self.document_type.type_name}"
    
    class Meta:
        verbose_name_plural = "Documents"
        db_table = 'documents'
        indexes = [
            models.Index(fields=['document_type']),
            models.Index(fields=['uploaded_by']),
            models.Index(fields=['is_public']),
            models.Index(fields=['is_active']),
        ]