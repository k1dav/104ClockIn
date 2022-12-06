import { test } from "@playwright/test";
const LOGIN_URL = "https://bsignin.104.com.tw/login";

test("login", async ({ page }) => {
  let stateFile = `${process.env.account}.json`;

  await page.goto(LOGIN_URL);
  await page
    .locator('input[data-qa-id="loginUserName"]')
    .fill(process.env.account);
  await page
    .locator('input[data-qa-id="loginPassword"]')
    .fill(process.env.password);
  await page.locator('button[data-qa-id="loginButton"]').click();

  await page.screenshot({ path: "screenshots/login.png", fullPage: true });
  await page.context().storageState({ path: stateFile });
});
