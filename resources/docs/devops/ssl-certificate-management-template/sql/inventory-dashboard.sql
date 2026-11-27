SELECT
  domain_name,
  issuer,
  expiry_date,
  owner_team,
  CASE
    WHEN expiry_date < NOW() + INTERVAL '7 days' THEN 'CRITICAL'
    WHEN expiry_date < NOW() + INTERVAL '30 days' THEN 'WARNING'
    WHEN expiry_date < NOW() + INTERVAL '60 days' THEN 'INFO'
    ELSE 'OK'
  END AS status
FROM certificate_inventory
WHERE expiry_date < NOW() + INTERVAL '90 days'
ORDER BY expiry_date ASC;
