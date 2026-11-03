# Chaos Engineering — Inyección de Fallos y Kit de Game Day

Código ejecutable complementario de la receta de StackPractices
[Chaos Engineering](https://stackpractices.com/es/recipes/chaos-engineering/).

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `src/litmus-pod-delete.yaml` | Manifiesto `ChaosEngine` de Litmus: experimento pod-delete acotado a un deployment. |
| `src/inject-latency.sh` | Inyección de latencia con `tc netem` (500ms durante 60s) con limpieza. |
| `src/toxiproxy-setup.sh` | Proxy Toxiproxy + toxics de latencia/timeout para una dependencia MySQL. |
| `src/gremlin-attacks.sh` | Ataques Gremlin CLI: estrés de CPU, blackhole, memoria. |
| `src/steady-state-check.py` | Verificador de SLOs para antes/durante/después de experimentos (endpoints health + metrics). |
| `src/game-day-template.md` | Plantilla de runbook de game day: participantes, alcance, experimentos, criterios de aborto, rollback. |

## Uso

```bash
sudo ./src/inject-latency.sh        # necesita root (tc)
python src/steady-state-check.py    # exit 0 = seguro experimentar
kubectl apply -f src/litmus-pod-delete.yaml
```

## Relacionados

- Receta (ES): <https://stackpractices.com/es/recipes/chaos-engineering/>
- Receta (EN): <https://stackpractices.com/recipes/chaos-engineering/>
- Guía: <https://stackpractices.com/es/guides/chaos-engineering-guide/>
