import { env } from "@/app/config/env";

export function HomePage() {
  return (
    <div style={{ padding: 16 }}>
      <h1>GeoAI Platform</h1>
      <p>Frontend skeleton is ready.</p>
      <p>
        API Base URL: <code>{env.apiBaseUrl}</code>
      </p>
    </div>
  );
}