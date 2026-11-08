"""Pydantic v2 user validation model — run with: python user_model.py

Requires: pip install "pydantic[email]"
"""

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ValidationError,
    field_validator,
)


class User(BaseModel):
    email: EmailStr
    age: int = Field(ge=18, le=120)
    role: str = Field(pattern='^(user|admin|moderator)$')
    tags: list[str] = Field(default_factory=list, max_length=10)

    @field_validator('email')
    @classmethod
    def lowercase_email(cls, v: str) -> str:
        return v.lower()


if __name__ == '__main__':
    user = User(email='ADMIN@EXAMPLE.COM', age=30, role='admin', tags=[])
    print('Valid user:', user.email, user.role)

    try:
        User(email='not-an-email', age=10, role='x')
    except ValidationError as e:
        print('Rejects bad input:', len(e.errors()), 'errors')
