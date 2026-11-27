-- Keep a shadow copy of the old column for fast rollback
ALTER TABLE customers ADD COLUMN email_shadow VARCHAR(255);
UPDATE customers SET email_shadow = email WHERE email_shadow IS NULL;

-- ... run the main migration (rename/type change) ...

-- Rollback if needed:
UPDATE customers SET email = email_shadow WHERE email IS NULL;

-- After a clean cutover:
ALTER TABLE customers DROP COLUMN email_shadow;
