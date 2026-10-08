/**
 * OAuth 2.0 login with Google — Express + Passport.
 *
 * Setup:
 *   npm install express express-session passport passport-google-oauth20
 *   export SESSION_SECRET=<random-secret>
 *   export GOOGLE_CLIENT_ID=<your-client-id>
 *   export GOOGLE_CLIENT_SECRET=<your-client-secret>
 *
 * Register http://localhost:3000/auth/google/callback in Google Cloud
 * Console, then run: node passport_app.js
 */

const express = require("express");
const session = require("express-session");
const passport = require("passport");
const GoogleStrategy = require("passport-google-oauth20").Strategy;

passport.use(
  new GoogleStrategy(
    {
      clientID: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
      callbackURL: "/auth/google/callback",
      state: true,
      pkce: true,
    },
    (accessToken, refreshToken, profile, done) => {
      return done(null, profile);
    }
  )
);

passport.serializeUser((user, done) => done(null, user.id));
passport.deserializeUser((id, done) => done(null, { id }));

const app = express();
app.use(
  session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
    cookie: { secure: false, httpOnly: true, sameSite: "lax" }, // secure:true requires HTTPS — disable for local dev only
  })
);
app.use(passport.initialize());
app.use(passport.session());

app.get("/", (req, res) =>
  res.send(req.user ? `Hello, user ${req.user.id}!` : '<a href="/auth/google">Sign in with Google</a>')
);
app.get("/auth/google", passport.authenticate("google", { scope: ["profile", "email"] }));
app.get(
  "/auth/google/callback",
  passport.authenticate("google", { failureRedirect: "/" }),
  (req, res) => res.redirect("/")
);
app.get("/logout", (req, res, next) =>
  req.logout((err) => (err ? next(err) : res.redirect("/")))
);

app.listen(3000, () => console.log("http://localhost:3000"));
