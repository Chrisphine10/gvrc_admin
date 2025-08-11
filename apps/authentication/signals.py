# -*- encoding: utf-8 -*-
"""
Authentication signals for email notifications
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

@receiver(post_save, sender=User)
def send_user_confirmation_email(sender, instance, created, **kwargs):
    """Send confirmation email when new user is created"""
    if created:
        # Determine user role
        if instance.is_superuser:
            role = "Super Admin"
        elif instance.is_staff:
            role = "Staff"
        else:
            role = "User"
        
        # Email content
        subject = f"Welcome to GVRC Admin - {role} Account Created"
        message = f"""
Hello {instance.first_name or instance.username},

Your {role} account has been successfully created for the GVRC Admin system.

Account Details:
- Username: {instance.username}
- Email: {instance.email}
- Role: {role}
- Login URL: {settings.APP_DOMAIN}/admin/login/

Please contact your administrator if you need your password reset.

Best regards,
GVRC Admin Team
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send email to {instance.email}: {e}")