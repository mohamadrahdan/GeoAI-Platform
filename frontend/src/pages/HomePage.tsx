import { useState } from "react";
import { usePlugins } from "@/features/plugins/usePlugins";
import { useDatasets } from "@/features/datasets/useDatasets";
import { useExecuteInference } from "@/features/inference/useExecuteInference";
import { RunConfigurationForm } from "@/features/inference/RunConfigurationForm";
import { ExecutionStatusMonitor } from "@/features/inference/ExecutionStatusMonitor";
import type { RunParameters } from "@/services/api/types";

export function HomePage() {
  const { state: pluginsState, refetch: refetchPlugins } = usePlugins();
  const { state: datasetsState, refetch: refetchDatasets } = useDatasets();
  const { state: execState, execute, reset } = useExecuteInference();

  const [selectedPlugin, setSelectedPlugin] = useState("");
  const [selectedDataset, setSelectedDataset] = useState("");
  
  const [customParams, setCustomParams] = useState<RunParameters>({
    mode: "standard_inference"
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedPlugin || !selectedDataset) return;

    execute({
      plugin_name: selectedPlugin,
      dataset_id: selectedDataset,
      parameters: customParams
    });
  };

  return (
    <div style={{ padding: 24, maxWidth: 800, margin: "0 auto", fontFamily: "sans-serif" }}>
      <h1>🌍 GeoAI Platform Dashboard</h1>
      <p style={{ color: "#666" }}>Modular Geospatial Analysis & Environmental Monitoring</p>

      {/* Core Setup Monitoring Sections (Plugins & Datasets Status) */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 20 }}>
        
        {/* Plugins Loading/Error Context */}
        <div style={{ border: "1px solid #ddd", padding: 16, borderRadius: 6 }}>
          <h4>Active Core Plugins</h4>
          {pluginsState.kind === "loading" && <div style={{ color: "#666" }}>🌀 Loading system plugins...</div>}
          {pluginsState.kind === "error" && (
            <div>
              <p style={{ color: "#c5221f", margin: "4px 0" }}>⚠️ Error: {pluginsState.message}</p>
              <button onClick={refetchPlugins} style={{ padding: "4px 8px" }}>Retry Connection 🔄</button>
            </div>
          )}
          {pluginsState.kind === "ok" && pluginsState.data.plugins.length === 0 && (
            <p style={{ color: "#888", fontStyle: "italic" }}>No custom plugins loaded in core context.</p>
          )}
          {pluginsState.kind === "ok" && pluginsState.data.plugins.length > 0 && (
            <ul style={{ paddingLeft: 20, margin: 0 }}>
              {pluginsState.data.plugins.map(name => <li key={name}><code>{name}</code></li>)}
            </ul>
          )}
        </div>

        {/* Datasets Loading/Error/Empty State Context */}
        <div style={{ border: "1px solid #ddd", padding: 16, borderRadius: 6 }}>
          <h4>Available Storage Datasets</h4>
          {datasetsState.kind === "loading" && <div style={{ color: "#666" }}>🌀 Accessing PostGIS storage layer...</div>}
          {datasetsState.kind === "error" && (
            <div>
              <p style={{ color: "#c5221f", margin: "4px 0" }}>⚠️ Error: {datasetsState.message}</p>
              <button onClick={refetchDatasets} style={{ padding: "4px 8px" }}>Retry Connection 🔄</button>
            </div>
          )}
          {datasetsState.kind === "ok" && datasetsState.data.length === 0 && (
            <div style={{ padding: "8px", background: "#fff3cd", color: "#856404", borderRadius: 4 }}>
              📭 <strong>Empty State:</strong> Database is online, but no active spatial layers found.
            </div>
          )}
          {datasetsState.kind === "ok" && datasetsState.data.length > 0 && (
            <ul style={{ paddingLeft: 20, margin: 0 }}>
              {datasetsState.data.map(d => <li key={d.id}>{d.name}</li>)}
            </ul>
          )}
        </div>
      </div>

      {/* Inference Pipeline Configuration Form */}
      <div style={{ background: "#f8f9fa", padding: 20, borderRadius: 8, marginBottom: 20 }}>
        <h3>🧱 Run Inference Pipeline</h3>
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: 12 }}>
            <label style={{ display: "block", marginBottom: 6 }}>Select Plugin:</label>
            <select 
              value={selectedPlugin} 
              onChange={(e) => setSelectedPlugin(e.target.value)}
              disabled={pluginsState.kind !== "ok" || execState.kind === "executing"}
              style={{ width: "100%", padding: 8, borderRadius: 4 }}
            >
              <option value="">-- Choose a Plugin --</option>
              {pluginsState.kind === "ok" && pluginsState.data.plugins.map(name => (
                <option key={name} value={name}>{name}</option>
              ))}
            </select>
          </div>

          <div style={{ marginBottom: 16 }}>
            <label style={{ display: "block", marginBottom: 6 }}>Select Target Dataset:</label>
            <select 
              value={selectedDataset} 
              onChange={(e) => setSelectedDataset(e.target.value)}
              disabled={pluginsState.kind !== "ok" || datasetsState.kind !== "ok" || execState.kind === "executing"}
              style={{ width: "100%", padding: 8, borderRadius: 4 }}
            >
              <option value="">-- Choose a Dataset --</option>
              {datasetsState.kind === "ok" && datasetsState.data.map(d => (
                <option key={d.id} value={d.id}>{d.name}</option>
              ))}
            </select>
          </div>

          <RunConfigurationForm 
            onParamChange={setCustomParams} 
            disabled={execState.kind === "executing"}
          />

          <button 
            type="submit"
            disabled={!selectedPlugin || execState.kind === "executing"}
            style={{
              background: execState.kind === "executing" ? "#ccc" : "#007bff",
              color: "#fff",
              padding: "10px 16px",
              border: "none",
              borderRadius: 4,
              cursor: "pointer",
              marginTop: 16
            }}
          >
            {execState.kind === "executing" ? "Processing Engine Active..." : "Trigger Model Inference 🚀"}
          </button>
        </form>
      </div>

      {/* Execution Monitor Block using the new Status Component */}
      <div style={{ background: "#fff", border: "1px solid #ddd", padding: 20, borderRadius: 8 }}>
        <h3>📊 Execution & Monitoring Console</h3>
        
        <ExecutionStatusMonitor 
          kind={execState.kind} 
          message={execState.kind === "error" ? execState.message : execState.kind === "success" ? "Payload processing complete." : ""} 
        />

        {/* Retain the strict JSON dump display for raw success verification */}
        {execState.kind === "success" && (
          <div style={{ marginTop: 16, background: "#e6f4ea", padding: 12, borderRadius: 4 }}>
            <pre style={{ background: "#fff", padding: 12, borderRadius: 4, overflowX: "auto", margin: 0 }}>
              {JSON.stringify(execState.data, null, 2)}
            </pre>
            <button onClick={reset} style={{ marginTop: 8, padding: "6px 12px" }}>Clear Console</button>
          </div>
        )}
      </div>
    </div>
  );
}