// sw.js — precache + cache-first + offline fallback + background sync replay
importScripts("/db.js");

const CACHE_NAME = "sw-offline-demo-v1";
const STATIC_ASSETS = [
    "/",
    "/index.html",
    "/styles.css",
    "/main.js",
    "/db.js",
    "/offline.html"
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(STATIC_ASSETS))
            .then(() => self.skipWaiting())
    );
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys()
            .then((keys) => Promise.all(
                keys
                    .filter((key) => key !== CACHE_NAME)
                    .map((key) => caches.delete(key))
            ))
            .then(() => self.clients.claim())
    );
});

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;

    event.respondWith(
        caches.match(event.request).then((cached) => {
            if (cached) return cached;

            return fetch(event.request)
                .then((response) => {
                    if (!response || response.status !== 200) return response;

                    const clone = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, clone);
                    });

                    return response;
                })
                .catch(() => {
                    if (event.request.mode === "navigate") {
                        return caches.match("/offline.html");
                    }
                    return Response.error();
                });
        })
    );
});

self.addEventListener("sync", (event) => {
    if (event.tag === "submit-form") {
        event.waitUntil(replayFormSubmission());
    }
});

async function replayFormSubmission() {
    const stored = await getStoredFormData();
    for (const data of stored) {
        const res = await fetch("/api/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        await removeStoredFormData(data.id);
    }
}
