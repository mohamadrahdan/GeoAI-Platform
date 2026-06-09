import { useState } from "react";

export function useExecuteInference() {
  const [state, setState] = useState<{
    kind: "idle" | "executing" | "success" | "error";
    data?: unknown;
    message?: string;
  }>({ kind: "idle" });

  const execute = async (payload: unknown) => {
    // 1. Immediately switch to executing state to trigger green progress bar
    setState({ kind: "executing" });
    
    // 2. Simulate container pipeline processing delay for video capture
    setTimeout(() => {
      setState({
        kind: "success",
        data: {
          status: "success",
          container_id: "geoai-unet-sub-01",
          execution_time_seconds: 12.84,
          detected_features_count: 1420,
          payload: payload
        }
      });
    }, 4000);
  };

  const reset = () => setState({ kind: "idle" });

  return { state, execute, reset };
}