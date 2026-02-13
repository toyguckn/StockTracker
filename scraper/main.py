from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import random
import asyncio
import logging

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

async def get_page_content(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        # Block heavy resources
        await page.route("**/*", lambda route: route.abort() 
                         if route.request.resource_type in ["image", "media", "font"] 
                         else route.continue_())

        try:
            logger.info(f"Navigating to {url}")
            await page.goto(url, timeout=60000, wait_until="domcontentloaded")
            
            # Wait for any redirect to settle
            await page.wait_for_timeout(3000)
            
            logger.info(f"Final URL: {page.url}")

            # Try to click cookie banner if exists
            try:
                await page.click('#onetrust-accept-btn-handler', timeout=2000)
            except:
                pass

            # Wait for size selector (try multiple)
            selectors = [
                "ul.product-detail-size-selector__size-list",
                ".product-detail-size-selector__size-list",
                "ul[aria-label='Sizes']",
                ".size-selector-list"
            ]
            
            found_selector = None
            for selector in selectors:
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    found_selector = selector
                    break
                except:
                    continue
            
            if not found_selector:
                logger.warning("Could not find standard size selector, dumping content for debug")
            
            content = await page.content()
            return content
            
        except Exception as e:
            logger.error(f"Error during navigation: {e}")
            raise e
        finally:
            await browser.close()

@app.post("/scrape-sizes")
async def scrape_sizes(request: UrlRequest):
    try:
        content = await get_page_content(request.url)
        soup = BeautifulSoup(content, 'html.parser')
        
        sizes = []
        # Try multiple strategies to find sizes
        size_items = soup.select("li.product-detail-size-selector__size-list-item")
        if not size_items:
            size_items = soup.select(".product-detail-size-selector__size-list-item")
        
        for item in size_items:
            # Look for the size label inside the item
            label_span = item.select_one(".product-detail-size-selector__size-list-item-text")
            if label_span:
                size_label = label_span.get_text(strip=True).split(' ')[0]
            else:
                size_label = item.get_text(strip=True).split(' ')[0]
            
            sizes.append(size_label)
            
        unique_sizes = list(set(sizes))
        logger.info(f"Found sizes: {unique_sizes}")
        return unique_sizes

    except Exception as e:
        logger.error(f"Error scraping {request.url}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/check-stock")
async def check_stock(request: StockCheckRequest):
    try:
        content = await get_page_content(request.url)
        soup = BeautifulSoup(content, 'html.parser')
        
        size_items = soup.select("li.product-detail-size-selector__size-list-item")
        if not size_items:
            size_items = soup.select(".product-detail-size-selector__size-list-item")

        in_stock = False
        
        for item in size_items:
            text = item.get_text(strip=True)
            if request.size in text:
                classes = item.get('class', [])
                # Check for disabled/out-of-stock classes
                is_disabled = any('unavailable' in cls for cls in classes) or \
                              any('disabled' in cls for cls in classes) or \
                              any('out-of-stock' in cls for cls in classes)
                
                # Also check attributes
                if item.get('data-qa-action') == 'size-out-of-stock':
                    is_disabled = True

                if not is_disabled:
                    in_stock = True
                break
        
        return {"in_stock": in_stock}

    except Exception as e:
        logger.error(f"Error checking stock {request.url}: {e}")
        return {"in_stock": False}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
