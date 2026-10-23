-- TimescaleDB time-series setup: hypertable + continuous aggregates + retention.
-- Companion to https://stackpractices.com/guides/time-series-database-guide/
-- Run inside PostgreSQL with the timescaledb extension available.

CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE sensor_data (
    time TIMESTAMPTZ NOT NULL,
    sensor_id INT NOT NULL,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION
);

-- Convert to hypertable with 1-day chunks
SELECT create_hypertable('sensor_data', by_range('time', INTERVAL '1 day'));

-- Continuous aggregate for hourly averages
CREATE MATERIALIZED VIEW hourly_avg
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) as bucket,
    sensor_id,
    AVG(temperature) as avg_temp,
    AVG(humidity) as avg_humidity
FROM sensor_data
GROUP BY bucket, sensor_id
WITH NO DATA;

-- Retention policy: drop chunks older than 90 days
SELECT add_retention_policy('sensor_data', INTERVAL '90 days');

-- Refresh policy: keep the aggregate current within a 1-hour lag
SELECT add_continuous_aggregate_policy('hourly_avg',
    start_offset => INTERVAL '3 hours',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour');
