/**
 * Google Maps integration for Japan Trip 2025
 * Displays attraction markers on destination and route pages with clickable pins
 */

class TripMap {
  constructor(containerId, markers) {
    this.containerId = containerId;
    this.markers = markers;
    this.map = null;
    this.markerObjects = [];
  }

  /**
   * Initialize the Google Map with markers
   */
  init() {
    const container = document.getElementById(this.containerId);

    if (!container) {
      console.warn(`Map container #${this.containerId} not found`);
      return;
    }

    if (!this.markers || this.markers.length === 0) {
      container.innerHTML = '<p class="map-no-data">No location data available for attractions.</p>';
      return;
    }

    // Calculate bounds from all markers
    const bounds = new google.maps.LatLngBounds();
    this.markers.forEach(marker => {
      bounds.extend(new google.maps.LatLng(marker.lat, marker.lng));
    });

    // Initialize map centered on bounds
    this.map = new google.maps.Map(container, {
      center: bounds.getCenter(),
      zoom: 12,
      mapTypeControl: true,
      streetViewControl: false,
      fullscreenControl: true,
      styles: this.getMapStyles()
    });

    // Fit map to show all markers
    this.map.fitBounds(bounds);

    // Add padding to bounds
    const paddingOptions = {
      top: 50,
      right: 50,
      bottom: 50,
      left: 50
    };
    this.map.fitBounds(bounds, paddingOptions);

    // Create markers
    this.createMarkers();

    // Add marker clustering if many markers
    if (this.markers.length > 10) {
      this.addMarkerClusterer();
    }
  }

  /**
   * Create map markers for each attraction
   */
  createMarkers() {
    this.markers.forEach((markerData, index) => {
      const marker = new google.maps.Marker({
        position: { lat: markerData.lat, lng: markerData.lng },
        map: this.map,
        title: markerData.title,
        animation: google.maps.Animation.DROP,
        label: {
          text: String(index + 1),
          color: 'white',
          fontSize: '12px',
          fontWeight: 'bold'
        }
      });

      // Create info window
      const infoWindow = new google.maps.InfoWindow({
        content: this.createInfoWindowContent(markerData)
      });

      // Show info window on hover
      marker.addListener('mouseover', () => {
        infoWindow.open(this.map, marker);
      });

      marker.addListener('mouseout', () => {
        infoWindow.close();
      });

      // Navigate to attraction page on click
      marker.addListener('click', () => {
        window.location.href = markerData.url;
      });

      this.markerObjects.push(marker);
    });
  }

  /**
   * Create HTML content for info window
   */
  createInfoWindowContent(markerData) {
    return `
      <div class="map-info-window">
        <h3>${markerData.title}</h3>
        <p><a href="${markerData.url}">View Details →</a></p>
      </div>
    `;
  }

  /**
   * Add marker clustering for better performance with many markers
   */
  addMarkerClusterer() {
    if (typeof MarkerClusterer !== 'undefined') {
      new MarkerClusterer(this.map, this.markerObjects, {
        imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m',
        maxZoom: 15
      });
    }
  }

  /**
   * Custom map styling for better visibility
   */
  getMapStyles() {
    return [
      {
        featureType: 'poi',
        elementType: 'labels',
        stylers: [{ visibility: 'off' }]
      },
      {
        featureType: 'transit',
        elementType: 'labels',
        stylers: [{ visibility: 'off' }]
      }
    ];
  }
}

/**
 * Initialize map when Google Maps API is loaded
 */
function initMap() {
  // Find all map containers on the page
  const mapContainers = document.querySelectorAll('[data-map-markers]');

  mapContainers.forEach(container => {
    const markersJson = container.getAttribute('data-map-markers');

    try {
      const markers = JSON.parse(markersJson);
      const map = new TripMap(container.id, markers);
      map.init();
    } catch (error) {
      console.error('Error parsing map markers:', error);
      container.innerHTML = '<p class="map-error">Error loading map data.</p>';
    }
  });
}

// Make initMap available globally for Google Maps callback
// Set immediately to ensure it's available before Google Maps API loads
if (typeof window !== 'undefined') {
  window.initMap = initMap;
}
