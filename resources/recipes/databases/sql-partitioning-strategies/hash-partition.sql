-- Hash partitioning: even distribution when there's no natural range
CREATE TABLE user_events (
  id BIGSERIAL,
  user_id BIGINT NOT NULL,
  event_type TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  PRIMARY KEY (id, user_id)
) PARTITION BY HASH (user_id);

CREATE TABLE user_events_p0 PARTITION OF user_events
  FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE user_events_p1 PARTITION OF user_events
  FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE user_events_p2 PARTITION OF user_events
  FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE user_events_p3 PARTITION OF user_events
  FOR VALUES WITH (MODULUS 4, REMAINDER 3);
