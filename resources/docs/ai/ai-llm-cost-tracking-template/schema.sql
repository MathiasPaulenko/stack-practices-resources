-- Storage schema for LLM usage tracking (Postgres).
-- Raw per-request log: one row per LLM call.

CREATE TABLE llm_usage (
    id                BIGSERIAL PRIMARY KEY,
    request_id        TEXT NOT NULL,
    ts                TIMESTAMPTZ NOT NULL DEFAULT now(),
    feature           TEXT NOT NULL,
    user_id           TEXT,
    model             TEXT NOT NULL,
    prompt_tokens     INTEGER NOT NULL,
    completion_tokens INTEGER NOT NULL,
    total_cost        NUMERIC(12,6) NOT NULL,
    latency_ms        INTEGER,
    status            TEXT NOT NULL DEFAULT 'success'
);

CREATE INDEX idx_llm_usage_ts_feature ON llm_usage (ts, feature);
CREATE INDEX idx_llm_usage_user       ON llm_usage (user_id, ts);

-- Daily rollup: a nightly job aggregates llm_usage into this table.
-- Dashboards and the monthly report read from here, not from the raw table.

CREATE TABLE llm_usage_daily (
    date         DATE NOT NULL,
    feature      TEXT NOT NULL,
    model        TEXT NOT NULL,
    requests     INTEGER NOT NULL,
    total_tokens BIGINT NOT NULL,
    total_cost   NUMERIC(12,4) NOT NULL,
    unique_users INTEGER,
    PRIMARY KEY (date, feature, model)
);
