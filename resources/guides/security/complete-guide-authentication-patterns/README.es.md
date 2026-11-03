# Guía Completa de Patrones de Autenticación — Código de acompañamiento

Bloques de autenticación ejecutables en Python para la guía
[Guía Completa de Patrones de Autenticación](https://stackpractices.com/es/guides/complete-guide-authentication-patterns/)
de StackPractices.

## Archivos

| Archivo | Qué implementa |
| --- | --- |
| `jwt_service.py` | Tokens de acceso + refresh con RS256 y claim `type` |
| `token_rotation.py` | Rotación de refresh, revocación por token y flag de logout global |
| `session_manager.py` | Sesiones Redis: TTL deslizante + absoluto, índice por usuario |
| `oauth2_client.py` | Cliente Authorization Code con `raise_for_status` |
| `oidc_provider.py` | Verificación de `id_token` con `PyJWKClient` + nonce |
| `passkey_manager.py` | Opciones de registro/autenticación WebAuthn + verificación |
| `mfa_service.py` | TOTP, códigos de respaldo hasheados de un solo uso, reto MFA pendiente |
| `abac_evaluator.py` | Mapa RBAC + políticas ABAC con placeholders `$subject.*` |
| `test_authentication.py` | Tests de humo con pytest (fakeredis, claves RSA desechables) |

## Puesta en marcha

```bash
pip install -r requirements.txt
pip install fakeredis pytest
pytest test_authentication.py -v
```

Los módulos son deliberadamente ligeros en framework: `session_manager.py` y
`oauth2_client.py` asumen FastAPI/`httpx`; el resto es Python plano sobre un
cliente Redis. Conecta `db`, `redis`, `verify_credentials` y `get_user` a tu
propia capa de datos — están pensados para que los aporte tu aplicación.
