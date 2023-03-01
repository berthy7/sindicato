const tilesProvider = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
let myMap = L.map('map').setView([-17.8603, -63.1513], 13);
let zoomMap = L.map('zoom-map').setView([-17.8603, -63.1513], 13);
let popup = L.popup();
let popup_zm = L.popup();
let marker, marker_zm;
let m_lat = -17.860312;
let m_lng = -63.151347;

function init_map() {
    if (marker === undefined) {
        marker = L.marker([m_lat, m_lng], {draggable: true}).addTo(myMap);
        L.tileLayer(tilesProvider, {
            maxZoom: 18,
        }).addTo(myMap);

        marker.on('moveend', e => {
            onMarkerClick(e.sourceTarget)
        });
        /* Cover whole map area */
        window.dispatchEvent(new Event('resize'));
        myMap.invalidateSize();
    }
    else marker.setLatLng(new L.LatLng(m_lat, m_lng));
    myMap.flyTo([m_lat, m_lng], 8)
}

function onMarkerClick(e) {
    console.log(e)
    popup.setLatLng(e._latlng).setContent("Ubicación: " + e._latlng.toString()).openOn(myMap);
    document.getElementById('latitud').value = e._latlng.lat
    document.getElementById('longitud').value = e._latlng.lng
    m_lat = e._latlng.lat
    m_lng =e._latlng.lng
    
    // if (marker_zm) marker_zm.setLatLng(new L.LatLng(e._latlng.lat, e._latlng.lng));
}

function init_zoom_map() {
    if (marker_zm === undefined) {
        marker_zm = L.marker([m_lat, m_lng], {draggable: true}).addTo(zoomMap);
        L.tileLayer(tilesProvider, {
            maxZoom: 18,
        }).addTo(zoomMap);

        marker_zm.on('moveend', e => {
            onMarkerClickZoom(e.sourceTarget)
        });
        /* Cover whole map area */
        // window.dispatchEvent(new Event('resize'));
        zoomMap.invalidateSize();
    }
    else marker_zm.setLatLng(new L.LatLng(m_lat, m_lng));
    zoomMap.flyTo([m_lat, m_lng], 8)
}

function onMarkerClickZoom(e) {
    console.log(e)
    popup_zm.setLatLng(e._latlng).setContent("Ubicación: " + e._latlng.toString()).openOn(zoomMap);
    document.getElementById('latitud').value = e._latlng.lat
    document.getElementById('longitud').value = e._latlng.lng
    m_lat = e._latlng.lat
    m_lng =e._latlng.lng
    
    // marker.setLatLng(new L.LatLng(e._latlng.lat, e._latlng.lng))
    
    if (marker !== undefined) {
        myMap.removeLayer(marker)
        was_removed = true
    }
    myMap.flyTo([e._latlng.lat, e._latlng.lng], 8)
    marker = L.marker([e._latlng.lat, e._latlng.lng], { draggable: true }).addTo(myMap)
    if (was_removed) {
        marker.on('moveend', e => {
            onMarkerClick(e.sourceTarget)
        });
    }
}
