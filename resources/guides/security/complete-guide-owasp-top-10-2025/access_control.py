"""Server-side access control helpers (A01). Framework-agnostic core + FastAPI adapters."""

from functools import wraps
from typing import Any, Callable


class AccessDenied(Exception):
    """Raised when a principal lacks permission for an action."""


def require_ownership(get_owner_id: Callable[[Any], int]):
    """Decorator: the current user's id must match the resource owner id (or be admin)."""
    def decorator(func):
        @wraps(func)
        def wrapper(current_user: dict, *args, **kwargs):
            owner_id = get_owner_id(*args, **kwargs)
            if current_user["id"] != owner_id and current_user.get("role") != "admin":
                raise AccessDenied("You can only access your own resources")
            return func(current_user, *args, **kwargs)
        return wrapper
    return decorator


def require_role(required_role: str):
    """Decorator: the current user must hold the required role."""
    def decorator(func):
        @wraps(func)
        def wrapper(current_user: dict, *args, **kwargs):
            if current_user.get("role") != required_role:
                raise AccessDenied("Insufficient permissions")
            return func(current_user, *args, **kwargs)
        return wrapper
    return decorator


# --- FastAPI adapter (uncomment with a real app) -----------------------------------
# from fastapi import Depends, HTTPException
#
# def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
#     user = decode_jwt(token)
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     return user
#
# def fastapi_require_role(required_role: str):
#     def role_checker(current_user: dict = Depends(get_current_user)):
#         if current_user["role"] != required_role:
#             raise HTTPException(status_code=403, detail="Insufficient permissions")
#         return current_user
#     return role_checker
