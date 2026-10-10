# Gestión de Sesiones — Ejemplos de Sesiones Seguras

Ejemplos ejecutables de la receta [Gestión de Sesiones Segura](https://stackpractices.com/es/recipes/session-management/) en StackPractices.

## Contenido

| Archivo | Qué es |
|---------|--------|
| `express_sessions.js` | Express + express-session + connect-redis v7: flags de cookie, regeneración de sesión en login, logout |
| `SessionConfig.java` | Spring Boot con `@EnableRedisHttpSession` + endpoint de logout |
| `concurrent_sessions.py` | Tope de sesiones activas por usuario en Redis, expulsando y borrando las más viejas |
| `fastapi_jwt.py` | Variante stateless con JWT para clientes sin navegador |
| `requirements.txt` | Dependencias de Python |
| `package.json` | Dependencias de Node.js |

## Inicio rápido

Redis corriendo en local (ej. `docker run -p 6379:6379 redis`).

Express:

```bash
npm install
npm start            # http://localhost:3000 — POST /login con demo@example.com / demo
```

Python:

```bash
pip install -r requirements.txt
python concurrent_sessions.py   # expulsa la sesión más vieja al superar el tope
```
