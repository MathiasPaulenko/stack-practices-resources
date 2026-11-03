// Cloudflare Worker: normalize the cache key by stripping tracking params.
// Source: https://stackpractices.com/guides/complete-guide-cdn-caching-strategy/

const TRACKING_PARAMS = [
  "utm_source", "utm_medium", "utm_campaign",
  "utm_term", "utm_content", "fbclid", "gclid",
];

addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  for (const param of TRACKING_PARAMS) {
    url.searchParams.delete(param);
  }
  // Normalized URL becomes the cache key
  event.respondWith(fetch(url.toString()));
});
