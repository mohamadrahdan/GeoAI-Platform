interface ExecutionStatusMonitorProps {
  kind: "idle" | "executing" | "success" | "error";
  message: string;
  onReset?: () => void;
}

export function ExecutionStatusMonitor({ kind, message, onReset }: ExecutionStatusMonitorProps) {
  if (kind === "idle") {
    return (
      <div style={{ padding: 12, background: "#f7fafc", color: "#4a5568", borderRadius: 4, fontStyle: "italic" }}>
        Console ready. Awaiting inference trigger pipeline activation...
      </div>
    );
  }

  return (
    <div style={{ marginTop: 12 }}>
      {/* 1. Dynamic Status Indicator Bar */}
      <div 
        style={{ 
          padding: 12, 
          borderRadius: 4, 
          fontWeight: "bold",
          background: kind === "executing" ? "#e8f0fe" : kind === "success" ? "#e6f4ea" : "#fce8e6",
          color: kind === "executing" ? "#1a73e8" : kind === "success" ? "#137333" : "#c5221f"
        }}
      >
        {kind === "executing" && "🌀 INFERENCE ENGINE ACTIVE (CONTAINER PROCESSING)"}
        {kind === "success" && "✅ PIPELINE EXECUTION SUCCESSFUL"}
        {kind === "error" && "❌ CONTAINER PIPELINE CRASHED"}
      </div>

      {/* 2. Self-Correcting Animated Progress Track */}
      <div style={{ background: "#e2e8f0", height: 8, borderRadius: 4, marginTop: 8, overflow: "hidden" }}>
        <div 
          style={{ 
            background: kind === "error" ? "#e53e3e" : "#3182ce", 
            height: "100%", 
            width: kind === "executing" ? "65%" : "100%",
            transition: "width 0.5s ease-in-out",
            animation: kind === "executing" ? "pulse 1.5s infinite" : "none"
          }} 
        />
      </div>

      {/* 3. Detailed Runtime Messages & Logs */}
      {message && (
        <p style={{ fontSize: 13, color: "#4a5568", marginTop: 8, paddingLeft: 4 }}>
          <strong>Status Report:</strong> {message}
        </p>
      )}

      {/* 4. Integrated Operational Reset Control Block */}
      {onReset && kind !== "executing" && (
        <button
          onClick={onReset}
          style={{
            marginTop: 12,
            padding: "6px 12px",
            background: "#edf2f7",
            color: "#4a5568",
            border: "1px solid #cbd5e0",
            borderRadius: 4,
            cursor: "pointer",
            fontSize: "12px",
            fontWeight: "500"
          }}
        >
          Reset Console State 🔄
        </button>
      )}
    </div>
  );
}