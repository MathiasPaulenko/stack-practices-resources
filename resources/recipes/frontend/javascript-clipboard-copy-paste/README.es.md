# Copiar y Pegar con Clipboard en JavaScript

Recurso companion de [StackPractices](https://stackpractices.com/es/recipes/javascript-clipboard-copy-paste/).

## Contenido

- `src/clipboard.js` — todos los helpers: `copyToClipboard` (API moderna + fallback `execCommand`), `readClipboardText`, `readRichClipboard` (HTML/imágenes vía `ClipboardItem`), `checkClipboardPermission`, `addCopyButtons`, `interceptPasteAsPlainText`, `interceptPasteImages`
- `src/demo.js` — cableado que ejercita cada helper
- `index.html` — demo ejecutable (copiar, leer, lectura rica, interceptación de pegado, botones en bloques de código)

## Uso

La Clipboard API requiere un contexto seguro, así que sirve la carpeta sobre HTTPS o `localhost`:

```bash
cd resources/recipes/frontend/javascript-clipboard-copy-paste
python -m http.server 8080
# abre http://localhost:8080
```

O importa los helpers como módulos ES:

```javascript
import { copyToClipboard, addCopyButtons } from "./src/clipboard.js";

await copyToClipboard("hola");           // dentro de un click handler
addCopyButtons();                        // agrega botones Copiar a bloques pre code
```

## Requisitos

- Cualquier navegador moderno; el fallback `execCommand` cubre motores legacy
- Sin dependencias — módulos ES puros
- Firefox/Safari muestran un menú efímero de "Pegar" para lecturas; los nombres de permiso `clipboard-read`/`clipboard-write` solo existen en Chromium
