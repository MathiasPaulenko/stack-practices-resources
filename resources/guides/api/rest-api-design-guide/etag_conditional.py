"""ETag + conditional requests on a read endpoint.

The client sends If-None-Match with the ETag it cached; when the
resource hasn't changed we answer 304 with no body.
"""

import hashlib
import json

from fastapi import FastAPI, Request, Response

app = FastAPI()
PRODUCT = {"sku": "PROD-001", "name": "Mechanical keyboard", "price": 59.99}


def make_etag(payload: dict) -> str:
    return hashlib.md5(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:12]


@app.get("/v1/products/{sku}")
async def get_product(sku: str, request: Request, response: Response):
    etag = f'"{make_etag(PRODUCT)}"'
    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "private, max-age=60"
    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304)
    return PRODUCT
