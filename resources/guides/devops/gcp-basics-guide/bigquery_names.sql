-- BigQuery public-dataset query from the GCP Basics guide.
-- Top female first names in US birth records (1910–2013).
-- Reminder: SELECT only the columns you need — you pay per TiB scanned.

SELECT
  name,
  SUM(number) AS total_births
FROM `bigquery-public-data.usa_names.usa_1910_2013`
WHERE gender = 'F'
GROUP BY name
ORDER BY total_births DESC
LIMIT 10;
