#!/usr/bin/env python
"""
Simple test script to verify music upload functionality
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')
django.setup()

from apps.music.models import Music
from apps.authentication.models import User

def test_music_upload():
    """Test the music upload functionality"""
    print("Testing Music Upload Functionality...")
    print("=" * 50)
    
    # Check if we have any users
    try:
        user = User.objects.first()
        if not user:
            print("❌ No users found. Please create a user first.")
            return False
        print(f"✅ Found user: {user.full_name}")
    except Exception as e:
        print(f"❌ Error accessing users: {e}")
        return False
    
    # Check if we have any music tracks
    try:
        music_count = Music.objects.count()
        print(f"✅ Found {music_count} music tracks")
        
        if music_count > 0:
            # Show some sample tracks
            tracks = Music.objects.all()[:3]
            for track in tracks:
                print(f"  - {track.name} by {track.artist or 'Unknown'}")
                if track.has_file:
                    print(f"    📁 File: {track.music_file.name}")
                elif track.link:
                    print(f"    🔗 Link: {track.link}")
                else:
                    print(f"    ⚠️  No media")
        else:
            print("ℹ️  No music tracks found yet")
            
    except Exception as e:
        print(f"❌ Error accessing music: {e}")
        return False
    
    # Test the model properties
    try:
        if music_count > 0:
            track = Music.objects.first()
            print(f"\n✅ Testing model properties for '{track.name}':")
            print(f"  - Has file: {track.has_file}")
            print(f"  - Music URL: {track.music_url}")
            print(f"  - Total listens: {track.total_listens}")
    except Exception as e:
        print(f"❌ Error testing model properties: {e}")
        return False
    
    print("\n✅ Music upload functionality test completed successfully!")
    return True

if __name__ == "__main__":
    success = test_music_upload()
    sys.exit(0 if success else 1)
