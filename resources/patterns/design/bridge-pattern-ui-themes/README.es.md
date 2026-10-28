# Patrón Bridge para Temas UI — Ejemplos TypeScript

Complemento del patrón de StackPractices [Patrón Bridge para Temas UI](https://stackpractices.com/es/patterns/bridge-pattern-ui-themes/).

| Archivo | Contiene |
|---|---|
| src/renderer.ts | Interfaz UIRenderer, renderizadores Web/Native, abstracciones Button/Checkbox |
| src/theme.ts | Interfaz Theme, temas claro/oscuro, ThemedButton |
| src/theme-switch.ts | Cambio de tema en runtime con setTheme() |
| src/dark-theme.ts | Ejemplo corregido de DarkTheme.renderButton |

Ejecutar con ts-node o compilar con tsc (TypeScript 4+).
