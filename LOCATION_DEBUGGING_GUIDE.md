# Location Debugging Guide

## How to Debug Location Issues

### 1. Open Browser Console
Press `F12` or `Ctrl+Shift+I` (Windows/Linux) or `Cmd+Option+I` (Mac) to open Developer Tools.

### 2. Check Console Messages
Look for these messages:
- `📍 Location obtained:` - Location was successfully obtained
- `✅✅✅ LOCATION OBTAINED:` - Location obtained and marked
- `✅✅✅ LOCATION SAVED TO SESSION:` - Location saved to Django session
- `📍📍📍 WATCHPOSITION GOT LOCATION:` - watchPosition successfully got location
- `⚠️⚠️⚠️ Initial location request failed:` - Initial request failed (but watchPosition may still work)
- `❌ No location available` - Location truly unavailable

### 3. Check Permission Status
In console, run:
```javascript
navigator.permissions.query({ name: 'geolocation' }).then(result => console.log('Permission:', result.state));
```

### 4. Test Location Manually
In console, run:
```javascript
navigator.geolocation.getCurrentPosition(
    pos => console.log('SUCCESS:', pos.coords.latitude, pos.coords.longitude),
    err => console.error('ERROR:', err.code, err.message)
);
```

### 5. Check Session Location
In console, run:
```javascript
fetch('/facilities/set-location/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json', 'X-CSRFToken': document.cookie.match(/csrftoken=([^;]+)/)[1]},
    body: JSON.stringify({latitude: null, longitude: null})
}).then(r => r.json()).then(d => console.log('Session location:', d));
```

### 6. Debug Location System
In console, run:
```javascript
LocationPermission.debug();
```

This will run a comprehensive test of the location system.

---

## Common Issues and Solutions

### Issue: "Location unavailable" even after granting permission
**Possible Causes:**
1. Browser geolocation API is slow to respond
2. GPS/network location not available
3. Permission granted but location service unavailable

**Solution:**
- Wait 5-10 seconds - watchPosition may still get location
- Check browser console for detailed error messages
- Try the "Refresh Location" button
- Check if location services are enabled in your OS

### Issue: Location obtained but not saved
**Check:**
- Console should show "LOCATION SAVED TO SESSION"
- Check network tab for POST to `/facilities/set-location/`
- Verify CSRF token is present

### Issue: Permission state not updating
**Check:**
- Browser may need refresh after granting permission
- Some browsers require page reload
- Check permission state in browser settings

---

## Current Implementation

### Location Request Flow
1. **watchPosition** starts immediately (continuous tracking)
2. **getCurrentPosition** makes one-time request
3. If initial fails, waits 5 seconds for watchPosition
4. Checks session before showing errors
5. Retries when permission state changes to "granted"

### Debugging Features
- ✅ Extensive console logging
- ✅ Permission state change monitoring
- ✅ Session location checking
- ✅ Automatic retry on permission grant
- ✅ Debug function available in console

---

**Version**: 2.2.0
**Last Updated**: 2025-12-13

