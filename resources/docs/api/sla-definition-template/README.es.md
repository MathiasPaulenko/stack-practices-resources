# Plantilla de Definición de SLA — Archivos Complementarios

Archivos complementarios de la [Plantilla de Definición de SLA](https://stackpractices.com/es/docs/sla-definition-template/)
en StackPractices. Todo está listo para copiar y pegar: completa los
placeholders, ajusta los números a tu servicio y adapta las políticas
al modelo operativo de tu equipo.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `sla-template.md` | Plantilla completa del documento SLA (EN) con SLOs, SLIs, presupuesto de error, matriz de severidad, exclusiones, créditos, plan de comunicación y cadencia de revisión |
| `sla-template.es.md` | La misma plantilla en español |
| `prometheus-slo-rules.yaml` | Recording rules de Prometheus (disponibilidad, presupuesto restante, burn rate multi-ventana) más reglas de alerta para burn 2x/10x y presupuesto agotado |
| `burn_rate.py` | Calculadora ejecutable en Python: computa burn rate, porcentaje de presupuesto restante y la acción de política de deploys recomendada |

## Inicio Rápido

1. Copia `sla-template.es.md` a tu repo de docs y reemplaza los
   placeholders (`<Nombre del Servicio>`, fechas, equipo, fuente de medición).
2. Fija objetivos desde el comportamiento medido — corre el servicio
   un mes primero y luego ajusta los números ligeramente.
3. Carga `prometheus-slo-rules.yaml` vía `rule_files` en tu config de
   Prometheus y ajusta el objetivo `0.999` y los tamaños de ventana.
4. Verifica presupuestos con la calculadora:

```bash
python burn_rate.py
# Burn rate: 13.9x
# Budget remaining: 95.4%
# Action: ship freely
```

## Notas

- Mantén la fuente de medición nombrada en el SLA — quien posee los
  números posee el argumento en una disputa.
- Las exclusiones solo funcionan si son precisas ("hasta 4 horas/mes
  con 7 días de aviso"), no abiertas.
- Las alertas de burn rate usan detección multi-ventana (5m + 1h) para
  no despertar a nadie por picos cortos.

Fuente: <https://stackpractices.com/es/docs/sla-definition-template/>
