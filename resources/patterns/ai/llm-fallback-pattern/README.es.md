# Patrón LLM Fallback — Código complementario

Implementaciones ejecutables del recurso [Patrón LLM Fallback](https://stackpractices.com/es/patterns/llm-fallback-pattern/) en StackPractices.

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `llm_fallback.py` | Demo autocontenida: cadena de proveedores con presupuestos de reintento por proveedor, taxonomía de errores reintentables/no reintentables, integración `CircuitBreaker` + `BreakerChain` y respuesta estática de último recurso. Funciona con Python 3 sin claves de API. |
| `llm-fallback.js` | La misma cadena en Node.js (versión async/await). |
| `LLMFallbackChain.java` | La misma cadena en Java 17+ (`javac` + `java`, sin dependencias). |

## Inicio rápido

```bash
python llm_fallback.py
node llm-fallback.js
javac LLMFallbackChain.java && java LLMFallbackChain
```

Salida esperada: una llamada limpia en `openai`, una tormenta de rate limits
que reintenta dos veces y cae a `anthropic`, y el resto de prompts servidos
por el primario. Todas las llamadas son mock, así que los fallos son
deterministas.

## Qué adaptar para producción

- Reemplaza `mock_provider_call` por un adaptador por proveedor real que
  mapee los errores de su SDK a la taxonomía `ErrorType` compartida — ese
  mapeo es la parte que sostiene el patrón.
- Añade una fecha límite a nivel cadena para que el peor caso no sea la suma
  del peor caso de cada proveedor.
- Emite una métrica en cada salto de proveedor; una alerta sobre la tasa de
  fallback detecta caídas antes que la factura.
