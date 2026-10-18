/* globals L */
(function () {
  function init (el) {
    var tiles = el.getAttribute('data-tiles')
    var lat = parseFloat(el.getAttribute('data-lat'))
    var lon = parseFloat(el.getAttribute('data-lon'))
    if (!tiles || isNaN(lat) || isNaN(lon)) return
    lat = Math.max(-90, Math.min(90, lat))
    lon = Math.max(-180, Math.min(180, lon))

    // Place the map inside the block with the event information, so it sits next to the location
    var info = el.previousElementSibling
    if (el.classList.contains('venuemap-beside') && info && info.querySelector('.info-row')) {
      info.classList.add('venuemap-host')
      info.insertBefore(el, info.firstChild)
      el.classList.add('venuemap-moved')
    }

    var map = L.map(el.querySelector('.venuemap-canvas'), {
      // Don't hijack page scrolling
      scrollWheelZoom: false,
      dragging: !L.Browser.mobile,
      tap: false
    })
    L.tileLayer(tiles, {
      attribution: el.getAttribute('data-attrib'),
      maxZoom: 18
    }).addTo(map)
    var title = el.getAttribute('data-title') || ''
    L.marker([lat, lon], {
      title: title,
      alt: title,
      icon: L.icon({
        iconUrl: el.getAttribute('data-icon'),
        shadowUrl: el.getAttribute('data-shadow'),
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        tooltipAnchor: [16, -28],
        shadowSize: [41, 41]
      })
    }).addTo(map)
    map.setView([lat, lon], parseInt(el.getAttribute('data-zoom'), 10) || 15)
  }

  function initAll () {
    if (!window.L) return
    var els = document.querySelectorAll('.venuemap')
    for (var i = 0; i < els.length; i++) init(els[i])
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll)
  } else {
    initAll()
  }
})()
