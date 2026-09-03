# Soft Deletes Companion

Implementations of the soft delete pattern in Python, JavaScript, and Java with tests.

## Files

| File | Language | Description |
|------|----------|-------------|
| `python_soft_deletes.py` | Python | SQLAlchemy SoftDeleteMixin, User/Post models, restore and purge functions |
| `javascript_soft_deletes.js` | JavaScript | Sequelize paranoid models with restore and purge |
| `java_soft_deletes.java` | Java | JPA/Hibernate with @Filter for soft delete filtering |
| `sql_schema.sql` | SQL | PostgreSQL schema with partial unique indexes and audit table |
| `test_soft_deletes.py` | Python | pytest tests for visibility, restore, purge, cascade |
| `test_soft_deletes.js` | JavaScript | Jest tests for visibility, restore, purge |

## Quick Start

### Python

```bash
pip install -r requirements.txt
python python_soft_deletes.py
pytest test_soft_deletes.py -v
```

### JavaScript

```bash
npm install
node javascript_soft_deletes.js
npx jest test_soft_deletes.js
```

### PostgreSQL (Docker)

```bash
docker-compose up -d
psql -h localhost -U demo -d soft_deletes_demo -f sql_schema.sql
```

## Key Features

- `deleted_at` timestamp column (NULL = active)
- `deleted_by` audit column tracking who deleted
- `query_visible()` / `paranoid: true` / `@Filter` for default filtering
- Partial unique indexes (`WHERE deleted_at IS NULL`)
- Restore flow (set `deleted_at = NULL`)
- Purge job with retention window
- Cascade soft delete and restore for related records
- Prometheus metrics for monitoring
