# JavaScript Clipboard Copy and Paste

Companion resource for [StackPractices](https://stackpractices.com/recipes/javascript-clipboard-copy-paste/).

## Contents

- `src/clipboard.js` — all helpers: `copyToClipboard` (modern API + `execCommand` fallback), `readClipboardText`, `readRichClipboard` (HTML/images via `ClipboardItem`), `checkClipboardPermission`, `addCopyButtons`, `interceptPasteAsPlainText`, `interceptPasteImages`
- `src/demo.js` — wiring that exercises every helper
- `index.html` — runnable demo page (copy, read, rich read, paste interception, code-block buttons)

## Usage

The Clipboard API requires a secure context, so serve the folder over HTTPS or `localhost`:

```bash
cd resources/recipes/frontend/javascript-clipboard-copy-paste
python -m http.server 8080
# open http://localhost:8080
```

Or import the helpers as ES modules:

```javascript
import { copyToClipboard, addCopyButtons } from "./src/clipboard.js";

await copyToClipboard("hello");          // inside a click handler
addCopyButtons();                        // adds Copy buttons to pre code blocks
```

## Requirements

- Any modern browser; the `execCommand` fallback covers legacy engines
- No dependencies — plain ES modules
- Firefox/Safari show an ephemeral "Paste" menu for reads; `clipboard-read`/`clipboard-write` permission names only exist in Chromium
