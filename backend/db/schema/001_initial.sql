-- Datasets
CREATE TABLE IF NOT EXISTS datasets (
  id            TEXT PRIMARY KEY,
  name          TEXT NOT NULL,
  description   TEXT,
  created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Runs (each pipeline execution)
CREATE TABLE IF NOT EXISTS runs (
  id            TEXT PRIMARY KEY,
  dataset_id    TEXT NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
  plugin_name   TEXT NOT NULL,
  status        TEXT NOT NULL,
  params_json   JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_runs_dataset_id ON runs(dataset_id);
CREATE INDEX IF NOT EXISTS idx_runs_status ON runs(status);

-- Results (outputs)
CREATE TABLE IF NOT EXISTS results (
  id             TEXT PRIMARY KEY,
  run_id         TEXT NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
  result_type    TEXT NOT NULL,
  uri            TEXT NOT NULL,
  metrics_json   JSONB,
  footprint_wkt  TEXT,
  footprint_geom geometry(Geometry, 4326),
  created_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_results_run_id ON results(run_id);
CREATE INDEX IF NOT EXISTS idx_results_type ON results(result_type);
CREATE INDEX IF NOT EXISTS idx_results_geom ON results USING GIST (footprint_geom);

-- Feedback (human-in-the-loop corrections)
CREATE TABLE IF NOT EXISTS feedback (
  id              TEXT PRIMARY KEY,
  result_id        TEXT NOT NULL REFERENCES results(id) ON DELETE CASCADE,
  corrected_label  TEXT NOT NULL,
  comment          TEXT,
  created_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_feedback_result_id ON feedback(result_id);
