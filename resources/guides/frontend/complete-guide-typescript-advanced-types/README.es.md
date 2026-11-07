# Tipos Avanzados de TypeScript — Playground

Playground ejecutable de TypeScript para la guía de StackPractices
[Tipos Avanzados de TypeScript: La Guía Completa](https://stackpractices.com/es/guides/complete-guide-typescript-advanced-types/).

Cada archivo compila en modo `strict`. La suite de tests es solo a nivel
de compilación: `npm test` ejecuta `tsc --noEmit` y falla el build cuando
un tipo calcula algo distinto de lo que declaran las aserciones.

## Instalación

```bash
npm install
npm run typecheck   # o npm test — es lo mismo
```

## Contenido

| Archivo | Patrón |
|---|---|
| `src/conditional-types.ts` | `T extends U ? X : Y`, `infer`, distribución, `ApiResponse<S, T>` |
| `src/mapped-types.ts` | `Partial`/`Readonly`/`Required` reimplementados, `SnakeCase` recursivo, `PickByValue` |
| `src/template-literals.ts` | Uniones de nombres de evento, `ExtractParams`, `HandlerName`, `CssLength` |
| `src/satisfies-const.ts` | `satisfies`, `as const`, parámetros de tipo `const` |
| `src/narrowing.ts` | Predicados de tipo (`x is T`), funciones de aserción |
| `src/variance.ts` | Anotaciones `in`/`out` (TS 4.7+) |
| `src/typed-emitter.ts` | Nombres de evento y payloads verificados juntos |
| `src/api-client.ts` | Tabla de rutas con opciones requeridas/prohibidas por ruta vía `never` |
| `src/state-machine.ts` | Extracción de eventos con `EventsOf` (la versión que funciona) |
| `src/branded-types.ts` | `Brand<T, B>` + smart constructors con validación UUID real |
| `test/types.test.ts` | 30+ aserciones en tiempo de compilación (`Expect`/`Equal`/`@ts-expect-error`) |

## Por qué una suite de tests solo de tipos

El sistema de tipos acepta sintaxis válida con semántica incorrecta — un
`SnakeCase` que emite `u_serid` compila sin problema. Las aserciones de
`test/types.test.ts` son la red de seguridad: fijan los tipos calculados
para que una regresión sea un error de build, no un cambio silencioso.

## No incluido aquí

La guía también trata overloads vs tipos condicionales, rendimiento del
checker y cuándo *no* recurrir a la programación a nivel de tipos —
secciones de prosa sin código ejecutable.
