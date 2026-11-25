# Patrón Registry — Companion

Código companion de la página del [Patrón Registry](https://stackpractices.com/es/patterns/registry-pattern/).

## Descripción

Implementaciones ejecutables del registry en cuatro lenguajes. Todas cubren lo mismo: un mapa central de instancias con nombre, factories lazy que crean y cachean la instancia en el primer lookup, un chequeo `has()` y un método `reset()` para aislar tests. El archivo TypeScript añade el escenario de registro de plugins de la sección Advanced Topics de la página.

## Estructura

```text
python/
└── registry.py            # Registry basado en clase con mapas de instancias y factories, y reset()
javascript/
└── registry.js            # La misma forma con campos privados estáticos (Node 18+)
java/
└── Registry.java          # Registry estático con factories Supplier, main() autocontenido
typescript/
└── plugin_registry.ts     # PluginRegistry con factories lazy, list() y unregister()
```

## Requisitos

- Python 3.9+ (sin dependencias)
- Node.js 18+ (sin dependencias; `tsx` o `tsc` para el archivo TypeScript)
- JDK 17+

## Ejecutar

```bash
python python/registry.py
node javascript/registry.js
javac java/Registry.java && java -cp java Registry
npx tsx typescript/plugin_registry.ts
```

Salida esperada: `Result: SELECT 1` y `cached-users`, más los chequeos de lookup. Las demos de Java y Python también muestran qué pasa al pedir una clave inexistente.
