# Generador de Sitemaps Dinámico — Archivos del Companion

Código ejecutable de la receta
[Generar Sitemaps XML Dinámicamente](https://stackpractices.com/es/recipes/generate-sitemaps/)
([English version](https://stackpractices.com/recipes/generate-sitemaps/)).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `sitemap_flask.py` | Flask: urlset + índice de sitemaps (`ceil(total/50000)` calculado) + decorador de caché Redis + ruta gzip |
| `sitemap_express.js` | Express: construcción manual de XML, `escapeXml`, anotaciones `<xhtml:link>` de hreflang |
| `SitemapController.java` | Spring Boot: endpoint de urlset basado en DOM |
| `robots.txt` | Directiva `Sitemap:` apuntando al índice |

## Uso

```bash
# Flask
pip install flask redis
python sitemap_flask.py          # sirve /sitemap.xml, /sitemap-index.xml, /sitemap.xml.gz

# Express
npm install express
node sitemap_express.js          # sirve /sitemap.xml, /sitemap-products.xml

# Spring Boot — suelta SitemapController.java en tu proyecto
```

Sustituye las listas de demo / `query_urls_from_db` / `getProducts` por tu fuente de datos real, y registra el índice de sitemaps en Google Search Console.
