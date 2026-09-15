// jwt-sign-example.js
// RS256 JWT signing with key rotation support via `kid` header.
// Companion to https://stackpractices.com/guides/api-security-checklist-guide/

const jwt = require("jsonwebtoken");
const crypto = require("crypto");
const fs = require("fs");

// Load key pair (in production, fetch from KMS / Secrets Manager, not disk)
const privateKey = fs.readFileSync("private.pem", "utf8");
const publicKey = fs.readFileSync("public.pem", "utf8");

// Key versioning: bump this when you rotate the signing key
const KEY_ID = "v1";

function createAccessToken(userId, options = {}) {
  const expiresIn = options.expiresIn || "15m";
  return jwt.sign(
    {
      sub: String(userId),
      iat: Math.floor(Date.now() / 1000),
      jti: crypto.randomUUID(),
    },
    privateKey,
    {
      algorithm: "RS256",
      expiresIn,
      keyid: KEY_ID, // verifiers fetch the right public key by kid
    }
  );
}

function verifyAccessToken(token) {
  try {
    return jwt.verify(token, publicKey, {
      algorithms: ["RS256"], // never accept "none"
    });
  } catch (err) {
    // Never log the token itself; log the reason only
    console.error("Token verification failed:", err.message);
    return null;
  }
}

module.exports = { createAccessToken, verifyAccessToken, KEY_ID };
