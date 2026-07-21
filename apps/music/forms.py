# -*- encoding: utf-8 -*-
"""
Music forms for GVRC Admin
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import Music
import os


class MusicForm(forms.ModelForm):
    """Form for creating and editing music tracks"""
    
    class Meta:
        model = Music
        fields = ['name', 'artist', 'description', 'link', 'music_file', 'genre', 'duration']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter track name'
            }),
            'artist': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter artist name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the music track...'
            }),
            'link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/music.mp3 or streaming link'
            }),
            'music_file': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'audio/*,.mp3,.wav,.ogg,.m4a,.flac'
            }),
            'genre': forms.Select(attrs={
                'class': 'form-control'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control duration-input',
                'placeholder': '00:03:45'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make link and music_file not required since at least one should be provided
        self.fields['link'].required = False
        self.fields['music_file'].required = False
        
        # Convert timedelta to string format for duration field when editing
        if self.instance and self.instance.pk and self.instance.duration:
            from datetime import timedelta
            duration = self.instance.duration
            if isinstance(duration, timedelta):
                total_seconds = int(duration.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                if hours > 0:
                    self.initial['duration'] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                else:
                    self.initial['duration'] = f"{minutes:02d}:{seconds:02d}"
    
    def clean(self):
        cleaned_data = super().clean()
        link = cleaned_data.get('link')
        music_file = cleaned_data.get('music_file')
        
        # Check if this is an edit (instance exists) and has existing file/link
        has_existing_file = self.instance and self.instance.pk and self.instance.music_file
        has_existing_link = self.instance and self.instance.pk and self.instance.link
        
        # At least one of link or music_file must be provided (new or existing)
        if not link and not music_file and not has_existing_file and not has_existing_link:
            raise ValidationError(
                'Please provide either a music file upload or an external link.'
            )
        
        # If both are provided, prefer the uploaded file
        if link and music_file:
            cleaned_data['link'] = ''  # Clear the link if file is uploaded
        
        return cleaned_data
    
    def clean_music_file(self):
        music_file = self.cleaned_data.get('music_file')
        
        # If no new file uploaded and editing existing music, keep the existing file
        if not music_file and self.instance and self.instance.pk and self.instance.music_file:
            return self.instance.music_file
        
        if music_file:
            # No file size limit for audio files - removed to allow unlimited uploads
            # Check file extension
            allowed_extensions = ['.mp3', '.wav', '.ogg', '.m4a', '.flac']
            file_extension = os.path.splitext(music_file.name)[1].lower()
            
            if file_extension not in allowed_extensions:
                raise ValidationError(
                    f'Only the following audio formats are allowed: {", ".join(allowed_extensions)}'
                )
        
        return music_file
    
    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if not duration:
            return None
        
        # If duration is already a timedelta (shouldn't happen, but handle it)
        from datetime import timedelta
        if isinstance(duration, timedelta):
            return duration
        
        # Convert string duration to timedelta
        if isinstance(duration, str):
            duration = duration.strip()
            if not duration:
                return None
            
            try:
                parts = duration.split(':')
                if len(parts) == 2:
                    # MM:SS format
                    minutes, seconds = map(int, parts)
                    if minutes < 0 or seconds < 0 or seconds >= 60:
                        raise ValidationError('Invalid duration format. Minutes must be >= 0, seconds must be 0-59.')
                    return timedelta(minutes=minutes, seconds=seconds)
                elif len(parts) == 3:
                    # HH:MM:SS format
                    hours, minutes, seconds = map(int, parts)
                    if hours < 0 or minutes < 0 or minutes >= 60 or seconds < 0 or seconds >= 60:
                        raise ValidationError('Invalid duration format. Hours must be >= 0, minutes and seconds must be 0-59.')
                    return timedelta(hours=hours, minutes=minutes, seconds=seconds)
                else:
                    raise ValidationError('Duration must be in MM:SS or HH:MM:SS format (e.g., 03:45 or 00:03:45).')
            except ValueError as e:
                raise ValidationError(f'Invalid duration format: {str(e)}. Please use MM:SS or HH:MM:SS format.')
        
        return duration
