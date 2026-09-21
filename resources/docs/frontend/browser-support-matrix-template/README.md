# Browser Support Matrix — Companion Resources

Companion files for the [Browser Support Matrix Template](https://stackpractices.com/docs/browser-support-matrix-template/) on StackPractices.com.

## What's included

| File | Format | Description |
|------|--------|-------------|
| `browser-support-matrix.md` | Markdown | The fillable matrix: support tiers, feature compatibility (JS / CSS / Web APIs), polyfill strategy, fallbacks, testing matrix, build config, banner policy |
| `feature-matrix.json` | JSON | Machine-readable version of the feature matrix — tiers plus per-feature support/polyfill/fallback data for tooling or dashboards |
| `babel.config.js` | JavaScript | `@babel/preset-env` targets matching the matrix baseline, with `useBuiltIns: 'usage'` |
| `browserslist` | Config | Production/development browserslist — the single source of truth that drives Babel, Autoprefixer, and ESLint |
| `upgrade-banner.html` | HTML | Feature-probe upgrade banner for below-baseline browsers (no UA sniffing) |

## Quick start

### 1. Set the baseline from analytics

Pull the last 90 days of browser/version traffic. Pick a usage threshold (common: >0.5% for Tier 1, >0.1% for Tier 2) and assign tiers mechanically.

### 2. Sync the config files

Copy `browserslist` to your repo root and keep `babel.config.js` targets aligned — the config enforces the matrix, the document mirrors it.

### 3. Fill the feature matrix

List only the features your app actually uses (or will use next two quarters). Each gap resolves to exactly one outcome: a polyfill with a measured gzipped cost, or a fallback.

### 4. Wire the banner

Drop `upgrade-banner.html` into your base layout. The feature probe (structuredClone/fetch/lazy-loading) flags any browser below the baseline without parsing user agents.

## Review quarterly

Check analytics for threshold crossings, caniuse for newly-shipped support, and re-run Tier 2 smoke tests. Browserslist's `last 2 versions` baseline moves every ~6 weeks whether you update the document or not.
