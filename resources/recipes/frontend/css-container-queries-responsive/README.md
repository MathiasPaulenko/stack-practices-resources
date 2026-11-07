# CSS Container Queries Demo

Companion resource for the StackPractices recipe
[CSS Container Queries for Responsive Components](https://stackpractices.com/recipes/css-container-queries-responsive/).

## Contents

- `container-queries-demo.html` — self-contained demo: one card component rendered in two different containers (a resizable sidebar and a resizable main column). The card adapts to each container's width, showing how `@container` decouples component layout from the viewport.

## Run it

Open `container-queries-demo.html` in any modern browser (Chrome/Edge 105+, Safari 16+, Firefox 110+). Drag the bottom-right corner of each panel to resize it and watch the card switch between stacked and horizontal layouts at 350px and 600px container width — independently in each panel.

## What it demonstrates

- `container-type: inline-size` + `container-name` on a parent wrapper
- `@container <name> (min-width: ...)` breakpoints at the component level
- Container-relative units (`cqi`) inside `clamp()` for fluid typography
- The same component producing different layouts in different slots, with no context-specific CSS
