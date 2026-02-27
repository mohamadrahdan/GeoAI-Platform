import { env } from "@/app/config/env";
import { ApiError } from "@/services/api/apiError";

type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

function joinUrl(baseUrl: string, path: string): string {
  const b = baseUrl.replace(/\/+$/, "");
  const p = path.startsWith("/") ? path : `/${path}`;
  return `${b}${p}`;
}

async function parseJsonSafe(res: Response): Promise<unknown> {
  const text = await res.text();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

export async function apiRequest<TResponse, TBody = unknown>(args: {
  method: HttpMethod;
  path: string;
  body?: TBody;
  timeoutMs?: number;
}): Promise<TResponse> {
  const url = joinUrl(env.apiBaseUrl, args.path);
  const controller = new AbortController();
  const timeoutMs = args.timeoutMs ?? 10_000;
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);

  try {
    const res = await fetch(url, {
      method: args.method,
      headers: { "Content-Type": "application/json" },
      body: args.body !== undefined ? JSON.stringify(args.body) : undefined,
      signal: controller.signal,
    });
    const data = await parseJsonSafe(res);

    if (!res.ok) {
      throw new ApiError({
        message: `${args.method} ${args.path} failed`,
        status: res.status,
        url,
        detail: data,
      });
    }

    return data as TResponse;
  } catch (err) {
    if (err instanceof DOMException && err.name === "AbortError") {
      throw new ApiError({
        message: `${args.method} ${args.path} timed out after ${timeoutMs}ms`,
        status: 408,
        url,
      });
    }
    throw err;
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export function apiGet<TResponse>(path: string, timeoutMs?: number): Promise<TResponse> {
  return apiRequest<TResponse>({ method: "GET", path, timeoutMs });
}

export function apiPost<TResponse, TBody>(path: string, body: TBody, timeoutMs?: number): Promise<TResponse> {
  return apiRequest<TResponse, TBody>({ method: "POST", path, body, timeoutMs });
}