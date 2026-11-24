# Rotación segura de refresh tokens JWT con Python

Proyecto ejecutable companion de la receta de StackPractices:
<https://stackpractices.com/es/recipes/python-jwt-refresh-token-rotation/>

## Archivos

- `token_manager.py` — clase `TokenManager`: generación de pares de tokens, verificación de access tokens, rotación de refresh con blacklist y detección de reuso, revocación individual y masiva. Incluye una demo `__main__` que recorre todo el flujo de rotación.
- `redis_token_manager.py` — variante Redis completamente cableada para despliegues multi-instancia: los jti activos viven en claves Redis con TTL y la rotación los consume de forma atómica vía `GETDEL` (Redis 6.2+).
- `app.py` — app FastAPI con `/auth/login`, `/auth/refresh`, `/auth/logout` y una ruta `/protected`.

## Requisitos

```bash
pip install pyjwt fastapi uvicorn
```

Opcional: `cryptography` para RS256, `redis` para la variante de blacklist distribuida.

## Ejecutar

```bash
# demo del flujo de rotación + detección de reuso
python token_manager.py

# API
uvicorn app:app --reload
```

## Notas

- `_active_refresh_tokens`/`_blacklist` en memoria sirven para una sola instancia. Para despliegues multi-instancia cámbialos por claves Redis con TTL (ver la variante Redis de la receta).
- La detección de reuso devuelve `None` ante un `jti` blacklisteado — en producción, trátalo como señal de robo y llama a `revoke_all_user_tokens`.
