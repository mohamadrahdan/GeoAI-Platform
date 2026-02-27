import { useEffect, useState } from "react";
import { env } from "@/app/config/env";
import { apiGet } from "@/services/api/apiClient";
import type { HealthResponse } from "@/services/api/types";

type UiState =
  | { kind: "idle" }
  | { kind: "loading" }
  | { kind: "ok"; data: HealthResponse }
  | { kind: "error"; message: string };

export function HomePage() {
  const [state, setState] = useState<UiState>({ kind: "idle" });

  useEffect(() => {
    let mounted = true;

    async function run() {
      try {
        setState({ kind: "loading" });
        const data = await apiGet<HealthResponse>("/health", 5000);
        if (!mounted) return;
        setState({ kind: "ok", data });
      } catch (e) {
        if (!mounted) return;
        const message = e instanceof Error ? e.message : "Unknown error";
        setState({ kind: "error", message });
      }
    }

    run();
    return () => {
      mounted = false;
    };
  }, []);

  return (
    <div style={{ padding: 16 }}>
      <h1>GeoAI Platform</h1>

      <p>Frontend skeleton is ready.</p>

      <p>
        API Base URL: <code>{env.apiBaseUrl}</code>
      </p>

      <div style={{ marginTop: 16 }}>
        <h3>Backend Health</h3>

        {state.kind === "idle" && <p>Idle</p>}
        {state.kind === "loading" && <p>Loading...</p>}
        {state.kind === "ok" && (
          <pre style={{ background: "#f6f6f6", padding: 12, borderRadius: 8 }}>
            {JSON.stringify(state.data, null, 2)}
          </pre>
        )}
        {state.kind === "error" && (
          <pre style={{ background: "#fff2f2", padding: 12, borderRadius: 8 }}>
            {state.message}
          </pre>
        )}
      </div>
    </div>
  );
}