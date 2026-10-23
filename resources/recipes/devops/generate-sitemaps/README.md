# Dynamic Sitemap Generator — Companion Files

Runnable code for the recipe
[Generate XML Sitemaps Dynamically](https://stackpractices.com/recipes/generate-sitemaps/)
([versión en español](https://stackpractices.com/es/recipes/generate-sitemaps/)).

## Files

| File | Purpose |
|------|---------|
| `sitemap_flask.py` | Flask: urlset + sitemap index (computed `ceil(total/50000)`) + Redis cache decorator + gzip route |
| `sitemap_express.js` | Express: manual XML building, `escapeXml`, hreflang `<xhtml:link>` annotations |
| `SitemapController.java` | Spring Boot: DOM-based urlset endpoint |
| `robots.txt` | `Sitemap:` directive pointing at the index |

## Usage

```bash
# Flask
pip install flask redis
python sitemap_flask.py          # serves /sitemap.xml, /sitemap-index.xml, /sitemap.xml.gz

# Express
npm install express
node sitemap_express.js          # serves /sitemap.xml, /sitemap-products.xml

# Spring Boot — drop SitemapController.java into your project
```

Replace the demo URL lists / `query_urls_from_db` / `getProducts` with your real data source, then register the sitemap index in Google Search Console.
