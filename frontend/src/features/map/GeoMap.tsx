import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import type { Feature, Polygon } from "geojson";

// Explicitly typed GeoJSON Feature representing a detected landslide zone
const sampleLandslideVector: Feature<Polygon> = {
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
  const vectorStyle = {
    color: "#e53e3e",
    weight: 3,
    fillColor: "#feb2b2",
    fillOpacity: 0.5
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
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          <GeoJSON 
            data={sampleLandslideVector} 
            style={vectorStyle} 
          />
        </MapContainer>
      </div>
    </div>
  );
}