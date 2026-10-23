-- IoT monitoring scenario: 10,000 sensors, ~100K readings/sec.
-- Companion to https://stackpractices.com/guides/time-series-database-guide/

CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE sensor_readings (
    time TIMESTAMPTZ NOT NULL,
    sensor_id INT NOT NULL,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    pressure DOUBLE PRECISION,
    battery_level DOUBLE PRECISION
);

-- Hypertable with 6-hour chunks, aligned with the common query windows
SELECT create_hypertable('sensor_readings',
    'time', chunk_time_interval => INTERVAL '6 hours');

CREATE INDEX idx_sensor_time ON sensor_readings(sensor_id, time DESC);

-- Synthetic ingest batch (10,000 points)
INSERT INTO sensor_readings (time, sensor_id, temperature, humidity, pressure)
SELECT
    NOW() - (generate_series(1, 10000) * INTERVAL '1 second'),
    (random() * 10000)::INT,
    20 + random() * 15,
    40 + random() * 20,
    1013 + random() * 10;

-- Continuous aggregates: 1-minute (real-time dashboards) and 1-hour (history)
CREATE MATERIALIZED VIEW sensor_1m
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 minute', time) AS bucket,
    sensor_id,
    AVG(temperature) AS avg_temp,
    MAX(temperature) AS max_temp,
    MIN(temperature) AS min_temp,
    AVG(humidity) AS avg_humidity
FROM sensor_readings
GROUP BY bucket, sensor_id
WITH NO DATA;

CREATE MATERIALIZED VIEW sensor_1h
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    sensor_id,
    AVG(temperature) AS avg_temp,
    MAX(temperature) AS max_temp,
    MIN(temperature) AS min_temp,
    COUNT(*) AS sample_count
FROM sensor_readings
GROUP BY bucket, sensor_id
WITH NO DATA;

-- Tiered retention: raw 7 days, 1-min 90 days, 1-hour 5 years
SELECT add_retention_policy('sensor_readings', INTERVAL '7 days');
SELECT add_retention_policy('sensor_1m', INTERVAL '90 days');
SELECT add_retention_policy('sensor_1h', INTERVAL '5 years');

-- Latest reading per sensor
SELECT DISTINCT ON (sensor_id)
    sensor_id, time, temperature, humidity
FROM sensor_readings
ORDER BY sensor_id, time DESC;

-- Alert: sensors with temp > 35C in last 10 minutes
SELECT sensor_id, MAX(temperature) AS max_temp
FROM sensor_readings
WHERE time > NOW() - INTERVAL '10 minutes'
  AND temperature > 35
GROUP BY sensor_id
ORDER BY max_temp DESC;

-- 24h trend for one sensor (from aggregate)
SELECT bucket, sensor_id, avg_temp, max_temp, min_temp
FROM sensor_1h
WHERE bucket > NOW() - INTERVAL '24 hours'
  AND sensor_id = 42
ORDER BY bucket;
