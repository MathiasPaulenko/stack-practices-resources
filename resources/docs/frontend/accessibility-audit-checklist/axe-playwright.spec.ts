import { test, expect } from '@playwright/test';
import { AxeBuilder } from '@axe-core/playwright';

// Automated accessibility pass for CI. Covers the mechanical ~30-40% of
// WCAG issues — the manual and screen-reader passes in the checklist still
// need a human.
const pages = ['/', '/pricing', '/checkout']; // list every scoped page/template

for (const path of pages) {
  test(`${path} passes axe automated checks`, async ({ page }) => {
    await page.goto(path);
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag22aa'])
      .analyze();
    expect(results.violations).toEqual([]);
  });
}
