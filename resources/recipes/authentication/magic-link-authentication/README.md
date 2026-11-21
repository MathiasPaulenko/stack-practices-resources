# Magic Link Authentication — Express + Nodemailer

Runnable companion for
[Implement Passwordless Login with Magic Links](https://stackpractices.com/recipes/magic-link-authentication/).

Passwordless login flow: request a link by email, get a signed single-use
token (15-min expiry, hash stored — never the raw token), verify via a
POST so email-scanner prefetch can't consume it.

## Run

```bash
npm install
cp .env.example .env   # set APP_SECRET
npm start
```

Without SMTP env vars the server uses an Ethereal test account and prints
a preview URL for the sent email.

## Try it

```bash
# 1. Request a link (uniform response either way)
curl -X POST http://localhost:3000/auth/login \
  -H 'content-type: application/json' -d '{"email":"you@example.com"}'

# 2. Open the Ethereal preview URL printed in the console, copy the link.

# 3. GET the link — it renders a confirm form (token not yet consumed).
#    POST the form (or simulate) to consume the token and get a session.
curl -X POST http://localhost:3000/auth/verify -d 'token=<token>'

# 4. Check the session
curl http://localhost:3000/auth/me -H 'x-session-id: <sessionId>'

# 5. Reuse the same link -> 400 "already used"
curl -X POST http://localhost:3000/auth/verify -d 'token=<token>'
```
