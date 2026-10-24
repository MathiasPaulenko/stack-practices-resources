# JavaScript Drag and Drop File Upload — Companion Demo

Runnable demo for the recipe [JavaScript Drag and Drop File Upload with HTML5 API](https://stackpractices.com/recipes/javascript-drag-drop-file-upload/).

## What's inside

- `uploader.js` — the `DragDropUploader` class from the recipe (drop zone events, type/size validation, XHR progress, image previews, folder drop via `webkitGetAsEntry`) plus `SimulatedUploader`, a subclass that fakes uploads with a timer.
- `index.html` — a demo page wiring the uploader to a drop zone, error list, progress bars and preview grid.
- `styles.css` — minimal styles for the drop zone, progress bars and previews.

## Run it

Open `index.html` in any modern browser — no build step and no backend needed. The demo uses `SimulatedUploader`, which animates progress bars locally.

To wire it to a real endpoint, edit the script in `index.html`:

```javascript
const uploader = new DragDropUploader("drop-zone", {
    uploadUrl: "/api/upload",
    // ...same callbacks
});
```

Your endpoint must accept `POST` requests with `multipart/form-data` and a `file` field.

## Related resources

- Recipe (EN): https://stackpractices.com/recipes/javascript-drag-drop-file-upload/
- Receta (ES): https://stackpractices.com/es/recipes/javascript-drag-drop-file-upload/
