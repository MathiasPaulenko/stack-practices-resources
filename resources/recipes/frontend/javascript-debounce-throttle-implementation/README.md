# Debounce and Throttle Functions in JavaScript

Companion resource for [StackPractices](https://stackpractices.com/recipes/javascript-debounce-throttle-implementation/).

## Contents

- `src/debounce.js` — Basic debounce (trailing edge)
- `src/throttle.js` — Basic throttle (leading edge)
- `src/debounce-advanced.js` — Debounce with leading/trailing options
- `src/throttle-trailing.js` — Throttle with trailing edge
- `src/debounce-cancelable.js` — Cancelable debounce with cancel() and flush()
- `src/autosave.js` — Practical autosave with debounce
- `src/scroll-progress.js` — Practical scroll progress with throttle
- `src/use-debounce.js` — React custom hook for debounce

## Usage

```bash
node -e "const { debounce } = require('./src/debounce'); const fn = debounce(() => console.log('called'), 300); fn(); fn(); fn();"
```

## Requirements

- Node.js 18+ (for the standalone scripts)
- React 18+ (for the useDebounce hook)
