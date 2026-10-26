# Abstract Factory for Cross-Platform UI Component Families

Companion code for the pattern [Abstract Factory for Cross-Platform UI Component Families](https://stackpractices.com/patterns/abstract-factory-cross-platform/).

## Contents

| File | What it is |
|------|------------|
| `ui_factory.ts` | Core implementation: `UIFactory` interface, Web and Mobile product families, and `SettingsScreen` as the client working against interfaces only |
| `factory_registry.ts` | Registry for runtime factory selection — detection happens once at bootstrap, never per view |
| `dynamic_factory_loader.ts` | Config-driven `import()` loading for plugin architectures and white-label builds |
| `configurable_factory.ts` | Factory carrying shared config (theme, locale, a11y) so every product inherits it |
| `lazy_factory.ts` | Proxy deferring concrete factory instantiation until first use |

## How to use

All files import from `ui_factory.ts`. Run any file with `npx tsx <file>` or Node 22+ type stripping (`node --experimental-strip-types <file>.ts`). No npm dependencies.

Start with `ui_factory.ts` for the base pattern, then pick the technique that fits your constraint: registry when a DI container is overkill, dynamic loading when factories ship as plugins, configurable when products share options, lazy when instantiation is expensive.
