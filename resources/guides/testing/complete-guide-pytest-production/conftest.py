# tests/conftest.py — Production fixture patterns from the pytest guide.
import os
import uuid
import pytest

# --- Scope-correct fixtures ---
@pytest.fixture(scope="session")
def db_url():
    """Each xdist worker gets its own database."""
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "gw0")
    return f"postgresql://localhost/test_db_{worker_id}"

@pytest.fixture(scope="session")
def db(db_url):
    """Session-scoped engine: expensive to create, safe to share."""
    from myapp.db import Database
    db = Database(db_url)
    db.create_tables()
    yield db
    db.drop_tables()

@pytest.fixture(scope="function")
def unique_email():
    """Unique per test — avoids collisions under xdist."""
    return f"test-{uuid.uuid4()}@example.com"

# --- Factory fixture with cleanup ---
@pytest.fixture
def make_order(db):
    """Creates orders with custom data; cleans everything it made."""
    from myapp.models import Order, Product
    created = []

    def _make(**kwargs):
        defaults = {
            "product": Product.create(db, name="Widget", price=10.00),
            "quantity": 1,
            "status": "pending",
        }
        defaults.update(kwargs)
        order = Order.create(db, **defaults)
        created.append(order)
        return order

    yield _make
    for order in created:
        order.delete(db)

# --- Hooks ---
def pytest_runtest_setup(item):
    """Skip DB tests when NO_DB is set."""
    if "requires_db" in item.keywords and os.environ.get("NO_DB"):
        pytest.skip("Database not available in this environment")
