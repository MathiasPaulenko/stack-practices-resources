"""PostgreSQL full-text search with SQLAlchemy 2.x.

Requires: pip install sqlalchemy psycopg2-binary
Start DB:  docker compose up -d postgres
Run:       python full_text_search.py
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, func, text
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)


engine = create_engine("postgresql://user:pass@localhost/db")


def setup() -> None:
    """Create the table, seed rows, and index the tsvector expression."""
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS articles"))
        conn.execute(text("""
            CREATE TABLE articles (
                id SERIAL PRIMARY KEY,
                title TEXT,
                content TEXT
            )
        """))
        conn.execute(text("""
            INSERT INTO articles (title, content) VALUES
            ('Database optimization', 'Indexing strategies for large tables'),
            ('Full-text search', 'Tokenization, stemming, and relevance ranking'),
            ('Query tuning', 'How to read EXPLAIN and fix slow queries')
        """))
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_articles_search
            ON articles USING GIN (to_tsvector('english', title || ' ' || content))
        """))
        conn.commit()


def search(query: str):
    """Ranked search using websearch_to_tsquery (safe for raw user input)."""
    with Session(engine) as session:
        tsquery = func.websearch_to_tsquery("english", query)
        rank = func.ts_rank(
            func.to_tsvector("english", Article.title + " " + Article.content),
            tsquery,
        )
        return (
            session.query(Article.title, rank.label("rank"))
            .filter(
                func.to_tsvector("english", Article.title + " " + Article.content)
                .op("@@")(tsquery)
            )
            .order_by(rank.desc())
            .all()
        )


if __name__ == "__main__":
    setup()
    for q in ["database", "slow queries", '"full-text"']:
        print(f"{q!r} ->")
        for title, rank in search(q):
            print(f"    {rank:.4f}  {title}")
