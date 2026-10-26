test("homepage passes WCAG", async ({ page }) => {
  await page.goto("https://shop.example.com");
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
    .analyze();
  expect(results.violations).toEqual([]);
});
