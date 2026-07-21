# Generated manually for essential settings fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationsettings',
            name='contact_email',
            field=models.EmailField(blank=True, help_text='Primary contact email address', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='applicationsettings',
            name='contact_phone',
            field=models.CharField(blank=True, help_text='Primary contact phone number', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='applicationsettings',
            name='support_email',
            field=models.EmailField(blank=True, help_text='Support email address for user inquiries', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='applicationsettings',
            name='organization_name',
            field=models.CharField(blank=True, help_text='Organization name', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='applicationsettings',
            name='organization_address',
            field=models.TextField(blank=True, help_text='Organization physical address', null=True),
        ),
        migrations.AddField(
            model_name='applicationsettings',
            name='website_url',
            field=models.URLField(blank=True, help_text='Main website URL', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='applicationsettings',
            name='facebook_url',
            field=models.URLField(blank=True, help_text='Facebook page URL', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='applicationsettings',
            name='twitter_url',
            field=models.URLField(blank=True, help_text='Twitter/X profile URL', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='applicationsettings',
            name='linkedin_url',
            field=models.URLField(blank=True, help_text='LinkedIn profile URL', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='applicationsettings',
            name='enable_application_tour',
            field=models.BooleanField(default=True, help_text='Enable the built-in application tour for new users'),
        ),
        migrations.AddField(
            model_name='applicationsettings',
            name='show_tour_on_first_login',
            field=models.BooleanField(default=True, help_text='Automatically show tour on first user login'),
        ),
    ]


