/**
 * AUTOMATIC LOCATION DETECTION - Zero Failure Design
 * Automatically gets device coordinates on page load
 * No user interaction required - fully automatic
 */

(function() {
    'use strict';
    
    console.log('🎯 AUTOMATIC LOCATION SYSTEM - Initializing...');
    
    // Track if location has been obtained
    let locationObtained = false;
    let locationRequested = false;
    
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
     * Save location to Django session
     */
    function saveLocation(latitude, longitude, accuracy) {
        const csrfToken = getCookie('csrftoken');
        
        return fetch('/facilities/set-location/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken || ''
            },
            body: JSON.stringify({
                latitude: latitude,
                longitude: longitude
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('✅ Location saved automatically:', latitude.toFixed(4), longitude.toFixed(4));
                locationObtained = true;
                return data;
            } else {
                console.warn('⚠️ Location save failed:', data.error);
                return null;
            }
        })
        .catch(err => {
            console.error('❌ Error saving location:', err);
            return null;
        });
    }
    
    /**
     * Try GPS location (most accurate)
     */
    function tryGPS() {
        return new Promise((resolve) => {
            if (!navigator.geolocation) {
                console.log('⚠️ Geolocation not supported');
                resolve(null);
                return;
            }
            
            console.log('🎯 Trying GPS location...');
            
            // Try high accuracy first
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const lat = position.coords.latitude;
                    const lng = position.coords.longitude;
                    const acc = position.coords.accuracy;
                    console.log('✅ GPS location obtained:', lat.toFixed(4), lng.toFixed(4), 'Accuracy: ±' + Math.round(acc) + 'm');
                    resolve({ latitude: lat, longitude: lng, accuracy: acc, source: 'gps' });
                },
                function(error) {
                    console.log('⚠️ GPS failed:', error.message);
                    // Try lenient GPS
                    navigator.geolocation.getCurrentPosition(
                        function(position) {
                            const lat = position.coords.latitude;
                            const lng = position.coords.longitude;
                            const acc = position.coords.accuracy;
                            console.log('✅ GPS location obtained (lenient):', lat.toFixed(4), lng.toFixed(4));
                            resolve({ latitude: lat, longitude: lng, accuracy: acc, source: 'gps_lenient' });
                        },
                        function(lenientError) {
                            console.log('⚠️ GPS failed (both attempts)');
                            resolve(null);
                        },
                        {
                            enableHighAccuracy: false,
                            timeout: 5000,
                            maximumAge: 300000
                        }
                    );
                },
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                }
            );
        });
    }
    
    /**
     * Try IP geolocation (fallback)
     */
    function tryIPGeolocation() {
        return new Promise((resolve) => {
            console.log('🌐 Trying IP geolocation...');
            
            // Try backend first (uses actual user IP)
            fetch('/facilities/get-ip-location/')
                .then(response => response.json())
                .then(data => {
                    if (data.success && data.latitude && data.longitude) {
                        console.log('✅ IP location obtained:', data.latitude.toFixed(4), data.longitude.toFixed(4), '-', data.city || 'Unknown');
                        resolve({
                            latitude: parseFloat(data.latitude),
                            longitude: parseFloat(data.longitude),
                            accuracy: data.accuracy || 10000,
                            source: 'ip_backend'
                        });
                    } else {
                        throw new Error('Backend IP geolocation failed');
                    }
                })
                .catch(() => {
                    // Try client-side IP geolocation
                    fetch('https://ipapi.co/json/')
                        .then(response => response.json())
                        .then(data => {
                            if (data.latitude && data.longitude) {
                                console.log('✅ IP location obtained (client):', data.latitude.toFixed(4), data.longitude.toFixed(4));
                                resolve({
                                    latitude: parseFloat(data.latitude),
                                    longitude: parseFloat(data.longitude),
                                    accuracy: 10000,
                                    source: 'ip_client'
                                });
                            } else {
                                throw new Error('Client IP geolocation failed');
                            }
                        })
                        .catch(() => {
                            console.log('⚠️ IP geolocation failed');
                            resolve(null);
                        });
                });
        });
    }
    
    /**
     * Automatic location detection - zero failure
     */
    function getLocationAutomatically() {
        if (locationRequested) {
            console.log('⏭️ Location already requested');
            return;
        }
        
        locationRequested = true;
        console.log('🎯 AUTOMATIC LOCATION DETECTION - Starting...');
        
        // Strategy: GPS first, then IP, then default Nairobi
        // Always get a location - zero failure
        
        tryGPS()
            .then(gpsLocation => {
                if (gpsLocation) {
                    // GPS succeeded - save it
                    return saveLocation(gpsLocation.latitude, gpsLocation.longitude, gpsLocation.accuracy)
                        .then(() => gpsLocation);
                } else {
                    // GPS failed - try IP
                    return tryIPGeolocation()
                        .then(ipLocation => {
                            if (ipLocation) {
                                // IP succeeded - save it
                                return saveLocation(ipLocation.latitude, ipLocation.longitude, ipLocation.accuracy)
                                    .then(() => ipLocation);
                            } else {
                                // Both failed - use default Nairobi
                                console.log('📍 Using default Nairobi location');
                                return saveLocation(-1.2921, 36.8219, 50000)
                                    .then(() => ({ latitude: -1.2921, longitude: 36.8219, accuracy: 50000, source: 'default' }));
                            }
                        });
                }
            })
            .then(location => {
                if (location) {
                    console.log('✅ Location detection complete:', location.source, location.latitude.toFixed(4), location.longitude.toFixed(4));
                    
                    // If on facilities page and GPS location, reload once
                    if (window.location.pathname.includes('/facilities/') && 
                        (location.source === 'gps' || location.source === 'gps_lenient') &&
                        location.accuracy < 1000 &&
                        !sessionStorage.getItem('locationReloaded')) {
                        console.log('🔄 Reloading page with GPS location...');
                        sessionStorage.setItem('locationReloaded', 'true');
                        setTimeout(() => window.location.reload(true), 1000);
                    }
                }
            })
            .catch(err => {
                console.error('❌ Location detection error:', err);
                // Final fallback - default Nairobi
                saveLocation(-1.2921, 36.8219, 50000);
            });
    }
    
    // Initialize on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', getLocationAutomatically);
    } else {
        // DOM already loaded
        getLocationAutomatically();
    }
    
    // Also expose for manual trigger if needed
    window.getLocationAutomatically = getLocationAutomatically;
    
    // Expose refresh function for refresh button
    window.refreshLocation = function() {
        console.log('🔄 Manual location refresh requested...');
        locationRequested = false; // Reset flag to allow new request
        locationObtained = false; // Reset obtained flag
        sessionStorage.removeItem('locationReloaded'); // Allow reload after refresh
        
        // Show notification
        if (window.toastManager) {
            window.toastManager.info('Refreshing location...', 2000);
        }
        
        // Force refresh
        getLocationAutomatically();
    };
    
    // Set up refresh button handler - multiple attempts to ensure it works
    function setupRefreshButton() {
        const refreshBtn = document.getElementById('refresh-location-btn');
        if (refreshBtn) {
            // Remove any existing click handlers by cloning
            const newBtn = refreshBtn.cloneNode(true);
            refreshBtn.parentNode.replaceChild(newBtn, refreshBtn);
            
            // Add click handler
            newBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('🔄 Refresh location button clicked');
                if (window.refreshLocation) {
                    window.refreshLocation();
                } else if (window.LocationPermission && window.LocationPermission.refresh) {
                    window.LocationPermission.refresh();
                } else {
                    console.log('⚠️ Refresh function not available, calling getLocationAutomatically');
                    locationRequested = false;
                    getLocationAutomatically();
                }
                return false;
            });
            console.log('✅ Refresh button handler attached to:', newBtn.id);
        } else {
            console.log('⚠️ Refresh button not found yet');
        }
    }
    
    // Try multiple times to attach handler
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(setupRefreshButton, 100);
            setTimeout(setupRefreshButton, 500);
            setTimeout(setupRefreshButton, 1000);
        });
    } else {
        // DOM already loaded - try immediately and with delays
        setTimeout(setupRefreshButton, 0);
        setTimeout(setupRefreshButton, 100);
        setTimeout(setupRefreshButton, 500);
        setTimeout(setupRefreshButton, 1000);
    }
    
    console.log('✅ AUTOMATIC LOCATION SYSTEM - Ready');
})();

