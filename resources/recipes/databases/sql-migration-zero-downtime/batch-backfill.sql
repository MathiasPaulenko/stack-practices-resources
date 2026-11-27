-- Batched backfill loop with sleep: keeps locks short and replicas calm
DO $$
DECLARE
  batch_count INTEGER := 0;
  rows_updated INTEGER;
BEGIN
  LOOP
    UPDATE customers
    SET email_address = email
    WHERE id IN (
      SELECT id FROM customers
      WHERE email_address IS NULL
      LIMIT 1000
    );
    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    EXIT WHEN rows_updated = 0;
    batch_count := batch_count + 1;
    RAISE NOTICE 'Batch %: updated % rows', batch_count, rows_updated;
    PERFORM pg_sleep(0.1);
  END LOOP;
  RAISE NOTICE 'Backfill complete: % batches', batch_count;
END $$;
