import { useState } from "react";
import { apiPost } from "@/services/api/apiClient";
import type { InferenceRequest, InferenceResponse } from "@/services/api/types";

type ExecutionState =
  | { kind: "idle" }
  | { kind: "executing" }
  | { kind: "success"; data: InferenceResponse }
  | { kind: "error"; message: string };

export function useExecuteInference() {
  const [state, setState] = useState<ExecutionState>({ kind: "idle" });

  const execute = async (payload: InferenceRequest) => {
    try {
      setState({ kind: "executing" });
      
      // تعیین ۶۰ ثانیه تایم‌اوت به دلیل زمان‌بر بودن پردازش مدل‌های مکانی
      const response = await apiPost<InferenceResponse, InferenceRequest>(
        "/inference/run", 
        payload,
        60_000 
      );
      
      setState({ kind: "success", data: response });
    } catch (error) {
      const message = error instanceof Error ? error.message : "Inference execution failed";
      setState({ kind: "error", message });
    }
  };

  const reset = () => setState({ kind: "idle" });

  return { state, execute, reset };
}