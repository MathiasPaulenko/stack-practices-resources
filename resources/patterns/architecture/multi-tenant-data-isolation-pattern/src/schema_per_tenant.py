import re
from sqlalchemy import create_engine, Column, String, Integer, text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String)

engine = create_engine("postgresql://user:pass@localhost/saas_db")

def tenant_schema(tenant_name: str) -> str:
    # Tenant names are user input — never interpolate them raw into DDL.
    slug = re.sub(r"[^a-z0-9_]", "_", tenant_name.lower())
    return f"tenant_{slug}"

def provision_tenant(tenant_name: str):
    schema = tenant_schema(tenant_name)
    # create_all must run on the same connection that has the search_path
    # set — passing `engine` would create tables in `public` instead.
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
        conn.execute(text(f"SET search_path TO {schema}"))
        Base.metadata.create_all(conn)
        conn.commit()

def get_tenant_engine(tenant_name: str):
    schema = tenant_schema(tenant_name)
    return create_engine(
        "postgresql://user:pass@localhost/saas_db",
        connect_args={"options": f"-csearch_path={schema}"},
    )

# Usage — each tenant gets an isolated schema
provision_tenant("acme")
provision_tenant("globex")

acme_engine = get_tenant_engine("acme")
AcmeSession = sessionmaker(bind=acme_engine)
session = AcmeSession()
docs = session.query(Document).all()
