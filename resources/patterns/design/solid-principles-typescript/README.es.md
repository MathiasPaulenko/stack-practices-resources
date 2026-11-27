# Principios SOLID en TypeScript — Servicio de Pedidos Companion

Código companion de [Principios SOLID en TypeScript](https://stackpractices.com/es/patterns/solid-principles-typescript/).

El escenario del servicio de pedidos del patrón, como TypeScript ejecutable:

- **SRP** — `OrderValidator`, `OrderRepository`, `OrderNotifier` poseen cada uno una tarea
- **OCP** — los nuevos descuentos son clases `DiscountStrategy` nuevas, no ediciones
- **LSP** — cualquier `DiscountStrategy` funciona donde funcionaba otra
- **ISP** — `Readable`/`Writable` separados para que los consumidores dependan solo de lo que usan
- **DIP** — `OrderService` recibe interfaces por inyección en el constructor

## Ejecutar los tests

```bash
npm install vitest typescript
npx vitest run
```
