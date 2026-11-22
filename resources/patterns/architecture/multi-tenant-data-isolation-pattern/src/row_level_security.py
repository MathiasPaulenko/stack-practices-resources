from sqlalchemy import create_engine, Column, String, Integer, text
from sqlalchemy.orm import declarative_base, Session
from contextlib import contextmanager

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(String)

engine = create_engine("postgresql://user:pass@localhost/saas_db")

# Enable RLS at database level. FORCE makes the policy apply to the
# table owner too — without it, the app role can bypass RLS entirely.
with engine.connect() as conn:
    conn.execute(text("ALTER TABLE documents ENABLE ROW LEVEL SECURITY"))
    conn.execute(text("ALTER TABLE documents FORCE ROW LEVEL SECURITY"))
    conn.execute(text("""
        CREATE POLICY tenant_isolation ON documents
        USING (tenant_id = current_setting('app.tenant_id', true)::int)
    """))
    conn.commit()

@contextmanager
def tenant_session(tenant_id: int):
    session = Session(engine)
    try:
        # Scope the tenant GUC to this transaction only. A plain SET would
        # persist on the pooled connection and leak to the next request.
        session.execute(
            text("SELECT set_config('app.tenant_id', :tid, true)"),
            {"tid": str(tenant_id)},
        )
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Usage — tenant 1 can only see their documents
with tenant_session(tenant_id=1) as session:
    docs = session.query(Document).all()  # RLS filters automatically
    print(f"Tenant 1 has {len(docs)} documents")

# Tenant 2 gets a different set
with tenant_session(tenant_id=2) as session:
    docs = session.query(Document).all()
    print(f"Tenant 2 has {len(docs)} documents")
