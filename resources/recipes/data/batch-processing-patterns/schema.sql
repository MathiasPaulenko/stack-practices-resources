-- Schema for reliable batch job tracking (PostgreSQL).
-- Companion to https://stackpractices.com/recipes/batch-processing-patterns/

-- Idempotent run tracking: skip work that already completed.
CREATE TABLE job_runs (
    job_id VARCHAR(64) PRIMARY KEY,
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('running', 'completed', 'failed')),
    checksum VARCHAR(64)
);

-- Resume point for long-running jobs.
CREATE TABLE job_checkpoints (
    job_id VARCHAR(64),
    batch_number INT,
    status VARCHAR(20),
    PRIMARY KEY (job_id, batch_number)
);

-- High-water mark for incremental loads.
CREATE TABLE job_watermarks (
    job_id VARCHAR(64) PRIMARY KEY,
    last_processed_id BIGINT,
    last_processed_at TIMESTAMP
);

-- Permanently failed items, kept for manual inspection and reprocessing.
CREATE TABLE dead_letters (
    id SERIAL PRIMARY KEY,
    job_id VARCHAR(64),
    item JSONB,
    error TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Source vs target comparisons after each batch.
CREATE TABLE reconciliation_results (
    id SERIAL PRIMARY KEY,
    job_id VARCHAR(64),
    batch_id INT,
    source_count BIGINT,
    target_count BIGINT,
    variance NUMERIC,
    status VARCHAR(20),
    checked_at TIMESTAMP DEFAULT NOW()
);
