from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re


def validate_kenyan_phone_number(value):
    """
    Validate Kenyan phone numbers
    """
    kenyan_phone_regex = re.compile(r'^(\+254|254|0)[17]\d{8}$')
    if not kenyan_phone_regex.match(value):
        raise ValidationError(
            'Enter a valid Kenyan phone number (e.g., +254712345678, 0712345678)'
        )


def validate_registration_number(value):
    """
    Validate facility registration numbers
    """
    if not re.match(r'^[A-Z]{2,4}\d{3,6}$', value):
        raise ValidationError(
            'Registration number must be in format like REG123 or HOSP1234'
        )


def validate_coordinates(latitude, longitude):
    """
    Validate coordinates are within Kenya bounds
    """
    # Kenya approximate bounds
    KENYA_BOUNDS = {
        'lat_min': -4.7,
        'lat_max': 5.0,
        'lng_min': 33.9,
        'lng_max': 41.9
    }
    
    if not (KENYA_BOUNDS['lat_min'] <= latitude <= KENYA_BOUNDS['lat_max']):
        raise ValidationError('Latitude must be within Kenya bounds')
    
    if not (KENYA_BOUNDS['lng_min'] <= longitude <= KENYA_BOUNDS['lng_max']):
        raise ValidationError('Longitude must be within Kenya bounds')


# Custom Django model fields for validation
from django.db import models

class KenyanPhoneNumberField(models.CharField):
    """
    Custom field for Kenyan phone numbers
    """
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 15
        kwargs['validators'] = [validate_kenyan_phone_number]
        super().__init__(*args, **kwargs)


class RegistrationNumberField(models.CharField):
    """
    Custom field for registration numbers
    """
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        kwargs['validators'] = [validate_registration_number]
        super().__init__(*args, **kwargs)