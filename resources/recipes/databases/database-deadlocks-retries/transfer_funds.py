"""Database deadlock retry example with SQLAlchemy and PostgreSQL."""
import random
import time

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from functools import wraps


def retry_on_deadlock(max_retries=3, base_delay=0.1):
    """Decorator that retries a function on PostgreSQL deadlock."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except OperationalError as e:
                    if "deadlock detected" not in str(e).lower():
                        raise
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


@retry_on_deadlock(max_retries=3)
def transfer_funds(session, from_id, to_id, amount):
    """Transfer funds between two accounts with deadlock-safe ordering."""
    row_ids = sorted([from_id, to_id])
    accounts = session.execute(
        text("SELECT * FROM accounts WHERE id = ANY(:ids) FOR UPDATE"),
        {"ids": row_ids}
    ).fetchall()

    from_acc = next(a for a in accounts if a.id == from_id)
    to_acc = next(a for a in accounts if a.id == to_id)

    from_acc.balance -= amount
    to_acc.balance += amount
    session.commit()


if __name__ == "__main__":
    engine = create_engine("postgresql://user:pass@localhost/mydb")
    Session = sessionmaker(bind=engine)
    session = Session()
    transfer_funds(session, 1, 2, 100)
    print("Transfer completed")
