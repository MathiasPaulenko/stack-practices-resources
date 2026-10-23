"""Flask sitemap generator — urlset, sitemap index, Redis caching, gzip variant.

Requires: flask, redis (caching decorator optional).
Swap `query_urls_from_db` / `total_url_count` for your real data source.
"""

import gzip
import math
import xml.etree.ElementTree as ET
from datetime import datetime
from functools import wraps

import redis
from flask import Flask, Response, request

app = Flask(__name__)
r = redis.Redis(host="localhost", port=6379, db=0)

URLS_PER_SITEMAP = 50_000


def query_urls_from_db():
    return [
        {"loc": "https://example.com/", "lastmod": "2024-06-01", "priority": "1.0"},
        {"loc": "https://example.com/blog/post-1", "lastmod": "2024-06-10", "priority": "0.8"},
        {"loc": "https://example.com/products/item-1", "lastmod": "2024-06-05", "priority": "0.6"},
    ]


def generate_sitemap(urls):
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for url_data in urls:
        url_elem = ET.SubElement(urlset, "url")
        ET.SubElement(url_elem, "loc").text = url_data["loc"]
        ET.SubElement(url_elem, "lastmod").text = url_data["lastmod"]
        ET.SubElement(url_elem, "changefreq").text = url_data.get("changefreq", "weekly")
        ET.SubElement(url_elem, "priority").text = str(url_data.get("priority", "0.5"))
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(urlset, encoding="unicode")


def cache_sitemap(ttl_seconds=3600):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            cache_key = f"sitemap:{request.path}"
            cached = r.get(cache_key)
            if cached:
                return Response(cached, mimetype="application/xml")
            xml = fn(*args, **kwargs)
            r.setex(cache_key, ttl_seconds, xml)
            return Response(xml, mimetype="application/xml")

        return wrapper

    return decorator


@app.route("/sitemap.xml")
@cache_sitemap(ttl_seconds=3600)
def sitemap():
    return Response(generate_sitemap(query_urls_from_db()), mimetype="application/xml")


@app.route("/sitemap-index.xml")
def sitemap_index():
    sitemap_count = math.ceil(total_url_count() / URLS_PER_SITEMAP)
    sitemapindex = ET.Element("sitemapindex", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for i in range(1, sitemap_count + 1):
        elem = ET.SubElement(sitemapindex, "sitemap")
        ET.SubElement(elem, "loc").text = f"https://example.com/sitemap-{i}.xml"
        ET.SubElement(elem, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
    return Response(
        '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(sitemapindex, encoding="unicode"),
        mimetype="application/xml",
    )


def total_url_count():
    return len(query_urls_from_db())


@app.route("/sitemap.xml.gz")
def sitemap_gzipped():
    compressed = gzip.compress(generate_sitemap(query_urls_from_db()).encode("utf-8"))
    return Response(compressed, mimetype="application/gzip")


if __name__ == "__main__":
    app.run(port=5000)
