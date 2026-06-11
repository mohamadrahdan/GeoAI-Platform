import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export function GeoMap() {
  return (
    <div style={{ marginTop: 20, borderRadius: 8, overflow: "hidden", border: "1px solid #ddd", background: "#fff" }}>
      <div style={{ padding: "12px 16px", borderBottom: "1px solid #eee", background: "#f8f9fa" }}>
        <h3 style={{ margin: 0, color: "#2d3748", fontSize: "16px" }}>🗺️ Spatial Visualization Interface</h3>
      </div>
      
      <div style={{ height: 450, width: "100%" }}>
        <MapContainer 
          center={[32.6539, 51.6660]} 
          zoom={10} 
          style={{ height: "100%", width: "100%" }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
        </MapContainer>
      </div>
    </div>
  );
}