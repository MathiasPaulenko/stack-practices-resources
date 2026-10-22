# Autenticación JWT

Archivos complementarios de la receta [Autenticación JWT](https://stackpractices.com/es/recipes/jwt-authentication/).

Flujos de tokens ejecutables — firma/verificación, rotación access + refresh, revocación — en los tres lenguajes que cubre la receta.

## Contenido

| Archivo | Qué hace |
| ------- | -------- |
| `jwt_demo.py` | Demo completa: emitir, verificar, refrescar, revocar (PyJWT) |
| `jwt_demo.js` | El mismo flujo en Node.js (`jsonwebtoken`) |
| `JwtUtil.java` | Firma/verificación con la API moderna de JJWT 0.12+ |
| `generate_keys.sh` | Crea `private.pem`/`public.pem` para experimentos con RS256 |
| `requirements.txt` | Dependencia Python (`PyJWT>=2.8`) |
| `package.json` | Dependencia Node (`jsonwebtoken`) |

## Ejecutar

```bash
# Python
pip install -r requirements.txt
python jwt_demo.py

# Node
npm install
node jwt_demo.js

# Claves RS256 para la variante asimétrica de la receta
./generate_keys.sh
```

Salida esperada de `jwt_demo.py`: el access token verifica, el refresh emite un nuevo access token, el refresh revocado es rechazado y el chequeo de tipo rechaza un access token pasado como refresh.

## Notas

- Los valores de `SECRET` son placeholders de desarrollo — nunca subas secretos reales; cárgalos desde variables de entorno.
- Los stores de refresh/blocklist son mapas en memoria para que la demo corra sin Redis; la receta muestra la variante con Redis.
- `JwtUtil.java` necesita los artefactos JJWT 0.12.x en el classpath (ver el comentario al inicio del archivo).
