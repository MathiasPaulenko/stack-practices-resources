# Bridge Pattern for UI Themes — TypeScript Examples

Companion to the StackPractices pattern [Bridge Pattern for UI Themes](https://stackpractices.com/patterns/bridge-pattern-ui-themes/).

| File | Contains |
|---|---|
| src/renderer.ts | UIRenderer interface, Web/Native renderers, Button/Checkbox abstractions |
| src/theme.ts | Theme interface, Light/Dark themes, ThemedButton |
| src/theme-switch.ts | Runtime theme switching via setTheme() |
| src/dark-theme.ts | Fixed DarkTheme renderButton example |

Run with ts-node or compile with tsc (TypeScript 4+).
