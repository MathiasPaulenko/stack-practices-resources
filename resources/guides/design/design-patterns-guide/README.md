# Design Patterns Guide — Companion Resources

Companion code for the guide [Practical Design Patterns Guide](https://stackpractices.com/guides/design-patterns-guide/).

A runnable TypeScript order pipeline that wires five patterns together: Strategy, Factory Method, Observer, Decorator, and Command. Each file is self-contained so you can read any pattern in isolation.

## Contents

| Path | What it shows |
| --- | --- |
| `order-system/shipping.ts` | Strategy: shipping cost algorithms selected at runtime via a `Record<string, ShippingStrategy>` map. |
| `order-system/notifications.ts` | Factory Method: `NotificationFactory.create(kind)` returns `EmailNotifier`, `SMSNotifier`, or `PushNotifier` behind the `Notifier` interface. |
| `order-system/events.ts` | Observer: an `EventBus` where `order.created` fans out to inventory, confirmation, and analytics listeners. |
| `order-system/products.ts` | Decorator: `withCache(withLogging(fetchProduct), ttl)` stacks cross-cutting behavior around a plain function. |
| `order-system/commands.ts` | Command: `CancelOrderCommand` encapsulates a multi-step cancellation with `execute()`/`undo()`. |
| `order-system/index.ts` | Composition root: wires all five patterns into the order pipeline from the guide's "Putting It Together" section. |

## How to use

1. Run the pipeline: `npx tsx order-system/index.ts` (or `ts-node`).
2. Swap `"express"` for `"standard"` in `index.ts` — only the strategy map lookup changes.
3. Add a `"whatsapp"` case to `NotificationFactory` — no caller changes needed.
4. Call `cmd.undo()` after `execute()` to see Command's reversibility in action.

No dependencies beyond a TypeScript runner; every collaborator is a plain interface you can mock in tests.
