# Property-Based Testing con Hypothesis — Archivos complementarios

Suite de tests ejecutable de la receta
[Property-Based Testing con Hypothesis](https://stackpractices.com/es/recipes/python-hypothesis-property-testing/).

## Archivos

- `test_properties.py` — property tests principales: strategies de string/lista/dict, round-trip de JSON, `assume`, `@example`, `@settings`.
- `test_strategies.py` — generador de emails con `@composite` y `st.builds` sobre un dataclass.
- `test_stateful.py` — `RuleBasedStateMachine` modelando un stack con reglas push/pop y un invariant de tamaño.
- `requirements.txt` — `hypothesis`, `pytest`.

## Uso

```bash
pip install -r requirements.txt
pytest -v
```

Rompe una propiedad a propósito (ej. cambia `test_min_le_max` a `min(lst) < max(lst)`) y mira cómo Hypothesis reduce el contraejemplo a una lista de un elemento.
