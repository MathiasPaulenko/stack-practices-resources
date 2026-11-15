/**
 * Minimal Web Storage–compatible mock for Node.js tests and demos.
 * Implements the surface TTLStorage/SWRStorage use:
 * setItem, getItem, removeItem, key enumeration via Object.keys semantics.
 */
export function createStorageMock(quotaBytes = Infinity) {
    const data = new Map();
    let used = 0;

    const storage = {
        setItem(key, value) {
            key = String(key); value = String(value);
            const prev = data.get(key);
            const delta = (value.length - (prev ? prev.length : 0)) * 2; // UTF-16
            if (used + delta > quotaBytes) {
                const err = new Error("QuotaExceededError");
                err.name = "QuotaExceededError";
                throw err;
            }
            used += delta;
            data.set(key, value);
        },
        getItem(key) {
            return data.has(String(key)) ? data.get(String(key)) : null;
        },
        removeItem(key) {
            const prev = data.get(String(key));
            if (prev !== undefined) used -= prev.length * 2;
            data.delete(String(key));
        },
        clear() { data.clear(); used = 0; },
        get length() { return data.size; }
    };

    // Object.keys() compatibility: real Web Storage exposes keys as own props.
    return new Proxy(storage, {
        ownKeys() { return [...data.keys()]; },
        getOwnPropertyDescriptor() {
            return { enumerable: true, configurable: true };
        },
        get(target, prop) {
            return target[prop];
        }
    });
}
