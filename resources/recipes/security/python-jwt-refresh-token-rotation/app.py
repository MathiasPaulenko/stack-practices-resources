"""FastAPI app wiring the TokenManager into login/refresh/logout endpoints.

Run: uvicorn app:app --reload
"""

import secrets

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from token_manager import TokenManager

app = FastAPI()
token_manager = TokenManager(secret_key=secrets.token_urlsafe(32))
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Dependency to extract and verify the access token."""
    payload = token_manager.verify_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload


@app.post("/auth/login")
def login(user_id: str = "user123"):
    """Login endpoint — returns access and refresh tokens."""
    pair = token_manager.generate_tokens(user_id)
    return {
        "access_token": pair.access_token,
        "refresh_token": pair.refresh_token,
        "token_type": "Bearer",
        "expires_in": token_manager.access_token_ttl,
    }


@app.post("/auth/refresh")
def refresh(refresh_token: str):
    """Refresh endpoint — rotate refresh token and issue a new access token."""
    pair = token_manager.rotate_refresh_token(refresh_token)
    if pair is None:
        raise HTTPException(status_code=401, detail="Invalid or reused refresh token")
    return {
        "access_token": pair.access_token,
        "refresh_token": pair.refresh_token,
        "token_type": "Bearer",
        "expires_in": token_manager.access_token_ttl,
    }


@app.post("/auth/logout")
def logout(refresh_token: str):
    """Logout endpoint — revoke the refresh token."""
    success = token_manager.revoke_refresh_token(refresh_token)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid refresh token")
    return {"message": "Logged out successfully"}


@app.get("/protected")
def protected_route(user: dict = Depends(get_current_user)):
    """Protected route requiring a valid access token."""
    return {"user_id": user["sub"], "message": "Access granted"}
