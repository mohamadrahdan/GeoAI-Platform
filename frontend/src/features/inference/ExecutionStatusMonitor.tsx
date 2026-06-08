interface ExecutionStatusMonitorProps {
  kind: "idle" | "executing" | "success" | "error";
  message: string;
}

export function ExecutionStatusMonitor({ kind, message }: ExecutionStatusMonitorProps) {
  if (kind === "idle") {
    return (
      <div style={{ color: "#888", fontStyle: "italic", padding: "12px 0" }}>
        📡 System standby. Ready to capture pipeline stream...
      </div>
    );
  }

  return (
    <div style={{ marginTop: 16, borderRadius: 6, overflow: "hidden", border: "1px solid #eee" }}>
      {/* Dynamic Status Header Badge */}
      <div style={{
        padding: "10px 16px",
        color: "#fff",
        fontWeight: "bold",
        backgroundColor: kind === "executing" ? "#0056b3" : kind === "success" ? "#137333" : "#c5221f"
      }}>
        {kind === "executing" && "⏳ CORE ENGINE ACTIVE (PROCESSING OVERLAYS)"}
        {kind === "success" && "✅ PIPELINE EXECUTION SUCCESSFUL"}
        {kind === "error" && "❌ CONTAINER PIPELINE CRASHED"}
      </div>

      {/* Visual Progress Steps Map */}
      <div style={{ padding: 16, backgroundColor: "#fafafa" }}>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 12, fontSize: "12px" }}>
          <span style={{ fontWeight: "bold", color: "#137333" }}>1. Init Container ✔</span>
          <span style={{ fontWeight: kind !== "executing" ? "bold" : "normal" }}>2. Feature Extraction</span>
          <span style={{ fontWeight: kind === "success" ? "bold" : "normal" }}>3. PostGIS Spatial Sync</span>
        </div>

        {/* CSS Animated Progress Track simulation */}
        <div style={{ width: "100%", height: "6px", backgroundColor: "#e0e0e0", borderRadius: 3, overflow: "hidden" }}>
          <div style={{
            height: "100%",
            width: kind === "executing" ? "65%" : kind === "success" ? "100%" : "10%",
            backgroundColor: kind === "error" ? "#c5221f" : "#28a745",
            transition: "width 0.5s ease-in-out"
          }} />
        </div>

        {/* Operational Context Logs Wrapper */}
        <div style={{ marginTop: 12, fontSize: "13px", color: "#555" }}>
          <strong>Status Report:</strong> {message || "Awaiting hardware resource allocation..."}
        </div>
      </div>
    </div>
  );
}