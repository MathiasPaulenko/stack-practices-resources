"""Tag-based invalidation: index entries by entity, purge by tag.

Source: https://stackpractices.com/guides/complete-guide-cache-invalidation/
"""
import json


def cache_product_with_tags(r, product):
    cache_key = f"product:{product['id']}"
    r.setex(cache_key, 3600, json.dumps(product))
    r.sadd(f"tag:product:{product['id']}", cache_key)
    r.sadd(f"tag:category:{product['category_id']}", cache_key)
    r.expire(f"tag:product:{product['id']}", 3600)
    r.expire(f"tag:category:{product['category_id']}", 3600)


def invalidate_tag(r, tag: str):
    keys = r.smembers(f"tag:{tag}")
    if keys:
        r.delete(*keys)
    r.delete(f"tag:{tag}")
