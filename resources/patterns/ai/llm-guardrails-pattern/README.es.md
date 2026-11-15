# Patrón LLM Guardrails — Código complementario

Implementaciones ejecutables del recurso [Patrón LLM Guardrails](https://stackpractices.com/es/patterns/llm-guardrails-pattern/) en StackPractices.

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `llm_guardrails.py` | Demo autocontenida: pipeline ordenado de guardrails de entrada/salida con fail-fast, verificaciones de prompt injection / contenido prohibido / PII de entrada, toxicidad y secretos en salida, y pista de auditoría completa de `GuardrailResult`. Corre con Python 3 estándar — sin claves de API. |
| `llm-guardrails.js` | El mismo pipeline en Node.js. |
| `LLMGuardrailPipeline.java` | El mismo pipeline en Java 17+ (`javac` + `java`, sin dependencias). |

## Inicio rápido

```bash
python llm_guardrails.py
node llm-guardrails.js
javac LLMGuardrailPipeline.java && java LLMGuardrailPipeline
```

Salida esperada: un pase limpio, tres bloqueos de entrada (injection, SSN,
palabra prohibida) y un bloqueo de salida — el modelo "filtra" una clave de
API y el guardrail de salida la atrapa. Todas las llamadas son simuladas,
así que los resultados son deterministas.

## Qué adaptar para producción

- Sustituye las listas de palabras y regex por tus capas reales: API de
  moderación, un clasificador de injection hecho a propósito, tu taxonomía
  de PII. La forma del pipeline se mantiene — las verificaciones son lo
  que evoluciona.
- Conserva el orden barato → caro: un clasificador de 200ms solo debería
  ver el tráfico que sobrevivió a las verificaciones gratis de regex y
  longitud.
- Decide bloquear vs. sanitizar por categoría: la demo lo bloquea todo por
  claridad; un guardrail de salida en producción enmascararía PII de baja
  severidad en lugar de tirar la respuesta entera.
- Envía cada `GuardrailResult` a tus logs — los conteos por categoría a lo
  largo del tiempo son cómo afinas las reglas y detectas campañas de
  sondeo.
