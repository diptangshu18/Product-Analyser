import os
import json
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Load environment variables (kept for when you add AI credits later)
load_dotenv()

# --- SELECTOR REGISTRY ---
# This makes your scraper "Universal". Adding a new site is now just adding a row here.
SITE_CONFIG = {
    "amazon": {
        "title": ["#productTitle", "h1#title", ".a-size-large"],
        "price": [".a-price-whole", "#priceblock_ourprice", ".a-offscreen"],
        "reviews": [".review-text-content", "[data-hook='review-body']"]
    },
    "flipkart": {
        "title": ["h1", ".VU-Z7M", ".B_NuCI"],
        "price": ["[class*='Nx9bqj']", "._30jeq3", ".div.Nx9bqj"],
        "reviews": [".Z_37Z8", ".t-ZTKy"]
    }
}

GENERIC_SELECTORS = {
    "title": ["h1", "meta[property='og:title']"],
    "price": ["[class*='price']", ".price", "#price"],
    "reviews": ["div[class*='review']", ".comments"]
}

def get_selectors(url):
    """Detects which site we are on and returns the right 'map'."""
    for domain, selectors in SITE_CONFIG.items():
        if domain in url.lower():
            return selectors
    return GENERIC_SELECTORS

def scrape_and_analyze(url: str):
    """
    Universal Scraper Engine
    1. Detects site
    2. Loops through possible selectors (Fallback logic)
    3. Returns structured data (Mocked AI for Demo)
    """
    selectors = get_selectors(url)
    site_name = "amazon" if "amazon" in url else "flipkart" if "flipkart" in url else "Unknown"

    # Initialize data holders
    title_text, price_text = "Not Found", "Not Found"

    with sync_playwright() as p:
        # Launch headed so you can see it bypass the bot checks
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            # Using 'domcontentloaded' as it's faster and more stable for retail sites
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # 1. TRY TO FIND TITLE
            for selector in selectors["title"]:
                element = page.locator(selector).first
                try:
                    # Wait briefly for each option to appear
                    element.wait_for(state="visible", timeout=3000)
                    title_text = element.inner_text().strip()
                    if title_text: break 
                except:
                    continue

            # 2. TRY TO FIND PRICE
            for selector in selectors["price"]:
                element = page.locator(selector).first
                try:
                    element.wait_for(state="visible", timeout=3000)
                    price_text = element.inner_text().strip()
                    if price_text: break
                except:
                    continue

        except Exception as e:
            print(f"Scraping Error: {e}")
        finally:
            browser.close()

    # 3. AI ANALYZER PHASE (Mocked due to 429 Quota Error)
    # This keeps your project running even without API credits
    analysis_data = {
        "product_name": title_text,
        "price": price_text,
        "platform": site_name.capitalize(),
        "sentiment_score": 8.5,
        "top_3_pros": ["High-quality build", "Excellent performance", "Great value"],
        "top_3_cons": ["Limited stock", "Premium pricing", "Slow shipping"],
        "verdict": "A top-tier choice for tech enthusiasts (Demo Mode)."
    }

    return analysis_data