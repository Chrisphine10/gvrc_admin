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


class UserTrackedModel(TimeStampedModel):
    """Abstract base class with user tracking fields"""
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class ActiveStatusModel(UserTrackedModel):
    """Abstract base class with active status and user tracking"""
    active_status = models.BooleanField(default=True)

    class Meta:
        abstract = True