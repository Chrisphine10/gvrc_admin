# Mobile File Access - Documents and Music

## Overview

Mobile endpoints now provide **fully accessible file URLs** for documents and music files. All file URLs are automatically converted to absolute URLs that mobile devices can directly access and download.

## Features

### ✅ Absolute URLs
- All file URLs are automatically converted to absolute URLs (e.g., `https://hodi.co.ke/media/documents/file.pdf`)
- Mobile devices can directly access files without additional processing
- URLs work across different network environments

### ✅ Document Access
- Documents are accessible via `/mobile/resources/list/` and `/mobile/documents/list/`
- Each document includes:
  - `file_url`: Direct download URL (absolute)
  - `file_name`: Original filename
  - `file_size_bytes`: File size for progress tracking
  - `title`, `description`: Document metadata

### ✅ Music Access
- Music tracks are accessible via `/mobile/resources/list/` and `/mobile/music/list/`
- Each track includes:
  - `music_file`: Direct download/stream URL (absolute)
  - `link`: External streaming link (if available)
  - `name`, `artist`, `duration`: Track metadata

## Endpoints

### 1. Resources Endpoint (Consolidated)
**GET** `/mobile/resources/list/?device_id=xxx`

Returns both documents and music with accessible URLs:
```json
{
  "documents": {
    "count": 51,
    "results": [
      {
        "document_id": 1,
        "title": "Document Title",
        "file_url": "https://hodi.co.ke/media/documents/file.pdf",
        "file_name": "file.pdf",
        "file_size_bytes": 1024000,
        "description": "Document description"
      }
    ]
  },
  "music": {
    "count": 1,
    "results": [
      {
        "music_id": 1,
        "name": "Track Name",
        "artist": "Artist Name",
        "music_file": "https://hodi.co.ke/media/music/track.mp3",
        "duration": "00:03:45"
      }
    ]
  },
  "total_count": 52
}
```

### 2. Documents Endpoint
**GET** `/mobile/documents/list/?device_id=xxx`

Returns only documents with accessible URLs:
```json
{
  "results": [
    {
      "document_id": 1,
      "title": "Document Title",
      "file_url": "https://hodi.co.ke/media/documents/file.pdf",
      "file_name": "file.pdf",
      "file_size_bytes": 1024000
    }
  ]
}
```

### 3. Music Endpoint
**GET** `/mobile/music/list/?device_id=xxx`

Returns only music tracks with accessible URLs:
```json
{
  "count": 1,
  "results": [
    {
      "music_id": 1,
      "name": "Track Name",
      "artist": "Artist Name",
      "music_file": "https://hodi.co.ke/media/music/track.mp3",
      "duration": "00:03:45"
    }
  ]
}
```

## Mobile App Integration

### Android (Kotlin)
```kotlin
// Download document
fun downloadDocument(document: Document) {
    val url = document.fileUrl  // Already absolute URL
    val request = DownloadManager.Request(Uri.parse(url))
    request.setDestinationInExternalPublicDir(
        Environment.DIRECTORY_DOWNLOADS,
        document.fileName
    )
    downloadManager.enqueue(request)
}

// Stream music
fun playMusic(track: Music) {
    val url = track.musicFile ?: track.link  // Absolute URL
    mediaPlayer.setDataSource(url)
    mediaPlayer.prepare()
    mediaPlayer.start()
}
```

### iOS (Swift)
```swift
// Download document
func downloadDocument(_ document: Document) {
    guard let url = URL(string: document.fileUrl) else { return }
    let task = URLSession.shared.downloadTask(with: url) { localURL, _, _ in
        if let localURL = localURL {
            // Save to Documents directory
            let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
            let destinationURL = documentsPath.appendingPathComponent(document.fileName)
            try? FileManager.default.moveItem(at: localURL, to: destinationURL)
        }
    }
    task.resume()
}

// Stream music
func playMusic(_ track: Music) {
    guard let urlString = track.musicFile ?? track.link,
          let url = URL(string: urlString) else { return }
    let player = AVPlayer(url: url)
    player.play()
}
```

## File Access Details

### URL Format
- **Documents**: `https://hodi.co.ke/media/documents/{filename}`
- **Music**: `https://hodi.co.ke/media/music/{filename}`
- All URLs are HTTPS in production
- URLs are automatically generated based on request scheme and host

### File Serving
- Files are served via Django's media file serving
- No authentication required for file access (public files)
- Files are cached with appropriate headers
- Supports range requests for streaming

### Security
- Only active documents/music are accessible
- File URLs are generated server-side
- No direct file system access from mobile
- Files are validated before serving

## Testing

### Test Document Access
```bash
# Get documents with URLs
curl "https://hodi.co.ke/mobile/resources/list/?device_id=test&resource_type=documents"

# Download a document
curl -O "https://hodi.co.ke/media/documents/file.pdf"
```

### Test Music Access
```bash
# Get music with URLs
curl "https://hodi.co.ke/mobile/resources/list/?device_id=test&resource_type=music"

# Stream music (test with audio player)
curl "https://hodi.co.ke/media/music/track.mp3" | mpv -
```

## Notes

1. **Absolute URLs**: All file URLs are automatically converted to absolute URLs
2. **HTTPS**: Production URLs use HTTPS for secure file transfer
3. **Caching**: Files are cached with appropriate headers for mobile optimization
4. **Streaming**: Music files support streaming via HTTP range requests
5. **Download**: Documents can be downloaded directly using the provided URLs

