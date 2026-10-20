# Modo Oscuro con prefers-color-scheme — Demo

Demo ejecutable para la [Receta de Modo Oscuro con prefers-color-scheme](https://stackpractices.com/es/recipes/css-dark-mode-prefers-color-scheme/) de StackPractices.

## Archivos

| Archivo | Qué es |
|---------|--------|
| `index.html` | Página demo con el script anti-FOUC inline en `<head>` |
| `styles.css` | Tematización por tokens: custom properties en `:root`/`[data-theme]` + `color-scheme` |
| `theme.js` | Toggle con persistencia en `localStorage` + listener de preferencia del sistema |

## Uso

Abre `index.html` en un navegador — sin build, sin dependencias. Cambia la preferencia del SO o haz clic en el botón; la elección persiste en `localStorage`. Para reiniciar, borra los datos del sitio o ejecuta `localStorage.removeItem("theme")` en DevTools.

## Relacionados

- [Receta de Modo Oscuro (ES)](https://stackpractices.com/es/recipes/css-dark-mode-prefers-color-scheme/)
- [Dark Mode recipe (EN)](https://stackpractices.com/recipes/css-dark-mode-prefers-color-scheme/)
- [Índice de recursos de StackPractices](https://mathiaspaulenko.github.io/stack-practices-resources/)
