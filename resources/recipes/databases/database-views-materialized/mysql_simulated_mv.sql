-- MySQL: Simulated Materialized View with Table + Triggers

-- Create the materialized view table
CREATE TABLE mv_daily_signups (
    day DATE PRIMARY KEY,
    signups INT NOT NULL DEFAULT 0
);

DELIMITER //

-- Trigger: increment on insert
CREATE TRIGGER trg_user_insert
AFTER INSERT ON users
FOR EACH ROW
BEGIN
    INSERT INTO mv_daily_signups (day, signups)
    VALUES (DATE(NEW.created_at), 1)
    ON DUPLICATE KEY UPDATE signups = signups + 1;
END //

-- Trigger: decrement on delete
CREATE TRIGGER trg_user_delete
AFTER DELETE ON users
FOR EACH ROW
BEGIN
    UPDATE mv_daily_signups
    SET signups = signups - 1
    WHERE day = DATE(OLD.created_at);
END //

-- Trigger: handle updates (move count between days)
CREATE TRIGGER trg_user_update
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    IF DATE(NEW.created_at) != DATE(OLD.created_at) THEN
        UPDATE mv_daily_signups SET signups = signups - 1 WHERE day = DATE(OLD.created_at);
        INSERT INTO mv_daily_signups (day, signups) VALUES (DATE(NEW.created_at), 1)
        ON DUPLICATE KEY UPDATE signups = signups + 1;
    END IF;
END //

DELIMITER ;

-- Query the simulated materialized view
SELECT * FROM mv_daily_signups
WHERE day >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY day DESC;
