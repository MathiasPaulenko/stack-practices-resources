-- deprecation-traffic.sql — request volume on deprecated endpoints by
-- client, so you know who still hasn't migrated.
SELECT
    endpoint,
    COUNT(*) AS request_count,
    COUNT(DISTINCT client_id) AS unique_clients,
    MAX(timestamp) AS last_request
FROM api_requests
WHERE endpoint LIKE '/v1/%'
    AND timestamp >= NOW() - INTERVAL '7 days'
GROUP BY endpoint
ORDER BY request_count DESC;
