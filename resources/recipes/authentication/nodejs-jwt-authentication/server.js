// Express JWT server from the StackPractices nodejs-jwt-authentication recipe.
// Run: npm install && npm start  →  then POST /auth/login with {"username":"admin","password":"admin123"}
// npm test spins the app up on a random port and exercises the full flow.

const express = require("express");
const jwt = require("jsonwebtoken");
const crypto = require("crypto");
const bcrypt = require("bcrypt");

const app = express();
app.use(express.json());

const ACCESS_TOKEN_SECRET = process.env.JWT_ACCESS_SECRET || "access-secret";
const REFRESH_TOKEN_SECRET = process.env.JWT_REFRESH_SECRET || "refresh-secret";
const ISSUER = "stackpractices-demo";
const AUDIENCE = "demo-api";

// Refresh token store: { jti: { userId, token, family, createdAt } }
// In production this lives in Redis keyed by jti with a TTL equal to the token lifetime.
const tokenStore = new Map();

// Demo user — password is "admin123", hashed at startup so the demo just runs
const users = [
    { id: 1, username: "admin", role: "admin", passwordHash: bcrypt.hashSync("admin123", 10) },
];

function signAccessToken(user) {
    return jwt.sign({ userId: user.id, role: user.role }, ACCESS_TOKEN_SECRET, {
        expiresIn: "15m",
        issuer: ISSUER,
        audience: AUDIENCE,
    });
}

function generateRotatedRefreshToken(userId, family) {
    const jti = crypto.randomUUID();
    const token = jwt.sign({ userId, jti, family }, REFRESH_TOKEN_SECRET, { expiresIn: "7d" });
    tokenStore.set(jti, { userId, token, family, createdAt: Date.now() });
    return token;
}

function revokeFamily(family) {
    for (const [jti, data] of tokenStore.entries()) {
        if (data.family === family) tokenStore.delete(jti);
    }
}

function rotateRefreshToken(oldToken) {
    let decoded;
    try {
        decoded = jwt.verify(oldToken, REFRESH_TOKEN_SECRET);
    } catch (err) {
        throw new Error("invalid_token");
    }

    const stored = tokenStore.get(decoded.jti);
    if (!stored) {
        // jti not found: the token was already consumed (or never issued).
        // A consumed token presented again means theft — kill the whole family.
        revokeFamily(decoded.family);
        throw new Error("reuse_detected");
    }
    if (stored.token !== oldToken) throw new Error("invalid_token");

    tokenStore.delete(decoded.jti);
    return generateRotatedRefreshToken(decoded.userId, decoded.family);
}

// --- Auth routes ---

app.post("/auth/login", async (req, res) => {
    const { username, password } = req.body;
    const user = users.find(u => u.username === username);
    if (!user || !(await bcrypt.compare(password || "", user.passwordHash))) {
        return res.status(401).json({ error: "Invalid credentials" });
    }

    res.json({
        accessToken: signAccessToken(user),
        refreshToken: generateRotatedRefreshToken(user.id, crypto.randomUUID()),
        expiresIn: 900,
    });
});

app.post("/auth/refresh", (req, res) => {
    try {
        const newRefreshToken = rotateRefreshToken(req.body.refreshToken);
        const decoded = jwt.verify(newRefreshToken, REFRESH_TOKEN_SECRET);
        const user = users.find(u => u.id === decoded.userId);

        res.json({
            accessToken: signAccessToken(user),
            refreshToken: newRefreshToken,
            expiresIn: 900,
        });
    } catch (err) {
        if (err.message === "reuse_detected") {
            return res.status(401).json({
                error: "Token reuse detected. All sessions revoked.",
                code: "reuse_detected",
            });
        }
        return res.status(401).json({ error: "Invalid refresh token" });
    }
});

app.post("/auth/logout", (req, res) => {
    try {
        const decoded = jwt.verify(req.body.refreshToken, REFRESH_TOKEN_SECRET);
        tokenStore.delete(decoded.jti);
    } catch (err) {
        // Already invalid or consumed — logout is idempotent
    }
    res.json({ message: "Logged out" });
});

// --- Protected routes ---

function authMiddleware(req, res, next) {
    const header = req.headers.authorization;
    if (!header || !header.startsWith("Bearer ")) {
        return res.status(401).json({ error: "Token required" });
    }

    try {
        req.user = jwt.verify(header.slice(7), ACCESS_TOKEN_SECRET, {
            issuer: ISSUER,
            audience: AUDIENCE,
        });
        next();
    } catch (err) {
        res.status(401).json({
            error: err.name === "TokenExpiredError" ? "Token expired" : "Invalid token",
            code: err.name === "TokenExpiredError" ? "token_expired" : "token_invalid",
        });
    }
}

app.get("/api/profile", authMiddleware, (req, res) => {
    const user = users.find(u => u.id === req.user.userId);
    res.json({ id: user.id, username: user.username, role: user.role });
});

app.use((err, req, res, next) => {
    console.error(err);
    res.status(500).json({ error: "Internal Server Error" });
});

if (require.main === module) {
    app.listen(3000, () => console.log("Listening on http://localhost:3000"));
}

module.exports = { app, tokenStore };
