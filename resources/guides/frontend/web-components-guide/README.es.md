# Mini-Librería de Web Components

Ejemplos ejecutables de [Web Components — Custom Elements, Shadow DOM y Templates](https://stackpractices.com/es/guides/web-components-guide/).

## Archivos

- `src/user-card.js` — elemento autónomo con shadow DOM, atributos observados, slots con nombre y un CustomEvent `composed`.
- `src/alert-box.js` — slots con nombre + theming mediante CSS custom properties (`--alert-accent`, `--alert-bg`).
- `src/rating-input.js` — elemento asociado a formularios vía `ElementInternals` (`setFormValue`, `setValidity`, `formResetCallback`).
- `index.html` — página demo que conecta los tres: composición con slots, escucha de eventos y envío nativo de formulario.
- `test/user-card.test.js` — unit tests con `@open-wc/testing`.

## Ejecutar la demo

Sin build — sirve la carpeta estáticamente (los módulos ES necesitan HTTP, `file://` no funciona):

```bash
npx serve .
# o
python -m http.server 8080
```

Abre `http://localhost:8080` (o el puerto indicado) y mira la consola: al pulsar "Select" dentro de un `user-card` se registra `user-selected`.

## Ejecutar los tests

```bash
npm i -D @web/test-runner @open-wc/testing
npx web-test-runner test/ --node-resolve --playwright --browsers chromium
```

Necesitas los navegadores de Playwright (`npx playwright install chromium`).
