# Implementar Property-Based Testing

Proyecto acompañante de la receta de StackPractices [Implementar Property-Based Testing](https://stackpractices.com/es/recipes/implement-property-based-testing/).

## Archivos

- `python/test_property_based.py` — propiedades con Hypothesis: involución, estrategias restringidas, una estrategia compuesta `users`, un ciclo de ida y vuelta JSON y un stack con `RuleBasedStateMachine`.
- `javascript/property-based.mjs` — propiedades con fast-check y un test basado en modelo con `fc.commands` y objetos `Command` (`check`/`run`).
- `java/` — proyecto Maven con propiedades jqwik y un test con estado mediante `ActionChain` sobre `Stack<Integer>`.

## Inicio rápido

```bash
# Python (Hypothesis)
cd python && pip install -r requirements.txt && pytest test_property_based.py -v

# JavaScript (fast-check)
cd javascript && npm install && npm test

# Java (jqwik)
cd java && mvn test
```

Todos los ejemplos pasan tal cual. Para ver el shrinking en acción, cambia `reverse` en el archivo de Python por una implementación rota (ej., `return s`) y vuelve a ejecutar — Hypothesis reporta el contraejemplo mínimo junto con una seed reproducible.
