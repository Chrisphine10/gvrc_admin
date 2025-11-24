# -*- encoding: utf-8 -*-
"""
Mobile Session Services
"""

from django.utils import timezone
from .models import MobileSession


class MobileSessionService:
    """Service class for mobile session operations"""
    
    @staticmethod
    def create_session(device_id, device_info=None, location_data=None):
        """Create a new mobile session"""
        session = MobileSession.objects.create(
            device_id=device_id,
            is_active=True,
            last_active_at=timezone.now()
        )
        
        # Update location if provided
        if location_data and 'latitude' in location_data and 'longitude' in location_data:
            session.update_location(
                latitude=location_data['latitude'],
                longitude=location_data['longitude']
            )
        
        return session
    
    @staticmethod
    def end_session(session):
        """End a mobile session"""
        session.is_active = False
        session.save(update_fields=['is_active', 'updated_at'])
        return session
    
    @staticmethod
    def get_active_session(device_id):
        """Get active session for device"""
        try:
            return MobileSession.objects.get(device_id=device_id, is_active=True)
        except MobileSession.DoesNotExist:
            return None
    
    @staticmethod
    def update_session_activity(device_id):
        """Update session activity timestamp"""
        try:
            session = MobileSession.objects.get(device_id=device_id, is_active=True)
            session.update_activity()
            return session
        except MobileSession.DoesNotExist:
            return None
