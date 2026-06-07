import { useState } from "react";
import { usePlugins } from "@/features/plugins/usePlugins";
import { useDatasets } from "@/features/datasets/useDatasets";
import { useExecuteInference } from "@/features/inference/useExecuteInference";

export function HomePage() {
  const pluginsState = usePlugins();
  const datasetsState = useDatasets();
  const { state: execState, execute, reset } = useExecuteInference();

  const [selectedPlugin, setSelectedPlugin] = useState("");
  const [selectedDataset, setSelectedDataset] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedPlugin || !selectedDataset) return;

    execute({
      plugin_name: selectedPlugin,
      dataset_id: selectedDataset,
      parameters: { mode: "standard_inference" }
    });
  };

  return (
    <div style={{ padding: 24, maxWidth: 800, margin: "0 auto", fontFamily: "sans-serif" }}>
      <h1>🌍 GeoAI Platform Dashboard</h1>
      <p style={{ color: "#666" }}>Modular Geospatial Analysis & Environmental Monitoring</p>

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
              disabled={datasetsState.kind !== "ok" || execState.kind === "executing"}
              style={{ width: "100%", padding: 8, borderRadius: 4 }}
            >
              <option value="">-- Choose a Dataset --</option>
              {datasetsState.kind === "ok" && datasetsState.data.map(d => (
                <option key={d.id} value={d.id}>{d.name}</option>
              ))}
            </select>
          </div>

          <button 
            type="submit"
            disabled={!selectedPlugin || !selectedDataset || execState.kind === "executing"}
            style={{
              background: execState.kind === "executing" ? "#ccc" : "#007bff",
              color: "#fff",
              padding: "10px 16px",
              border: "none",
              borderRadius: 4,
              cursor: "pointer"
            }}
          >
            {execState.kind === "executing" ? "Processing Engine Active..." : "Trigger Model Inference 🚀"}
          </button>
        </form>
      </div>

      {/* Execution Monitor & Response Display */}
      <div style={{ background: "#fff", border: "1px solid #ddd", padding: 20, borderRadius: 8 }}>
        <h3>📊 Execution & Monitoring Console</h3>
        
        {execState.kind === "idle" && <p style={{ color: "#888" }}>Waiting for pipeline trigger...</p>}
        
        {execState.kind === "executing" && (
          <div style={{ color: "#0056b3" }}>
            <p>⏳ <strong>Inference Running:</strong> Processing geospatial layers inside container...</p>
          </div>
        )}

        {execState.kind === "success" && (
          <div style={{ background: "#e6f4ea", padding: 16, borderRadius: 6, color: "#137333" }}>
            <h4>✅ Inference Completed Successfully!</h4>
            <pre style={{ background: "#fff", padding: 12, borderRadius: 4, overflowX: "auto" }}>
              {JSON.stringify(execState.data, null, 2)}
            </pre>
            <button onClick={reset} style={{ marginTop: 8, padding: "6px 12px" }}>Clear Console</button>
          </div>
        )}

        {execState.kind === "error" && (
          <div style={{ background: "#fce8e6", padding: 16, borderRadius: 6, color: "#c5221f" }}>
            <h4>❌ Pipeline Execution Failure</h4>
            <p><code>{execState.message}</code></p>
            <button onClick={reset} style={{ marginTop: 8, padding: "6px 12px" }}>Reset Console</button>
          </div>
        )}
      </div>
    </div>
  );
}