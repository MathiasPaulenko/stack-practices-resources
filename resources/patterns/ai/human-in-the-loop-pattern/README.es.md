# Patrón Human-in-the-Loop — Código complementario

Versión ejecutable del gate de aprobación del patrón
[Human-in-the-Loop](https://stackpractices.com/es/patterns/human-in-the-loop-pattern/)
en StackPractices.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `human_in_the_loop.py` | Gate `HumanInTheLoop` con matriz `RiskLevel` x confianza, callback `reviewer` inyectable y suite `unittest` que cubre cada camino de aprobación |

## Requisitos

- Python 3.10+ — sin dependencias externas.

## Uso

```python
from human_in_the_loop import (
    AgentAction, HumanInTheLoop, RiskLevel,
)

hitl = HumanInTheLoop(confidence_threshold=0.8)

action = AgentAction(
    "deploy", "Deploy a producción", RiskLevel.HIGH,
    {"env": "prod", "version": "v2.1.0"}, 0.6,
)

result = hitl.execute_with_approval(action, real_deploy_fn, "paso de release")
```

## Matriz de aprobación

| Riesgo | Confianza | Decisión |
|--------|-----------|----------|
| HIGH | cualquiera | siempre pausa para revisión |
| MEDIUM | < umbral | pausa para revisión |
| MEDIUM | >= umbral | se ejecuta solo |
| LOW | cualquiera | se ejecuta solo (salvo `auto_approve_low_risk=False`) |

## Notas

- El revisor por defecto es un prompt interactivo de CLI; inyecta cualquier
  callable para enrutar aprobaciones a Slack, una UI web o un LLM secundario.
- `ApprovalStatus.MODIFIED` permite al revisor ajustar parámetros antes de
  ejecutar — el dict modificado reemplaza `action.parameters`.
- Los rechazos devuelven texto de feedback en vez de ejecutar, para que el
  agente pueda adaptar su plan.
