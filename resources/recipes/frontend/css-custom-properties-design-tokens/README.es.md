# Design Tokens con custom properties de CSS

Recurso complementario de la receta de StackPractices
[Design Tokens con custom properties de CSS](https://stackpractices.com/es/recipes/css-custom-properties-design-tokens/).

## Contenido

- `tokens.css` — archivo de tokens listo para usar: escalas de color base, tokens semánticos, tema oscuro con `[data-theme="dark"]`, escala de espaciado, tipografía fluida con `clamp()`, radios, sombras, z-index y transiciones.
- `demo.html` — página autocontenida que importa `tokens.css` y muestra tarjetas, botones y chips consumiendo solo tokens semánticos, con un toggle claro/oscuro persistido en `localStorage`.

## Cómo ejecutarla

Abre `demo.html` en cualquier navegador moderno y pulsa **Toggle theme**. Cada cambio de color, espaciado y fuente sale de re-mapear tokens semánticos: ninguna regla de componente se toca.

## Modelo por capas

```
escala base (--color-primary-500) -> tokens semánticos (--color-accent) -> tokens de componente (--button-bg) -> UI
```

Los componentes leen solo tokens semánticos, así que los temas y las marcas son un re-mapeo de una capa, no una reescritura de cada regla.
