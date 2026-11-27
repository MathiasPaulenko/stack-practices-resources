# Flujo de Pedidos con AWS Step Functions

Companion ejecutable de la receta
[Orquestar Flujos Serverless con AWS Step Functions](https://stackpractices.com/es/recipes/serverless-step-functions-workflow/).

Una máquina de estados completa de procesamiento de pedidos: validación,
comprobación de inventario, rama de elección sobre el stock, pago con
retry/catch y envío — desplegada con AWS SAM.

## Archivos

| Archivo | Propósito |
|---|---|
| `order_workflow.asl.json` | Definición en Amazon States Language con placeholders `${...}` de sustitución |
| `template.yaml` | Plantilla SAM: máquina de estados, 5 funciones Lambda, rol IAM de mínimo privilegio |
| `handlers.py` | Handlers de tareas en Python (validar pedido, comprobar inventario, procesar pago) |
| `start_execution.py` | Helper `boto3` para arrancar ejecuciones y consultar su estado |

## Despliegue

```bash
sam build
sam deploy --guided
```

`DefinitionSubstitutions` en `template.yaml` rellena los placeholders tipo
`${ValidateFunctionArn}` del archivo ASL con los ARN reales al desplegar —
la misma definición sirve para todos los stages.

## Arrancar una ejecución

```python
from start_execution import start_order_workflow
arn = start_order_workflow({"id": "ord-123", "items": [...], "customer": {...}})
```

O desde consola/CLI:

```bash
aws stepfunctions start-execution \
  --state-machine-arn <STATE_MACHINE_ARN> \
  --name order-demo-1 \
  --input '{"order":{"id":"ord-123"},"paymentMethod":{}}'
```

## Notas

- `handlers.py` referencia los stubs `check_stock` y `charge_payment` —
  conéctalos a tus proveedores de inventario y pago antes de desplegar.
- La plantilla usa `STANDARD` por defecto; cambia `Type:` a `EXPRESS` para
  flujos de alto volumen por debajo de 5 minutos.
