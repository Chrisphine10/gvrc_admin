from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from facilities.models import Facility, FacilityContact, UserSession
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Create auth token when user is created
    """
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Facility)
def log_facility_changes(sender, instance, created, **kwargs):
    """
    Log facility creation and updates
    """
    if created:
        logger.info(f"New facility created: {instance.facility_name} by {instance.created_by}")
    else:
        logger.info(f"Facility updated: {instance.facility_name}")


@receiver(post_delete, sender=Facility)
def log_facility_deletion(sender, instance, **kwargs):
    """
    Log facility deletion
    """
    logger.warning(f"Facility deleted: {instance.facility_name}")


@receiver(post_save, sender=FacilityContact)
def validate_contact_on_save(sender, instance, **kwargs):
    """
    Additional validation when facility contact is saved
    """
    if instance.contact_type.type_name == 'Phone':
        try:
            validate_kenyan_phone_number(instance.contact_value)
        except ValidationError as e:
            logger.warning(f"Invalid phone number saved for facility {instance.facility}: {e}")

