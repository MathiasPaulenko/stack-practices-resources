// Flow test for server.js — needs no external deps beyond what server.js uses.
// Run: npm install && npm test

const { test } = require("node:test");
const assert = require("node:assert/strict");
const { app, tokenStore } = require("./server");

const post = (base, path, body, token) =>
    fetch(`${base}${path}`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            ...(token ? { authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify(body),
    });

test("login → protected route → rotation → reuse detection → logout", async () => {
    const server = app.listen(0);
    const base = `http://localhost:${server.address().port}`;

    try {
        // Wrong password is rejected
        let res = await post(base, "/auth/login", { username: "admin", password: "wrong" });
        assert.equal(res.status, 401);

        // Login issues both tokens
        res = await post(base, "/auth/login", { username: "admin", password: "admin123" });
        assert.equal(res.status, 200);
        const { accessToken, refreshToken } = await res.json();
        assert.ok(accessToken && refreshToken);

        // Access token opens the protected route; no token gets 401
        res = await fetch(`${base}/api/profile`);
        assert.equal(res.status, 401);
        res = await fetch(`${base}/api/profile`, {
            headers: { authorization: `Bearer ${accessToken}` },
        });
        assert.equal(res.status, 200);
        assert.equal((await res.json()).username, "admin");

        // Refresh rotates: new tokens, old refresh consumed
        res = await post(base, "/auth/refresh", { refreshToken });
        assert.equal(res.status, 200);
        const rotated = await res.json();
        assert.ok(rotated.refreshToken && rotated.refreshToken !== refreshToken);

        // Reusing the consumed token trips reuse detection and kills the family
        res = await post(base, "/auth/refresh", { refreshToken });
        assert.equal(res.status, 401);
        assert.equal((await res.json()).code, "reuse_detected");

        // The legitimately rotated token dies with its family
        res = await post(base, "/auth/refresh", { refreshToken: rotated.refreshToken });
        assert.equal(res.status, 401);

        // Fresh login, then logout burns the refresh token
        res = await post(base, "/auth/login", { username: "admin", password: "admin123" });
        const second = await res.json();
        res = await post(base, "/auth/logout", { refreshToken: second.refreshToken });
        assert.equal(res.status, 200);
        res = await post(base, "/auth/refresh", { refreshToken: second.refreshToken });
        assert.equal(res.status, 401);
    } finally {
        tokenStore.clear();
        server.close();
    }
});
