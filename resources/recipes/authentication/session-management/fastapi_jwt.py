"""Stateless alternative: JWT auth with FastAPI.

For browser apps prefer cookie sessions; use this when the client is a
mobile app or another service. Requires: fastapi, python-jose, uvicorn.
Run: `uvicorn fastapi_jwt:app --reload`.
"""

from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

SECRET_KEY = "your-secret-key"  # Load from env in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception


@app.post("/token")
def token() -> dict:
    # Demo only — authenticate the user first in production.
    return {"access_token": create_access_token({"sub": "user-1"})}


@app.get("/me")
def me(user_id: str = Depends(get_current_user)) -> dict:
    return {"user_id": user_id}
