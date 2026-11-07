# Demo de CSS Container Queries

Recurso complementario de la receta de StackPractices
[Container Queries de CSS para componentes responsivos](https://stackpractices.com/es/recipes/css-container-queries-responsive/).

## Contenido

- `container-queries-demo.html` — demo autocontenida: un mismo componente de tarjeta renderizado en dos contenedores distintos (un sidebar redimensionable y una columna principal redimensionable). La tarjeta se adapta al ancho de cada contenedor, mostrando cómo `@container` desacopla el layout del componente del viewport.

## Cómo ejecutarla

Abre `container-queries-demo.html` en cualquier navegador moderno (Chrome/Edge 105+, Safari 16+, Firefox 110+). Arrastra la esquina inferior derecha de cada panel para redimensionarlo y observa cómo la tarjeta alterna entre layout apilado y horizontal en 350px y 600px de ancho de contenedor, de forma independiente en cada panel.

## Qué demuestra

- `container-type: inline-size` + `container-name` en un wrapper padre
- Breakpoints `@container <nombre> (min-width: ...)` a nivel de componente
- Unidades relativas al contenedor (`cqi`) dentro de `clamp()` para tipografía fluida
- El mismo componente produciendo layouts distintos según el hueco, sin CSS específico de contexto
