import { useEffect, useState, useCallback } from "react";
import { apiGet } from "@/services/api/apiClient";
import type { DatasetsResponse } from "@/services/api/types";

type State =
  | { kind: "loading" }
  | { kind: "ok"; data: DatasetsResponse }
  | { kind: "error"; message: string };

export function useDatasets() {
  const [state, setState] = useState<State>({ kind: "loading" });

  const load = useCallback(async () => {
    setState({ kind: "loading" });
    try {
      const data = await apiGet<DatasetsResponse>("/datasets");
      setState({ kind: "ok", data });
    } catch (e) {
      const message = e instanceof Error ? e.message : "Unknown error loading datasets";
      setState({ kind: "error", message });
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  return { state, refetch: load };
}