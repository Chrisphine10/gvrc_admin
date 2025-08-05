# -*- encoding: utf-8 -*-
"""
Common utilities and helper functions
"""

import os
import random
import string
from django.conf import settings

def generate_random_string(length=10):
    """Generate a random string of specified length"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_upload_path(instance, filename):
    """Generate upload path for file uploads"""
    return f"uploads/{instance.__class__.__name__.lower()}/{filename}"

# Legacy helper functions for backward compatibility
def h_random(aLen=32):
    """Generate random string with letters, digits and special chars"""
    letters = string.ascii_letters
    digits  = string.digits
    chars   = '_<>,.+'
    return ''.join(random.choices( letters + digits + chars, k=aLen))

def h_random_ascii(aLen=32):
    """Generate random ASCII string with letters and digits only"""
    letters = string.ascii_letters
    digits  = string.digits
    return ''.join(random.choices( letters + digits, k=aLen))