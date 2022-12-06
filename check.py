"""讀取 session 打卡"""
import asyncio
import json
import os
import pathlib
from datetime import date

from playwright.async_api import Browser, async_playwright
from playwright_stealth import stealth_async

base_path = pathlib.Path(__file__).resolve().parent

HOLIDAY = {}
with open("holiday.json", "r") as f:
    HOLIDAY = json.load(f)


def is_holiday(validated_date: date) -> bool:
    """是否為放假日"""
    try:
        is_national_holiday = (
            validated_date.strftime("%m-%d") in HOLIDAY[str(validated_date.year)]
        )
        return is_national_holiday or date.isoweekday(validated_date) > 5
    except KeyError:
        print("錯誤：新的一年到囉！請填寫新的假日表！")
    return False


async def run(browser: Browser):
    auth_file = base_path / "cred.json"
    if not os.path.isfile(auth_file):
        print("No Auth File")

    context = await browser.new_context(storage_state=auth_file)
    page = await context.new_page()
    await stealth_async(page)

    await page.goto("https://bsignin.104.com.tw/login")
    assert page.url == "https://bsignin.104.com.tw/product"

    await page.goto("https://pro.104.com.tw/psc2")
    await page.wait_for_timeout(3000)
    await page.screenshot(path="try.png")

    await page.locator(".PSC-ClockIn span").click()

    isSucc = False
    try:
        await page.locator(".success").click()
        isSucc = True
    except:
        pass
    assert isSucc
    print("打卡成功")


async def main():
    async with async_playwright() as pw:
        chromium = pw.chromium
        browser = await chromium.launch()

        try:
            today = date.today()
            if not is_holiday(today):
                await run(browser)
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())

