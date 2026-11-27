# Receta del Strategy Pattern — Código complementario

Ejemplos ejecutables de [Intercambiar Algoritmos en Runtime con el Strategy Pattern](https://stackpractices.com/es/recipes/strategy-pattern-recipe/) en StackPractices.

## Archivos

| Archivo | Qué muestra |
|---|---|
| `shipping_strategy.ts` | Interfaz `ShippingStrategy` basada en clases con implementaciones flat-rate, por peso y por distancia, más un contexto `CheckoutService` |
| `TaxStrategy.java` | Enum strategy en Java: cálculo de impuestos `US`, `EU` y `UK` detrás de un único método `calculate` |
| `function_strategies.py` | Estrategias con funciones en Python — callables despachados por clave, sin clases |
| `strategy_registry.ts` | Un `StrategyRegistry` genérico que mapea claves de texto a estrategias seleccionadas en runtime |
| `pricing_decorators.ts` | Composición de estrategias: decorators de descuento, impuesto y envío gratis envolviendo una estrategia base |
| `payment_context.py` | Un `PaymentContext` que registra estrategias de tarjeta, PayPal y cripto y despacha por nombre de método |

## Uso

- Los `.py` corren en Python 3.8+ sin dependencias.
- Los `.ts` necesitan TypeScript (`tsc` o `ts-node`); los tipos compartidos como `Order` y `Money` se definen donde se usan.
- `TaxStrategy.java` compila solo; añade un `main` para ejecutarlo.
