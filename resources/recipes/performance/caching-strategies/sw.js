// Service Worker: offline-first caching for an SPA shell.
// Register from the page: navigator.serviceWorker.register('/sw.js')
const CACHE_NAME = 'app-v1';
const urlsToCache = ['/static/app.js', '/static/styles.css', '/api/config'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('activate', (event) => {
  // Drop caches from previous versions
  event.waitUntil(
    caches.keys().then((names) =>
      Promise.all(names.filter((n) => n !== CACHE_NAME).map((n) => caches.delete(n)))
    )
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      // Cache-first: serve the cached copy or go to the network
      return response || fetch(event.request);
    })
  );
});
