
import asyncio
from playwright.async_api import async_playwright
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URL = "https://www.zara.com/tr/tr/cift-tarafli-suni-deri-ceket-p08073327.html?v1=507142418&utm_campaign=productShare&utm_medium=mobile_sharing_iOS&utm_source=red_social_movil"

async def debug():
    logger.info(f"CWD: {os.getcwd()}")
    async with async_playwright() as p:
        # Standard Playwright launch
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        context = await browser.new_context(
             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
             viewport={"width": 1920, "height": 1080},
             locale="tr-TR",
             timezone_id="Europe/Istanbul"
        )
        page = await context.new_page()
        try:
            logger.info(f"Navigating to {URL}")
            await page.goto(URL, timeout=60000, wait_until="domcontentloaded")
            await page.wait_for_timeout(5000)
            
            title = await page.title()
            logger.info(f"Page Title: {title}")
            
            await page.screenshot(path="server_debug.png", full_page=True)
            logger.info("Saved server_debug.png")
            
            content = await page.content()
            with open("server_debug.html", "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("Saved server_debug.html")
            
            zara = await page.evaluate("() => window.zara")
            if zara:
                logger.info("window.zara found!")
            else:
                logger.error("window.zara NOT found!")

        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug())
