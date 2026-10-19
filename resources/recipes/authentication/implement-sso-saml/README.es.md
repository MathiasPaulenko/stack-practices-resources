# Implementar SSO con SAML 2.0 — Demo ejecutable

Código acompañante de la receta de StackPractices
[Implementar SSO con SAML 2.0](https://stackpractices.com/es/recipes/implement-sso-saml/).

Un Service Provider SAML 2.0 mínimo pero completo: una app Flask con
[python3-saml](https://github.com/SAML-Toolkits/python3-saml) que incluye
endpoints de login, ACS, SLS y metadatos SP, más un contenedor de Keycloak
para usar como Identity Provider de pruebas.

## Qué incluye

| Archivo | Propósito |
| --- | --- |
| `app.py` | SP en Flask: `/saml/login`, `/saml/acs`, `/saml/sls`, `/saml/metadata`, `/dashboard` |
| `saml_settings.json` | Configuración de python3-saml (SP + IdP + flags de seguridad) |
| `docker-compose.yml` | Keycloak 26 en modo dev como IdP de pruebas local |
| `requirements.txt` | Dependencias de Python |

## Inicio rápido

### 1. Levantar el IdP de pruebas

```bash
docker compose up -d
```

Luego configura Keycloak en <http://localhost:8080> (admin / admin):

1. Crea un realm llamado `saml-demo`.
2. En ese realm, crea un **cliente SAML** con Client ID
   `https://localhost:5000/saml/metadata` (el entityId del SP).
3. En la configuración del cliente, define **Valid redirect URIs** como
   `https://localhost:5000/*` y **Master SAML Processing URL** como
   `https://localhost:5000/saml/acs`.
4. En la pestaña **Keys** del cliente, habilita la firma y copia el
   certificado de firma del IdP desde **Realm settings → Keys** (o desde
   `http://localhost:8080/realms/saml-demo/protocol/saml/descriptor`).
5. Crea un usuario de prueba con contraseña.

### 2. Configurar el SP

Edita `saml_settings.json`:

- `idp.entityId`, `idp.singleSignOnService.url`, `idp.singleLogoutService.url`
  — por defecto apuntan a los endpoints del realm `saml-demo`.
- `idp.x509cert` — pega el certificado de firma del IdP (cuerpo PEM, sin cabeceras).
- `sp.x509cert` / `sp.privateKey` — opcionales en local; obligatorios si
  activas `authnRequestsSigned` / `logoutRequestSigned`.

### 3. Ejecutar el SP

```bash
pip install -r requirements.txt
export SECRET_KEY="dev-secret-change-me"
python app.py
```

La app corre en `https://localhost:5000` con un certificado autofirmado
(`ssl_context="adhoc"`), porque los IdPs rechazan URLs de ACS por HTTP plano.
Acepta el aviso del navegador una vez.

### 4. Probar el flujo

- `https://localhost:5000/` → "Log in with SSO" redirige a Keycloak.
- Tras el login, Keycloak envía por POST la Response firmada a `/saml/acs`.
- `/saml/metadata` devuelve el XML de metadatos del SP para registrarlo en el IdP.
- `/saml/sls` gestiona el Single Logout; `/dashboard` es la página protegida.

## Notas

- `strict: true` rechaza respuestas no solicitadas (iniciadas por el IdP).
  Usa `"strict": false` solo si un cliente requiere SSO iniciado por el IdP.
- La cookie de sesión usa `SameSite=None; Secure` — necesario para el POST
  cross-site que el IdP envía al ACS.
- `RelayState` se valida antes de redirigir para que no se convierta en un
  open redirect.
