# CSS Architecture Pattern — Companion Resources

Companion files for the StackPractices resource
[CSS Architecture: Utility-First with Component-Scoped Layers](https://stackpractices.com/patterns/css-architecture-pattern/).

## Contents

- `design-tokens.css` — drop-in design tokens: colors, typography, spacing, radius,
  shadows, transitions, plus a `prefers-color-scheme: dark` override block.
- `cascade-layers.css` — `@layer base, components, utilities` order with example
  base styles, component classes (`.btn`, `.card`), and utility classes.
- `Button.module.css` — scoped component styles via CSS modules: `.button`,
  `.primary`, `.secondary`, `.disabled`, `.icon`.
- `tokens.json` — the same design tokens in JSON (Style Dictionary-style),
  ready to transform for other platforms.
- `cube-css.css` — the CUBE CSS variant: Composition / Utility / Block / Exception.

## Usage

Import the files in order — tokens first, then layers:

```css
@import "design-tokens.css";
@import "cascade-layers.css";
```

Or reference them directly:

```html
<link rel="stylesheet" href="design-tokens.css" />
<link rel="stylesheet" href="cascade-layers.css" />
```

`Button.module.css` is imported by your bundler as a CSS module:

```jsx
import styles from './Button.module.css';

function Button({ variant = 'primary', disabled, children }) {
  const className = [styles.button, styles[variant], disabled && styles.disabled]
    .filter(Boolean)
    .join(' ');
  return <button className={className} disabled={disabled}>{children}</button>;
}
```

## Why layered CSS?

`@layer base, components, utilities` makes utilities always win without
specificity fights or `!important`. Component classes (`.btn`, `.card`) sit in the
middle; base styles go first.
