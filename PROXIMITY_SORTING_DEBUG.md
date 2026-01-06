# Proximity Sorting Debug Guide

## Complete Flow Debugging

### 1. Location Detection Flow

**Step 1: Browser Gets Location**
- JavaScript requests location via `navigator.geolocation`
- Check browser console for: `📍 Location obtained:`
- If you see this, location was successfully obtained

**Step 2: Location Saved to Session**
- Location is saved via POST to `/facilities/set-location/`
- Check browser console for: `✅✅✅ LOCATION SAVED TO SESSION:`
- Check network tab for POST request with status 200

**Step 3: Session Verification**
- After saving, system verifies location is in session
- Check browser console for: `✅✅✅ VERIFIED: Location is in session:`
- If this fails, session save didn't work

**Step 4: Page Reload**
- Page should reload automatically after location is saved
- Check browser console for: `🔄 Reloading page to apply proximity sorting...`
- Page reloads after 1.5 seconds

**Step 5: Facility List Uses Location**
- Backend reads location from session
- Check server logs for: `📍 Facility list - Using location from SESSION:`
- Check browser console for: `📍 Using proximity sorting: true`

### 2. Visual Indicators

**On Facilities Page:**
- **Green Badge**: "Sorting by proximity (lat, lng)" - Location is active
- **Gray Badge**: "Default sorting" - Using default Nairobi location
- **Location Status**: Shows current location coordinates

### 3. Debug Commands

**In Browser Console:**

```javascript
// Check if location is in session
fetch('/facilities/set-location/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json', 'X-CSRFToken': document.cookie.match(/csrftoken=([^;]+)/)[1]},
    body: JSON.stringify({latitude: null, longitude: null})
}).then(r => r.json()).then(d => console.log('Session:', d));

// Run full debug
LocationPermission.debug();

// Manually set location (for testing)
fetch('/facilities/set-location/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json', 'X-CSRFToken': document.cookie.match(/csrftoken=([^;]+)/)[1]},
    body: JSON.stringify({latitude: -1.2921, longitude: 36.8219})
}).then(r => r.json()).then(d => {
    console.log('Location set:', d);
    window.location.reload();
});
```

### 4. Server Logs

**Check Gunicorn Logs:**
```bash
tail -f /var/log/gvrc_admin/gunicorn_error.log | grep "📍"
```

**Look for:**
- `📍 Location request received` - Location save request
- `📍 Facility list - Using location from SESSION` - Location read from session
- `📍 Applying proximity sorting` - Sorting is active
- `📍 Sample facilities with distances` - Shows distances for first 5 facilities

### 5. Common Issues

**Issue: Location obtained but not saved**
- Check network tab for POST to `/facilities/set-location/`
- Check for CSRF token errors
- Check server logs for session save errors

**Issue: Location saved but not used**
- Check if page reloaded after saving
- Check server logs for "Using location from SESSION"
- Verify session key is consistent

**Issue: Default location always used**
- Check if location is actually in session
- Check browser console for location source
- Verify session is not being cleared

### 6. Testing Proximity Sorting

**Manual Test:**
1. Open facilities page
2. Check badge - should show "Default sorting"
3. Enable location permission
4. Wait for location to be obtained
5. Page should reload automatically
6. Check badge - should show "Sorting by proximity"
7. Facilities should be sorted by distance

**Verify Sorting:**
- First facility should be closest to your location
- Check browser console for "Sample facilities with distances"
- Distances should increase as you scroll down

### 7. Debug Checklist

- [ ] Location permission granted
- [ ] Location obtained (check console)
- [ ] Location saved to session (check console)
- [ ] Location verified in session (check console)
- [ ] Page reloaded after saving
- [ ] Server logs show "Using location from SESSION"
- [ ] Badge shows "Sorting by proximity"
- [ ] Facilities sorted by distance

---

**Last Updated**: 2025-12-13
**Version**: 2.2.0

