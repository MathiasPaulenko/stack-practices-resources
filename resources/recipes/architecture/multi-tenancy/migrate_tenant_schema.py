from sqlalchemy import MetaData, create_engine, text


def migrate_tenant_schema(tenant_id: str):
    # Identifiers can't be parameterized — validate before interpolating
    if not tenant_id.replace('_', '').isalnum():
        raise ValueError(f'invalid tenant id: {tenant_id}')
    engine = create_engine("postgresql://user:pass@localhost/db")
    with engine.begin() as conn:
        # SQLAlchemy 2.x requires text() for raw SQL strings
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS tenant_{tenant_id}"))
        metadata = MetaData(schema=f"tenant_{tenant_id}")
        metadata.create_all(conn)
