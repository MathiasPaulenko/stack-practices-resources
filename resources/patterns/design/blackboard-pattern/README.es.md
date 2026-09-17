# Patrón Blackboard — Recursos de acompañamiento

Código de apoyo para el recurso de StackPractices
[Patrón Blackboard](https://stackpractices.com/es/patterns/blackboard-pattern/).

## Contenido

- `blackboard-solver.py` — demo ejecutable de clasificación de texto: tres knowledge
  sources (matcher de palabras clave, analizador de sentimiento, evaluador de
  confianza) cooperan sobre un blackboard compartido hasta converger en una solución.
  Solo biblioteca estándar.
- `blackboard-event-driven.py` — la variante dirigida por eventos: las fuentes se
  suscriben a cambios del blackboard y se activan solas; sin bucle de controller.

## Uso

```bash
python blackboard-solver.py "cancel my subscription"
python blackboard-event-driven.py "cancel my subscription"
```

La salida muestra cada hipótesis a medida que se contribuye, con su confianza y fuente:

```text
[LOW   ] KeywordMatcher       -> intent=cancellation
[MEDIUM] SentimentAnalyzer    -> sentiment=negative
[HIGH  ] ConfidenceEvaluator  -> intent=cancellation (sentiment=negative)
Solution: intent=cancellation (sentiment=negative)
```

## Ideas para extenderlo

- Añade una cuarta fuente (p. ej., extracción de entidades) y mira cómo el controller la incorpora.
- Cambia el `Controller` lineal por una cola de prioridad donde cada fuente puja por relevancia.
- Añade logging de iteraciones para trazar por qué la solución converge — o no.
