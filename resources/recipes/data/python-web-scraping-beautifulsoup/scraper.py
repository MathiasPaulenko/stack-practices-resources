"""Rate-limited HTML scraper built on requests + BeautifulSoup.

Fetches pages politely (delay between requests, exponential-backoff
retries, descriptive User-Agent) and extracts structured data via
CSS selectors. Exports results to CSV or JSON.

Configure the target with env vars and run:

    pip install -r requirements.txt
    SCRAPE_URL=https://example.com LIST_SELECTOR="article" python scraper.py
"""

from __future__ import annotations

import csv
import json
import os
import sys
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

USER_AGENT = os.environ.get("SCRAPE_UA", "Mozilla/5.0 (compatible; MyScraper/1.0)")


class Scraper:
    """Polite scraper: per-request delay plus retries with backoff."""

    def __init__(self, delay: float = 1.0, max_retries: int = 3, timeout: int = 10):
        self.delay = delay
        self.max_retries = max_retries
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        self._last_request = 0.0

    def fetch(self, url: str) -> BeautifulSoup:
        """Fetch a URL and return its parsed BeautifulSoup tree."""
        elapsed = time.time() - self._last_request
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                self._last_request = time.time()
                return BeautifulSoup(response.text, "html.parser")
            except requests.RequestException as exc:
                if attempt == self.max_retries - 1:
                    raise
                wait = 2**attempt
                print(f"Retry {attempt + 1} in {wait}s: {exc}")
                time.sleep(wait)

        raise AssertionError("unreachable")  # loop either returns or raises

    def fetch_text(self, url: str, selector: str, limit: int = 10) -> list[dict]:
        """Fetch a page and extract text + href from each matched element."""
        soup = self.fetch(url)
        items = []
        for el in soup.select(selector)[:limit]:
            link = el.find("a")
            items.append(
                {
                    "text": el.get_text(strip=True),
                    "url": urljoin(url, link.get("href", "")) if link else "",
                }
            )
        return items

    def crawl_paginated(
        self,
        url_template: str,
        item_selector: str,
        max_pages: int = 3,
    ) -> list[dict]:
        """Crawl a paginated listing, extracting items from each page."""
        all_items: list[dict] = []
        for page in range(1, max_pages + 1):
            url = url_template.format(page=page)
            try:
                items = self.fetch_text(url, item_selector)
            except requests.RequestException as exc:
                print(f"Page {page} failed after {self.max_retries} retries: {exc}")
                break
            if not items:
                print(f"Page {page}: no items, stopping")
                break
            all_items.extend(items)
            print(f"Scraped page {page}: {len(items)} items")
        return all_items


def export_csv(items: list[dict], filename: str) -> None:
    """Write a list of dicts to CSV."""
    if not items:
        return
    with open(filename, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=items[0].keys())
        writer.writeheader()
        writer.writerows(items)


def export_json(items: list[dict], filename: str) -> None:
    """Write a list of dicts to JSON."""
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(items, fh, indent=2, ensure_ascii=False)


def main() -> int:
    url = os.environ.get("SCRAPE_URL", "https://example.com")
    selector = os.environ.get("LIST_SELECTOR", "article")
    pages = int(os.environ.get("SCRAPE_PAGES", "1"))
    delay = float(os.environ.get("SCRAPE_DELAY", "2.0"))

    scraper = Scraper(delay=delay)
    if pages > 1:
        results = scraper.crawl_paginated(url, selector, max_pages=pages)
    else:
        results = scraper.fetch_text(url, selector)

    print(f"\n{len(results)} items scraped")
    export_json(results, "scraped.json")
    export_csv(results, "scraped.csv")
    print("Wrote scraped.json and scraped.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
