import assert from "assert";
import fs from "fs";

const LOGIN_URL = "https://bsignin.104.com.tw/login";
const CLOCK_URL = "https://pro.104.com.tw/psc2";

const { chromium } = require("playwright-extra");
const stealth = require("puppeteer-extra-plugin-stealth")();
chromium.use(stealth);

chromium.launch({ headless: true }).then(async (browser) => {
  let stateFile = `${process.env.account}.json`;
  assert(fs.existsSync(stateFile));

  const loginedContext = await browser.newContext({
    storageState: stateFile,
  });

  const page = await loginedContext.newPage();
  await page.goto(LOGIN_URL);

  // 登入狀態
  assert(page.url() == "https://bsignin.104.com.tw/product");

  await page.goto(CLOCK_URL);
  await page.waitForTimeout(3000);
  await page.screenshot({ path: "screenshots/d.png", fullPage: true });
  await page.locator(".PSC-ClockIn span").click();

  let isSucc = false;
  try {
    await page.locator(".success").click();
    isSucc = true;
  } catch (error) {}

  assert(isSucc);
  browser.close();
});
