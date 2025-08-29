# -*- encoding: utf-8 -*-
"""
Document management models for GVRC Admin
"""

from django.db import models
from django.utils import timezone
from apps.common.utils import get_document_upload_path, secure_filename
import os


class Document(models.Model):
    """Document model for file and content management"""
    document_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True)
    
    # File upload field with unique naming
    file = models.FileField(
        upload_to=get_document_upload_path,
        blank=True,
        null=True,
        help_text="Upload document file"
    )
    
    # Legacy fields for backward compatibility
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
    
    def get_original_filename(self):
        """Get the original filename from metadata if available"""
        if hasattr(self, '_original_filename'):
            return self._original_filename
        return None
    
    def set_original_filename(self, filename):
        """Set the original filename for later retrieval"""
        self._original_filename = secure_filename(filename)
    
    def get_file_size_mb(self):
        """Get file size in MB"""
        if self.file:
            return round(self.file.size / (1024 * 1024), 2)
        elif self.file_size_bytes:
            return round(self.file_size_bytes / (1024 * 1024), 2)
        return None
    
    def get_file_extension(self):
        """Get file extension"""
        if self.file:
            return os.path.splitext(self.file.name)[1].lower()
        elif self.file_name:
            return os.path.splitext(self.file_name)[1].lower()
        return None
    
    def save(self, *args, **kwargs):
        """Override save to handle file metadata"""
        # Update file metadata if file is present
        if self.file:
            # Update file_name and file_size_bytes for backward compatibility
            self.file_name = os.path.basename(self.file.name)
            self.file_size_bytes = self.file.size
            
            # Store original filename if not already set
            if not hasattr(self, '_original_filename'):
                self._original_filename = self.file.name
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Documents"
        db_table = 'documents'
        indexes = [
            models.Index(fields=['document_type']),
            models.Index(fields=['uploaded_by']),
            models.Index(fields=['is_public']),
            models.Index(fields=['is_active']),
        ]