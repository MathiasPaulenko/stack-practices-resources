from sqlalchemy import text


class AccountQueryService:
    def __init__(self, session_factory):
        self.Session = session_factory

    def get_account(self, account_id: str) -> dict:
        session = self.Session()
        try:
            result = session.execute(
                text(
                    "SELECT id, owner_name, balance, status FROM account_projection WHERE id = :id"
                ),
                {"id": account_id},
            ).fetchone()
            return dict(result._mapping) if result else None
        finally:
            session.close()

    def get_transactions(self, account_id: str, limit: int = 50) -> list:
        session = self.Session()
        try:
            results = session.execute(
                text(
                    """SELECT type, amount, description, timestamp FROM transaction_projection
                       WHERE account_id = :id ORDER BY timestamp DESC LIMIT :lim"""
                ),
                {"id": account_id, "lim": limit},
            ).fetchall()
            return [dict(r._mapping) for r in results]
        finally:
            session.close()

    def get_active_accounts(self) -> list:
        session = self.Session()
        try:
            results = session.execute(
                text(
                    "SELECT id, owner_name, balance, status FROM account_projection WHERE status = 'active'"
                )
            ).fetchall()
            return [dict(r._mapping) for r in results]
        finally:
            session.close()
