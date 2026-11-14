// Runnable tests with node:test + a real mock server (node:http).
// No external dependencies — run: node --test

import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import http from "node:http";
import { fetchWithRetry } from "./fetch_with_retry.js";
import { FetchWithRetry } from "./fetch_retry_breaker.js";

let server, baseUrl;
let calls = 0;
let plan = () => ({ status: 200, body: { ok: true } });

before(async () => {
    server = http.createServer((req, res) => {
        calls++;
        const { status, body, headers = {} } = plan();
        res.writeHead(status, { "Content-Type": "application/json", ...headers });
        res.end(JSON.stringify(body));
    });
    await new Promise(r => server.listen(0, r));
    baseUrl = `http://127.0.0.1:${server.address().port}`;
});

after(() => server.close());

const tiny = { retries: 3, baseDelay: 1, timeoutMs: 2000 };

test("succeeds after two 503s", async () => {
    calls = 0;
    let n = 0;
    plan = () => (++n < 3 ? { status: 503, body: {} } : { status: 200, body: { ok: true } });
    const res = await fetchWithRetry(`${baseUrl}/data`, {}, tiny);
    assert.equal(res.ok, true);
    assert.equal(calls, 3);
});

test("does not retry a definitive 404", async () => {
    calls = 0;
    plan = () => ({ status: 404, body: {} });
    const res = await fetchWithRetry(`${baseUrl}/missing`, {}, tiny);
    assert.equal(res.status, 404);
    assert.equal(calls, 1);
});

test("honors Retry-After on 429", async () => {
    calls = 0;
    plan = () => ({ status: 429, body: {}, headers: { "Retry-After": "0" } });
    const res = await fetchWithRetry(`${baseUrl}/limited`, {}, tiny);
    assert.equal(res.status, 429); // exhausted retries
    assert.equal(calls, 4);        // 1 + 3 retries
});

test("breaker counts availability failures only", async () => {
    const client = new FetchWithRetry({ retries: 0, baseDelay: 1, timeoutMs: 2000, breakerThreshold: 2 });
    calls = 0;
    plan = () => ({ status: 404, body: {} });
    await client.request(`${baseUrl}/a`);
    await client.request(`${baseUrl}/b`);
    await client.request(`${baseUrl}/c`);
    assert.equal(client.breaker.state, "closed"); // 404s don't trip it

    plan = () => ({ status: 503, body: {} });
    await client.request(`${baseUrl}/d`).catch(() => {});
    await client.request(`${baseUrl}/e`).catch(() => {});
    assert.equal(client.breaker.state, "open");
});
