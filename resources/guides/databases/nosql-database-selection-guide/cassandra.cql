-- Cassandra data models from the NoSQL selection guide.
-- Companion to https://stackpractices.com/guides/nosql-database-selection-guide/
-- Run with: cqlsh -f cassandra.cql

CREATE KEYSPACE IF NOT EXISTS nosql_examples
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE nosql_examples;

-- Query-first time-series table: last N readings per sensor per day
CREATE TABLE IF NOT EXISTS sensor_readings (
    sensor_id UUID,
    day TEXT,        -- partition key component
    timestamp TIMESTAMP,
    temperature DOUBLE,
    humidity DOUBLE,
    PRIMARY KEY ((sensor_id, day), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

-- Social platform posts, partitioned by user
CREATE TABLE IF NOT EXISTS posts_by_user (
    user_id UUID,
    post_id TIMEUUID,
    content TEXT,
    media_urls LIST<TEXT>,
    created_at TIMESTAMP,
    PRIMARY KEY ((user_id), post_id)
) WITH CLUSTERING ORDER BY (post_id DESC);

-- Sample query: last 100 readings for a sensor today
-- SELECT * FROM sensor_readings
-- WHERE sensor_id = ? AND day = '2024-06-12'
-- LIMIT 100;
