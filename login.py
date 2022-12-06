"""用 Debug Mode 手動登入"""
import asyncio
import os

from playwright.async_api import Page, async_playwright
from playwright_stealth import stealth_async


async def run(page: Page):
    auth_file = f"cred.json"

    await page.goto("https://bsignin.104.com.tw/login")
    await page.locator('input[data-qa-id="loginUserName"]').fill(os.environ["ac"])
    await page.locator('input[data-qa-id="loginPassword"]').fill(os.environ["pwd"])
    await page.locator('button[data-qa-id="loginButton"]').click()

    await page.wait_for_timeout(60000)
    await page.context.storage_state(path=auth_file)


async def main():
    async with async_playwright() as pw:
        chromium = pw.chromium
        browser = await chromium.launch(headless=False)

        try:
            page = await browser.new_page()
            await stealth_async(page)
            await run(page)
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())

