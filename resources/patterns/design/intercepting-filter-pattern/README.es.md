# Patrón Intercepting Filter — Recursos Complementarios

Ejemplos ejecutables del [Patrón Intercepting Filter](https://stackpractices.com/es/patterns/intercepting-filter-pattern/) en StackPractices.

El patrón compone responsabilidades transversales (autenticación, logging, compresión) en una cadena de filtros que interceptan las peticiones antes del manejador destino — y las respuestas en el camino de vuelta. Es el mecanismo detrás del middleware de Express, los filtros servlet de Java y los pipelines de ASP.NET Core.

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `filter_chain.py` | Cadena de filtros en Python: cortocircuito de auth, logging en ambos sentidos, postprocesamiento gzip |
| `filter_chain.js` | La misma cadena en JavaScript, con un punto de entrada `execute()` que reinicia el cursor entre peticiones |
| `test_filter_chain.py` | Suite pytest: 6 tests sobre cortocircuito, postprocesamiento y reuso de la cadena |
| `express_app.js` | Los mismos filtros como middleware estilo Express (`req, res, next`) con un motor de middleware mínimo |
| `express_app.test.js` | Suite `node:test` para la cadena JS y el pipeline de middleware |

## Ejecutar

```bash
# Demo y tests en Python
python filter_chain.py
python -m pytest test_filter_chain.py -v

# Demo y tests en JavaScript (Node 18+)
node filter_chain.js
node --test express_app.test.js

# Servidor estilo Express
node express_app.js   # luego curl http://localhost:3000/api/hello
```

## Ideas clave

- Un filtro que no delega = cortocircuito (el camino del 401 nunca llega al destino).
- El código después de `chain.doFilter()` / `next()` corre en el sentido de respuesta — así funcionan la compresión y el logging a la salida.
- El cursor de la cadena es estado; `execute()` lo reinicia para que una misma instancia sirva todas las peticiones.
- En pipelines asíncronos, olvidar el `await`/`next()` hace que los filtros de respuesta nunca se ejecuten — el bug de producción más común del middleware.

CI: `.github/workflows/test.yml` ejecuta ambas suites en cada cambio de esta carpeta.
