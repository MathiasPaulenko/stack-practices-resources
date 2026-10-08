// checkout.e2e.spec.ts — Playwright
// Requires a running shop app at the configured baseURL with the
// data-testid hooks shown below.
// Run: npx playwright test checkout.e2e.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Checkout flow', () => {
  test('user completes a purchase', async ({ page }) => {
    await page.goto('/products');
    await page.click('[data-testid="product-1"]');
    await page.click('[data-testid="add-to-cart"]');
    await page.click('[data-testid="checkout"]');

    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="card"]', '4242424242424242');
    await page.click('[data-testid="pay"]');

    await expect(page.locator('.order-confirmation'))
      .toContainText('Order confirmed');
  });
});
