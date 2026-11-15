/**
 * TTLStorage — localStorage wrapper with per-key TTL expiration.
 *
 * Works in the browser (window.localStorage) and in Node.js tests by
 * injecting any Web Storage–compatible object (see storage.js for a mock).
 *
 * Entries are stored as JSON: { value: <json-string>, expiry, created }.
 * Expiration is lazy: an entry is deleted the next time get() touches it,
 * or when cleanup() runs — "expired" and "deleted" are different states.
 */
class TTLStorage {
    constructor(prefix = "ttl:", storage = globalThis.localStorage) {
        this.prefix = prefix;
        this.storage = storage;
        // In-memory fallback: private mode / disabled storage
        this.memoryFallback = new Map();
        this.available = this.checkAvailable();
    }

    checkAvailable() {
        if (!this.storage) return false;
        try {
            const probe = this.prefix + "__probe__";
            this.storage.setItem(probe, "1");
            this.storage.removeItem(probe);
            return true;
        } catch (err) {
            return false;
        }
    }

    set(key, value, ttlMs = 300000) {
        const item = {
            value: JSON.stringify(value),
            expiry: Date.now() + ttlMs,
            created: Date.now()
        };

        if (!this.available) {
            this.memoryFallback.set(this.prefix + key, item);
            return true;
        }

        try {
            this.storage.setItem(this.prefix + key, JSON.stringify(item));
            return true;
        } catch (err) {
            if (err.name === "QuotaExceededError") {
                this.cleanup();
                try {
                    this.storage.setItem(this.prefix + key, JSON.stringify(item));
                    return true;
                } catch (err2) {
                    console.error("Storage quota exceeded even after cleanup");
                    return false;
                }
            }
            console.error("Failed to set item:", err);
            return false;
        }
    }

    get(key, fallback = null) {
        const fullKey = this.prefix + key;

        if (!this.available) {
            const item = this.memoryFallback.get(fullKey);
            if (!item) return fallback;
            return Date.now() > item.expiry ? fallback : JSON.parse(item.value);
        }

        const raw = this.storage.getItem(fullKey);
        if (!raw) return fallback;

        try {
            const item = JSON.parse(raw);

            if (Date.now() > item.expiry) {
                this.storage.removeItem(fullKey);
                return fallback;
            }

            return JSON.parse(item.value);
        } catch (err) {
            this.storage.removeItem(fullKey);
            return fallback;
        }
    }

    has(key) {
        return this.get(key, Symbol.for("ttl:miss")) !== Symbol.for("ttl:miss");
    }

    remove(key) {
        if (this.available) this.storage.removeItem(this.prefix + key);
        this.memoryFallback.delete(this.prefix + key);
    }

    cleanup() {
        if (!this.available) return;
        for (const key of Object.keys(this.storage)) {
            if (!key.startsWith(this.prefix)) continue;
            const raw = this.storage.getItem(key);
            if (!raw) continue;

            try {
                const item = JSON.parse(raw);
                if (Date.now() > item.expiry) {
                    this.storage.removeItem(key);
                }
            } catch (err) {
                this.storage.removeItem(key);
            }
        }
    }

    clearAll() {
        for (const key of Object.keys(this.storage)) {
            if (key.startsWith(this.prefix)) this.storage.removeItem(key);
        }
        this.memoryFallback.clear();
    }

    size() {
        return Object.keys(this.storage)
            .filter(k => k.startsWith(this.prefix)).length;
    }
}

export { TTLStorage };
