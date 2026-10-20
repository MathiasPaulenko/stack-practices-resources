# Dark Mode with prefers-color-scheme — Demo

Runnable demo for the [Dark Mode with prefers-color-scheme recipe](https://stackpractices.com/recipes/css-dark-mode-prefers-color-scheme/) on StackPractices.

## Files

| File | What it is |
|------|------------|
| `index.html` | Demo page with the anti-FOUC inline script in `<head>` |
| `styles.css` | Token-based theming: `:root`/`[data-theme]` custom properties + `color-scheme` |
| `theme.js` | Toggle with `localStorage` persistence + system-preference listener |

## Usage

Open `index.html` in a browser — no build step, no dependencies. Flip the OS preference or click the toggle button; the choice persists in `localStorage`. To reset, clear site data or run `localStorage.removeItem("theme")` in DevTools.

## Related

- [Dark Mode recipe (EN)](https://stackpractices.com/recipes/css-dark-mode-prefers-color-scheme/)
- [Receta de Modo Oscuro (ES)](https://stackpractices.com/es/recipes/css-dark-mode-prefers-color-scheme/)
- [StackPractices resources index](https://mathiaspaulenko.github.io/stack-practices-resources/)
