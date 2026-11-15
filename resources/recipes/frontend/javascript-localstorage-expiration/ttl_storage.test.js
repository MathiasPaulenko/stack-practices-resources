import { test } from "node:test";
import assert from "node:assert/strict";
import { TTLStorage } from "./ttl_storage.js";
import { SWRStorage } from "./swr_storage.js";
import { createStorageMock } from "./storage_mock.js";

test("set/get round-trip returns the original value", () => {
    const cache = new TTLStorage("app:", createStorageMock());
    cache.set("users", [{ id: 1, name: "Alice" }], 60000);
    assert.deepEqual(cache.get("users"), [{ id: 1, name: "Alice" }]);
});

test("expired entry returns fallback and deletes itself", () => {
    const cache = new TTLStorage("app:", createStorageMock());
    cache.set("k", "v", -1); // already expired
    assert.equal(cache.get("k", "fallback"), "fallback");
    // Lazy deletion: the key is gone now
    assert.equal(cache.size(), 0);
});

test("cleanup() removes expired keys but keeps fresh and foreign ones", () => {
    const backend = createStorageMock();
    backend.setItem("foreign:key", JSON.stringify({ expiry: 1 })); // not ours
    const cache = new TTLStorage("app:", backend);
    cache.set("old", "x", -1);
    cache.set("fresh", "y", 60000);
    cache.cleanup();
    assert.equal(cache.get("old"), null);
    assert.equal(cache.get("fresh"), "y");
    assert.notEqual(backend.getItem("foreign:key"), null); // untouched
});

test("clearAll() only removes prefixed keys", () => {
    const backend = createStorageMock();
    backend.setItem("someone-else", "data");
    const cache = new TTLStorage("app:", backend);
    cache.set("mine", 1);
    cache.clearAll();
    assert.equal(backend.getItem("app:mine"), null);
    assert.equal(backend.getItem("someone-else"), "data");
});

test("SWR returns fresh, then stale, then expired", () => {
    const swr = new SWRStorage("swr:", createStorageMock());
    // ttl=-10 (already stale), staleMs=200 (still inside stale window)
    swr.set("cfg", { theme: "dark" }, -10, 200);
    let r = swr.get("cfg");
    assert.deepEqual(r, { data: { theme: "dark" }, stale: true, expired: false });
    // past staleUntil → expired and removed
    swr.set("cfg2", 1, -10, -5);
    r = swr.get("cfg2");
    assert.equal(r.expired, true);
});

test("memory fallback kicks in when storage throws", () => {
    const dead = {
        setItem() { throw new Error("denied"); },
        getItem() { return null; },
        removeItem() {},
    };
    const cache = new TTLStorage("app:", dead);
    assert.equal(cache.available, false);
    cache.set("k", "v", 60000);
    assert.equal(cache.get("k"), "v"); // served from Map
});
