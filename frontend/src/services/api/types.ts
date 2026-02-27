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

export type DatasetsResponse = {
  datasets: Dataset[];
};