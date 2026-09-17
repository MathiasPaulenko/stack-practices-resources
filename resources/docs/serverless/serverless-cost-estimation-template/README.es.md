# Plantilla de Estimación de Costos Serverless — Recursos Complementarios

Archivos complementarios de la [Plantilla de Estimación de Costos Serverless](https://stackpractices.com/es/docs/serverless-cost-estimation-template/) en StackPractices.com.

## Qué incluye

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `cost-estimation.md` | Markdown | Hoja de estimación standalone: perfil de función, desglose de costos, costos ocultos, resumen de escenarios, log de validación |
| `estimate-costs.py` | Python 3 | Calculadora de costo mensual de Lambda: función única por flags CLI o lista de workloads en JSON; soporta precios x86 y arm64 |

## Inicio rápido

### Función única

```bash
python estimate-costs.py --invocations 10000000 --duration-ms 200 --memory-mb 512
```

### Múltiples funciones

```bash
python estimate-costs.py workloads.json
```

## Adaptación antes de producción

1. Verifica las constantes `PRICE_*` contra la [página de precios de AWS Lambda](https://aws.amazon.com/lambda/pricing/) — las tarifas cambian sin aviso.
2. Alimenta duración e invocaciones desde pruebas de carga, no suposiciones; modela escenarios 3x y 10x.
3. Añade las filas de costos ocultos (logs, NAT, colas) a la estimación — suelen representar un tercio de la factura.
4. Concilia la estimación contra Cost Explorer cada mes y actualiza el log de validación.
