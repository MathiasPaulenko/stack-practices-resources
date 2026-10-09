-- Endpoint compliance queries for osquery.
-- Works on Windows, macOS and Linux; osquery tables join to system_info via uuid.
-- Run: osqueryi --json < endpoint-compliance.sql

-- Devices with unencrypted disks
SELECT
  si.hostname,
  de.name AS disk,
  de.encrypted
FROM disk_encryption de
JOIN system_info si ON si.uuid = de.uuid
WHERE de.encrypted = 0;

-- macOS devices with the application firewall off (use windows_firewall on Windows)
SELECT
  si.hostname,
  alf.global_state
FROM alf
JOIN system_info si ON si.uuid = alf.uuid
WHERE alf.global_state = 0;

-- Hosts with no EDR/AV agent process running (CrowdStrike csagent, SentinelOne, Defender)
SELECT DISTINCT si.hostname
FROM system_info si
WHERE si.hostname NOT IN (
  SELECT DISTINCT si2.hostname
  FROM processes p
  JOIN system_info si2 ON si2.uuid = p.uuid
  WHERE p.name LIKE '%csagent%'
     OR p.name LIKE '%SentinelAgent%'
     OR p.name LIKE '%MsMpEng%'
);

-- Removable USB devices currently attached
SELECT
  si.hostname,
  u.vendor,
  u.product,
  u.serial_number
FROM usb_devices u
JOIN system_info si ON si.uuid = u.uuid
WHERE u.removable = 1;
