"""Event-driven CDN invalidation: purge after the write, not before.

Source: https://stackpractices.com/guides/complete-guide-cdn-caching-strategy/
"""
import os
import requests

API_KEY = os.environ.get("FASTLY_API_KEY", "")


def update_product(db_products, product_id: int, data: dict):
    product = db_products.update(product_id, data)   # 1. write first
    requests.post(
        "https://api.fastly.com/purge/{service_id}",
        headers={"Fastly-Key": API_KEY},
        data={"surrogate_keys": [f"product-{product_id}", "products"]},
        timeout=5,
    )                                                 # 2. then purge
    return product
