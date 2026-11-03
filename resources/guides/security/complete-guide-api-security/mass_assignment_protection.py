# VULNERABLE: Mass assignment
@app.put("/api/users/{user_id}")
async def update_user(user_id: int, body: dict = Body(...)):
    user = db.query(User).filter(User.id == user_id).first()
    for key, value in body.items():
        setattr(user, key, value)  # Attacker can set role=admin!
    db.commit()
    return user

# SAFE: Explicit field mapping with Pydantic
class UpdateUserRequest(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[str] = Field(default=None, max_length=255)
    bio: Optional[str] = Field(default=None, max_length=500)
    # Note: 'role', 'is_admin', 'password_hash' are NOT included

@app.put("/api/users/{user_id}")
async def update_user(
    user_id: int,
    request: UpdateUserRequest,
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(403, "Access denied")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    # Only update allowed fields that were actually sent
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    return {"id": user.id, "username": user.username}
