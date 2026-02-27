import { useEffect, useState } from "react";
import { apiGet } from "@/services/api/apiClient";
import type { PluginsResponse } from "@/services/api/types";

type State =
  | { kind: "loading" }
  | { kind: "ok"; data: PluginsResponse }
  | { kind: "error"; message: string };

export function usePlugins() {
  const [state, setState] = useState<State>({ kind: "loading" });

  useEffect(() => {
    let mounted = true;

    async function load() {
      try {
        const data = await apiGet<PluginsResponse>("/plugins");
        if (!mounted) return;
        setState({ kind: "ok", data });
      } catch (e) {
        if (!mounted) return;
        const message = e instanceof Error ? e.message : "Unknown error";
        setState({ kind: "error", message });
      }
    }

    load();
    return () => {
      mounted = false;
    };
  }, []);

  return state;
}