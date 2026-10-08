# Inicio de Sesión OAuth 2.0 — Recursos Companion

Ejemplos ejecutables para la [receta de Login OAuth 2.0](https://stackpractices.com/es/recipes/oauth2-login/): flujo Authorization Code con PKCE en Flask (Authlib), Express (Passport) y Spring Security.

## Archivos

| Archivo | Descripción |
| --- | --- |
| `flask_app.py` | App Flask completa — login con Google, validación de state, sesión |
| `passport_app.js` | App Express completa — Passport + GoogleStrategy con `state` y `pkce` |
| `SecurityConfig.java` | Filter chain de Spring Security con `oauth2Login` |
| `application.yml.example` | Client registration de Spring para Google + GitHub |

## Inicio rápido (Flask)

```bash
pip install flask authlib requests
export FLASK_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
export GOOGLE_CLIENT_ID=<tu-client-id>
export GOOGLE_CLIENT_SECRET=<tu-client-secret>
python flask_app.py  # → http://localhost:5000
```

Registrá `http://localhost:5000/callback` (Flask) o `http://localhost:3000/auth/google/callback` (Express) como URI de redirección autorizada en [Google Cloud Console](https://console.cloud.google.com/apis/credentials) — la URI tiene que coincidir byte a byte.
