# Web Scraping with BeautifulSoup — Companion Code

Runnable companion for the StackPractices recipe
[Extract Data from HTML Pages with Python and BeautifulSoup](https://stackpractices.com/recipes/python-web-scraping-beautifulsoup/).

`scraper.py` consolidates the recipe's snippets into one script: a `Scraper`
class with per-request delay, exponential-backoff retries and connection
pooling via `requests.Session`, plus paginated crawling and CSV/JSON export.

## Usage

```bash
pip install -r requirements.txt
python scraper.py
```

Configure with environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `SCRAPE_URL` | `https://example.com` | Target URL (use `{page}` placeholder for pagination) |
| `LIST_SELECTOR` | `article` | CSS selector for the items to extract |
| `SCRAPE_PAGES` | `1` | Pages to crawl |
| `SCRAPE_DELAY` | `2.0` | Seconds between requests |
| `SCRAPE_UA` | `MyScraper/1.0` | User-Agent header |

Example — crawl 3 pages of a listing:

```bash
SCRAPE_URL="https://example.com/products?page={page}" \
LIST_SELECTOR=".product-card" \
SCRAPE_PAGES=3 \
python scraper.py
```

Results land in `scraped.json` and `scraped.csv`.

Before scraping a real site, check its `robots.txt` and Terms of Service,
and keep the delay respectful.
