export type HealthResponse = {
  status: "ok";
  core_loaded: boolean;
};

// export type PluginsResponse = {
//   plugins: unknown[];
// };

export type PluginMeta = {
  name: string;
  version: string;
  description?: string;
};

export type PluginsResponse = {
  plugins: string[];
};

export type Dataset = {
  id: string;
  name: string;
  created_at: string;
};

export type DatasetsResponse = Dataset[];

export type InferenceRequest = {
  plugin_name: string;
  dataset_id: string;
  parameters?: Record<string, unknown>;
};

export type InferenceResponse = {
  run_id: string;
  status: "success" | "failed";
  plugin_name: string;
  metrics?: Record<string, number>;
  result_path?: string;
  artifacts?: string[];
};