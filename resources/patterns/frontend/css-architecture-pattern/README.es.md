# Patrón de Arquitectura CSS — Recursos de acompañamiento

Ficheros de apoyo para el recurso de StackPractices
[Arquitectura CSS: Utility-First y Capas por Componente](https://stackpractices.com/es/patterns/css-architecture-pattern/).

## Contenido

- `design-tokens.css` — design tokens listos para usar: colores, tipografía,
  espaciado, radios, sombras, transiciones, más un bloque de override para
  `prefers-color-scheme: dark`.
- `cascade-layers.css` — orden de capas `@layer base, components, utilities` con
  estilos base, clases de componente (`.btn`, `.card`) y utilidades de ejemplo.
- `Button.module.css` — estilos con ámbito mediante CSS modules: `.button`,
  `.primary`, `.secondary`, `.disabled`, `.icon`.
- `tokens.json` — los mismos design tokens en JSON (estilo Style Dictionary),
  listos para transformar a otras plataformas.
- `cube-css.css` — la variante CUBE CSS: Composition / Utility / Block / Exception.

## Uso

Importa los ficheros en orden — primero los tokens, luego las capas:

```css
@import "design-tokens.css";
@import "cascade-layers.css";
```

O enlázalos directamente:

```html
<link rel="stylesheet" href="design-tokens.css" />
<link rel="stylesheet" href="cascade-layers.css" />
```

`Button.module.css` lo importa tu bundler como CSS module:

```jsx
import styles from './Button.module.css';

function Button({ variant = 'primary', disabled, children }) {
  const className = [styles.button, styles[variant], disabled && styles.disabled]
    .filter(Boolean)
    .join(' ');
  return <button className={className} disabled={disabled}>{children}</button>;
}
```

## ¿Por qué CSS por capas?

`@layer base, components, utilities` hace que las utilidades siempre ganen sin
peleas de especificidad ni `!important`. Las clases de componente (`.btn`, `.card`)
van en medio; los estilos base primero.
