from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import RedirectResponse
import httpx
import jwt
import time

app = FastAPI()

GOOGLE_CLIENT_ID = "your-client-id"
GOOGLE_CLIENT_SECRET = "your-client-secret"
GOOGLE_REDIRECT_URI = "http://localhost:8000/auth/callback"
GOOGLE_DISCOVERY = "https://accounts.google.com/.well-known/openid-configuration"

async def get_google_discovery():
    async with httpx.AsyncClient() as client:
        resp = await client.get(GOOGLE_DISCOVERY)
        return resp.json()

async def extract_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.split(" ")[1]
    discovery = await get_google_discovery()
    jwks_client = jwt.PyJWKClient(discovery["jwks_uri"])
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        decoded = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=GOOGLE_CLIENT_ID,
        )
        return decoded
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/auth/login")
async def login():
    discovery = await get_google_discovery()
    auth_url = (
        f"{discovery['authorization_endpoint']}"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid email profile"
    )
    return RedirectResponse(auth_url)

@app.get("/auth/callback")
async def callback(code: str):
    discovery = await get_google_discovery()
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            discovery["token_endpoint"],
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        tokens = token_resp.json()

    id_token = tokens.get("id_token")
    jwks_client = jwt.PyJWKClient(discovery["jwks_uri"])
    signing_key = jwks_client.get_signing_key_from_jwt(id_token)
    decoded = jwt.decode(
        id_token,
        signing_key.key,
        algorithms=["RS256"],
        audience=GOOGLE_CLIENT_ID,
    )
    return {
        "user": {
            "email": decoded["email"],
            "name": decoded["name"],
            "sub": decoded["sub"],
        },
        "access_token": tokens["access_token"],
    }

@app.get("/protected")
async def protected(user: dict = Depends(extract_user)):
    return {"message": f"Hello {user['email']}"}

