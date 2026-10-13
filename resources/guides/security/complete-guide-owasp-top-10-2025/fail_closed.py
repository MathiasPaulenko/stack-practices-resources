"""Fail-closed error handling (A10 — Mishandling of Exceptional Conditions)."""

from contextlib import contextmanager


class TransferError(Exception):
    """Expected, safe-to-surface transfer failure."""


class InsufficientFunds(TransferError):
    pass


@contextmanager
def transaction(store: dict):
    """Tiny atomic store: roll back on any exception inside the block."""
    snapshot = {k: dict(v) for k, v in store.items()}
    try:
        yield store
    except Exception:
        store.clear()
        store.update(snapshot)
        raise


def transfer_funds(accounts: dict, from_id: str, to_id: str, amount: float) -> dict:
    """Move funds atomically; expected failures raise typed errors, unexpected ones propagate."""
    try:
        with transaction(accounts):
            sender = accounts.get(from_id)
            if sender is None:
                raise TransferError("sender not found")
            if sender["balance"] < amount:
                raise InsufficientFunds("insufficient funds")
            sender["balance"] -= amount

            receiver = accounts.get(to_id)
            if receiver is None:
                raise TransferError("receiver not found")
            receiver["balance"] += amount
    except TransferError:
        raise  # expected failure — caller maps it to a 4xx
    return {"status": "ok"}
