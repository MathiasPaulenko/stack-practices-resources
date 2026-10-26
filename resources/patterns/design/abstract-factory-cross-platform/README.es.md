# Abstract Factory para Familias de Componentes UI Multiplataforma

Código complementario del patrón [Abstract Factory para Familias de Componentes UI](https://stackpractices.com/es/patterns/abstract-factory-cross-platform/).

## Contenido

| Archivo | Qué es |
|---------|--------|
| `ui_factory.ts` | Implementación base: interfaz `UIFactory`, familias de productos Web y Mobile, y `SettingsScreen` como cliente trabajando solo contra interfaces |
| `factory_registry.ts` | Registro para selección de factory en runtime — la detección ocurre una vez en el bootstrap, nunca por vista |
| `dynamic_factory_loader.ts` | Carga con `import()` basada en config para arquitecturas de plugins y builds white-label |
| `configurable_factory.ts` | Factory que porta config compartida (tema, locale, a11y) heredada por cada producto |
| `lazy_factory.ts` | Proxy que difiere la instanciación de la factory concreta hasta el primer uso |

## Cómo usarlo

Todos los archivos importan desde `ui_factory.ts`. Ejecuta cualquiera con `npx tsx <archivo>` o con type stripping de Node 22+ (`node --experimental-strip-types <archivo>.ts`). Sin dependencias npm.

Empieza por `ui_factory.ts` para el patrón base y luego elige la técnica según tu restricción: registro cuando un contenedor DI sobra, carga dinámica cuando las factories llegan como plugins, configurable cuando los productos comparten opciones, lazy cuando la instanciación es cara.
