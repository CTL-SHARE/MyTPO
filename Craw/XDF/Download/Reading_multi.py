import asyncio
import os
import time
from urllib.parse import urlparse, parse_qs

import asyncpg
from playwright.async_api import async_playwright


async def craw(semaphore, browser, url, conn):
    async with semaphore:
        idx = parse_qs(urlparse(url).query)['orderNum'][0]
        async with conn.transaction():
            await conn.execute("UPDATE tpo.xdf.reading SET question_index = $1 WHERE url = $2", idx, url)
            page = await browser.new_page()
            await page.goto(url)
            html = await page.content()
            await conn.execute("UPDATE tpo.xdf.reading SET full_html = $1 WHERE url = $2", html, url)
            await page.close()
            print(f"examid: {parse_qs(urlparse(url).query)['examId'][0]}, idx: {idx}, successful")


async def main():
    semaphore = asyncio.Semaphore(10)

    conn = await asyncpg.connect(
        host="localhost",
        port="5432",
        database="tpo",
        user="",
        password=""
    )

    rows = await conn.fetch("SELECT url FROM tpo.xdf.reading WHERE full_html = '' AND downloaded = false")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        # Login first
        login_page = await browser.new_page()
        await login_page.goto("https://passport.testgts.com/preLogin?gotoURL=https://www.testgts.com")
        # Add login steps here, e.g., filling out forms and submitting
        await login_page.wait_for_load_state('networkidle')

        uname = os.getenv("UNAME")
        password = os.getenv("PASSWORD")
        if not uname or not password:
            raise ValueError("Environment variables UNAME or PASSWORD are not set")

        await login_page.fill('input[name="telemail"]', uname)
        await login_page.fill('input[name="password"]', password)

        await login_page.click('button[type="submit"]')

        await login_page.wait_for_load_state('networkidle')
        time.sleep(3)
        await login_page.close()

        urls = [row['url'] for row in rows]

        tasks = [craw(semaphore, browser, url, conn) for url in urls]

        await asyncio.gather(*tasks)

        await browser.close()

    await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
