# -*- encoding: utf-8 -*-
"""
Music models for GVRC Admin
"""

from django.db import models
from django.utils import timezone
from apps.authentication.models import User


class Music(models.Model):
    """Music track model"""
    music_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False, help_text="Name of the music track")
    description = models.TextField(blank=True, help_text="Description of the music track")
    link = models.URLField(max_length=500, blank=True, null=True, help_text="Link to external music file or streaming service")
    music_file = models.FileField(upload_to='music_files/%Y/%m/%d/', blank=True, null=True, help_text="Upload music file directly")
    artist = models.CharField(max_length=200, blank=True, help_text="Artist or creator of the music")
    duration = models.DurationField(blank=True, null=True, help_text="Duration of the music track")
    genre = models.CharField(max_length=100, blank=True, help_text="Genre of the music")
    is_active = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    updated_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='music_created', db_column='created_by', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='music_updated', db_column='updated_by')
    
    def __str__(self):
        return f"{self.name} - {self.artist}" if self.artist else self.name
    
    @property
    def total_listens(self):
        """Calculate total listens from MusicPlay records"""
        return self.musicplay_set.count()
    
    @property
    def music_url(self):
        """Return the music URL - either uploaded file or external link"""
        if self.music_file:
            return self.music_file.url
        return self.link
    
    @property
    def has_file(self):
        """Check if music has an uploaded file"""
        return bool(self.music_file)
    
    class Meta:
        verbose_name_plural = "Music"
        db_table = 'music'
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['genre']),
            models.Index(fields=['created_at']),
        ]


class MusicPlay(models.Model):
    """Music play tracking for analytics"""
    play_id = models.AutoField(primary_key=True)
    music = models.ForeignKey(Music, on_delete=models.CASCADE, db_column='music_id', null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', null=False)
    played_at = models.DateTimeField(default=timezone.now, null=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    session_duration = models.DurationField(blank=True, null=True, help_text="How long the user listened to this track")
    
    def __str__(self):
        return f"{self.music.name} played by {self.user.full_name} at {self.played_at}"
    
    class Meta:
        verbose_name_plural = "Music Plays"
        db_table = 'music_plays'
        indexes = [
            models.Index(fields=['music']),
            models.Index(fields=['user']),
            models.Index(fields=['played_at']),
        ]
