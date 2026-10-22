-- URL shortener analytics: Cassandra table for append-only click events.
-- Write-heavy workload (~100M rows/day), queried per short_code,
-- most recent first — a natural wide-column store fit.

CREATE TABLE click_events (
    short_code text,
    clicked_at timestamp,
    ip_address text,
    user_agent text,
    referrer   text,
    PRIMARY KEY (short_code, clicked_at)
) WITH CLUSTERING ORDER BY (clicked_at DESC);

-- Typical query: last N clicks for a code (dashboard "recent activity").
-- SELECT * FROM click_events WHERE short_code = 'my-link' LIMIT 100;
