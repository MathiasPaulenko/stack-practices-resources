const { test, before, after } = require("node:test");
const assert = require("node:assert");
const { createApp } = require("./server");
const { createStub } = require("./github-stub");

const STUB_PORT = 4100;
const APP_PORT = 4101;
const APP_BASE = `http://127.0.0.1:${APP_PORT}`;

let stubServer;
let appServer;

// Minimal cookie jar so requests behave like a browser session
function withCookies(jar, response) {
    for (const cookie of response.headers.getSetCookie()) {
        jar = cookie.split(";")[0];
    }
    return jar;
}

async function get(url, jar) {
    const res = await fetch(url, {
        redirect: "manual",
        headers: jar ? { cookie: jar } : {}
    });
    return { res, jar: withCookies(jar, res) };
}

before(async () => {
    process.env.REDIRECT_URI = `${APP_BASE}/auth/github/callback`;
    await new Promise(resolve => {
        stubServer = createStub().listen(STUB_PORT, resolve);
    });
    await new Promise(resolve => {
        appServer = createApp({
            githubWeb: `http://127.0.0.1:${STUB_PORT}`,
            githubApi: `http://127.0.0.1:${STUB_PORT}`
        }).listen(APP_PORT, resolve);
    });
});

after(() => {
    stubServer.close();
    appServer.close();
});

test("full OAuth2 flow: authorize → callback → profile → logout", async () => {
    let jar = "";

    // 1. Unauthenticated profile is rejected
    let r = await get(`${APP_BASE}/profile`, jar);
    assert.equal(r.res.status, 401);
    jar = r.jar;

    // 2. /auth/github redirects to the provider with a state
    r = await get(`${APP_BASE}/auth/github`, jar);
    jar = r.jar;
    assert.equal(r.res.status, 302);
    const authorizeUrl = new URL(r.res.headers.get("location"));
    assert.equal(authorizeUrl.pathname, "/login/oauth/authorize");
    const state = authorizeUrl.searchParams.get("state");
    assert.ok(state);

    // 3. A forged state is rejected before any token exchange
    const forged = await get(`${APP_BASE}/auth/github/callback?code=x&state=forged`, jar);
    assert.equal(forged.res.status, 403);

    // 4. The provider "approves" and redirects back with code + state
    r = await get(authorizeUrl.href, "");
    assert.equal(r.res.status, 302);
    const callbackUrl = new URL(r.res.headers.get("location"));
    assert.ok(callbackUrl.searchParams.get("code"));
    assert.equal(callbackUrl.searchParams.get("state"), state);

    // 5. The app exchanges the code and creates the session
    r = await get(`${APP_BASE}${callbackUrl.pathname}${callbackUrl.search}`, jar);
    jar = r.jar;
    assert.equal(r.res.status, 302);
    assert.equal(r.res.headers.get("location"), "/profile");

    // 6. Profile now returns the stub user
    r = await get(`${APP_BASE}/profile`, jar);
    jar = r.jar;
    assert.equal(r.res.status, 200);
    const body = await r.res.json();
    assert.equal(body.user.username, "stubuser");
    assert.equal(body.user.email, "stub@example.com");

    // 7. Logout destroys the session
    r = await get(`${APP_BASE}/auth/logout`, jar);
    jar = r.jar;
    assert.equal(r.res.status, 302);
    r = await get(`${APP_BASE}/profile`, jar);
    assert.equal(r.res.status, 401);
});

test("access_denied from the provider goes back to login", async () => {
    let jar = "";
    let r = await get(`${APP_BASE}/auth/github`, jar);
    jar = r.jar;
    const authorizeUrl = new URL(r.res.headers.get("location"));
    authorizeUrl.searchParams.set("error", "access_denied");

    r = await get(authorizeUrl.href, "");
    const callbackUrl = new URL(r.res.headers.get("location"));
    r = await get(`${APP_BASE}${callbackUrl.pathname}${callbackUrl.search}`, jar);
    assert.equal(r.res.status, 302);
    assert.equal(r.res.headers.get("location"), "/login?error=denied");
});
