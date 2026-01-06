/**
 * Location Permission Handler for PC/Desktop Testing
 * Requests browser geolocation and updates mobile session
 * Uses continuous tracking (watchPosition) for better accuracy like Google Maps
 */

(function() {
    'use strict';

    // Check if geolocation is supported
    if (!navigator.geolocation) {
        console.warn('Geolocation is not supported by this browser.');
        return;
    }

    // Prevent multiple simultaneous location requests
    let isRequestingLocation = false;
    let watchId = null;
    let lastLocationUpdate = null;
    let locationUpdateInterval = 30000; // Update every 30 seconds max
    let hasShownInitialError = false;
    let currentToastId = null;
    let isLocationTrackingActive = false; // Track if watchPosition is active
    let locationObtained = false; // Track if we've successfully obtained location
    
    // Prevent multiple reloads - check sessionStorage on initialization
    if (typeof window !== 'undefined' && typeof sessionStorage !== 'undefined') {
        if (!window.locationReloaded) {
            window.locationReloaded = sessionStorage.getItem('locationReloaded') === 'true';
        }
    }
    
    // Debug mode - set to true for extensive logging
    const DEBUG_MODE = true;
    
    function debugLog(message, data = null) {
        if (DEBUG_MODE) {
            const timestamp = new Date().toISOString();
            console.log(`[LOCATION DEBUG ${timestamp}] ${message}`, data || '');
        }
    }
    
    function debugError(message, error = null) {
        if (DEBUG_MODE) {
            const timestamp = new Date().toISOString();
            console.error(`[LOCATION ERROR ${timestamp}] ${message}`, error || '');
        }
    }

    /**
     * Request location permission and get coordinates (one-time)
     * @param {Function} callback - Callback function with (latitude, longitude) or error
     */
    function requestLocationPermission(callback) {
        debugLog('🔍 requestLocationPermission called', { isRequestingLocation, callback: typeof callback });
        
        if (isRequestingLocation) {
            debugLog('⏭️ Location request already in progress, skipping...');
            return;
        }

        isRequestingLocation = true;
        
        // Start with lenient options for better compatibility
        const options = {
            enableHighAccuracy: false,  // Start with false for faster response, try high accuracy later
            timeout: 10000,  // 10 seconds - reasonable timeout
            maximumAge: 60000  // Accept cached positions up to 1 minute old (faster response)
        };

        debugLog('🌐 Requesting location with options', options);
        debugLog('🌐 Browser geolocation support', {
            geolocation: !!navigator.geolocation,
            permissions: navigator.permissions ? 'available' : 'not available'
        });
        
        // Check permissions API if available and listen for changes
        if (navigator.permissions) {
            navigator.permissions.query({ name: 'geolocation' }).then(function(result) {
                debugLog('🔐 Geolocation permission status', {
                    state: result.state,
                    onchange: typeof result.onchange
                });
                
                // Listen for permission state changes
                result.onchange = function() {
                    const newState = result.state;
                    debugLog('🔐 Permission state changed', { state: newState });
                    console.log('🔐 Location permission changed to:', newState);
                    
                    // If permission was just granted, immediately retry location request
                    if (newState === 'granted' && !locationObtained) {
                        console.log('✅ Location permission granted! Retrying location request...');
                        isRequestingLocation = false; // Reset flag to allow retry
                        
                        // Wait a moment for permission to fully activate, then retry
                        setTimeout(function() {
                            if (!locationObtained) {
                                debugLog('🔄 Retrying location request after permission granted');
                                requestLocationPermission(callback);
                            }
                        }, 500);
                    }
                };
            }).catch(function(err) {
                debugError('🔐 Permission query error', err);
            });
        }
        
        navigator.geolocation.getCurrentPosition(
            function(position) {
                isRequestingLocation = false;
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                const accuracy = position.coords.accuracy; // Accuracy in meters
                const altitude = position.coords.altitude;
                const altitudeAccuracy = position.coords.altitudeAccuracy;
                const heading = position.coords.heading;
                const speed = position.coords.speed;
                
                debugLog('✅ Location obtained successfully', {
                    latitude,
                    longitude,
                    accuracy: Math.round(accuracy) + 'm',
                    altitude,
                    altitudeAccuracy,
                    heading,
                    speed,
                    timestamp: new Date(position.timestamp).toISOString()
                });
                
                console.log('📍 Location obtained:', latitude, longitude);
                console.log('📍 Accuracy: ±' + Math.round(accuracy) + ' meters');
                console.log('📍 Timestamp: ' + new Date(position.timestamp).toLocaleString());
                
                // Warn if accuracy is poor
                if (accuracy > 1000) {
                    console.warn('⚠️ Low accuracy location (>1km). GPS might not be available.');
                    debugLog('⚠️ Low accuracy warning', { accuracy: Math.round(accuracy) + 'm' });
                }
                
                // Mark location as obtained
                locationObtained = true;
                
                if (callback) {
                    debugLog('📞 Calling callback with location', { latitude, longitude, accuracy });
                    callback(null, latitude, longitude, accuracy);
                }
            },
            function(error) {
                // If timeout or unavailable, try IP-based geolocation as fallback
                if (error.code === error.TIMEOUT || error.code === error.POSITION_UNAVAILABLE) {
                    debugLog('⏳ GPS unavailable, will wait for watchPosition to get location...');
                    console.log('⏳ GPS initial request failed, but watchPosition is still running...');
                    console.log('⏳ Waiting for watchPosition to get accurate GPS location...');
                    
                    // Don't use IP geolocation immediately - wait for watchPosition to get GPS
                    // IP geolocation is inaccurate and should only be used as absolute last resort
                    // Return error but don't show it yet - watchPosition might still succeed
                    isRequestingLocation = false;
                    
                    // Give watchPosition more time (it's running in background)
                    // Only use IP if watchPosition also fails after waiting
                    setTimeout(function() {
                        // Check if location was obtained by watchPosition
                        if (!locationObtained) {
                            console.log('⚠️ watchPosition also failed, using IP geolocation as last resort...');
                            debugLog('⚠️ All GPS attempts failed, using IP geolocation as last resort');
                            
                            // Try backend IP geolocation as absolute last resort
                            console.log('🌐 Trying backend IP geolocation (last resort - may not be accurate)...');
                            debugLog('🌐 Attempting backend IP geolocation as last resort');
                    
                    fetch('/facilities/get-ip-location/')
                        .then(response => {
                            if (!response.ok) throw new Error(`Backend IP geolocation failed: ${response.status}`);
                            return response.json();
                        })
                        .then(data => {
                            if (data.success && data.latitude && data.longitude) {
                                const ipLat = parseFloat(data.latitude);
                                const ipLng = parseFloat(data.longitude);
                                const ipAccuracy = data.accuracy || 10000; // ~10km accuracy
                                
                                console.log('✅ Backend IP-based location obtained:', ipLat, ipLng);
                                console.log('📍 City:', data.city || 'Unknown', 'Country:', data.country || 'Unknown');
                                debugLog('✅ Backend IP-based location obtained', {
                                    latitude: ipLat,
                                    longitude: ipLng,
                                    accuracy: ipAccuracy,
                                    city: data.city,
                                    country: data.country,
                                    source: data.source
                                });
                                
                                isRequestingLocation = false;
                                locationObtained = true;
                                
                                if (callback) {
                                    callback(null, ipLat, ipLng, ipAccuracy);
                                }
                            } else {
                                throw new Error(data.error || 'No coordinates in backend IP geolocation response');
                            }
                        })
                        .catch(backendError => {
                            debugError('❌ Backend IP geolocation failed', backendError);
                            console.warn('⚠️ Backend IP geolocation failed, trying client-side services...');
                            
                            // Fallback to client-side IP geolocation
                            const ipServices = [
                                'https://ipapi.co/json/',
                                'https://ip-api.com/json/'
                            ];
                            
                            let ipAttempts = 0;
                            
                            function tryIpService(serviceIndex) {
                                if (serviceIndex >= ipServices.length) {
                                    // All IP services failed, try final GPS retry
                                    debugLog('⏳ All IP services failed, trying final GPS retry...');
                                    const retryOptions = {
                                        enableHighAccuracy: false,
                                        timeout: 5000,
                                        maximumAge: 600000  // Accept cached positions up to 10 minutes old
                                    };
                                    
                                    navigator.geolocation.getCurrentPosition(
                                        function(position) {
                                            isRequestingLocation = false;
                                            const latitude = position.coords.latitude;
                                            const longitude = position.coords.longitude;
                                            const accuracy = position.coords.accuracy;
                                            
                                            debugLog('✅ Location obtained on final GPS retry', { latitude, longitude, accuracy });
                                            console.log('📍 Location obtained (final GPS retry):', latitude, longitude);
                                            
                                            locationObtained = true;
                                            
                                            if (callback) {
                                                callback(null, latitude, longitude, accuracy);
                                            }
                                        },
                                        function(finalError) {
                                            isRequestingLocation = false;
                                            let errorMessage = 'Location information unavailable (GPS and IP both failed)';
                                            
                                            switch(finalError.code) {
                                                case finalError.PERMISSION_DENIED:
                                                    errorMessage = 'Location permission denied by user';
                                                    break;
                                                case finalError.POSITION_UNAVAILABLE:
                                                    errorMessage = 'Location information unavailable (GPS and IP both failed)';
                                                    break;
                                                case finalError.TIMEOUT:
                                                    errorMessage = 'Location request timed out (GPS and IP both failed)';
                                                    break;
                                            }
                                            
                                            debugError('❌ Geolocation error (final)', {
                                                code: finalError.code,
                                                message: errorMessage
                                            });
                                            
                                            console.error('Geolocation error (final):', errorMessage);
                                            
                                            if (callback) {
                                                callback(errorMessage, null, null, null);
                                            }
                                        },
                                        retryOptions
                                    );
                                    return;
                                }
                                
                                const serviceUrl = ipServices[serviceIndex];
                                ipAttempts++;
                                debugLog(`🌐 Trying client IP service ${ipAttempts}: ${serviceUrl}`);
                                
                                fetch(serviceUrl)
                                    .then(response => {
                                        if (!response.ok) throw new Error(`IP geolocation API failed: ${response.status}`);
                                        return response.json();
                                    })
                                    .then(data => {
                                        // Handle different response formats
                                        let lat, lng, city, country;
                                        
                                        if (serviceUrl.includes('ipapi.co')) {
                                            lat = data.latitude;
                                            lng = data.longitude;
                                            city = data.city;
                                            country = data.country_name;
                                        } else if (serviceUrl.includes('ip-api.com')) {
                                            lat = data.lat;
                                            lng = data.lon;
                                            city = data.city;
                                            country = data.country;
                                        }
                                        
                                        if (lat && lng && !isNaN(parseFloat(lat)) && !isNaN(parseFloat(lng))) {
                                            const ipLat = parseFloat(lat);
                                            const ipLng = parseFloat(lng);
                                            const ipAccuracy = 10000; // IP-based is typically ~10km accuracy
                                            
                                            console.log('✅ Client IP-based location obtained:', ipLat, ipLng);
                                            console.log('📍 City:', city || 'Unknown', 'Country:', country || 'Unknown');
                                            debugLog('✅ Client IP-based location obtained', {
                                                latitude: ipLat,
                                                longitude: ipLng,
                                                accuracy: ipAccuracy,
                                                city: city,
                                                country: country,
                                                service: serviceUrl
                                            });
                                            
                                            isRequestingLocation = false;
                                            locationObtained = true;
                                            
                                            if (callback) {
                                                callback(null, ipLat, ipLng, ipAccuracy);
                                            }
                                        } else {
                                            throw new Error('Invalid coordinates in IP geolocation response');
                                        }
                                    })
                                    .catch(ipError => {
                                        debugError(`❌ IP service ${ipAttempts} failed`, ipError);
                                        console.warn(`⚠️ IP service ${ipAttempts} failed, trying next...`);
                                        
                                        // Try next service
                                        if (serviceIndex + 1 < ipServices.length) {
                                            setTimeout(() => tryIpService(serviceIndex + 1), 500);
                                        } else {
                                            // All IP services failed, try final GPS retry
                                            tryIpService(ipServices.length);
                                        }
                                    });
                            }
                            
                            // Start with first client-side IP service
                            tryIpService(0);
                        });
                    return; // Don't call callback with error yet, wait for IP fallback or retry
                }
                
                // For permission denied, don't retry
                isRequestingLocation = false;
                let errorMessage = 'Unknown error occurred';
                let errorCode = error.code;
                
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        errorMessage = 'Location permission denied by user';
                        break;
                    case error.POSITION_UNAVAILABLE:
                        errorMessage = 'Location information unavailable';
                        break;
                    case error.TIMEOUT:
                        errorMessage = 'Location request timed out';
                        break;
                }
                
                debugError('❌ Geolocation error', {
                    code: errorCode,
                    message: errorMessage,
                    error: error
                });
                
                console.error('Geolocation error:', errorMessage);
                
                if (callback) {
                    callback(errorMessage, null, null, null);
                }
            },
            options
        );
    }

    /**
     * Start continuous location tracking (like Google Maps)
     * This improves accuracy over time as GPS gets better signal
     * @param {Function} onLocationUpdate - Callback when location updates
     * @param {Function} onError - Callback on error
     */
    function startLocationTracking(onLocationUpdate, onError) {
        // Stop any existing watch
        if (watchId !== null) {
            navigator.geolocation.clearWatch(watchId);
        }

        // Detect if on mobile device for better GPS accuracy
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        
        const options = {
            enableHighAccuracy: isMobile,  // Use high accuracy on mobile devices for better GPS
            timeout: isMobile ? 20000 : 10000,  // Longer timeout on mobile for GPS to lock (20s), shorter on desktop (10s)
            maximumAge: isMobile ? 0 : 60000  // No cache on mobile (want fresh GPS), accept cache on desktop (1 min)
        };
        
        debugLog('📱 Device detection for watchPosition', { isMobile, enableHighAccuracy: options.enableHighAccuracy, timeout: options.timeout });

        console.log('🔄 Starting continuous location tracking (like Google Maps)...');
        isLocationTrackingActive = true; // Mark tracking as active
        locationObtained = false; // Reset flag
        
        watchId = navigator.geolocation.watchPosition(
            function(position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                const accuracy = position.coords.accuracy;
                const timestamp = position.timestamp;

                // Mark that we've obtained location
                locationObtained = true;
                
                // Clear any error messages since we got location
                if (currentToastId && window.toastManager) {
                    window.toastManager.remove(currentToastId);
                    currentToastId = null;
                    hasShownInitialError = false; // Reset so we can show success
                }

                // Only update if enough time has passed or accuracy improved significantly
                const now = Date.now();
                const timeSinceLastUpdate = lastLocationUpdate ? (now - lastLocationUpdate) : Infinity;
                
                // Update if:
                // 1. First update
                // 2. More than 30 seconds passed
                // 3. Accuracy improved by more than 50%
                const shouldUpdate = !lastLocationUpdate || 
                    timeSinceLastUpdate > locationUpdateInterval ||
                    (lastLocationUpdate && accuracy < lastLocationUpdate.accuracy * 0.5);

                if (shouldUpdate) {
                    console.log('📍 Location updated:', latitude, longitude, 'Accuracy: ±' + Math.round(accuracy) + 'm');
                    lastLocationUpdate = {
                        latitude,
                        longitude,
                        accuracy,
                        timestamp
                    };
                    
                    if (onLocationUpdate) {
                        onLocationUpdate(latitude, longitude, accuracy);
                    }
                } else {
                    console.log('📍 Location tracked (not updating yet):', latitude, longitude, 'Accuracy: ±' + Math.round(accuracy) + 'm');
                }
            },
            function(error) {
                let errorMessage = 'Unknown error occurred';
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        errorMessage = 'Location permission denied by user';
                        break;
                    case error.POSITION_UNAVAILABLE:
                        errorMessage = 'Location information unavailable';
                        break;
                    case error.TIMEOUT:
                        errorMessage = 'Location request timed out';
                        break;
                }
                console.error('Geolocation tracking error:', errorMessage);
                if (onError) {
                    onError(errorMessage);
                }
            },
            options
        );
    }

    /**
     * Stop continuous location tracking
     */
    function stopLocationTracking() {
        if (watchId !== null) {
            navigator.geolocation.clearWatch(watchId);
            watchId = null;
            isLocationTrackingActive = false;
            console.log('🛑 Stopped location tracking');
        }
    }

    /**
     * Update mobile session with GPS coordinates AND Django session
     * @param {string} deviceId - Device ID for mobile session
     * @param {number} latitude - Latitude
     * @param {number} longitude - Longitude
     * @param {Function} callback - Callback function with success/error
     */
    function updateMobileSessionLocation(deviceId, latitude, longitude, callback) {
        // Update Django session for admin dashboard proximity sorting
        const sessionUrl = '/facilities/set-location/';
        fetch(sessionUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                latitude: latitude,
                longitude: longitude
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Django session updated with location:', data);
                // Only reload if location is accurate (GPS, not IP-based) AND not already reloaded
                // Check accuracy from the location data - GPS is typically < 100m, IP is > 10000m
                const isAccurate = data.accuracy && data.accuracy < 1000; // Less than 1km = GPS
                const alreadyReloaded = window.locationReloaded || sessionStorage.getItem('locationReloaded') === 'true';
                
                if (window.location.pathname.includes('/facilities/') && isAccurate && !alreadyReloaded) {
                    console.log('✅ Accurate GPS location saved, will reload page once...');
                    window.locationReloaded = true;
                    sessionStorage.setItem('locationReloaded', 'true');
                    // Small delay to ensure session is saved
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                } else if (window.location.pathname.includes('/facilities/') && !isAccurate) {
                    console.log('⚠️ Location saved but not accurate enough (IP-based), not reloading');
                    if (window.toastManager) {
                        window.toastManager.info('Location saved but not accurate. Enable GPS for precise location.', 3000);
                    }
                } else if (alreadyReloaded) {
                    console.log('⏭️ Page already reloaded, skipping');
                }
            } else {
                console.warn('Could not update Django session:', data.error);
            }
        })
        .catch(error => {
            console.warn('Could not update Django session (may not be logged in):', error);
        });

        // Also update mobile session if deviceId is provided
        if (deviceId) {
            const updateUrl = '/api/mobile/sessions/update/';
            const data = {
                device_id: deviceId,
                latitude: latitude,
                longitude: longitude
            };

            fetch(updateUrl, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Failed to update mobile session:', data.error);
                    if (callback) callback(data.error, false);
                } else {
                    console.log('Mobile session updated with location:', data);
                    if (callback) callback(null, true);
                }
            })
            .catch(error => {
                console.error('Error updating mobile session:', error);
                if (callback) callback(error.message, false);
            });
        } else {
            // No device ID, but session was updated, so success
            if (callback) callback(null, true);
        }
    }

    /**
     * Get CSRF token from cookies
     */
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    /**
     * Save location to Django session (with rate limiting)
     */
    function saveLocationToSession(latitude, longitude, showNotification = true, accuracy = null) {
        debugLog('💾 saveLocationToSession called', { latitude, longitude, showNotification, accuracy });
        
        // Check if this is accurate GPS location (accuracy < 1000m) or inaccurate IP location
        const isAccurateGPS = accuracy !== null && accuracy < 1000; // Less than 1km = GPS
        const isInaccurateIP = accuracy !== null && accuracy >= 10000; // >= 10km = IP-based
        
        if (isInaccurateIP) {
            console.log('⚠️ Skipping save for inaccurate IP location (accuracy: ' + Math.round(accuracy) + 'm)');
            debugLog('⚠️ Skipping save for inaccurate IP location', { accuracy });
            // Still save it but mark as inaccurate
        }
        
        const now = Date.now();
        const lastSave = localStorage.getItem('lastLocationSave');
        
        // Rate limit: don't save more than once every 5 seconds (unless it's accurate GPS)
        if (!isAccurateGPS && lastSave && (now - parseInt(lastSave)) < 5000) {
            const timeSinceLastSave = now - parseInt(lastSave);
            debugLog('⏭️ Skipping location save (rate limited)', { 
                timeSinceLastSave: timeSinceLastSave + 'ms',
                remaining: (5000 - timeSinceLastSave) + 'ms'
            });
            console.log('⏭️ Skipping location save (rate limited)');
            return Promise.resolve({ success: true, skipped: true, accuracy: accuracy });
        }

        localStorage.setItem('lastLocationSave', now.toString());
        
        const csrfToken = getCookie('csrftoken');
        debugLog('🔐 CSRF token', { 
            hasToken: !!csrfToken, 
            tokenLength: csrfToken ? csrfToken.length : 0 
        });
        
        const requestBody = {
            latitude: latitude,
            longitude: longitude
        };
        
        debugLog('📤 Sending location to server', {
            url: '/facilities/set-location/',
            method: 'POST',
            body: requestBody,
            hasCSRF: !!csrfToken
        });

        return fetch('/facilities/set-location/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken || ''
            },
            body: JSON.stringify(requestBody)
        })
        .then(response => {
            debugLog('📥 Response received', {
                status: response.status,
                statusText: response.statusText,
                contentType: response.headers.get('content-type'),
                url: response.url
            });
            
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return response.json();
            } else {
                return response.text().then(text => {
                    debugError('❌ Non-JSON response received', {
                        status: response.status,
                        contentType: contentType,
                        textPreview: text.substring(0, 200)
                    });
                    console.warn('Non-JSON response:', text.substring(0, 100));
                    return { success: false, error: 'Invalid response format', rawResponse: text.substring(0, 200) };
                });
            }
        })
        .then(data => {
            debugLog('📦 Response data parsed', data);
            
            if (data && data.success) {
                console.log('✅ Location saved:', data.latitude.toFixed(4), data.longitude.toFixed(4));
                debugLog('✅ Location saved successfully', {
                    latitude: data.latitude,
                    longitude: data.longitude,
                    sessionKey: data.session_key
                });
                
                if (showNotification && window.toastManager) {
                    // Remove any existing location toast
                    if (currentToastId) {
                        window.toastManager.remove(currentToastId);
                    }
                    
                    const latStr = data.latitude.toFixed(4);
                    const lngStr = data.longitude.toFixed(4);
                    
                    currentToastId = window.toastManager.success(
                        `Location updated (${latStr}, ${lngStr}). Facilities sorted by proximity.`,
                        3000
                    );
                }
                
                return data;
            } else {
                const errorMsg = data ? data.error : 'Unknown error';
                debugError('❌ Location save failed', { error: errorMsg, data });
                throw new Error(errorMsg);
            }
        })
        .catch(error => {
            debugError('❌ Fetch error in saveLocationToSession', {
                error: error.message,
                stack: error.stack,
                name: error.name
            });
            throw error;
        });
    }

    /**
     * Request location and update mobile session
     * @param {string} deviceId - Device ID
     * @param {Function} callback - Callback with (error, success)
     */
    function requestAndUpdateLocation(deviceId, callback) {
        requestLocationPermission(function(error, latitude, longitude) {
            if (error) {
                if (callback) callback(error, false);
                return;
            }

            updateMobileSessionLocation(deviceId, latitude, longitude, function(updateError, success) {
                if (callback) callback(updateError, success);
            });
        });
    }

    /**
     * Force refresh location (for manual refresh button)
     */
    function forceRefreshLocation() {
        const isFacilitiesPage = window.location.pathname.includes('/facilities/');
        
        // Reset the error flag so we can show messages again
        hasShownInitialError = false;
        
        if (window.toastManager) {
            window.toastManager.info('Requesting fresh location...', 3000);
        }
        
        console.log('🔄 Force refreshing location...');
        debugLog('🔄 Force refresh initiated');
        
        // Stop current tracking and restart for fresh location
        stopLocationTracking();
        lastLocationUpdate = null;
        isRequestingLocation = false; // Reset flag to allow new request
        
        // Clear any existing error messages
        if (currentToastId && window.toastManager) {
            window.toastManager.remove(currentToastId);
            currentToastId = null;
        }
        
        requestLocationPermission(function(error, latitude, longitude, accuracy) {
            if (error) {
                debugError('❌ Refresh location failed', { error });
                // Show as info, not error - location is optional
                if (window.toastManager) {
                    window.toastManager.info(
                        'Location unavailable: ' + error + '. Using default location. Enable permissions for proximity sorting.',
                        5000  // Auto-dismiss after 5 seconds
                    );
                }
                // Restart tracking even on error
                startLocationTracking(
                    function(lat, lng, acc) {
                        saveLocationToSession(lat, lng, false);
                    },
                    function(err) {
                        console.error('Tracking error:', err);
                    }
                );
                return;
            }
            
            console.log('📍 Fresh location obtained:', latitude, longitude, 'Accuracy: ±' + Math.round(accuracy) + 'm');
            debugLog('✅ Refresh location success', { latitude, longitude, accuracy });
            
            // Save to Django session
            saveLocationToSession(latitude, longitude, true, accuracy).then((data) => {
                debugLog('✅ Location saved after refresh', data);
                
                // Restart continuous tracking
                startLocationTracking(
                    function(lat, lng, acc) {
                        saveLocationToSession(lat, lng, false);
                    },
                    function(err) {
                        console.error('Tracking error:', err);
                    }
                );
                
                // Only reload if location is accurate GPS (not IP-based) AND not already reloaded
                const alreadyReloaded = window.locationReloaded || sessionStorage.getItem('locationReloaded') === 'true';
                
                if (isFacilitiesPage && data.isAccurateGPS && !alreadyReloaded) {
                    window.locationReloaded = true;
                    sessionStorage.setItem('locationReloaded', 'true');
                    if (window.toastManager) {
                        window.toastManager.success('GPS location updated! Refreshing page...', 2000);
                    }
                    setTimeout(() => window.location.reload(), 2000);
                } else if (isFacilitiesPage && !data.isAccurateGPS) {
                    console.log('⚠️ Location updated but not accurate enough (IP-based), not reloading');
                    if (window.toastManager) {
                        window.toastManager.info('Location updated but not accurate. Enable GPS for precise sorting.', 3000);
                    }
                } else if (alreadyReloaded) {
                    console.log('⏭️ Page already reloaded, skipping');
                } else {
                    if (window.toastManager) {
                        window.toastManager.success('Location updated successfully!', 3000);
                    }
                }
            }).catch(err => {
                console.error('Error refreshing location:', err);
                debugError('❌ Error saving location after refresh', err);
                if (window.toastManager) {
                    // Show as info, not error - location is optional
                    window.toastManager.info('Location refresh unavailable. Using default location.', 3000);
                }
            });
        });
    }

    /**
     * Debug function to test location connection step by step
     * Call from browser console: LocationPermission.debug()
     */
    function debugLocationConnection() {
        console.log('🔍 === COMPREHENSIVE LOCATION DEBUG TEST ===');
        console.log('');
        
        // Step 1: Check browser support
        console.log('Step 1: Checking browser geolocation support...');
        console.log('  - navigator.geolocation:', !!navigator.geolocation);
        console.log('  - navigator.permissions:', !!navigator.permissions);
        console.log('  - isSecureContext:', window.isSecureContext);
        console.log('  - protocol:', window.location.protocol);
        
        if (!navigator.geolocation) {
            console.error('❌ Geolocation not supported!');
            return;
        }
        console.log('✅ Browser supports geolocation');
        console.log('');
        
        // Step 2: Check permissions
        let permissionState = 'unknown';
        if (navigator.permissions) {
            console.log('Step 2: Checking permissions...');
            navigator.permissions.query({ name: 'geolocation' }).then(function(result) {
                permissionState = result.state;
                console.log('  - Permission state:', result.state);
                console.log('  - Permission onchange:', typeof result.onchange);
            }).catch(function(err) {
                console.error('  - Permission query error:', err);
            });
        } else {
            console.log('  - Permissions API not available');
        }
        console.log('');
        
        // Step 3: Check CSRF token
        console.log('Step 3: Checking CSRF token...');
        const csrfToken = getCookie('csrftoken');
        console.log('  - CSRF token exists:', !!csrfToken);
        console.log('  - CSRF token length:', csrfToken ? csrfToken.length : 0);
        console.log('  - CSRF token preview:', csrfToken ? csrfToken.substring(0, 20) + '...' : 'N/A');
        console.log('');
        
        // Step 4: Test endpoint connection
        console.log('Step 4: Testing endpoint connection...');
        fetch('/facilities/set-location/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken || ''
            },
            body: JSON.stringify({
                latitude: null,
                longitude: null
            })
        })
        .then(response => {
            console.log('  - Response status:', response.status);
            console.log('  - Response statusText:', response.statusText);
            console.log('  - Response ok:', response.ok);
            console.log('  - Content-Type:', response.headers.get('content-type'));
            
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return response.json();
            } else {
                return response.text().then(text => {
                    console.error('  - Non-JSON response:', text.substring(0, 200));
                    return { error: 'Non-JSON response', text: text.substring(0, 200) };
                });
            }
        })
        .then(data => {
            console.log('  - Response data:', data);
            console.log('');
            
            // Step 5: Test location request
            console.log('Step 5: Testing location request...');
            requestLocationPermission(function(error, latitude, longitude, accuracy) {
                if (error) {
                    console.error('  ❌ Location request failed:', error);
                    console.log('');
                    console.log('🔍 === DEBUG TEST COMPLETE (WITH ERRORS) ===');
                    return;
                }
                
                console.log('  ✅ Location obtained:');
                console.log('    - Latitude:', latitude);
                console.log('    - Longitude:', longitude);
                console.log('    - Accuracy: ±' + Math.round(accuracy) + 'm');
                console.log('');
                
                // Step 6: Test saving location
                console.log('Step 6: Testing location save...');
                saveLocationToSession(latitude, longitude, true, null)
                    .then(data => {
                        console.log('  ✅ Location saved successfully:', data);
                        console.log('');
                        console.log('🔍 === DEBUG TEST COMPLETE (SUCCESS) ===');
                    })
                    .catch(err => {
                        console.error('  ❌ Location save failed:', err);
                        console.log('');
                        console.log('🔍 === DEBUG TEST COMPLETE (WITH ERRORS) ===');
                    });
            });
        })
        .catch(err => {
            console.error('  ❌ Endpoint connection failed:', err);
            console.log('');
            console.log('🔍 === DEBUG TEST COMPLETE (WITH ERRORS) ===');
        });
    }

    // Expose functions globally for use in other scripts
    window.LocationPermission = {
        request: requestLocationPermission,
        updateSession: updateMobileSessionLocation,
        requestAndUpdate: requestAndUpdateLocation,
        refresh: forceRefreshLocation,
        startTracking: startLocationTracking,
        stopTracking: stopLocationTracking,
        debug: debugLocationConnection,
        saveLocation: saveLocationToSession
    };
    
    // Add refresh button handler when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        // Wait a bit for button to be added
        setTimeout(function() {
            const refreshBtn = document.getElementById('refresh-location-btn');
            if (refreshBtn) {
                refreshBtn.addEventListener('click', function() {
                    forceRefreshLocation();
                });
            }
        }, 500);
    });

    // MANDATORY: Always request location permission on page load
    document.addEventListener('DOMContentLoaded', function() {
        debugLog('🚀 DOMContentLoaded - Starting location initialization');
        
        // Wait for toast manager to be ready
        const waitForToastManager = function(callback, maxAttempts = 10) {
            if (window.toastManager) {
                debugLog('✅ Toast manager ready');
                callback();
            } else if (maxAttempts > 0) {
                debugLog(`⏳ Waiting for toast manager... (${maxAttempts} attempts remaining)`);
                setTimeout(() => waitForToastManager(callback, maxAttempts - 1), 100);
            } else {
                console.warn('Toast manager not loaded, using console fallback');
                debugLog('⚠️ Toast manager not loaded after max attempts');
                callback();
            }
        };

        waitForToastManager(function() {
            debugLog('📋 Initializing location system');
            
            // Get device_id from URL params or localStorage
            const urlParams = new URLSearchParams(window.location.search);
            let deviceId = urlParams.get('device_id');
            debugLog('🔍 Device ID from URL', { deviceId });

            // If not in URL, check localStorage
            if (!deviceId) {
                deviceId = localStorage.getItem('mobile_device_id');
                debugLog('🔍 Device ID from localStorage', { deviceId });
            }

            // If no device_id, generate one and store it
            if (!deviceId) {
                deviceId = 'pc_user_' + Date.now();
                localStorage.setItem('mobile_device_id', deviceId);
                debugLog('🆕 Generated new device ID', { deviceId });
            }

            const isFacilitiesPage = window.location.pathname.includes('/facilities/');
            debugLog('📍 Page check', { 
                isFacilitiesPage, 
                pathname: window.location.pathname 
            });

            // Check if location is already saved and recent (less than 2 minutes old)
            debugLog('🔍 Checking for existing location in session');
            
            const csrfToken = getCookie('csrftoken');
            debugLog('🔐 CSRF token for initial check', { 
                hasToken: !!csrfToken,
                tokenLength: csrfToken ? csrfToken.length : 0
            });
            
            fetch('/facilities/set-location/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken || ''
                },
                body: JSON.stringify({
                    latitude: null,
                    longitude: null
                })
            })
            .then(response => {
                debugLog('📥 Initial location check response', {
                    status: response.status,
                    statusText: response.statusText,
                    contentType: response.headers.get('content-type'),
                    ok: response.ok
                });
                
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    return response.json();
                } else {
                    return response.text().then(text => {
                        debugError('❌ Non-JSON response on initial check', {
                            status: response.status,
                            contentType: contentType,
                            textPreview: text.substring(0, 200)
                        });
                        return { success: false, error: 'Server returned non-JSON response', rawText: text.substring(0, 200) };
                    });
                }
            })
            .then(data => {
                debugLog('📦 Initial location check data', data);
                
                // AUTOMATIC LOCATION DETECTION - Zero failure design
                // Strategy: Try GPS immediately, if fails try IP geolocation, always get location
                console.log('🎯 AUTOMATIC LOCATION DETECTION - Getting device coordinates...');
                
                // Check if we already have a recent location in session
                if (data.success && data.latitude && data.longitude) {
                    console.log('✅ Location already in session:', data.latitude, data.longitude);
                    // Still start tracking for updates, but don't reload
                    startLocationTracking(
                        function(lat, lng, acc) {
                            saveLocationToSession(lat, lng, false, acc);
                        },
                        function(err) {
                            console.log('Tracking error (non-blocking):', err);
                        }
                    );
                    return; // Already have location, no need to request
                }
                
                // No location in session - get it automatically NOW
                console.log('📍 No location in session - requesting automatically...');
                
                // Try GPS first (most accurate)
                requestLocationPermission(function(gpsError, latitude, longitude, accuracy) {
                    if (!gpsError && latitude && longitude) {
                        // GPS succeeded - save immediately
                        console.log('✅ GPS location obtained automatically:', latitude, longitude);
                        saveLocationToSession(latitude, longitude, false, accuracy).then((saveData) => {
                            console.log('✅ GPS location saved to session');
                            
                            // Start continuous tracking for updates
                            startLocationTracking(
                                function(lat, lng, acc) {
                                    saveLocationToSession(lat, lng, false, acc);
                                },
                                function(err) {
                                    console.log('Tracking error (non-blocking):', err);
                                }
                            );
                            
                            // Reload page once if on facilities page and accurate GPS
                            if (isFacilitiesPage && !window.locationReloaded && saveData.isAccurateGPS) {
                                const alreadyReloaded = window.locationReloaded || (typeof sessionStorage !== 'undefined' && sessionStorage.getItem('locationReloaded') === 'true');
                                if (!alreadyReloaded) {
                                    window.locationReloaded = true;
                                    sessionStorage.setItem('locationReloaded', 'true');
                                    console.log('🔄 Reloading page with GPS location...');
                                    setTimeout(() => window.location.reload(true), 1000);
                                }
                            }
                        });
                    } else {
                        // GPS failed - try IP geolocation immediately (automatic fallback)
                        console.log('⚠️ GPS failed, trying IP geolocation automatically...');
                        fetch('/facilities/get-ip-location/')
                            .then(response => response.json())
                            .then(ipData => {
                                if (ipData.success && ipData.latitude && ipData.longitude) {
                                    console.log('✅ IP geolocation obtained automatically:', ipData.latitude, ipData.longitude);
                                    // Save IP location (less accurate but better than nothing)
                                    saveLocationToSession(ipData.latitude, ipData.longitude, false, ipData.accuracy || 10000).then((saveData) => {
                                        console.log('✅ IP location saved to session');
                                        
                                        // Still try GPS in background for better accuracy
                                        startLocationTracking(
                                            function(lat, lng, acc) {
                                                // If GPS becomes available, update with more accurate location
                                                if (acc < 1000) { // GPS accuracy
                                                    console.log('✅ GPS location improved, updating session...');
                                                    saveLocationToSession(lat, lng, false, acc);
                                                }
                                            },
                                            function(err) {
                                                console.log('Tracking error (non-blocking):', err);
                                            }
                                        );
                                        
                                        // Don't reload for IP location (not accurate enough)
                                        console.log('📍 IP location saved (approximate) - proximity sorting will use this');
                                    });
                                } else {
                                    // Both GPS and IP failed - use default Nairobi
                                    console.log('⚠️ Both GPS and IP failed, using default Nairobi location');
                                    saveLocationToSession(-1.2921, 36.8219, false, 50000).then(() => {
                                        console.log('✅ Default location saved');
                                    });
                                }
                            })
                            .catch(ipError => {
                                console.error('IP geolocation error:', ipError);
                                // Final fallback - default Nairobi
                                saveLocationToSession(-1.2921, 36.8219, false, 50000).then(() => {
                                    console.log('✅ Default location saved (fallback)');
                                });
                            });
                    }
                }, 'automatic'); // Request with 'automatic' strategy
                
                // Also start continuous tracking in background (for GPS improvements)
                // Start continuous tracking in background (for GPS improvements)
                startLocationTracking(
                    // onLocationUpdate callback - continuous updates only
                    function(latitude, longitude, accuracy) {
                        console.log('📍📍📍 WATCHPOSITION GOT LOCATION (background update):', latitude, longitude, 'Accuracy:', accuracy);
                        locationObtained = true; // Mark as obtained
                        
                        // Clear any error messages
                        if (currentToastId && window.toastManager) {
                            window.toastManager.remove(currentToastId);
                            currentToastId = null;
                            hasShownInitialError = false;
                        }
                        
                        // Save location to session (silent update)
                        saveLocationToSession(latitude, longitude, false, accuracy).then((data) => {
                            console.log('✅✅✅ WATCHPOSITION LOCATION SAVED (background update):', data);
                            // Update mobile session if deviceId is provided
                            if (deviceId) {
                                updateMobileSessionLocation(deviceId, latitude, longitude, function(updateError, success) {
                                    if (updateError) {
                                        console.warn('Could not update mobile session:', updateError);
                                    }
                                });
                            }
                            
                            // DON'T reload on watchPosition updates - these are continuous background updates
                            console.log('📍 Background location update - not reloading');
                        }).catch(err => {
                            console.error('Error saving location:', err);
                        });
                    },
                    // onError callback
                    function(errorMessage) {
                        // Error handler for watchPosition
                        console.log('Location tracking error (non-blocking):', errorMessage);
                    }
                );
            })
            .catch(err => {
                debugError('❌ Error checking existing location', {
                    error: err.message,
                    stack: err.stack
                });
                console.warn('Could not check existing location:', err);
                // Start tracking anyway
                debugLog('🔄 Starting location tracking despite check error');
                startLocationTracking(
                    function(latitude, longitude, accuracy) {
                        saveLocationToSession(latitude, longitude, false, accuracy);
                    },
                    function(errorMessage) {
                        // Don't show persistent errors - location is optional
                        debugError('Location tracking error (non-blocking)', { error: errorMessage });
                        console.log('ℹ️ Location unavailable - using default location for sorting. This is optional.');
                        
                        // Don't show error immediately - wait a bit to see if location is obtained
                        setTimeout(function() {
                            // Only show brief info message if not already shown and location not obtained
                            if (!hasShownInitialError && window.toastManager && !locationObtained) {
                                hasShownInitialError = true;
                                currentToastId = window.toastManager.info(
                                    'Location unavailable - facilities sorted by default. Enable location for proximity sorting.',
                                    5000  // Auto-dismiss after 5 seconds
                                );
                            }
                        }, 5000); // Wait 5 seconds for location to be obtained
                    }
                );
            });
    });
    
    // Legacy initialization - keep for backward compatibility
    document.addEventListener('DOMContentLoaded', function() {
        // This is now handled by location-auto.js, but keep this for manual refresh button
        const refreshBtn = document.getElementById('refresh-location-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', function() {
                if (window.LocationPermission && window.LocationPermission.refresh) {
                    window.LocationPermission.refresh();
                }
            });
        }
    });
    
    // Clean up on page unload
    window.addEventListener('beforeunload', function() {
        stopLocationTracking();
    });
})();
                    // onError callback
                    function(errorMessage) {
                        // Error handler for watchPosition
                        console.log('Location tracking error (non-blocking):', errorMessage);
                    }
                );
            })
            .catch(err => {
                debugError('❌ Error checking existing location', {
                    error: err.message,
                    stack: err.stack
                });
                console.warn('Could not check existing location:', err);
                // Start tracking anyway
                debugLog('🔄 Starting location tracking despite check error');
                startLocationTracking(
                    function(latitude, longitude, accuracy) {
                        saveLocationToSession(latitude, longitude, false, accuracy);
                    },
                    function(errorMessage) {
                        // Don't show persistent errors - location is optional
                        debugError('Location tracking error (non-blocking)', { error: errorMessage });
                        console.log('ℹ️ Location unavailable - using default location for sorting. This is optional.');
                        
                        // Don't show error immediately - wait a bit to see if location is obtained
                        setTimeout(function() {
                            // Only show brief info message if not already shown and location not obtained
                            if (!hasShownInitialError && window.toastManager && !locationObtained) {
                                hasShownInitialError = true;
                                currentToastId = window.toastManager.info(
                                    'Location unavailable - facilities sorted by default. Enable location for proximity sorting.',
                                    5000  // Auto-dismiss after 5 seconds
                                );
                            }
                        }, 5000); // Wait 5 seconds for location to be obtained
                    }
                );
            });
    });
    
    // Legacy initialization - keep for backward compatibility
    document.addEventListener('DOMContentLoaded', function() {
        // This is now handled by location-auto.js, but keep this for manual refresh button
        const refreshBtn = document.getElementById('refresh-location-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', function() {
                if (window.LocationPermission && window.LocationPermission.refresh) {
                    window.LocationPermission.refresh();
                }
            });
        }
    });
    
    // Clean up on page unload
    window.addEventListener('beforeunload', function() {
        stopLocationTracking();
    });
})();
                        // Don't show persistent errors - location is optional
                        // Only log to console for debugging
                        debugError('Location tracking error (non-blocking)', { error: errorMessage });
                        console.log('ℹ️ Location unavailable - using default location for sorting. This is optional.');
                        
                        // Don't show error immediately - wait a bit to see if location is obtained
                        // Only show error if location hasn't been obtained after a delay
                        setTimeout(function() {
                            // Only show a brief info message, not an error
                            // Check if location was actually obtained before showing error
                            if (!hasShownInitialError && window.toastManager && !locationObtained) {
                                // Check if we have location in session first
                                fetch('/facilities/set-location/', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json',
                                        'X-CSRFToken': getCookie('csrftoken') || ''
                                    },
                                    body: JSON.stringify({ latitude: null, longitude: null })
                                })
                                .then(response => response.json())
                                .then(data => {
                                    // Only show error if location is truly not available
                                    if (!data.success || !data.latitude) {
                                        // Double-check if location was obtained
                                        if (!locationObtained) {
                                            hasShownInitialError = true;
                                            currentToastId = window.toastManager.info(
                                                'Location unavailable - facilities sorted by default. Enable location for proximity sorting.',
                                                5000  // Auto-dismiss after 5 seconds
                                            );
                                        }
                                    } else {
                                        // Location is available, don't show error
                                        debugLog('✅ Location already available in session', data);
                                    }
                                })
                                .catch(() => {
                                    // If check fails and location not obtained, show message
                                    if (!locationObtained) {
                                        hasShownInitialError = true;
                                        currentToastId = window.toastManager.info(
                                            'Location unavailable - facilities sorted by default. Enable location for proximity sorting.',
                                            5000  // Auto-dismiss after 5 seconds
                                        );
                                    }
                                });
                            }
                        }, 5000); // Wait 5 seconds for location to be obtained
                    }
                );

                // Also do an initial one-time request for immediate result
                debugLog('🎯 Making initial one-time location request');
                requestLocationPermission(function(error, latitude, longitude, accuracy) {
                    if (error) {
                        debugError('❌ Initial location request failed (non-blocking)', { error });
                        console.log('⚠️⚠️⚠️ Initial location request failed:', error);
                        console.log('⏳ Waiting for watchPosition to get location...');
                        console.log('📊 Current state - isLocationTrackingActive:', isLocationTrackingActive, 'locationObtained:', locationObtained);
                        
                        // Don't show error immediately - give watchPosition time to get location
                        // Wait a bit to see if watchPosition succeeds
                        setTimeout(function() {
                            console.log('⏰ Timeout check - isLocationTrackingActive:', isLocationTrackingActive, 'locationObtained:', locationObtained);
                            
                            // Only show error if:
                            // 1. We haven't shown an error yet
                            // 2. Location tracking is not active OR location hasn't been obtained
                            // 3. Location is not in session
                            if (!hasShownInitialError && window.toastManager && (!isLocationTrackingActive || !locationObtained)) {
                                console.log('🔍 Checking session for location...');
                                // Check if we have location in session first
                                fetch('/facilities/set-location/', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json',
                                        'X-CSRFToken': getCookie('csrftoken') || ''
                                    },
                                    body: JSON.stringify({ latitude: null, longitude: null })
                                })
                                .then(response => response.json())
                                .then(data => {
                                    console.log('📋 Session location check result:', data);
                                    // Only show error if location is truly not available
                                    if (!data.success || !data.latitude) {
                                        // Double-check if location was obtained by watchPosition
                                        if (!locationObtained) {
                                            console.log('❌ No location available - showing info message');
                                            hasShownInitialError = true;
                                            currentToastId = window.toastManager.info(
                                                'Location unavailable - using default sorting. Enable location for proximity-based sorting.',
                                                5000  // Auto-dismiss after 5 seconds
                                            );
                                        } else {
                                            console.log('✅ Location was obtained by watchPosition - no error needed');
                                        }
                                    } else {
                                        // Location is available, don't show error
                                        console.log('✅ Location already available in session:', data.latitude, data.longitude);
                                        debugLog('✅ Location already available in session', data);
                                    }
                                })
                                .catch((err) => {
                                    console.error('❌ Error checking session location:', err);
                                    // If check fails and location not obtained, show message
                                    if (!locationObtained) {
                                        hasShownInitialError = true;
                                        currentToastId = window.toastManager.info(
                                            'Location unavailable - using default sorting. Enable location for proximity-based sorting.',
                                            5000  // Auto-dismiss after 5 seconds
                                        );
                                    }
                                });
                            } else {
                                if (locationObtained) {
                                    console.log('✅ Location was obtained - no error message needed');
                                }
                            }
                        }, 5000); // Wait 5 seconds for watchPosition to get location
                        console.log('ℹ️ Location unavailable - page will work with default location');
                        return;
                    }

                    debugLog('✅ Initial location obtained, saving to session', { latitude, longitude, accuracy });
                    console.log('✅✅✅ LOCATION OBTAINED:', latitude, longitude, 'Accuracy:', accuracy);
                    locationObtained = true; // Mark as obtained
                    
                    // Save initial location
                    saveLocationToSession(latitude, longitude, true, accuracy).then((data) => {
                        debugLog('✅ Initial location saved successfully', data);
                        console.log('✅✅✅ LOCATION SAVED TO SESSION:', data);
                        
                        // Verify it was saved by checking session
                        const csrfToken = getCookie('csrftoken') || '';
                        fetch('/facilities/set-location/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': csrfToken
                            },
                            body: JSON.stringify({ latitude: null, longitude: null })
                        })
                        .then(r => r.json())
                        .then(verify => {
                            if (verify.success && verify.latitude && verify.longitude) {
                                console.log('✅✅✅ VERIFIED: Location is in session:', verify.latitude, verify.longitude);
                            } else {
                                console.error('❌ VERIFICATION FAILED: Location not in session');
                            }
                        });
                        
                        // Clear any error messages since we got location
                        if (currentToastId && window.toastManager) {
                            window.toastManager.remove(currentToastId);
                            currentToastId = null;
                            hasShownInitialError = false; // Reset flag
                        }
                        
                        // Update mobile session
                        if (deviceId) {
                            updateMobileSessionLocation(deviceId, latitude, longitude, function(updateError, success) {
                                if (updateError) {
                                    console.warn('Could not update mobile session:', updateError);
                                } else {
                                    console.log('✅ Mobile session updated with location');
                                }
                            });
                        }
                        
                        // Only reload if location is accurate GPS (not IP-based) AND not already reloaded
                        const alreadyReloaded = window.locationReloaded || sessionStorage.getItem('locationReloaded') === 'true';
                        
                        if (isFacilitiesPage && !alreadyReloaded && data.isAccurateGPS) {
                            window.locationReloaded = true;
                            sessionStorage.setItem('locationReloaded', 'true');
                            if (window.toastManager) {
                                window.toastManager.success('GPS location obtained! Refreshing page once...', 2000);
                            }
                            console.log('🔄 Reloading page with accurate GPS location (once)...');
                            // Force reload after a short delay to ensure session is saved
                            setTimeout(() => {
                                console.log('🔄 Executing page reload now...');
                                window.location.reload(true); // Force reload from server
                            }, 1500);
                        } else if (isFacilitiesPage && !alreadyReloaded && !data.isAccurateGPS) {
                            console.log('⚠️ Location obtained but not accurate (IP-based), not reloading page');
                            if (window.toastManager) {
                                window.toastManager.info('Location obtained but not accurate. Enable GPS for precise sorting.', 3000);
                            }
                        } else if (alreadyReloaded) {
                            console.log('⏭️ Page already reloaded, skipping');
                        }
                    }).catch(err => {
                        console.error('❌❌❌ Error saving initial location:', err);
                        debugError('❌ Error saving initial location', err);
                    });
                });
            })
            .catch(err => {
                debugError('❌ Error checking existing location', {
                    error: err.message,
                    stack: err.stack,
                    name: err.name
                });
                console.warn('Could not check existing location:', err);
                // Start tracking anyway
                debugLog('🔄 Starting location tracking despite check error');
                startLocationTracking(
                    function(latitude, longitude, accuracy) {
                        saveLocationToSession(latitude, longitude, false, accuracy);
                    },
                    function(errorMessage) {
                        // Don't show persistent errors - location is optional
                        debugError('Location tracking error (non-blocking)', { error: errorMessage });
                        console.log('ℹ️ Location unavailable - using default location. This is optional.');
                        
                        // Don't show error immediately - wait to see if location is obtained
                        setTimeout(function() {
                            // Only show brief info message if not already shown and location not obtained
                            if (!hasShownInitialError && window.toastManager && !locationObtained) {
                                hasShownInitialError = true;
                                currentToastId = window.toastManager.info(
                                    'Location unavailable - facilities sorted by default. Enable location for proximity sorting.',
                                    5000  // Auto-dismiss after 5 seconds
                                );
                            }
                        }, 5000); // Wait 5 seconds for location to be obtained
                    }
                );
            });
        });
    });

    // Clean up on page unload
    window.addEventListener('beforeunload', function() {
        stopLocationTracking();
    });
})();

