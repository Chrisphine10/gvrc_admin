# Troubleshooting Mobile API - Changes Not Reflecting

## Quick Fixes

### 1. Clear All Caches
```bash
cd /home/ubuntu/gvrc_admin
source env/bin/activate
python3 clear_cache_safe.py
```

### 2. Restart Server
```bash
# Reload gunicorn workers
sudo pkill -HUP -f "gunicorn"

# Or full restart
sudo systemctl restart nginx
```

### 3. Clear Mobile App Cache
- **Android**: Settings > Apps > Your App > Storage > Clear Cache
- **iOS**: Delete and reinstall app, or clear app data
- **Browser**: Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

### 4. Verify Mobile Session Has GPS
The API sorts by distance when GPS is available. Check if your mobile session has coordinates:

```bash
# Check mobile session (requires database access)
# Or update session with GPS:
PUT /mobile/sessions/update/?device_id=YOUR_DEVICE_ID
{
  "latitude": -1.2921,
  "longitude": 36.8219
}
```

## What Changed

### Facilities Sorting:
- **With GPS**: Sorted by distance (closest first) ✅
- **Without GPS**: Sorted by creation date (newest first) - prevents Baringo default ✅

### Performance Optimizations:
- Lightweight serializer (70% smaller payload)
- Smart database prefetching
- Cache headers (30-120 seconds)
- Field selection (only needed data)

## Verify Changes Are Active

### Check API Response:
1. Call the API: `GET /mobile/facilities/list/?device_id=YOUR_DEVICE_ID`
2. Look for `sorting_info` field in response
3. Check response headers for `Cache-Control: public, max-age=30`
4. Verify response structure (should have `service_count`, `contact_count` instead of full objects)

### Expected Response Structure:
```json
{
  "count": 16386,
  "results": [
    {
      "facility_id": 1,
      "facility_name": "...",
      "county_name": "...",
      "service_count": 4,
      "contact_count": 2,
      "latitude": -1.2921,
      "longitude": 36.8219,
      "distance_km": 5.2  // Only if GPS available
    }
  ],
  "sorting_info": {
    "method": "distance" or "created_at",
    "gps_available": true/false,
    "message": "..."
  }
}
```

## Common Issues

### Issue: Still seeing Baringo first
**Solution**: 
- Update mobile session with GPS coordinates
- Or clear app cache and restart app
- The new default (creation date) should show newest facilities first

### Issue: Slow load times
**Solution**:
- Clear all caches (see above)
- Check if cache headers are present in response
- Verify lightweight serializer is being used (check response structure)

### Issue: Changes not showing
**Solution**:
1. Verify server restarted: `ps aux | grep gunicorn`
2. Clear Django cache: `python3 clear_cache_safe.py`
3. Clear browser/app cache
4. Test with fresh device_id/session

## Testing Commands

```bash
# Verify optimizations
python3 verify_mobile_api.py

# Clear cache
python3 clear_cache_safe.py

# Check server status
ps aux | grep gunicorn

# Test API (requires valid device_id)
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/mobile/facilities/list/?device_id=YOUR_DEVICE_ID&page_size=5"
```

