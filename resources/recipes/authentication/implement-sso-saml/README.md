# Implement SSO with SAML 2.0 — Runnable Demo

Companion code for the StackPractices recipe
[Implement SSO with SAML 2.0](https://stackpractices.com/recipes/implement-sso-saml/).

A minimal but complete SAML 2.0 Service Provider: a Flask app using
[python3-saml](https://github.com/SAML-Toolkits/python3-saml) with login,
ACS, SLS, and SP metadata endpoints, plus a Keycloak container you can use
as a real test Identity Provider.

## What's included

| File | Purpose |
| --- | --- |
| `app.py` | Flask SP: `/saml/login`, `/saml/acs`, `/saml/sls`, `/saml/metadata`, `/dashboard` |
| `saml_settings.json` | python3-saml configuration (SP + IdP + security flags) |
| `docker-compose.yml` | Keycloak 26 in dev mode as a local test IdP |
| `requirements.txt` | Python dependencies |

## Quick start

### 1. Start the test IdP

```bash
docker compose up -d
```

Then configure Keycloak at <http://localhost:8080> (admin / admin):

1. Create a realm named `saml-demo`.
2. In that realm, create a **SAML client** with Client ID
   `https://localhost:5000/saml/metadata` (the SP entityId).
3. In the client settings, set **Valid redirect URIs** to
   `https://localhost:5000/*` and **Master SAML Processing URL** to
   `https://localhost:5000/saml/acs`.
4. Under the **Keys** tab of the client, enable signing and note the IdP
   signing certificate from **Realm settings → Keys** (or fetch it from
   `http://localhost:8080/realms/saml-demo/protocol/saml/descriptor`).
5. Create a test user with a password.

### 2. Configure the SP

Edit `saml_settings.json`:

- `idp.entityId`, `idp.singleSignOnService.url`, `idp.singleLogoutService.url`
  — default to the `saml-demo` realm endpoints.
- `idp.x509cert` — paste the IdP signing certificate (PEM body, no headers).
- `sp.x509cert` / `sp.privateKey` — optional for local testing; required if
  you enable `authnRequestsSigned` / `logoutRequestSigned`.

### 3. Run the SP

```bash
pip install -r requirements.txt
export SECRET_KEY="dev-secret-change-me"
python app.py
```

The app runs on `https://localhost:5000` with a self-signed certificate
(`ssl_context="adhoc"`), because IdPs reject plain-HTTP ACS URLs. Accept the
browser warning once.

### 4. Exercise the flow

- `https://localhost:5000/` → "Log in with SSO" redirects to Keycloak.
- After login, Keycloak POSTs the signed Response to `/saml/acs`.
- `/saml/metadata` returns the SP metadata XML to register in the IdP.
- `/saml/sls` handles Single Logout; `/dashboard` is the protected page.

## Notes

- `strict: true` rejects unsolicited (IdP-initiated) responses. Set
  `"strict": false` only if a customer requires IdP-initiated SSO.
- The session cookie uses `SameSite=None; Secure` — required for the
  cross-site POST the IdP sends to the ACS.
- `RelayState` is validated before redirecting so it can't become an open
  redirect.
