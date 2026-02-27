import { useEffect, useState } from "react";
import { env } from "@/app/config/env";
import { apiGet } from "@/services/api/apiClient";
import type { HealthResponse } from "@/services/api/types";
import { usePlugins } from "@/features/plugins/usePlugins";
import { useDatasets } from "@/features/datasets/useDatasets";

type UiState =
  | { kind: "idle" }
  | { kind: "loading" }
  | { kind: "ok"; data: HealthResponse }
  | { kind: "error"; message: string };

export function HomePage() {
  const [state, setState] = useState<UiState>({ kind: "idle" });
  const pluginsState = usePlugins();
  const datasetsState = useDatasets();

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

      <h2>Plugins</h2>
      {pluginsState.kind === "loading" && <p>Loading plugins...</p>}
      {pluginsState.kind === "error" && <p>{pluginsState.message}</p>}
      {pluginsState.kind === "ok" && (
        <ul>
          {pluginsState.data.plugins.map((name) => (
            <li key={name}>{name}</li>
          ))}
        </ul>
      )}

      <h2>Datasets</h2>
      {datasetsState.kind === "loading" && <p>Loading datasets...</p>}
      {datasetsState.kind === "error" && <p>{datasetsState.message}</p>}
      {datasetsState.kind === "ok" && (
        <ul>
          {datasetsState.data.datasets.map((d) => (
            <li key={d.id}>{d.name}</li>
          ))}
        </ul>
      )}

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