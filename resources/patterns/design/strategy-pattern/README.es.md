# Patrón Strategy — Código complementario

Ejemplos ejecutables de [Patrón Strategy: algoritmos intercambiables en runtime](https://stackpractices.com/es/patterns/strategy-pattern/) en StackPractices.

## Archivos

| Archivo | Qué muestra |
|---|---|
| `payment_strategy.py` | Interfaz abstracta `PaymentStrategy` con implementaciones de tarjeta y PayPal, más un contexto `Checkout` |
| `strategy_checkout.js` | Las mismas estrategias de pago como clases JavaScript simples — sin interfaz necesaria |
| `StrategyCheckout.java` | `interface` Java + implementaciones + `Checkout` con `setStrategy` |
| `pricing_strategy.ts` | Servicio de precios completo: estrategias regular/miembro/senior/festivo más un `CompositePricing` que las apila |

## Uso

- `payment_strategy.py` corre en Python 3.8+ sin dependencias.
- `strategy_checkout.js` corre en cualquier Node.js moderno.
- `StrategyCheckout.java` compila solo; añade un `main` para ejecutarlo.
- `pricing_strategy.ts` necesita TypeScript (`tsc` o `ts-node`).
