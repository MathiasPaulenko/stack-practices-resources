/**
 * SWRStorage — stale-while-revalidate cache on top of localStorage.
 *
 * Each entry has two timestamps:
 *   expiry    — after this, the value is "stale" (serve it, refresh in background)
 *   staleUntil — after this, the entry is dead and gets removed
 *
 * get() always returns { data, stale, expired } so the caller decides
 * what to render and when to refetch.
 */
class SWRStorage {
    constructor(prefix = "swr:", storage = globalThis.localStorage) {
        this.prefix = prefix;
        this.storage = storage;
    }

    set(key, value, ttlMs = 60000, staleMs = 300000) {
        const item = {
            value: JSON.stringify(value),
            expiry: Date.now() + ttlMs,
            staleUntil: Date.now() + ttlMs + staleMs
        };
        this.storage.setItem(this.prefix + key, JSON.stringify(item));
    }

    get(key) {
        const raw = this.storage.getItem(this.prefix + key);
        if (!raw) return { data: null, stale: false, expired: true };

        try {
            const item = JSON.parse(raw);
            const now = Date.now();

            if (now > item.staleUntil) {
                this.storage.removeItem(this.prefix + key);
                return { data: null, stale: false, expired: true };
            }
            if (now > item.expiry) {
                return { data: JSON.parse(item.value), stale: true, expired: false };
            }
            return { data: JSON.parse(item.value), stale: false, expired: false };
        } catch (err) {
            this.storage.removeItem(this.prefix + key);
            return { data: null, stale: false, expired: true };
        }
    }
}

export { SWRStorage };
