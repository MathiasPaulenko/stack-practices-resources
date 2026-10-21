# State Pattern — Companion

Companion code for the [State Pattern](https://stackpractices.com/patterns/state-pattern/) page.

## Overview

The order lifecycle example from the pattern page, runnable in three languages: `pending -> paid -> shipped`, with `cancelled` reachable from `pending` and `paid`. Each state is a class that owns its behavior and decides the legal transitions — no giant `switch` in the context.

The Python file also includes the **table-driven variant** (`TRANSITIONS` dict + `InvalidTransition`) for machines with many states and thin per-state logic.

## Structure

```text
python/
└── state_pattern.py      # GoF implementation + table-driven variant + invalid-transition demo
javascript/
└── state_pattern.js      # GoF implementation with state-owned transitions
java/
└── StatePatternDemo.java # GoF implementation, self-contained demo
```

## Requirements

- Python 3.9+ (no dependencies)
- Node.js 18+ (no dependencies)
- JDK 17+

## Run

```bash
python python/state_pattern.py
node javascript/state_pattern.js
cd java && javac StatePatternDemo.java && java StatePatternDemo
```

Expected output (all three languages):

```text
Processing payment...
Shipping order...
Cannot cancel: already shipped
```

## Related

- [State Pattern on StackPractices](https://stackpractices.com/patterns/state-pattern/) — full explanation, trade-offs, transition-table variant, and testing notes
