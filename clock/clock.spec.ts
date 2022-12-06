import { test } from '@playwright/test';

test('Clock In', async ({ page }) => {
  await page.goto('https://bsignin.104.com.tw/login');

  await page.locator('input[data-qa-id="loginUserName"]').fill(process.env.account);
  await page.locator('input[data-qa-id="loginPassword"]').fill(process.env.account);
  await page.locator('button[data-qa-id="loginButton"]').click();
  await page.screenshot({ path: 'screenshots/1.png', fullPage: true });

  try {
    await page.waitForNavigation();
  } catch (error) {
    await page.screenshot({ path: 'screenshots/2.png', fullPage: true });
  }

});
