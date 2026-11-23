// Local GitHub OAuth stub — lets you run the full authorization code flow
// without registering a real GitHub OAuth App.
//
//   node github-stub.js            # stub on :4000
//   GITHUB_WEB=http://localhost:4000 GITHUB_API=http://localhost:4000 node server.js

const express = require("express");

function createStub() {
    const app = express();
    app.use(express.json());
    app.use(express.urlencoded({ extended: false }));

    // Where the user would normally log in and approve the app.
    // The stub just "approves" instantly and echoes the state back.
    app.get("/login/oauth/authorize", (req, res) => {
        const { redirect_uri, state, error } = req.query;
        if (!redirect_uri || !state) {
            return res.status(400).json({ error: "missing redirect_uri or state" });
        }
        if (error === "access_denied") {
            return res.redirect(`${redirect_uri}?error=access_denied&state=${state}`);
        }
        res.redirect(`${redirect_uri}?code=stub-code-${Date.now()}&state=${state}`);
    });

    app.post("/login/oauth/access_token", (req, res) => {
        const { code } = req.body;
        if (!code) {
            return res.status(400).json({ error: "bad_verification_code" });
        }
        res.json({ access_token: "stub-access-token", token_type: "bearer", scope: "user:email" });
    });

    app.get("/user", (req, res) => {
        if (!req.headers.authorization?.startsWith("Bearer ")) {
            return res.status(401).json({ message: "Requires authentication" });
        }
        res.json({
            id: 4242,
            login: "stubuser",
            name: "Stub User",
            avatar_url: "https://example.com/avatar.png"
        });
    });

    app.get("/user/emails", (req, res) => {
        if (!req.headers.authorization?.startsWith("Bearer ")) {
            return res.status(401).json({ message: "Requires authentication" });
        }
        res.json([
            { email: "stub@example.com", primary: true, verified: true },
            { email: "secondary@example.com", primary: false, verified: true }
        ]);
    });

    return app;
}

if (require.main === module) {
    createStub().listen(4000, () => {
        console.log("GitHub stub running on http://localhost:4000");
    });
}

module.exports = { createStub };
