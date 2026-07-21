# -*- encoding: utf-8 -*-
"""
Management command to create sample music data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.music.models import Music
from apps.authentication.models import User
from datetime import timedelta


class Command(BaseCommand):
    help = 'Create sample music data for testing'

    def handle(self, *args, **options):
        # Try to get an existing user, or create a simple one
        try:
            user = User.objects.first()
            if not user:
                self.stdout.write(
                    self.style.WARNING('No users found. Please create a user first.')
                )
                return
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error accessing users: {e}')
            )
            return

        # Sample music data
        sample_music = [
            {
                'name': 'Peaceful Morning',
                'artist': 'Nature Sounds',
                'description': 'A calming morning melody with birds and gentle streams',
                'link': 'https://example.com/music/peaceful-morning.mp3',
                'genre': 'Ambient',
                'duration': timedelta(minutes=3, seconds=45),
            },
            {
                'name': 'Community Spirit',
                'artist': 'Local Artists',
                'description': 'Uplifting community song celebrating unity and hope',
                'link': 'https://example.com/music/community-spirit.mp3',
                'genre': 'Folk',
                'duration': timedelta(minutes=4, seconds=12),
            },
            {
                'name': 'Healing Journey',
                'artist': 'Therapeutic Music',
                'description': 'Soothing instrumental piece for relaxation and healing',
                'link': 'https://example.com/music/healing-journey.mp3',
                'genre': 'Classical',
                'duration': timedelta(minutes=5, seconds=30),
            },
            {
                'name': 'Empowerment Anthem',
                'artist': 'Women\'s Choir',
                'description': 'Inspiring anthem promoting women\'s empowerment and strength',
                'link': 'https://example.com/music/empowerment-anthem.mp3',
                'genre': 'Gospel',
                'duration': timedelta(minutes=4, seconds=55),
            },
            {
                'name': 'Hope for Tomorrow',
                'artist': 'Youth Ensemble',
                'description': 'Hopeful song about building a better future together',
                'link': 'https://example.com/music/hope-for-tomorrow.mp3',
                'genre': 'Pop',
                'duration': timedelta(minutes=3, seconds=28),
            },
        ]

        created_count = 0
        for music_data in sample_music:
            music, created = Music.objects.get_or_create(
                name=music_data['name'],
                defaults={
                    'artist': music_data['artist'],
                    'description': music_data['description'],
                    'link': music_data['link'],
                    'genre': music_data['genre'],
                    'duration': music_data['duration'],
                    'created_by': user,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created music: {music.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} sample music tracks'
            )
        )
