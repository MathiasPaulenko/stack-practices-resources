# Web Scraping con BeautifulSoup — Código Complementario

Código ejecutable que acompaña a la receta de StackPractices
[Extrae Datos de Páginas HTML con Python y BeautifulSoup](https://stackpractices.com/es/recipes/python-web-scraping-beautifulsoup/).

`scraper.py` consolida los snippets de la receta en un solo script: una clase
`Scraper` con espera entre peticiones, reintentos con backoff exponencial y
reutilización de conexiones vía `requests.Session`, además de crawling
paginado y exportación a CSV/JSON.

## Uso

```bash
pip install -r requirements.txt
python scraper.py
```

Se configura con variables de entorno:

| Variable | Default | Propósito |
| --- | --- | --- |
| `SCRAPE_URL` | `https://example.com` | URL objetivo (usa `{page}` para paginación) |
| `LIST_SELECTOR` | `article` | Selector CSS de los elementos a extraer |
| `SCRAPE_PAGES` | `1` | Páginas a recorrer |
| `SCRAPE_DELAY` | `2.0` | Segundos entre peticiones |
| `SCRAPE_UA` | `MyScraper/1.0` | Header User-Agent |

Ejemplo — recorrer 3 páginas de un listado:

```bash
SCRAPE_URL="https://example.com/products?page={page}" \
LIST_SELECTOR=".product-card" \
SCRAPE_PAGES=3 \
python scraper.py
```

Los resultados quedan en `scraped.json` y `scraped.csv`.

Antes de scrapear un sitio real, revisa su `robots.txt` y sus términos de
servicio, y mantén una espera respetuosa entre peticiones.
