# Location Debugging Instructions

## Quick Debug Steps

### 1. Open Browser Console
- Press `F12` or `Ctrl+Shift+I` (Windows/Linux)
- Or `Cmd+Option+I` (Mac)
- Go to the "Console" tab

### 2. Run Debug Function
Type this in the console and press Enter:
```javascript
LocationPermission.debug()
```

This will run a comprehensive test that:
- ✅ Checks browser geolocation support
- ✅ Checks permission status
- ✅ Tests endpoint connection
- ✅ Tests actual geolocation API
- ✅ Tests saving location to session
- ✅ Verifies location was saved
- ✅ Shows current system state

### 3. Check the Output
Look for these messages:
- `✅✅✅ GEOLOCATION SUCCESS!` - Location was obtained
- `✅✅✅ LOCATION SAVED SUCCESSFULLY!` - Location was saved
- `✅✅✅ VERIFICATION SUCCESS!` - Location is in session
- `🎉🎉🎉 ALL TESTS PASSED!` - Everything works!

If you see errors:
- `❌ PERMISSION_DENIED` - Check browser location permissions
- `❌ POSITION_UNAVAILABLE` - Check OS location services
- `❌ TIMEOUT` - Network or GPS issue

### 4. Manual Tests

#### Test Permission State
```javascript
navigator.permissions.query({ name: 'geolocation' }).then(r => console.log('Permission:', r.state));
```

#### Test Direct Geolocation
```javascript
navigator.geolocation.getCurrentPosition(
    pos => console.log('SUCCESS:', pos.coords.latitude, pos.coords.longitude),
    err => console.error('ERROR:', err.code, err.message)
);
```

#### Check Session Location
```javascript
fetch('/facilities/set-location/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json', 'X-CSRFToken': document.cookie.match(/csrftoken=([^;]+)/)[1]},
    body: JSON.stringify({latitude: null, longitude: null})
}).then(r => r.json()).then(d => console.log('Session:', d));
```

#### Manually Request Location
```javascript
LocationPermission.request(function(error, lat, lng, accuracy) {
    if (error) {
        console.error('Error:', error);
    } else {
        console.log('Location:', lat, lng, 'Accuracy:', accuracy);
    }
});
```

#### Refresh Location
```javascript
LocationPermission.refresh();
```

### 5. Common Issues

#### Issue: Permission Denied
**Solution:**
1. Check browser settings → Privacy → Location
2. Make sure site has permission
3. Try clearing site data and re-requesting

#### Issue: Position Unavailable
**Solution:**
1. Check OS location services are enabled
2. Check if GPS/network location is available
3. Try a different network

#### Issue: Timeout
**Solution:**
1. Check internet connection
2. Wait longer (GPS can be slow)
3. Try refreshing the page

#### Issue: Location Obtained But Not Saved
**Check:**
1. Look for "LOCATION SAVED SUCCESSFULLY" in console
2. Check network tab for POST to `/facilities/set-location/`
3. Verify CSRF token is present

### 6. What to Share

If location still doesn't work, share:
1. Output from `LocationPermission.debug()`
2. Any error messages in console
3. Permission state from browser
4. Browser and OS version

---

**Last Updated**: 2025-12-13
**Version**: 2.2.0

