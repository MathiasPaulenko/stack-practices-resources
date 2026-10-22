"""Strawberry + FastAPI GraphQL server from the recipe.

Run:
    pip install fastapi "strawberry-graphql[fastapi]" uvicorn
    uvicorn server:app --reload

Then open http://localhost:8000/graphql for GraphiQL.
"""

import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

BOOKS = [
    {"title": "Clean Code", "author": "Robert C. Martin", "pages": 464},
    {"title": "The Pragmatic Programmer", "author": "Andy Hunt", "pages": 352},
]


@strawberry.type
class Book:
    title: str
    author: str
    pages: int


@strawberry.type
class Query:
    @strawberry.field
    def books(self) -> list[Book]:
        return [Book(**b) for b in BOOKS]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, title: str, author: str, pages: int) -> Book:
        BOOKS.append({"title": title, "author": author, "pages": pages})
        return Book(title=title, author=author, pages=pages)


schema = strawberry.Schema(query=Query, mutation=Mutation)
app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")
