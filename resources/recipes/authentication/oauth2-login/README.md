# OAuth 2.0 Login — Companion Resources

Runnable examples for the [OAuth 2.0 Login recipe](https://stackpractices.com/recipes/oauth2-login/): Authorization Code flow with PKCE in Flask (Authlib), Express (Passport), and Spring Security.

## Files

| File | Description |
| --- | --- |
| `flask_app.py` | Complete Flask app — Google login, state validation, session |
| `passport_app.js` | Complete Express app — Passport + GoogleStrategy with `state` and `pkce` |
| `SecurityConfig.java` | Spring Security filter chain with `oauth2Login` |
| `application.yml.example` | Spring client registration for Google + GitHub |

## Quick start (Flask)

```bash
pip install flask authlib requests
export FLASK_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
export GOOGLE_CLIENT_ID=<your-client-id>
export GOOGLE_CLIENT_SECRET=<your-client-secret>
python flask_app.py  # → http://localhost:5000
```

Register `http://localhost:5000/callback` (Flask) or `http://localhost:3000/auth/google/callback` (Express) as an authorized redirect URI in [Google Cloud Console](https://console.cloud.google.com/apis/credentials) — the URI must match byte-for-byte.
