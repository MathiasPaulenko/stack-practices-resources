-- Saga state persistence schema (PostgreSQL)
-- From https://stackpractices.com/recipes/saga-pattern-recipe/

CREATE TABLE saga_state (
    saga_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id         UUID NOT NULL,
    saga_type        VARCHAR(100) NOT NULL,
    current_step     VARCHAR(50),
    status           VARCHAR(20) NOT NULL DEFAULT 'STARTED',
    error            TEXT,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at     TIMESTAMPTZ
);

CREATE INDEX idx_saga_status ON saga_state(status);
CREATE INDEX idx_saga_order ON saga_state(order_id);

CREATE TABLE saga_steps (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    saga_id      UUID NOT NULL REFERENCES saga_state(saga_id),
    step_name    VARCHAR(50) NOT NULL,
    step_status  VARCHAR(20) NOT NULL,
    started_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    error        TEXT
);

CREATE INDEX idx_steps_saga ON saga_steps(saga_id);
