# WCAG 2.2 Accessibility Guide — Companion Resources

Companion files for the [WCAG 2.2 Accessibility Guide](https://stackpractices.com/guides/accessibility-wcag-guide/) on StackPractices. Each snippet maps to a section of the guide and is ready to drop into a project.

## Contents

| File | Purpose |
|------|---------|
| `skip-link.css` | "Skip to main content" link — visually hidden until focused |
| `sr-only.css` | Screen-reader-only utility class (visually hidden, still announced) |
| `accessible-form.html` | Form with labels, `aria-describedby` hints and `aria-invalid` errors |
| `form-validation.ts` | Accessible form validation that moves focus and announces errors |
| `accessible-modal.html` | Native `<dialog>` modal with labelled title/description and focus return |
| `accessible-modal.ts` | `AccessibleModal` class: focus trap, Escape close, focus restore |
| `roving-tabindex-tabs.ts` | Tab interface with roving tabindex + arrow-key navigation |
| `a11y-playwright.spec.ts` | Playwright + axe-core spec for the automated WCAG pass in CI |

## Usage

Copy the snippets into your project and adapt the selectors. For the automated pass:

```bash
npm i -D @playwright/test @axe-core/playwright
npx playwright test a11y-playwright.spec.ts
```
