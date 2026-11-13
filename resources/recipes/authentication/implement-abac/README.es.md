# Implementar ABAC — Companion

Código de acompañamiento para la receta de StackPractices [Implementar ABAC](https://stackpractices.com/es/recipes/implement-abac/).

## Archivos

- `evaluate_policy.py` — evaluador mínimo de políticas ABAC (solo stdlib). Semántica first-match, referencias `${subject.x}`, comparadores `_lt`/`_gt`, deny por defecto.
- `policy.json` — política de ejemplo: deniega top-secret fuera de la oficina, deniega fuera de horario, permite a editores leer su propio departamento.

## Uso

```bash
python evaluate_policy.py --demo                      # política y escenarios incluidos
python evaluate_policy.py policy.json request.json    # tu propia política + request
```

El orden de las reglas importa: el evaluador usa first-match, así que las
reglas deny deben ir antes que las allow generales.
