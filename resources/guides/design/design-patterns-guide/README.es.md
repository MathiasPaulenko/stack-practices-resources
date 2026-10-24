# Guía Práctica de Design Patterns — Recursos complementarios

Código de apoyo de la guía [Guía Práctica de Design Patterns](https://stackpractices.com/es/guides/design-patterns-guide/).

Un pipeline de pedidos ejecutable en TypeScript que conecta cinco patrones: Strategy, Factory Method, Observer, Decorator y Command. Cada archivo es autocontenido para leer cualquier patrón de forma aislada.

## Contenido

| Ruta | Qué muestra |
| --- | --- |
| `order-system/shipping.ts` | Strategy: algoritmos de coste de envío elegidos en runtime con un mapa `Record<string, ShippingStrategy>`. |
| `order-system/notifications.ts` | Factory Method: `NotificationFactory.create(kind)` devuelve `EmailNotifier`, `SMSNotifier` o `PushNotifier` tras la interfaz `Notifier`. |
| `order-system/events.ts` | Observer: un `EventBus` donde `order.created` dispara listeners de inventario, confirmación y analítica. |
| `order-system/products.ts` | Decorator: `withCache(withLogging(fetchProduct), ttl)` apila comportamiento transversal sobre una función simple. |
| `order-system/commands.ts` | Command: `CancelOrderCommand` encapsula una cancelación de varios pasos con `execute()`/`undo()`. |
| `order-system/index.ts` | Raíz de composición: conecta los cinco patrones en el pipeline de la sección "Poniéndolo todo junto" de la guía. |

## Cómo usarlo

1. Ejecuta el pipeline: `npx tsx order-system/index.ts` (o `ts-node`).
2. Cambia `"express"` por `"standard"` en `index.ts` — solo cambia la búsqueda en el mapa de estrategias.
3. Añade un caso `"whatsapp"` a `NotificationFactory` — ningún llamador necesita cambios.
4. Llama a `cmd.undo()` tras `execute()` para ver la reversibilidad de Command en acción.

Sin dependencias más allá de un runner de TypeScript; cada colaborador es una interfaz simple que puedes mockear en tests.
