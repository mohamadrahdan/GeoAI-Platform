import { Component, ErrorInfo, ReactNode } from "react";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error caught by GeoAI ErrorBoundary:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: 24, border: "2px solid #c5221f", backgroundColor: "#fce8e6", borderRadius: 8, margin: 16 }}>
          <h2 style={{ color: "#c5221f", marginTop: 0 }}>🚨 Critical UI Crash Intercepted</h2>
          <p style={{ color: "#333" }}>An unexpected rendering error occurred within the platform dashboard.</p>
          <pre style={{ backgroundColor: "#fff", padding: 12, borderRadius: 4, overflowX: "auto" }}>
            {this.state.error?.toString()}
          </pre>
          <button 
            onClick={() => window.location.reload()}
            style={{ padding: "8px 16px", backgroundColor: "#c5221f", color: "#fff", border: "none", borderRadius: 4, cursor: "pointer" }}
          >
            Reload Platform Application
          </button>
        </div>
      );
    }

    return this.children;
  }
}