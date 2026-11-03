# VULNERABLE: String concatenation
def get_user_vulnerable(name: str):
    query = f"SELECT * FROM users WHERE name = '{name}'"
    # Attack: name = "'; DROP TABLE users; --"
    return db.execute(query)

# SAFE: Parameterized queries
def get_user_safe(name: str):
    query = "SELECT * FROM users WHERE name = :name"
    return db.execute(query, {"name": name})

# SAFE: ORM with parameterized queries
def get_user_orm(name: str):
    return db.query(User).filter(User.name == name).first()

# SAFE: SQLAlchemy with explicit parameters
from sqlalchemy import text

def search_users(search_term: str):
    query = text("""
        SELECT id, username, email 
        FROM users 
        WHERE username ILIKE :pattern 
        ORDER BY created_at DESC
        LIMIT 50
    """)
    return db.execute(query, {"pattern": f"%{search_term}%"})

# SAFE: Input sanitization for dynamic queries
def safe_order_by(column: str, allowed_columns: set) -> str:
    """Validate column name for ORDER BY clause."""
    if column not in allowed_columns:
        raise ValueError(f"Invalid sort column: {column}")
    return column

# Usage
allowed = {"username", "email", "created_at", "updated_at"}
sort_column = safe_order_by(request.args.get("sort", "created_at"), allowed)
query = f"SELECT * FROM users ORDER BY {sort_column} DESC"
