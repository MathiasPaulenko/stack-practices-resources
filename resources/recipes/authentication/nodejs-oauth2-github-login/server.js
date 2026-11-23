// Manual GitHub OAuth2 authorization code flow in Express, from the
// StackPractices nodejs-oauth2-github-login recipe.
//
// For local development without a real GitHub OAuth App, run the bundled
// github-stub.js first and point GITHUB_WEB / GITHUB_API at it (see README).

const express = require("express");
const session = require("express-session");
const crypto = require("crypto");

function createApp(options = {}) {
    const githubWeb = options.githubWeb || process.env.GITHUB_WEB || "https://github.com";
    const githubApi = options.githubApi || process.env.GITHUB_API || "https://api.github.com";

    const app = express();

    app.use(session({
        secret: process.env.SESSION_SECRET || "session-secret",
        resave: false,
        saveUninitialized: false
    }));

    const GITHUB_CLIENT_ID = process.env.GITHUB_CLIENT_ID || "demo-client-id";
    const GITHUB_CLIENT_SECRET = process.env.GITHUB_CLIENT_SECRET || "demo-client-secret";
    const REDIRECT_URI = process.env.REDIRECT_URI || "http://localhost:3000/auth/github/callback";

    app.get("/", (req, res) => {
        res.send('<a href="/auth/github">Login with GitHub</a>');
    });

    app.get("/login", (req, res) => {
        const note = req.query.error ? ` (${req.query.error})` : "";
        res.status(401).send(`Login required${note}`);
    });

    app.get("/auth/github", (req, res) => {
        const state = crypto.randomUUID();
        req.session.oauthState = state;

        const params = new URLSearchParams({
            client_id: GITHUB_CLIENT_ID,
            redirect_uri: REDIRECT_URI,
            scope: "user:email",
            state: state
        });

        res.redirect(`${githubWeb}/login/oauth/authorize?${params}`);
    });

    app.get("/auth/github/callback", async (req, res) => {
        const { code, state, error } = req.query;

        // The user denied the authorization request on GitHub
        if (error === "access_denied") {
            return res.redirect("/login?error=denied");
        }

        if (!state || state !== req.session.oauthState) {
            return res.status(403).json({ error: "Invalid state parameter" });
        }

        delete req.session.oauthState;

        try {
            const tokenResponse = await fetch(`${githubWeb}/login/oauth/access_token`, {
                method: "POST",
                headers: { "Content-Type": "application/json", Accept: "application/json" },
                body: JSON.stringify({
                    client_id: GITHUB_CLIENT_ID,
                    client_secret: GITHUB_CLIENT_SECRET,
                    code: code,
                    redirect_uri: REDIRECT_URI
                })
            });
            const { access_token: accessToken } = await tokenResponse.json();

            const auth = { headers: { Authorization: `Bearer ${accessToken}` } };
            const userResponse = await fetch(`${githubApi}/user`, auth);
            const userData = await userResponse.json();

            const emailsResponse = await fetch(`${githubApi}/user/emails`, auth);
            const emails = await emailsResponse.json();
            const primaryEmail = emails.find(e => e.primary)?.email;

            req.session.user = {
                id: userData.id,
                username: userData.login,
                name: userData.name,
                email: primaryEmail,
                avatar: userData.avatar_url,
                accessToken: accessToken
            };

            res.redirect("/profile");
        } catch (err) {
            res.status(500).json({ error: "OAuth callback failed" });
        }
    });

    app.get("/auth/logout", (req, res) => {
        req.session.destroy(() => {
            res.redirect("/");
        });
    });

    app.get("/profile", (req, res) => {
        if (!req.session.user) {
            return res.status(401).json({ error: "Not authenticated" });
        }
        res.json({ user: req.session.user });
    });

    return app;
}

if (require.main === module) {
    createApp().listen(3000, () => {
        console.log("Server running on http://localhost:3000");
    });
}

module.exports = { createApp };
