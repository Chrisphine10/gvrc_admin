# Music Playback Fix for Mobile App

## Problem
Music files were not playing directly in the mobile app because:
1. The API was returning relative URLs instead of absolute URLs
2. URLs were not using HTTPS in production
3. CORS headers were missing for media file access

## Solution

### 1. Updated MusicSerializer (`apps/api/serializers.py`)
- **Added `music_url` field**: Returns the primary music URL (uses `music_file` if available, otherwise `link`)
- **Added `music_file_url` field**: Returns absolute URL specifically for uploaded music files
- **Absolute URL generation**: All URLs are now converted to absolute URLs with proper HTTPS support
- **HTTPS enforcement**: Production domain (`hodi.co.ke`) automatically uses HTTPS

### 2. Updated Nginx Configuration (`nginx/appseed-app.conf`)
- **Added CORS headers** to `/media/` location block:
  - `Access-Control-Allow-Origin: *`
  - `Access-Control-Allow-Methods: GET, HEAD, OPTIONS`
  - `Access-Control-Allow-Headers: Range`
  - `Access-Control-Expose-Headers: Content-Length, Content-Range`
- **Added range request support**: `Accept-Ranges: bytes` for audio/video streaming

## API Response Format

The `/mobile/music/list/` endpoint now returns:

```json
{
  "music_id": 1,
  "name": "Test",
  "description": "test",
  "link": null,
  "music_file": "https://hodi.co.ke/media/music_files/2025/11/10/Test.mp3",
  "music_file_url": "https://hodi.co.ke/media/music_files/2025/11/10/Test.mp3",
  "music_url": "https://hodi.co.ke/media/music_files/2025/11/10/Test.mp3",
  "artist": "Tester",
  "duration": "00:00:03",
  "genre": "pop",
  "is_active": true,
  "created_at": "2025-11-10T07:41:04.359277Z"
}
```

## Mobile App Implementation

### Recommended Approach
Use the `music_url` field for playback as it handles both uploaded files and external links:

```dart
// Example (Flutter/Dart)
String? musicUrl = track['music_url'];
if (musicUrl != null) {
  // Use musicUrl for audio playback
  audioPlayer.play(UrlSource(musicUrl));
}
```

### Fallback Strategy
If `music_url` is null, fallback to `music_file_url` or `music_file`:

```dart
String? musicUrl = track['music_url'] ?? 
                  track['music_file_url'] ?? 
                  track['music_file'];
```

## Testing

1. **Test the endpoint**:
   ```bash
   curl -X GET "https://hodi.co.ke/mobile/music/list/?device_id=YOUR_DEVICE_ID"
   ```

2. **Verify URLs**:
   - All URLs should be absolute (start with `https://`)
   - URLs should point to `hodi.co.ke` domain
   - Media files should be accessible via HTTPS

3. **Test CORS**:
   ```bash
   curl -I -X OPTIONS "https://hodi.co.ke/media/music_files/2025/11/10/Test.mp3" \
     -H "Origin: https://your-mobile-app-domain.com" \
     -H "Access-Control-Request-Method: GET"
   ```

## Next Steps

1. **Restart Nginx** (if nginx config was updated):
   ```bash
   sudo nginx -t  # Test configuration
   sudo systemctl reload nginx  # Reload nginx
   ```

2. **Update Mobile App**:
   - Use `music_url` field for playback
   - Ensure audio player supports HTTPS URLs
   - Test playback with the new absolute URLs

3. **Verify Media File Access**:
   - Ensure media files are accessible via HTTPS
   - Check that CORS headers are present in responses
   - Verify range requests work for streaming

## Notes

- The `music_url` field is the primary field to use as it intelligently handles both uploaded files and external links
- All URLs are automatically converted to HTTPS for production domain
- CORS headers allow mobile apps from any origin to access media files
- Range request support enables efficient audio/video streaming
