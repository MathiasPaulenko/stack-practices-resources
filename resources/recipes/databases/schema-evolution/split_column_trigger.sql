-- Split users.full_name into first_name + last_name with a dual-write trigger.

ALTER TABLE users ADD COLUMN first_name VARCHAR(100);
ALTER TABLE users ADD COLUMN last_name VARCHAR(100);

CREATE OR REPLACE FUNCTION split_name() RETURNS TRIGGER AS $$
BEGIN
  IF NEW.first_name IS DISTINCT FROM OLD.first_name
     OR NEW.last_name IS DISTINCT FROM OLD.last_name THEN
    NEW.full_name := NEW.first_name || ' ' || NEW.last_name;
  ELSIF NEW.full_name IS DISTINCT FROM OLD.full_name THEN
    NEW.first_name := split_part(NEW.full_name, ' ', 1);
    NEW.last_name := split_part(NEW.full_name, ' ', 2);
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_split_name
BEFORE INSERT OR UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION split_name();

UPDATE users
SET first_name = split_part(full_name, ' ', 1),
    last_name = split_part(full_name, ' ', 2)
WHERE first_name IS NULL AND full_name IS NOT NULL;
