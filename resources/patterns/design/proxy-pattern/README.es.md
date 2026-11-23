# Patrón Proxy — Recursos Companion

Ejemplos ejecutables del [patrón Proxy](https://stackpractices.com/es/patterns/proxy-pattern/) de StackPractices.

Un proxy se sitúa delante de un objeto real tras la misma interfaz y decide qué ocurre con cada llamada: reenviarla, rechazarla, devolver un resultado en caché o aplazar el trabajo real. Estos ejemplos componen tres proxies de un solo propósito — virtual (inicialización perezosa), de caché y de protección — alrededor de un `ReportService`, de modo que cada capa se mantiene pequeña y la composición hace el trabajo.

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `proxy.py` | `LazyReportService`, `CachedReportService` y `ProtectedReportService` en Python envolviendo un `ReportService` |
| `test_proxy.py` | Suite pytest: 7 tests de inicialización perezosa, estadísticas de memoización, caché por clave, invalidación y control por roles |
| `proxy.js` | Los mismos tres proxies en JavaScript |
| `proxy.test.js` | Suite `node:test`: 7 tests equivalentes a la cobertura de Python |

## Ejecutar

```bash
# Demo + tests en Python
python proxy.py
python -m pytest test_proxy.py -v

# Demo + tests en JavaScript
node proxy.js
node --test proxy.test.js
```

La salida de la demo muestra el proxy perezoso sin inicializar hasta la primera llamada, la caché sirviendo un acierto en el segundo `generate()` y el proxy de protección rechazando un rol desconocido sin llegar nunca al sujeto real.
