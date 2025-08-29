# -*- encoding: utf-8 -*-
"""
Common models and abstract base classes
"""

from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Abstract base class with created_at and modified_at fields"""
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserTrackedModel(models.Model):
    """Abstract base class with user tracking fields"""
    created_by = models.IntegerField(null=True, blank=True)  # Reference to users.user_id
    updated_by = models.IntegerField(null=True, blank=True)  # Reference to users.user_id

    class Meta:
        abstract = True


class ActiveStatusModel(models.Model):
    """Abstract base class with active status"""
    is_active = models.BooleanField(default=True, null=False)

    class Meta:
        abstract = True


class CodeModel(models.Model):
    """Abstract base class for models with unique codes"""
    code = models.CharField(max_length=50, unique=True, null=False)
    
    class Meta:
        abstract = True


class SortableModel(models.Model):
    """Abstract base class for models with sort order"""
    sort_order = models.IntegerField(default=0, null=False)
    
    class Meta:
        abstract = True
        ordering = ['sort_order']