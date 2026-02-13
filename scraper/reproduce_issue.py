import asyncio
from playwright.async_api import async_playwright
from playwright_stealth.stealth import Stealth
import logging
import random
import sys
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

TARGET_URL = "https://www.zara.com/tr/tr/cift-tarafli-suni-deri-ceket-p08073327.html?v1=507142418&utm_campaign=productShare&utm_medium=mobile_sharing_iOS&utm_source=red_social_movil"

async def reproduce():
    url = TARGET_URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
    
    logger.info(f"Testing URL: {url}")

    proxy_settings = None
    proxy_url = os.getenv("PROXY_URL")
    if proxy_url:
        logger.info(f"Using proxy: {proxy_url}")
        proxy_settings = {"server": proxy_url}

    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(
            headless=True,
            proxy=proxy_settings
        )
        context = await browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={"width": 1920, "height": 1080},
            locale="tr-TR",
            timezone_id="Europe/Istanbul"
        )
        page = await context.new_page()

        try:
            logger.info("Navigating...")
            await page.goto(url, timeout=60000, wait_until="domcontentloaded")
            await page.wait_for_timeout(5000)

            logger.info(f"Page Title: {await page.title()}")

            # Extract data from window.zara
            data = await page.evaluate("() => window.zara")
            
            if not data:
                logger.error("window.zara is empty or undefined.")
                return

            if 'viewPayload' in data:
                 product = data['viewPayload'].get('product', {})
                 name = product.get('name', 'N/A')
                 logger.info(f"Product Name: {name}")

                 detail = product.get('detail', {})
                 colors = detail.get('colors', [])
                 
                 # Image extraction (try first color)
                 if colors:
                     try:
                         image_url = colors[0].get('mainImgs', [{}])[0].get('url', 'N/A')
                         logger.info(f"Product Image: {image_url}")
                     except Exception as img_err:
                         logger.error(f"Image extraction error: {img_err}")
                 
                 found_sizes = []
                 if colors:
                     for color in colors:
                         logger.info(f"Processing Color: {color.get('name')}")
                         sizes = color.get('sizes', [])
                         for size in sizes:
                             size_name = size.get('name')
                             availability = size.get('availability')
                             logger.info(f"  - Size: {size_name} ({availability})")
                             
                             if availability == 'in_stock':
                                 found_sizes.append(size_name)
                 
                 logger.info(f"Final Extracted Sizes: {found_sizes}")
                 
            else:
                 logger.error("'viewPayload' not found in window.zara")
                 # Check analyticsData as backup
                 if 'analyticsData' in data:
                     logger.info("Found analyticsData (but looking for viewPayload for sizes).")

        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(reproduce())
