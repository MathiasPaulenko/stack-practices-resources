"""Input validation — runnable Pydantic v2 example.

Schema-first validation: declare the shape once, get structured
field-level errors for free.

Run:  python validate_user.py
"""
from pydantic import BaseModel, EmailStr, Field, ValidationError, field_validator


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)
    bio: str | None = Field(default=None, max_length=500)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name cannot be blank")
        return v.strip()


def format_errors(exc: ValidationError) -> list[dict]:
    """Turn ValidationError into field-level error objects for a 400 response."""
    return [
        {"field": ".".join(map(str, e["loc"])), "message": e["msg"], "type": e["type"]}
        for e in exc.errors()
    ]


if __name__ == "__main__":
    # Valid input
    user = UserCreate(name="Ada Lovelace", email="ada@example.com", age=36)
    print("valid:", user.model_dump())

    # Invalid input — all violations at once, not just the first
    try:
        UserCreate(name="  ", email="not-an-email", age=200)
    except ValidationError as e:
        print("invalid:", format_errors(e))
