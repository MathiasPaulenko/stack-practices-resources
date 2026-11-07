# TypeScript Advanced Types — Playground

Runnable TypeScript playground for the StackPractices guide
[TypeScript Advanced Types: The Complete Guide](https://stackpractices.com/guides/complete-guide-typescript-advanced-types/).

Every file compiles under `strict`. The test suite is compile-time only:
`npm test` runs `tsc --noEmit` and fails the build when a type computes
something different from what the assertions declare.

## Setup

```bash
npm install
npm run typecheck   # or npm test — same thing
```

## What's inside

| File | Pattern |
|---|---|
| `src/conditional-types.ts` | `T extends U ? X : Y`, `infer`, distribution, `ApiResponse<S, T>` |
| `src/mapped-types.ts` | `Partial`/`Readonly`/`Required` reimplemented, recursive `SnakeCase`, `PickByValue` |
| `src/template-literals.ts` | Event-name unions, `ExtractParams`, `HandlerName`, `CssLength` |
| `src/satisfies-const.ts` | `satisfies`, `as const`, `const` type parameters |
| `src/narrowing.ts` | Type predicates (`x is T`), assertion functions |
| `src/variance.ts` | `in`/`out` annotations (TS 4.7+) |
| `src/typed-emitter.ts` | Event names and payloads checked together |
| `src/api-client.ts` | Route table with per-route required/forbidden options via `never` |
| `src/state-machine.ts` | `EventsOf` event extraction (the working version) |
| `src/branded-types.ts` | `Brand<T, B>` + smart constructors with real UUID validation |
| `test/types.test.ts` | 30+ compile-time assertions (`Expect`/`Equal`/`@ts-expect-error`) |

## Why a type-only test suite

The type system accepts valid syntax with wrong semantics — a `SnakeCase`
that emits `u_serid` compiles fine. The assertions in `test/types.test.ts`
are the safety net: they pin the computed types so a regression is a build
error, not a silent change.

## Not covered here

The guide also discusses overloads vs conditional types, checker
performance, and when *not* to reach for type-level programming — prose
sections without runnable code.
