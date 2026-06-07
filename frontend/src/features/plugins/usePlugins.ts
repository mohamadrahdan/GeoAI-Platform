import { useEffect, useState, useCallback } from "react";
import { apiGet } from "@/services/api/apiClient";
import type { PluginsResponse } from "@/services/api/types";

type State =
  | { kind: "loading" }
  | { kind: "ok"; data: PluginsResponse }
  | { kind: "error"; message: string };

export function usePlugins() {
  const [state, setState] = useState<State>({ kind: "loading" });

  const load = useCallback(async () => {
    setState({ kind: "loading" });
    try {
      const data = await apiGet<PluginsResponse>("/plugins");
      setState({ kind: "ok", data });
    } catch (e) {
      const message = e instanceof Error ? e.message : "Unknown error loading plugins";
      setState({ kind: "error", message });
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  return { state, refetch: load };
}