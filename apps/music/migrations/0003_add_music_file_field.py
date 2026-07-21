# Generated manually to add music_file field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_alter_music_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='music_file',
            field=models.FileField(blank=True, help_text='Upload music file directly', null=True, upload_to='music_files/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='music',
            name='link',
            field=models.URLField(blank=True, help_text='Link to external music file or streaming service', max_length=500, null=True),
        ),
    ]
