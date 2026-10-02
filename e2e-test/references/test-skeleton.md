// tests/e2e/[flow].spec.ts
// Skeleton for one user flow. Selectors are roles/labels only — never CSS
// class chains. Each test seeds its own data and shares no state.
import { test, expect } from '@playwright/test';

test.describe('[flow]', () => {
  test.beforeEach(async ({ page }) => {
    await seed(page); // this test's own data — no dependence on other tests
  });

  test('[happy path]: [what the user does]', async ({ page }) => {
    await page.goto('/[entry-path]');
    await page.getByRole('textbox', { name: /[label]/ }).fill('[value]');
    await page.getByRole('button', { name: /[action]/ }).click();
    await expect(page.getByRole('heading', { name: /[outcome]/ })).toBeVisible();
  });

  test('[unhappy path]: [bad input / network failure / expired session]', async ({ page }) => {
    // exactly one unhappy path per flow — the one most likely to hurt in prod
    await page.goto('/[entry-path]');
    // ...
    await expect(page.getByRole('alert')).toContainText(/[error message]/);
  });
});

// playwright.config.ts — artifacts on failure only, nothing on green runs:
//   use: { trace: 'on-first-retry', screenshot: 'only-on-failure', video: 'retain-on-failure' }
