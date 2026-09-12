# Funciones Debounce y Throttle en JavaScript

Recurso companion para [StackPractices](https://stackpractices.com/es/recipes/javascript-debounce-throttle-implementation/).

## Contenidos

- `src/debounce.js` — Debounce básico (trailing edge)
- `src/throttle.js` — Throttle básico (leading edge)
- `src/debounce-advanced.js` — Debounce con opciones leading/trailing
- `src/throttle-trailing.js` — Throttle con trailing edge
- `src/debounce-cancelable.js` — Debounce cancelable con cancel() y flush()
- `src/autosave.js` — Autoguardado práctico con debounce
- `src/scroll-progress.js` — Progreso de scroll práctico con throttle
- `src/use-debounce.js` — Custom hook de React para debounce

## Uso

```bash
node -e "const { debounce } = require('./src/debounce'); const fn = debounce(() => console.log('called'), 300); fn(); fn(); fn();"
```

## Requisitos

- Node.js 18+ (para los scripts standalone)
- React 18+ (para el hook useDebounce)
