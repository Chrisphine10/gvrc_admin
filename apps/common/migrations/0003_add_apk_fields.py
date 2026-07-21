# Generated manually for APK fields

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_add_essential_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationsettings',
            name='android_apk',
            field=models.FileField(blank=True, help_text='Android APK file for mobile app download', null=True, upload_to='settings/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['apk'])]),
        ),
        migrations.AddField(
            model_name='applicationsettings',
            name='android_apk_version',
            field=models.CharField(blank=True, help_text='APK version number (e.g., 1.0.0)', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='applicationsettings',
            name='android_apk_size',
            field=models.CharField(blank=True, help_text='APK file size (e.g., 25.5 MB)', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='applicationsettings',
            name='enable_apk_download',
            field=models.BooleanField(default=True, help_text='Show APK download button on landing page'),
        ),
    ]


