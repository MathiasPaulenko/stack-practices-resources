"""FastAPI example — code-first OpenAPI generation.

Run: uvicorn python_fastapi:app --reload
Then open http://localhost:8000/docs (Swagger UI) or /redoc (Redoc).
"""

from fastapi import FastAPI

app = FastAPI(title="Book API", version="1.0.0")


@app.get("/books/{book_id}", tags=["books"])
def get_book(book_id: int):
    """Retrieve a book by its ID."""
    return {"id": book_id, "title": "Clean Code"}


# FastAPI auto-generates /openapi.json and /docs (Swagger UI)
