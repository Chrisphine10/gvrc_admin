# -*- encoding: utf-8 -*-
"""
Google Directions, called from the server instead of the handset.

The app used to call maps.googleapis.com directly with a key compiled into
the APK. Anyone could unzip the release, lift the key and spend GVRC's Maps
budget; there is no way to rotate it without shipping a new app version, and
no way to see who is using it.

Only the routing call moves here. The Maps SDK key in AndroidManifest.xml
cannot follow: the native SDK reads it out of the manifest when the process
starts, long before any network call could fetch one. That key should be a
separate credential restricted to Android apps by package name and signing
certificate, which makes it useless to anyone who extracts it. This one - the
web service key - is the one that had to stop shipping, because an Android
restriction does not protect a web service call.
"""

import logging
import os

import requests

logger = logging.getLogger(__name__)

DIRECTIONS_URL = 'https://maps.googleapis.com/maps/api/directions/json'
TIMEOUT_SECONDS = 12

# Anything else Google accepts here is either unsupported by the app's UI or
# costs more per call. Reject rather than forward.
ALLOWED_MODES = {'driving', 'walking', 'bicycling', 'transit'}


def _key():
    return (os.getenv('GOOGLE_MAPS_SERVER_KEY')
            or os.getenv('GOOGLE_MAPS_API_KEY')
            or '').strip()


def _coord(value):
    """Accepts "lat,lng" and returns it normalised, or None.

    This is a proxy holding a billable credential, so the input is validated
    rather than passed through. Without this the endpoint would forward
    arbitrary query text to Google on GVRC's account.
    """
    if not value or not isinstance(value, str):
        return None
    parts = value.split(',')
    if len(parts) != 2:
        return None
    try:
        lat = float(parts[0])
        lng = float(parts[1])
    except (TypeError, ValueError):
        return None
    if not (-90.0 <= lat <= 90.0) or not (-180.0 <= lng <= 180.0):
        return None
    # 0,0 is the null island the facility importer leaves behind on missing
    # coordinates; routing to it is never what anyone meant.
    if lat == 0.0 and lng == 0.0:
        return None
    return '{0:.6f},{1:.6f}'.format(lat, lng)


def route(origin, destination, mode='driving'):
    """Returns (payload, meta). Never raises.

    payload mirrors what the app needs and nothing more: the encoded polyline
    plus the distance and duration text. The full Google response is not
    forwarded, so the endpoint cannot become an open proxy for Maps data.
    """
    origin = _coord(origin)
    destination = _coord(destination)
    if not origin or not destination:
        return None, {'ok': False, 'reason': 'bad_coordinates'}

    mode = (mode or 'driving').strip().lower()
    if mode not in ALLOWED_MODES:
        mode = 'driving'

    key = _key()
    if not key:
        logger.error('Directions proxy: no Maps key configured on the server')
        return None, {'ok': False, 'reason': 'no_api_key'}

    try:
        response = requests.get(
            DIRECTIONS_URL,
            params={
                'origin': origin,
                'destination': destination,
                'mode': mode,
                'key': key,
            },
            timeout=TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        logger.warning('Directions proxy: request failed -> %s', exc)
        return None, {'ok': False, 'reason': 'upstream_error'}

    if response.status_code != 200:
        logger.warning('Directions proxy: HTTP %s', response.status_code)
        return None, {'ok': False, 'reason': 'upstream_status'}

    try:
        data = response.json()
    except ValueError:
        return None, {'ok': False, 'reason': 'bad_upstream_body'}

    google_status = data.get('status')
    if google_status != 'OK':
        # ZERO_RESULTS is ordinary - islands, or a facility with no road to
        # it. The app falls back to a straight line. Log the rest, and log
        # error_message because REQUEST_DENIED without it is unreadable.
        if google_status != 'ZERO_RESULTS':
            logger.warning(
                'Directions proxy: status %s (%s)',
                google_status, data.get('error_message', ''),
            )
        return None, {'ok': False, 'reason': google_status or 'unknown'}

    try:
        first = data['routes'][0]
        leg = first['legs'][0]
        payload = {
            'polyline': first['overview_polyline']['points'],
            'distance_text': leg.get('distance', {}).get('text', ''),
            'duration_text': leg.get('duration', {}).get('text', ''),
        }
    except (KeyError, IndexError, TypeError):
        return None, {'ok': False, 'reason': 'unexpected_shape'}

    return payload, {'ok': True, 'mode': mode}
