from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from playwright.async_api import async_playwright
from playwright_stealth.stealth import Stealth
import random
import asyncio
import os
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class UrlRequest(BaseModel):
    url: str

class StockCheckRequest(BaseModel):
    url: str
    size: str

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

async def get_zara_product_data(url: str):
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
             # Block heavy resources to speed up
            await page.route("**/*", lambda route: route.abort() 
                             if route.request.resource_type in ["image", "media", "font"] 
                             else route.continue_())

            logger.info(f"Navigating to {url}")
            await page.goto(url, timeout=60000, wait_until="domcontentloaded")
            # Smart wait: poll for window.zara instead of hard sleep
            await page.wait_for_function("() => !!window.zara && !!window.zara.viewPayload", timeout=15000)

            # Try to click cookie banner just in case it interferes (though for window.zara it shouldn't)
            try:
                await page.click('#onetrust-accept-btn-handler', timeout=2000)
            except:
                pass

            # Extract data from window.zara
            logger.info("Extracting window.zara data...")
            data = await page.evaluate("() => window.zara")
            
            if not data or 'viewPayload' not in data:
                raise Exception("window.zara or viewPayload is undefined")

            return data['viewPayload']

        except Exception as e:
            logger.error(f"Error extracting data: {e}")
            raise e
        finally:
            await browser.close()

@app.post("/scrape-sizes")
async def scrape_sizes(request: UrlRequest):
    try:
        payload = await get_zara_product_data(request.url)
        
        product = payload.get('product', {})
        detail = product.get('detail', {})
        colors = detail.get('colors', [])

        # Extract product name
        product_name = product.get('name', '')

        # Extract product image (first color, first image)
        product_image = ''
        if colors:
            try:
                main_imgs = colors[0].get('mainImgs', [])
                if main_imgs:
                    product_image = main_imgs[0].get('url', '')
            except Exception:
                pass

        # Extract sizes
        sizes = set()
        for color in colors:
             for size in color.get('sizes', []):
                 sizes.add(size.get('name'))
        
        sorted_sizes = sorted(list(sizes))
        logger.info(f"Found sizes: {sorted_sizes} for '{product_name}'")
        
        return {
            "name": product_name,
            "image": product_image,
            "sizes": sorted_sizes
        }

    except Exception as e:
        logger.error(f"Error scraping {request.url}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/check-stock")
async def check_stock(request: StockCheckRequest):
    try:
        payload = await get_zara_product_data(request.url)
        
        product = payload.get('product', {})
        detail = product.get('detail', {})
        colors = detail.get('colors', [])
        
        in_stock = False
        
        for color in colors:
            for size in color.get('sizes', []):
                if size.get('name') == request.size:
                    availability = size.get('availability', 'out_of_stock')
                    if availability == 'in_stock' or availability == 'low_on_stock':
                        in_stock = True
                        break
            if in_stock:
                break
        
        return {"in_stock": in_stock}

    except Exception as e:
        logger.error(f"Error checking stock {request.url}: {e}")
        return {"in_stock": False} # Default to false on error

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
