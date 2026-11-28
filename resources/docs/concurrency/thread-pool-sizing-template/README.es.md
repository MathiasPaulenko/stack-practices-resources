# Plantilla de Dimensionado de Thread Pools — Recursos complementarios

Recursos complementarios de la [Plantilla de Dimensionado de Thread Pools](https://stackpractices.com/es/docs/thread-pool-sizing-template/) en StackPractices.

## Archivos

| Archivo | Descripción |
| --- | --- |
| `template.md` | Hoja de trabajo rellenable en blanco — cópiala a los docs operativos del servicio y rellena una por pool |
| `example-checkout-service.md` | Ejemplo completo: un servicio de checkout I/O-bound que llama a una API de inventario, con los números trabajados de principio a fin |

## Uso

Copia `template.md`, mide el ratio W/C de tu carga bajo tráfico real y rellena los placeholders. Compara con el ejemplo completo cuando dudes del nivel de detalle — el objetivo es una decisión de dimensionado defendible en revisión, con fecha para volver a medirla.
