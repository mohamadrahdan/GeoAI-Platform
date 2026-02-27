export type HealthResponse = {
  status: "ok";
  core_loaded: boolean;
};

export type PluginsResponse = {
  plugins: unknown[];
};