"""Deprecation signaling with standard headers.

Deprecated endpoints keep working but announce their sunset date
and point clients at the successor version.
"""

from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/v1/users")
async def list_users_v1(response: Response):
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = "Sat, 31 Dec 2026 23:59:59 GMT"
    response.headers["Link"] = '</v2/users>; rel="successor-version"'
    return {"data": [], "cursor": None}
