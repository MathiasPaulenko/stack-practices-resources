// Companion for https://stackpractices.com/recipes/nodejs-caching-redis/
// Express + ioredis cache-aside playground with tags, lock and hit-rate metrics.
// Run: docker compose up -d && npm install && node app.js

const express = require("express");
const Redis = require("ioredis");

const app = express();
const redis = new Redis({ host: "localhost", port: 6379 });

let cacheHits = 0;
let cacheMisses = 0;

// --- cache-aside with lock (stampede protection) ---
async function getOrSet(key, fetchFn, ttl = 300) {
    try {
        const cached = await redis.get(key);
        if (cached) {
            cacheHits++;
            return { data: JSON.parse(cached), source: "cache" };
        }
    } catch (err) {
        console.error("Cache read failed:", err.message);
    }

    const lockKey = `lock:${key}`;
    const acquired = await redis.set(lockKey, "1", "EX", 10, "NX");
    if (!acquired) {
        await new Promise((r) => setTimeout(r, 100));
        return getOrSet(key, fetchFn, ttl);
    }

    try {
        cacheMisses++;
        const fresh = await fetchFn();
        await redis.setex(key, ttl, JSON.stringify(fresh));
        return { data: fresh, source: "database" };
    } finally {
        await redis.del(lockKey);
    }
}

// --- tag-based invalidation ---
async function setWithTags(key, data, tags, ttl = 300) {
    const pipeline = redis.pipeline();
    pipeline.setex(key, ttl, JSON.stringify(data));
    for (const tag of tags) {
        pipeline.sadd(`tag:${tag}`, key);
        pipeline.expire(`tag:${tag}`, ttl + 60);
    }
    await pipeline.exec();
}

async function invalidateTag(tag) {
    const keys = await redis.smembers(`tag:${tag}`);
    if (keys.length === 0) return;
    const pipeline = redis.pipeline();
    for (const key of keys) pipeline.del(key);
    pipeline.del(`tag:${tag}`);
    await pipeline.exec();
}

// --- demo routes ---
async function fetchUser(id) {
    await new Promise((r) => setTimeout(r, 150)); // pretend this is a slow query
    return { id, name: "Ada Lovelace", department: "engineering" };
}

app.get("/api/users/:id", async (req, res) => {
    const result = await getOrSet(`user:${req.params.id}`, () =>
        fetchUser(req.params.id)
    );
    res.json(result);
});

app.post("/api/users/:id/refresh", async (req, res) => {
    await invalidateTag("users");
    res.json({ message: "users cache invalidated" });
});

app.get("/metrics", (req, res) => {
    const total = cacheHits + cacheMisses;
    res.json({
        hits: cacheHits,
        misses: cacheMisses,
        hitRate: total ? ((cacheHits / total) * 100).toFixed(1) + "%" : "N/A",
    });
});

app.listen(3000, () => console.log("http://localhost:3000"));
