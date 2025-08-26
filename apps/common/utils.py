# -*- encoding: utf-8 -*-
"""
Common utilities and helper functions
"""

import os
import random
import string
import uuid
from datetime import datetime
from django.conf import settings
from django.core.files.storage import default_storage

def generate_random_string(length=10):
    """Generate a random string of specified length"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_upload_path(instance, filename):
    """Generate upload path for file uploads"""
    return f"uploads/{instance.__class__.__name__.lower()}/{filename}"

def generate_unique_filename(original_filename, prefix="", suffix=""):
    """
    Generate a unique filename with timestamp and UUID to prevent conflicts
    
    Args:
        original_filename: Original filename from user upload
        prefix: Optional prefix to add to filename
        suffix: Optional suffix to add to filename
    
    Returns:
        Unique filename string
    """
    # Get file extension
    name, ext = os.path.splitext(original_filename)
    
    # Generate unique identifier
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]  # First 8 characters of UUID
    
    # Clean the original name (remove special chars, limit length)
    clean_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
    clean_name = clean_name[:50]  # Limit length
    
    # Construct unique filename
    unique_filename = f"{prefix}{clean_name}_{timestamp}_{unique_id}{suffix}{ext}"
    
    return unique_filename

def get_document_upload_path(instance, filename):
    """
    Generate unique upload path for documents
    
    Args:
        instance: Document model instance
        filename: Original filename
    
    Returns:
        Unique file path string
    """
    # Generate unique filename
    unique_filename = generate_unique_filename(filename, prefix="doc_")
    
    # Create path with year/month structure
    year_month = datetime.now().strftime("%Y/%m")
    return f"documents/{year_month}/{unique_filename}"

def get_chat_file_upload_path(instance, filename):
    """
    Generate unique upload path for chat files
    
    Args:
        instance: Message model instance
        filename: Original filename
    
    Returns:
        Unique file path string
    """
    # Generate unique filename
    unique_filename = generate_unique_filename(filename, prefix="chat_")
    
    # Create path with year/month/day structure
    year_month_day = datetime.now().strftime("%Y/%m/%d")
    return f"chat_files/{year_month_day}/{unique_filename}"

def get_music_upload_path(instance, filename):
    """
    Generate unique upload path for music files
    
    Args:
        instance: Music model instance
        filename: Original filename
    
    Returns:
        Unique file path string
    """
    # Generate unique filename
    unique_filename = generate_unique_filename(filename, prefix="music_")
    
    # Create path with year/month structure
    year_month = datetime.now().strftime("%Y/%m")
    return f"music_files/{year_month}/{unique_filename}"

def secure_filename(filename):
    """
    Sanitize filename for security
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove or replace potentially dangerous characters
    dangerous_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    
    # Remove multiple consecutive underscores
    while '__' in filename:
        filename = filename.replace('__', '_')
    
    # Remove leading/trailing underscores and dots
    filename = filename.strip('_.')
    
    return filename

def validate_file_extension(filename, allowed_extensions):
    """
    Validate file extension against allowed list
    
    Args:
        filename: Filename to validate
        allowed_extensions: List of allowed extensions (e.g., ['.pdf', '.jpg'])
    
    Returns:
        bool: True if extension is allowed, False otherwise
    """
    if not filename:
        return False
    
    file_ext = os.path.splitext(filename)[1].lower()
    return file_ext in allowed_extensions

def validate_file_size(file_obj, max_size_mb):
    """
    Validate file size
    
    Args:
        file_obj: File object to validate
        max_size_mb: Maximum size in MB
    
    Returns:
        bool: True if file size is acceptable, False otherwise
    """
    if not file_obj:
        return False
    
    max_size_bytes = max_size_mb * 1024 * 1024
    return file_obj.size <= max_size_bytes

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