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
    
    def clean(self):
        cleaned_data = super().clean()
        link = cleaned_data.get('link')
        music_file = cleaned_data.get('music_file')
        
        # At least one of link or music_file must be provided
        if not link and not music_file:
            raise ValidationError(
                'Please provide either a music file upload or an external link.'
            )
        
        # If both are provided, prefer the uploaded file
        if link and music_file:
            cleaned_data['link'] = ''  # Clear the link if file is uploaded
        
        return cleaned_data
    
    def clean_music_file(self):
        music_file = self.cleaned_data.get('music_file')
        if music_file:
            # Check file size (limit to 50MB)
            if music_file.size > 50 * 1024 * 1024:
                raise ValidationError('Music file size must be under 50MB.')
            
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
        if duration:
            # Convert string duration to timedelta
            try:
                from datetime import timedelta
                parts = duration.split(':')
                if len(parts) == 2:
                    # MM:SS format
                    minutes, seconds = map(int, parts)
                    return timedelta(minutes=minutes, seconds=seconds)
                elif len(parts) == 3:
                    # HH:MM:SS format
                    hours, minutes, seconds = map(int, parts)
                    return timedelta(hours=hours, minutes=minutes, seconds=seconds)
                else:
                    raise ValidationError('Duration must be in MM:SS or HH:MM:SS format.')
            except ValueError:
                raise ValidationError('Duration must be in MM:SS or HH:MM:SS format.')
        
        return duration
