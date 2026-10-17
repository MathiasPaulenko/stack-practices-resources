# Principios SOLID — Recursos complementarios

Código complementario de la guía [Principios SOLID Explicados con Ejemplos](https://stackpractices.com/es/guides/solid-principles-guide/).

Un refactor antes/después de un servicio de pagos en TypeScript que muestra los cinco principios SOLID aplicados sobre la misma clase.

## Contenido

| Ruta | Qué muestra |
| --- | --- |
| `before/payment-processor.ts` | La versión heredada: un método que valida, cobra con un cliente de Stripe fijo, loguea, envía emails y escribe en una conexión MySQL fija. Viola SRP, OCP y DIP. |
| `after/interfaces.ts` | Los contratos: `PaymentValidator`, `PaymentGateway`, `PaymentRepository`, `NotificationService`, `Logger`. Interfaces angostas (ISP). |
| `after/implementations.ts` | Implementaciones concretas: `StripeGateway`, `PayPalGateway`, `PostgresPaymentRepository`, `EmailNotificationService`, `WinstonLogger`. Una responsabilidad cada una (SRP); los gateways nuevos extienden sin modificar código existente (OCP). |
| `after/payment-processor.ts` | La clase refactorizada: depende solo de las interfaces (DIP), así que cualquier `PaymentGateway` puede sustituirse (LSP). |
| `after/composition.ts` | El composition root que conecta abstracciones con implementaciones, más un procesador totalmente simulado para tests — sin framework de patching. |

## Cómo usarlo

1. Lee `before/payment-processor.ts` y detecta las violaciones.
2. Compara con los módulos de `after/` para ver cómo cada principio remodela el código.
3. Cambia `StripeGateway` por `PayPalGateway` en `after/composition.ts` — nada más tiene que cambiar.
4. Usa `testProcessor` como punto de partida para tests unitarios con mocks de objetos planos.
