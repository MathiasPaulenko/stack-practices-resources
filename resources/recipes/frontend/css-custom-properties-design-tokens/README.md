# Design Tokens with CSS Custom Properties

Companion resource for the StackPractices recipe
[Design Tokens with CSS Custom Properties](https://stackpractices.com/recipes/css-custom-properties-design-tokens/).

## Contents

- `tokens.css` — drop-in design token file: raw color scales, semantic tokens, dark theme via `[data-theme="dark"]`, spacing scale, fluid typography with `clamp()`, radius, shadows, z-index, and transitions.
- `demo.html` — self-contained page that imports `tokens.css` and shows cards, buttons and chips consuming only semantic tokens, with a runtime light/dark toggle persisted to `localStorage`.

## Run it

Open `demo.html` in any modern browser and press **Toggle theme**. Every color, spacing and font-size change comes from remapping semantic tokens — no component rule is touched.

## Layer model

```
raw scale (--color-primary-500) -> semantic tokens (--color-accent) -> component tokens (--button-bg) -> UI
```

Components read semantic tokens only, so themes and brands are a re-mapping of one layer, not a rewrite of every rule.
