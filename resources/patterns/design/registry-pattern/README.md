# Registry Pattern — Companion

Companion code for the [Registry Pattern](https://stackpractices.com/patterns/registry-pattern/) page.

## Overview

Runnable registry implementations in four languages. Each one covers the same core: a central map of named instances, lazy factories that create and cache instances on first lookup, a `has()` check, and a `reset()` method for test isolation. The TypeScript file adds the plugin-registry scenario from the page's Advanced Topics section.

## Structure

```text
python/
└── registry.py            # Class-based registry with instance + factory maps and reset()
javascript/
└── registry.js            # Same shape using static private fields (Node 18+)
java/
└── Registry.java          # Static registry with Supplier factories, self-contained main()
typescript/
└── plugin_registry.ts     # PluginRegistry with lazy factories, list() and unregister()
```

## Requirements

- Python 3.9+ (no dependencies)
- Node.js 18+ (no dependencies; `tsx` or `tsc` for the TypeScript file)
- JDK 17+

## Run

```bash
python python/registry.py
node javascript/registry.js
javac java/Registry.java && java -cp java Registry
npx tsx typescript/plugin_registry.ts
```

Expected output: `Result: SELECT 1` and `cached-users`, plus the lookup checks. The Java and Python demos also print what happens when a missing key is requested.
