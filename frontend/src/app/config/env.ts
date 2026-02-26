function readEnv(key: string, fallback?: string): string {
  const value = (import.meta.env as Record<string, string | undefined>)[key];
  return value ?? fallback ?? "";
}

// Keep it explicit and centralized
export const env = {
  apiBaseUrl: readEnv("VITE_API_BASE_URL", "http://localhost:8000"),
};

// export const env = {
//   apiBaseUrl: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
// };