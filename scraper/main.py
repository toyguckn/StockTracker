from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import random
import asyncio

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

@app.post("/scrape-sizes")
async def scrape_sizes(request: UrlRequest):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=random.choice(USER_AGENTS))
        page = await context.new_page()

        # Block heavy resources
        await page.route("**/*", lambda route: route.abort() 
                         if route.request.resource_type in ["image", "media", "font"] 
                         else route.continue_())

        try:
            await page.goto(request.url, timeout=60000, wait_until="domcontentloaded")
            # Try to grab the initial state or wait for selector
            # Zara's structure might vary, but simplified selector logic:
            # Look for size list items
            try:
                await page.wait_for_selector("ul.product-detail-size-selector__size-list", timeout=15000)
            except:
                pass # Continue anyway, maybe it loaded fast or different structure

            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            sizes = []
            size_items = soup.select("li.product-detail-size-selector__size-list-item")
            
            for item in size_items:
                size_label = item.get_text(strip=True).split(' ')[0] # Basic cleaning
                # Check directly if it has 'out-of-stock' class or similar logic
                # For now just return all sizes found to let user pick
                sizes.append(size_label)
                
            return list(set(sizes)) # Unique sizes

        except Exception as e:
            print(f"Error scraping {request.url}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            await browser.close()

@app.post("/check-stock")
async def check_stock(request: StockCheckRequest):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=random.choice(USER_AGENTS))
        page = await context.new_page()
        
        await page.route("**/*", lambda route: route.abort() 
                         if route.request.resource_type in ["image", "media", "font"] 
                         else route.continue_())

        in_stock = False
        try:
            await page.goto(request.url, timeout=60000, wait_until="domcontentloaded")
            try:
                await page.wait_for_selector("ul.product-detail-size-selector__size-list", timeout=15000)
            except:
                pass

            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            size_items = soup.select("li.product-detail-size-selector__size-list-item")
            
            for item in size_items:
                text = item.get_text(strip=True)
                if request.size in text:
                    # Check classes for out of stock
                    classes = item.get('class', [])
                    # Zara usually adds a class like 'product-detail-size-selector__size-list-item--unavailable'
                    # or the span inside has 'product-detail-size-selector__size-list-item-text--disabled'
                    
                    is_disabled = any('unavailable' in cls for cls in classes) or \
                                  any('disabled' in cls for cls in classes) or \
                                  any('out-of-stock' in cls for cls in classes)
                    
                    if not is_disabled:
                        in_stock = True
                    break
            
            return {"in_stock": in_stock}

        except Exception as e:
            print(f"Error checking stock {request.url}: {e}")
            return {"in_stock": False} # Default to false on error
        finally:
            await browser.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
