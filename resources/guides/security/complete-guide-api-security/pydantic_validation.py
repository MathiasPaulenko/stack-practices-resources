from pydantic import BaseModel, Field, field_validator
from typing import Optional

class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_]+$')
    email: str = Field(min_length=5, max_length=255, pattern=r'^[^@]+@[^@]+\.[^@]+$')
    password: str = Field(min_length=12, max_length=128)
    age: int = Field(ge=13, le=120)
    bio: Optional[str] = Field(default=None, max_length=500)
    
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain lowercase")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digits")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v):
            raise ValueError("Password must contain special characters")
        return v

@app.post("/api/users")
async def create_user(request: CreateUserRequest):
    # Pydantic validates automatically — invalid data raises 422
    user = User(
        username=request.username,
        email=request.email,
        password_hash=hash_password(request.password),
        age=request.age,
        bio=request.bio
    )
    db.add(user)
    db.commit()
    return {"id": user.id, "username": request.username}
