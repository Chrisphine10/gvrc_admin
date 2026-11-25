/*
 * HodiMap - one small API over OpenStreetMap (Leaflet) and Google Maps.
 *
 * The provider is chosen by the admin under Administration > Map Settings and
 * reaches the page as JSON in <script id="hodi-map-config">. Pages call:
 *
 *   HodiMap.create('element-id', {zoom, center}).then(map => {
 *     const m = map.addMarker({lat, lng, title, popupHtml, draggable, onDragEnd, onClick});
 *     map.fitTo([m, ...]); map.setView(lat, lng, zoom); map.clearMarkers();
 *     map.onClick((lat, lng) => ...); map.onMoveEnd(() => ...);
 *     map.getBounds() -> {ne: {lat, lng}, sw: {lat, lng}}; map.getZoom();
 *   });
 *
 * HodiMap.escape(text) escapes values before they go into popup HTML.
 */
(function (global) {
  'use strict';

  const LEAFLET_JS = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
  const LEAFLET_JS_SRI = 'sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=';
  const LEAFLET_CSS = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
  const LEAFLET_CSS_SRI = 'sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=';

  const PIN_SVG = '<svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">' +
    '<circle cx="16" cy="16" r="12" fill="#e74c3c" stroke="#c0392b" stroke-width="2"/>' +
    '<circle cx="16" cy="16" r="6" fill="#ffffff"/><circle cx="16" cy="16" r="3" fill="#e74c3c"/></svg>';

  function readConfig() {
    const el = document.getElementById('hodi-map-config');
    let cfg = {};
    if (el) {
      try { cfg = JSON.parse(el.textContent) || {}; } catch (e) { cfg = {}; }
    }
    return Object.assign({
      provider: 'openstreetmap',
      osm_tile_url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
      osm_attribution: '© OpenStreetMap contributors',
      default_center: {lat: -1.286389, lng: 36.817223},
      default_zoom: 7,
      google_maps_api_key: ''
    }, cfg);
  }

  function escape(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  const loaded = {};
  function loadScript(src, integrity) {
    if (loaded[src]) return loaded[src];
    loaded[src] = new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = src; s.async = true;
      if (integrity) { s.integrity = integrity; s.crossOrigin = 'anonymous'; }
      s.onload = resolve;
      s.onerror = () => reject(new Error('Could not load ' + src));
      document.head.appendChild(s);
    });
    return loaded[src];
  }
  function loadCss(href, integrity) {
    if (document.querySelector('link[href="' + href + '"]')) return;
    const l = document.createElement('link');
    l.rel = 'stylesheet'; l.href = href;
    if (integrity) { l.integrity = integrity; l.crossOrigin = 'anonymous'; }
    document.head.appendChild(l);
  }

  // ---------------------------------------------------------------- Leaflet
  function createLeaflet(el, cfg, opts) {
    loadCss(LEAFLET_CSS, LEAFLET_CSS_SRI);
    return loadScript(LEAFLET_JS, LEAFLET_JS_SRI).then(() => {
      const L = global.L;
      const center = opts.center || cfg.default_center;
      const map = L.map(el, {scrollWheelZoom: true}).setView([center.lat, center.lng], opts.zoom || cfg.default_zoom);
      L.tileLayer(cfg.osm_tile_url, {maxZoom: 19, attribution: escape(cfg.osm_attribution)}).addTo(map);
      const icon = L.divIcon({html: PIN_SVG, className: 'hodi-map-pin', iconSize: [32, 32], iconAnchor: [16, 16], popupAnchor: [0, -14]});
      let markers = [];
      return {
        provider: 'openstreetmap',
        raw: map,
        addMarker(o) {
          const m = L.marker([o.lat, o.lng], {title: o.title || '', draggable: !!o.draggable, icon: o.plainIcon ? new L.Icon.Default() : icon}).addTo(map);
          if (o.popupHtml) m.bindPopup(o.popupHtml);
          if (o.onClick) m.on('click', () => o.onClick(m));
          if (o.onDragEnd) m.on('dragend', () => { const p = m.getLatLng(); o.onDragEnd(p.lat, p.lng); });
          m._hodi = {lat: o.lat, lng: o.lng};
          markers.push(m);
          return m;
        },
        moveMarker(m, lat, lng) { m.setLatLng([lat, lng]); },
        openPopup(m) { m.openPopup(); },
        removeMarker(m) { map.removeLayer(m); markers = markers.filter(x => x !== m); },
        clearMarkers() { markers.forEach(m => map.removeLayer(m)); markers = []; },
        markers() { return markers.slice(); },
        fitTo(list, maxZoom) {
          list = list || markers;
          if (!list.length) return;
          map.fitBounds(L.featureGroup(list).getBounds().pad(0.1), {maxZoom: maxZoom || 15});
        },
        setView(lat, lng, zoom) { map.setView([lat, lng], zoom || map.getZoom()); },
        getZoom() { return map.getZoom(); },
        getBounds() {
          const b = map.getBounds();
          return {ne: {lat: b.getNorthEast().lat, lng: b.getNorthEast().lng}, sw: {lat: b.getSouthWest().lat, lng: b.getSouthWest().lng}};
        },
        onClick(cb) { map.on('click', e => cb(e.latlng.lat, e.latlng.lng)); },
        onMoveEnd(cb) { map.on('moveend', cb); },
        resize() { map.invalidateSize(); }
      };
    });
  }

  // ----------------------------------------------------------------- Google
  function createGoogle(el, cfg, opts) {
    const cbName = '__hodiGoogleReady';
    const ready = global.google && global.google.maps ? Promise.resolve() : new Promise((resolve, reject) => {
      global[cbName] = resolve;
      loadScript('https://maps.googleapis.com/maps/api/js?key=' + encodeURIComponent(cfg.google_maps_api_key) +
        '&callback=' + cbName + '&libraries=geometry,places&loading=async').catch(reject);
    });
    return ready.then(() => {
      const g = global.google.maps;
      const center = opts.center || cfg.default_center;
      const map = new g.Map(el, {
        zoom: opts.zoom || cfg.default_zoom, center: center, mapTypeControl: true, streetViewControl: false,
        fullscreenControl: true, styles: [{featureType: 'poi', elementType: 'labels', stylers: [{visibility: 'off'}]}]
      });
      const info = new g.InfoWindow();
      let markers = [];
      return {
        provider: 'google',
        raw: map,
        addMarker(o) {
          const m = new g.Marker({
            position: {lat: o.lat, lng: o.lng}, map: map, title: o.title || '', draggable: !!o.draggable,
            icon: o.plainIcon ? undefined : {url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(PIN_SVG),
              scaledSize: new g.Size(32, 32), anchor: new g.Point(16, 16)}
          });
          if (o.popupHtml) m.addListener('click', () => { info.setContent(o.popupHtml); info.open(map, m); });
          if (o.onClick) m.addListener('click', () => o.onClick(m));
          if (o.onDragEnd) m.addListener('dragend', () => { const p = m.getPosition(); o.onDragEnd(p.lat(), p.lng()); });
          m._hodi = {lat: o.lat, lng: o.lng, popupHtml: o.popupHtml};
          markers.push(m);
          return m;
        },
        moveMarker(m, lat, lng) { m.setPosition({lat: lat, lng: lng}); },
        openPopup(m) { if (m._hodi.popupHtml) { info.setContent(m._hodi.popupHtml); info.open(map, m); } },
        removeMarker(m) { m.setMap(null); markers = markers.filter(x => x !== m); },
        clearMarkers() { markers.forEach(m => m.setMap(null)); markers = []; },
        markers() { return markers.slice(); },
        fitTo(list, maxZoom) {
          list = list || markers;
          if (!list.length) return;
          const b = new g.LatLngBounds();
          list.forEach(m => b.extend(m.getPosition()));
          map.fitBounds(b);
          g.event.addListenerOnce(map, 'bounds_changed', () => { if (map.getZoom() > (maxZoom || 15)) map.setZoom(maxZoom || 15); });
        },
        setView(lat, lng, zoom) { map.setCenter({lat: lat, lng: lng}); if (zoom) map.setZoom(zoom); },
        getZoom() { return map.getZoom(); },
        getBounds() {
          const b = map.getBounds();
          if (!b) return null;
          return {ne: {lat: b.getNorthEast().lat(), lng: b.getNorthEast().lng()}, sw: {lat: b.getSouthWest().lat(), lng: b.getSouthWest().lng()}};
        },
        onClick(cb) { map.addListener('click', e => cb(e.latLng.lat(), e.latLng.lng())); },
        onMoveEnd(cb) { map.addListener('idle', cb); },
        resize() { g.event.trigger(map, 'resize'); }
      };
    });
  }

  function create(elementOrId, opts) {
    opts = opts || {};
    const el = typeof elementOrId === 'string' ? document.getElementById(elementOrId) : elementOrId;
    const cfg = readConfig();
    if (!el) return Promise.reject(new Error('Map element not found'));
    el.innerHTML = '';
    const useGoogle = cfg.provider === 'google' && cfg.google_maps_api_key;
    const make = useGoogle ? createGoogle : createLeaflet;
    return make(el, cfg, opts).catch(err => {
      // Google failing (bad key, blocked script) falls back to OpenStreetMap
      // rather than leaving staff with an empty box.
      if (useGoogle) {
        console.warn('Google Maps failed, falling back to OpenStreetMap:', err);
        el.innerHTML = '';
        return createLeaflet(el, cfg, opts);
      }
      el.innerHTML = '<div class="alert alert-danger m-3">The map could not load. Check the internet connection and try again.</div>';
      throw err;
    });
  }

  global.HodiMap = {create: create, escape: escape, config: readConfig};
})(window);
