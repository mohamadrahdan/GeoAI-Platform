import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import type { GeoJsonObject } from "geojson";

// Simulated GeoJSON Polygon representing a detected environmental zone in Isfahan region
const sampleLandslideVector: GeoJsonObject = {
  type: "Feature",
  properties: {
    zone_name: "Isfahan Mountainous Hazard Area A",
    severity: "high"
  },
  geometry: {
    type: "Polygon",
    coordinates: [
      [
        [51.6200, 32.6800],
        [51.7000, 32.6800],
        [51.7000, 32.6200],
        [51.6200, 32.6200],
        [51.6200, 32.6800]
      ]
    ]
  }
};

export function GeoMap() {
  // Custom style injector for geospatial vector layers
  const vectorStyle = {
    color: "#e53e3e",       // Border line crimson color
    weight: 3,             // Border thickness
    fillColor: "#feb2b2",  // Filled inner area translucent red
    fillOpacity: 0.5       // Visible transparency factor for underlay tracking
  };

  return (
    <div style={{ marginTop: 20, borderRadius: 8, overflow: "hidden", border: "1px solid #ddd", background: "#fff" }}>
      <div style={{ padding: "12px 16px", borderBottom: "1px solid #eee", background: "#f8f9fa" }}>
        <h3 style={{ margin: 0, color: "#2d3748", fontSize: "16px" }}>
          🗺️ Spatial Visualization Interface (Active Overlay Vector Mode)
        </h3>
      </div>
      
      <div style={{ height: 450, width: "100%" }}>
        <MapContainer 
          center={[32.6539, 51.6660]} 
          zoom={11} 
          style={{ height: "100%", width: "100%" }}
        >
          {/* Base Topographic Tile Mapping Layer */}
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {/* Core Geospatial Vector Injected Component */}
          <GeoJSON 
            data={sampleLandslideVector} 
            style={vectorStyle} 
          />
        </MapContainer>
      </div>
    </div>
  );
}