# Autenticación con API Keys — Recursos complementarios

Archivos complementarios de [Autenticación Segura con API Keys](https://stackpractices.com/es/recipes/api-key-authentication/) en StackPractices.com.

## Qué incluye

| Archivo | Descripción |
|---------|-------------|
| `api-key-manager.py` | `APIKeyManager` — genera/valida keys firmadas con HMAC |
| `api-key-middleware.js` | Middleware Express: lookup de key, expiración, check de scope |
| `key-hash.py` | Helper de hash SHA-256 en reposo |
| `rotate-keys.py` | Rotación dual con ventana de gracia |

## Inicio rápido

1. `python api-key-manager.py` — genera una key de ejemplo y la valida.
2. Integra `api-key-middleware.js` en Express con tu cliente Redis.
3. Ejecuta `rotate-keys.py` programado para retirar keys fuera de ventana.
