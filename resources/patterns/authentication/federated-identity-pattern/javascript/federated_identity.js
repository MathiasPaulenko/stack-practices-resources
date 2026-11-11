const express = require("express");
const { auth } = require("express-openid-connect");

const app = express();

app.use(
    auth({
        issuerBaseURL: "https://accounts.google.com",
        baseURL: "http://localhost:3000",
        clientID: "your-client-id",
        secret: "your-secret-key",
        authRequired: false,
        auth0Logout: true,
        routes: {
            login: "/auth/login",
            callback: "/auth/callback",
            logout: "/auth/logout",
        },
    })
);

app.get("/", (req, res) => {
    if (req.oidc.isAuthenticated()) {
        res.json({
            user: req.oidc.user,
            token: req.oidc.accessToken,
        });
    } else {
        res.json({ message: "Not authenticated. Visit /auth/login" });
    }
});

app.get("/profile", (req, res) => {
    if (!req.oidc.isAuthenticated()) {
        return res.status(401).json({ error: "Unauthorized" });
    }
    res.json({ user: req.oidc.user });
});

app.listen(3000);

