# Web Components Mini-Library

Runnable examples from [Web Components — Custom Elements, Shadow DOM & Templates](https://stackpractices.com/guides/web-components-guide/).

## Files

- `src/user-card.js` — autonomous element with shadow DOM, observed attributes, named slots, and a `composed` CustomEvent.
- `src/alert-box.js` — named slots + theming through CSS custom properties (`--alert-accent`, `--alert-bg`).
- `src/rating-input.js` — form-associated element via `ElementInternals` (`setFormValue`, `setValidity`, `formResetCallback`).
- `index.html` — demo page wiring all three: slot composition, event listening, native form submission.
- `test/user-card.test.js` — unit tests with `@open-wc/testing`.

## Run the demo

No build step — just serve the folder statically (ES modules need HTTP, `file://` won't work):

```bash
npx serve .
# or
python -m http.server 8080
```

Open `http://localhost:8080` (or the printed port) and check the console: clicking "Select" inside a `user-card` logs `user-selected`.

## Run the tests

```bash
npm i -D @web/test-runner @open-wc/testing
npx web-test-runner test/ --node-resolve --playwright --browsers chromium
```

Playwright browsers are required (`npx playwright install chromium`).
