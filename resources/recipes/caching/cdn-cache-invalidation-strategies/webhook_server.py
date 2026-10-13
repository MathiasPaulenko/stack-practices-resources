"""FastAPI webhook that triggers CDN invalidation from CMS events.

Companion code for:
https://stackpractices.com/recipes/cdn-cache-invalidation-strategies/

Run:
    uvicorn webhook_server:app --port 8080

Environment variables:
    WEBHOOK_SECRET          shared secret sent in the POST body
    CLOUDFLARE_ZONE_ID      zone for Cloudflare tag purges
    CLOUDFLARE_API_TOKEN    token with cache purge permission
"""

import os

from fastapi import FastAPI, HTTPException, Request

from cdn_invalidate import invalidate_on_deploy, invalidate_product

app = FastAPI()


@app.post("/webhook/cdn-invalidate")
async def invalidate_webhook(request: Request) -> dict:
    """Handle CMS events: product updates purge tags, deploys purge all."""
    payload = await request.json()
    if payload.get("secret") != os.getenv("WEBHOOK_SECRET"):
        raise HTTPException(status_code=403, detail="invalid secret")

    if payload["type"] == "product_updated":
        result = await invalidate_product(
            payload["product_id"],
            payload["category_id"],
            os.environ["CLOUDFLARE_ZONE_ID"],
            os.environ["CLOUDFLARE_API_TOKEN"],
        )
        return {"status": "purged", "provider_response": result}

    if payload["type"] == "full_deploy":
        await invalidate_on_deploy()
        return {"status": "purged"}

    raise HTTPException(status_code=400, detail="unknown event type")
