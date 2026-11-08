-- Consent management schema (PostgreSQL).
-- Stores one row per (user, purpose) so every grant/withdrawal is auditable.

CREATE TABLE user_consents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    purpose VARCHAR(50) NOT NULL,  -- 'marketing', 'analytics', 'third_party'
    granted BOOLEAN NOT NULL DEFAULT false,
    granted_at TIMESTAMPTZ,
    withdrawn_at TIMESTAMPTZ,
    ip_address INET,
    user_agent TEXT
);

-- Index for fast DSAR lookups
CREATE INDEX idx_consents_user ON user_consents(user_id);
