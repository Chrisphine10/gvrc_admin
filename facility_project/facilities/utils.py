import hashlib
import secrets
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from geopy.distance import geodesic


def generate_session_id():
    """Generate a secure session ID"""
    return secrets.token_urlsafe(32)


def hash_token(token):
    """Hash a token for storage"""
    return hashlib.sha256(token.encode()).hexdigest()


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates using geodesic distance
    """
    point1 = (lat1, lon1)
    point2 = (lat2, lon2)
    return geodesic(point1, point2).kilometers


def send_notification_email(user_email, subject, message):
    """
    Send notification email to user
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {user_email}: {e}")
        return False


def format_phone_number(phone_number):
    """
    Format phone number to standard Kenyan format
    """
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone_number)
    
    # Convert to standard format
    if digits_only.startswith('254'):
        return f"+{digits_only}"
    elif digits_only.startswith('0'):
        return f"+254{digits_only[1:]}"
    elif len(digits_only) == 9:
        return f"+254{digits_only}"
    
    return phone_number  # Return original if can't format


def get_facilities_within_radius(center_lat, center_lon, radius_km=10):
    """
    Get facilities within a specified radius of a center point
    """
    from facilities.models import Facility, FacilityCoordinate
    
    facilities_with_coords = Facility.objects.filter(
        coordinates__isnull=False,
        active_status=True
    ).select_related('coordinates')
    
    nearby_facilities = []
    
    for facility in facilities_with_coords:
        if facility.coordinates:
            distance = calculate_distance(
                center_lat, center_lon,
                float(facility.coordinates.latitude),
                float(facility.coordinates.longitude)
            )
            
            if distance <= radius_km:
                nearby_facilities.append({
                    'facility': facility,
                    'distance': distance
                })
    
    # Sort by distance
    nearby_facilities.sort(key=lambda x: x['distance'])
    
    return nearby_facilities


def generate_facility_report(facility):
    """
    Generate a comprehensive report for a facility
    """
    report_data = {
        'facility_info': {
            'name': facility.facility_name,
            'registration_number': facility.registration_number,
            'operational_status': facility.operational_status.status_name,
            'location': {
                'ward': facility.ward.ward_name,
                'constituency': facility.ward.constituency.constituency_name,
                'county': facility.ward.constituency.county.county_name
            }
        },
        'contacts': [
            {
                'type': contact.contact_type.type_name,
                'value': contact.contact_value
            }
            for contact in facility.contacts.filter(active_status=True)
        ],
        'services': [
            {
                'category': service.service_category.category_name,
                'description': service.service_description
            }
            for service in facility.services.filter(active_status=True)
        ],
        'owners': [
            {
                'name': owner.owner_name,
                'type': owner.owner_type.type_name
            }
            for owner in facility.owners.filter(active_status=True)
        ],
        'coordinates': None
    }
    
    if hasattr(facility, 'coordinates') and facility.coordinates:
        report_data['coordinates'] = {
            'latitude': float(facility.coordinates.latitude),
            'longitude': float(facility.coordinates.longitude)
        }
    
    return report_data