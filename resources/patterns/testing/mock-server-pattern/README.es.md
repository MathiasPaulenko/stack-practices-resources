# Patrón Mock Server — Código complementario

Implementaciones ejecutables y sin dependencias del [Patrón Mock Server](https://stackpractices.com/es/patterns/mock-server-pattern/): un servidor HTTP real en un puerto local que devuelve respuestas predefinidas, graba cada petición y permite a los tests verificar las llamadas después.

Ambos archivos implementan el mismo ciclo de cuatro pasos que usan WireMock, nock, MSW y Mountebank:

1. **Configurar** — `stub(method, path, status, body)` registra una respuesta predefinida.
2. **Interceptar** — el código bajo test dispara una petición HTTP real a un socket real.
3. **Matchear y responder** — gana el primer stub cuyo método + path matchean; los paths sin stub devuelven 404.
4. **Verificar** — `verify(method, path)` confirma que la petición realmente llegó.

## Archivos

| Archivo | Stack | Tests |
|---------|-------|-------|
| `mock_server.py` | Python stdlib (`http.server`, `threading`, `urllib`) | 5 casos unittest |
| `mock_server.mjs` | Node.js (`node:http`, `node:test`, `fetch`) | 5 casos con `node --test` |

## Ejecutar

```bash
# Python — demo + suite de tests
python mock_server.py
python -m unittest mock_server -v

# Node — solo tests (el archivo también corre una demo al ejecutarlo directo)
node --test mock_server.mjs
node mock_server.mjs
```

## Qué cubren los tests

- Una respuesta stubeada llega al cliente por un socket real.
- Los errores stubeados (404) se propagan a excepciones del cliente.
- Los paths sin stub devuelven 404 por defecto — el comportamiento sin match también es testeable.
- `verify()` distingue "la petición ocurrió" de "el test pasó".
- `reset()` entre tests evita stubs filtrados — la causa principal de fallos fantasma en suites reales.

## Cuándo usar un mock server real vs. un interceptor

Un puerto real (como estos) ejercita el comportamiento de socket de tu cliente HTTP — timeouts, reintentos, TLS. Los interceptores en proceso como nock o `responses` son más rápidos y no pueden tener colisiones de puertos, por eso suelen ser la elección en CI. La [página del patrón](https://stackpractices.com/es/patterns/mock-server-pattern/) tiene la tabla de decisión completa.
