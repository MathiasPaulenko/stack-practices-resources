-- Retire old data instantly by detaching the partition
ALTER TABLE orders DETACH PARTITION orders_2023_01;

-- The data is now a standalone table: archive or move it
ALTER TABLE orders_2023_01 SET TABLESPACE archive_tablespace;

-- Or drop it entirely (instant, unlike DELETE)
DROP TABLE orders_2023_01;
