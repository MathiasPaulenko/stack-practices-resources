-- Consent tracking schema for GDPR compliance
CREATE TABLE user_consents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  purpose VARCHAR(100) NOT NULL,  -- marketing, analytics, etc
  consent_given BOOLEAN NOT NULL,
  consent_date TIMESTAMP NOT NULL DEFAULT NOW(),
  withdrawal_date TIMESTAMP,
  ip_address VARCHAR(45),
  UNIQUE(user_id, purpose)
);

-- DSAR (Data Subject Access Requests) tracking
CREATE TABLE dsar_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  request_type VARCHAR(50) NOT NULL,  -- access, deletion, portability
  status VARCHAR(20) DEFAULT 'pending',
  requested_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  notes TEXT
);

-- Auto-deletion: inactive users after 2 years
-- Cron job: DELETE FROM users WHERE last_login < NOW() - INTERVAL '2 years';
