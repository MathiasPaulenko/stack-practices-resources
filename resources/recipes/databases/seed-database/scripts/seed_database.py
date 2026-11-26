"""Idempotent database seeding with SQLAlchemy. Aborts in production."""
import os
from sqlalchemy.orm import Session
from app.models import User, Product, Order
from app.database import SessionLocal
from app.core.security import get_password_hash


def seed():
    if os.getenv("ENV") == "production":
        raise RuntimeError("Cannot seed production database")

    db: Session = SessionLocal()
    try:
        if db.query(User).filter(User.email == "admin@example.com").first():
            print("Database already seeded")
            return

        admin = User(
            email="admin@example.com",
            name="Admin User",
            role="admin",
            hashed_password=get_password_hash("changeme"),
        )
        db.add(admin)

        products = [
            Product(sku="SKU-001", name="Wireless Mouse", price=29.99, stock=150),
            Product(sku="SKU-002", name="Keyboard", price=89.99, stock=75),
        ]
        db.add_all(products)
        db.flush()

        db.add(Order(user_id=admin.id, total=119.98, status="completed"))
        db.commit()
        print("Seeding complete")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
