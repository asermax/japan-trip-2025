/**
 * Google Maps integration for Japan Trip 2025
 * Displays attraction markers on destination and route pages with clickable pins
 * Uses AdvancedMarkerElement (v3.56+) for improved performance and features
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
  async init() {
    const container = document.getElementById(this.containerId);

    if (!container) {
      console.warn(`Map container #${this.containerId} not found`);
      return;
    }

    if (!this.markers || this.markers.length === 0) {
      container.innerHTML = '<p class="map-no-data">No location data available for attractions.</p>';
      return;
    }

    // Import the marker library for AdvancedMarkerElement
    const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");
    this.AdvancedMarkerElement = AdvancedMarkerElement;
    this.PinElement = PinElement;

    // Calculate bounds from all markers
    const bounds = new google.maps.LatLngBounds();
    this.markers.forEach(marker => {
      bounds.extend(new google.maps.LatLng(marker.lat, marker.lng));
    });

    // Initialize map centered on bounds
    // mapId is required for AdvancedMarkerElement
    // Note: Custom styles cannot be set when mapId is present
    this.map = new google.maps.Map(container, {
      center: bounds.getCenter(),
      zoom: 12,
      mapId: 'JAPAN_TRIP_MAP',  // Required for advanced markers
      mapTypeControl: true,
      streetViewControl: false,
      fullscreenControl: true
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
    await this.createMarkers();
  }

  /**
   * Create map markers for each attraction using AdvancedMarkerElement
   */
  async createMarkers() {
    this.markers.forEach((markerData, index) => {
      // Create a custom pin with label
      const pinElement = new this.PinElement({
        glyph: String(index + 1),
        glyphColor: 'white',
        background: '#d63384',
        borderColor: '#9c1f6a',
        scale: 1.2
      });

      // Create advanced marker
      const marker = new this.AdvancedMarkerElement({
        map: this.map,
        position: { lat: markerData.lat, lng: markerData.lng },
        title: markerData.title,
        content: pinElement.element
      });

      // Create info window
      const infoWindow = new google.maps.InfoWindow({
        content: this.createInfoWindowContent(markerData)
      });

      // Show info window on hover
      marker.addListener('gmp-mouseover', () => {
        infoWindow.open({
          map: this.map,
          anchor: marker
        });
      });

      marker.addListener('gmp-mouseout', () => {
        infoWindow.close();
      });

      // Navigate to attraction page on click
      marker.addListener('gmp-click', () => {
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

}

/**
 * Initialize map when Google Maps API is loaded
 */
async function initMap() {
  // Find all map containers on the page
  const mapContainers = document.querySelectorAll('[data-map-markers]');

  for (const container of mapContainers) {
    const markersJson = container.getAttribute('data-map-markers');

    try {
      const markers = JSON.parse(markersJson);
      const map = new TripMap(container.id, markers);
      await map.init();
    } catch (error) {
      console.error('Error initializing map:', error);
      container.innerHTML = '<p class="map-error">Error loading map data.</p>';
    }
  }
}

// Make initMap available globally for Google Maps callback
if (typeof window !== 'undefined') {
  window.initMap = initMap;
}
