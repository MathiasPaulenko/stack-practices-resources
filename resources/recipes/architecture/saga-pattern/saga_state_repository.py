# Saga state repository (asyncpg): query, update and resume stuck sagas
# From https://stackpractices.com/recipes/saga-pattern-recipe/

import asyncpg
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class SagaStatus(Enum):
    STARTED = "STARTED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    COMPENSATING = "COMPENSATING"
    COMPENSATED = "COMPENSATED"
    FAILED = "FAILED"

@dataclass
class SagaState:
    saga_id: str
    order_id: str
    saga_type: str
    current_step: str
    status: SagaStatus
    error: str | None

class SagaStateRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def create(self, order_id: str, saga_type: str) -> SagaState:
        row = await self.pool.fetchrow(
            """INSERT INTO saga_state (order_id, saga_type, status)
               VALUES ($1, $2, 'STARTED')
               RETURNING saga_id, order_id, saga_type, current_step, status, error""",
            order_id, saga_type
        )
        return SagaState(
            saga_id=str(row['saga_id']),
            order_id=str(row['order_id']),
            saga_type=row['saga_type'],
            current_step=row['current_step'],
            status=SagaStatus(row['status']),
            error=row['error']
        )

    async def update_step(self, saga_id: str, step: str, status: SagaStatus, error: str = None):
        await self.pool.execute(
            """UPDATE saga_state
               SET current_step = $2, status = $3, error = $4, updated_at = NOW()
               WHERE saga_id = $1""",
            saga_id, step, status.value, error
        )

    async def record_step(self, saga_id: str, step_name: str, status: str, error: str = None):
        await self.pool.execute(
            """INSERT INTO saga_steps (saga_id, step_name, step_status, error)
               VALUES ($1, $2, $3, $4)""",
            saga_id, step_name, status, error
        )

    async def get_stuck_sagas(self, older_than_minutes: int = 5) -> list[SagaState]:
        rows = await self.pool.fetch(
            """SELECT * FROM saga_state
               WHERE status IN ('COMPENSATING', 'RUNNING')
               AND updated_at < NOW() - INTERVAL '%s minutes'
               ORDER BY updated_at ASC""",
            older_than_minutes
        )
        return [SagaState(
            saga_id=str(r['saga_id']),
            order_id=str(r['order_id']),
            saga_type=r['saga_type'],
            current_step=r['current_step'],
            status=SagaStatus(r['status']),
            error=r['error']
        ) for r in rows]
