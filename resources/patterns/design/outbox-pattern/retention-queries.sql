-- Archive/delete published events older than 7 days
DELETE FROM outbox
WHERE published_at IS NOT NULL
  AND published_at < NOW() - INTERVAL '7 days';

-- Alert source: events stuck unpublished or retrying
SELECT event_type, COUNT(*)
FROM outbox
WHERE published_at IS NULL
  AND (retry_count > 5 OR created_at < NOW() - INTERVAL '1 hour')
GROUP BY event_type;
