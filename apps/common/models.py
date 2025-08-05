# -*- encoding: utf-8 -*-
"""
Common models and abstract base classes
"""

from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    """Abstract base class with created_at and modified_at fields"""
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True