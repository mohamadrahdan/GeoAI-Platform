import React, { useState } from "react";
import type { RunParameters } from "@/services/api/types";

interface RunConfigurationFormProps {
  onParamChange: (params: RunParameters) => void;
  disabled: boolean;
}

export function RunConfigurationForm({ onParamChange, disabled }: RunConfigurationFormProps) {
  const [resolution, setResolution] = useState<number>(10);
  const [spatialFilter, setSpatialFilter] = useState<string>("none");
  const [mode, setMode] = useState<string>("standard_inference");

  const handleModeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const nextMode = e.target.value;
    setMode(nextMode);
    onParamChange({ mode: nextMode, resolution, spatial_filter: spatialFilter });
  };

  const handleResolutionChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const nextRes = Number(e.target.value) || 10;
    setResolution(nextRes);
    onParamChange({ mode, resolution: nextRes, spatial_filter: spatialFilter });
  };

  const handleFilterChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const nextFilter = e.target.value;
    setSpatialFilter(nextFilter);
    onParamChange({ mode, resolution, spatial_filter: nextFilter });
  };

  return (
    <div style={{ marginTop: 16, paddingTop: 16, borderTop: "1px dashed #ccc" }}>
      <h4 style={{ marginBottom: 12, color: "#333" }}>⚙️ Advanced Execution Parameters</h4>
      
      <div style={{ marginBottom: 12 }}>
        <label style={{ display: "block", marginBottom: 4, fontSize: "14px" }}>Execution Mode:</label>
        <select 
          value={mode} 
          onChange={handleModeChange}
          disabled={disabled}
          style={{ width: "100%", padding: 6, borderRadius: 4, border: "1px solid #ccc" }}
        >
          <option value="standard_inference">Standard Prediction Engine</option>
          <option value="evaluation_validation">Validation & Accuracy Assessment</option>
          <option value="high_resolution_tile">High-Resolution Tile Segmentation</option>
        </select>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
        <div>
          <label style={{ display: "block", marginBottom: 4, fontSize: "14px" }}>Target Resolution (meters):</label>
          <input 
            type="number" 
            min={1} 
            max={100}
            value={resolution}
            onChange={handleResolutionChange}
            disabled={disabled}
            style={{ width: "100%", padding: 6, borderRadius: 4, border: "1px solid #ccc" }}
          />
        </div>

        <div>
          <label style={{ display: "block", marginBottom: 4, fontSize: "14px" }}>Spatial Vector Filter:</label>
          <select 
            value={spatialFilter} 
            onChange={handleFilterChange}
            disabled={disabled}
            style={{ width: "100%", padding: 6, borderRadius: 4, border: "1px solid #ccc" }}
          >
            <option value="none">No Spatial Mask (Full Extent)</option>
            <option value="mountainous_bounding_box">Mountainous Terrain Mask Only</option>
            <option value="hydrological_buffer">Water Basin Buffer Region</option>
          </select>
        </div>
      </div>
    </div>
  );
}