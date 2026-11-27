-- Automatic partition creation and rotation with pg_partman
CREATE EXTENSION IF NOT EXISTS pg_partman;

SELECT partman.create_parent(
  'public.events',
  'created_at',
  'weekly',
  p_count := 4  -- keep 4 future partitions ready
);

-- Schedule this via cron to create/drop partitions automatically
SELECT partman.run_maintenance_proc();
