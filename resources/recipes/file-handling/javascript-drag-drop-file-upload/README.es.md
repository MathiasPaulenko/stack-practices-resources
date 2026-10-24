# Subida de Archivos Drag and Drop en JavaScript — Demo complementaria

Demo ejecutable de la receta [Subida de Archivos Drag and Drop en JavaScript con HTML5](https://stackpractices.com/es/recipes/javascript-drag-drop-file-upload/).

## Qué incluye

- `uploader.js` — la clase `DragDropUploader` de la receta (eventos de la drop zone, validación por tipo/tamaño, progreso con XHR, previews de imagen y drop de carpetas con `webkitGetAsEntry`), más `SimulatedUploader`, una subclase que simula las subidas con un timer.
- `index.html` — página demo que conecta el uploader con una drop zone, lista de errores, barras de progreso y grid de previews.
- `styles.css` — estilos mínimos para la drop zone, las barras de progreso y los previews.

## Cómo ejecutarla

Abre `index.html` en cualquier navegador moderno — sin build y sin backend. La demo usa `SimulatedUploader`, que anima las barras de progreso en local.

Para conectarla a un endpoint real, edita el script en `index.html`:

```javascript
const uploader = new DragDropUploader("drop-zone", {
    uploadUrl: "/api/upload",
    // ...los mismos callbacks
});
```

Tu endpoint debe aceptar `POST` con `multipart/form-data` y un campo `file`.

## Recursos relacionados

- Recipe (EN): https://stackpractices.com/recipes/javascript-drag-drop-file-upload/
- Receta (ES): https://stackpractices.com/es/recipes/javascript-drag-drop-file-upload/
