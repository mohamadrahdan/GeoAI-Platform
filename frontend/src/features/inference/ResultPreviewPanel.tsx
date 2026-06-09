interface SpatialPreviewData {
  detected_features_count?: number;
  execution_time_seconds?: number;
  [key: string]: unknown;
}

interface ResultPreviewPanelProps {
  data: SpatialPreviewData;
}

export function ResultPreviewPanel({ data }: ResultPreviewPanelProps) {
  // Extract real metrics from the inference engine payload with safe defaults
  const pixels = data.detected_features_count ?? 0;
  const executionTime = data.execution_time_seconds ?? 0;
  
  // Dynamic geospatial calculation: 1 pixel roughly equals 100 sqm for Sentinel-2 10m resolution
  const estimatedAreaSqm = pixels * 100;

  return (
    <div style={{ marginTop: 16, padding: 16, background: "#fdfdfd", border: "1px solid #e2e8f0", borderRadius: 6 }}>
      <h4 style={{ margin: "0 0 12px 0", color: "#2d3748" }}>📊 Geospatial Analytics Preview</h4>
      
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12 }}>
        {/* Metric Card 1: Detected Features Count */}
        <div style={{ background: "#f7fafc", padding: 12, borderRadius: 6, borderLeft: "4px solid #4a5568" }}>
          <div style={{ fontSize: "11px", color: "#718096", textTransform: "uppercase" }}>Detected Pixels</div>
          <div style={{ fontSize: "18px", fontWeight: "bold", color: "#2d3748", marginTop: 4 }}>
            {pixels.toLocaleString()}
          </div>
        </div>

        {/* Metric Card 2: Calculated Spatial Extent */}
        <div style={{ background: "#f7fafc", padding: 12, borderRadius: 6, borderLeft: "4px solid #3182ce" }}>
          <div style={{ fontSize: "11px", color: "#718096", textTransform: "uppercase" }}>Estimated Extent</div>
          <div style={{ fontSize: "18px", fontWeight: "bold", color: "#2b6cb0", marginTop: 4 }}>
            {estimatedAreaSqm.toLocaleString()} m²
          </div>
        </div>

        {/* Metric Card 3: Backend Runtime Tracking */}
        <div style={{ background: "#f7fafc", padding: 12, borderRadius: 6, borderLeft: "4px solid #38a169" }}>
          <div style={{ fontSize: "11px", color: "#718096", textTransform: "uppercase" }}>Engine Runtime</div>
          <div style={{ fontSize: "18px", fontWeight: "bold", color: "#38a169", marginTop: 4 }}>
            {executionTime.toFixed(2)}s
          </div>
        </div>
      </div>
    </div>
  );
}