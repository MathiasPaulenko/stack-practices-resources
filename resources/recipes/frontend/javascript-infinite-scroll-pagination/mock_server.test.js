// Tests the pagination contract the client relies on: items, hasMore, edges.
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import { paginate, createServer } from "./mock_server.js";

test("paginate returns slices with hasMore", () => {
    const p1 = paginate({ page: 1, limit: 12 });
    assert.equal(p1.items.length, 12);
    assert.equal(p1.items[0].id, 1);
    assert.equal(p1.hasMore, true);

    const last = paginate({ page: 10, limit: 12 });
    assert.equal(last.items.length, 12);
    assert.equal(last.hasMore, false); // 120 total, 10*12 = 120
});

test("paginate past the end returns empty with hasMore false", () => {
    const over = paginate({ page: 11, limit: 12 });
    assert.equal(over.items.length, 0);
    assert.equal(over.hasMore, false);
});

let server, base;
before(async () => {
    server = createServer();
    await new Promise(r => server.listen(0, r));
    base = `http://127.0.0.1:${server.address().port}`;
});
after(() => server.close());

test("GET /api/posts honors page and limit", async () => {
    const res = await fetch(`${base}/api/posts?page=2&limit=5`);
    const data = await res.json();
    assert.equal(data.items.length, 5);
    assert.equal(data.items[0].id, 6);
    assert.equal(data.hasMore, true);
    assert.equal(data.total, 120);
});

test("GET /demo.html serves the page", async () => {
    const res = await fetch(`${base}/demo.html`);
    const html = await res.text();
    assert.match(html, /Infinite Scroll Demo/);
});
