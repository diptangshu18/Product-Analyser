import os
import json
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import openai
import time

# Load environment variables (API Keys)
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- SELECTOR REGISTRY ---
# Centralized location to manage website changes
SELECTORS = {
    "amazon": {
        # IDs (#) are the most stable things on Amazon
        "title": "#productTitle, h1#title",
        "price": ".a-price-whole, #priceblock_ourprice, #priceblock_dealprice",
        "reviews": ".review-text-content, [data-hook='review-body']"
    },
    "flipkart": {
        # Uses 'Contains' logic: finds any class that looks like a price/title
        "title": "h1, .VU-Z7M, .B_NuCI",
        "price": "[class*='Nx9bqj'], ._30jeq3, [class*='price']",
        "reviews": ".Z_37Z8, .t-ZTKy, [class*='comment']"
    }
}

def scrape_and_analyze(url: str):
    """
    Partner A Logic: 
    1. Detect Site 
    2. Scrape Data 
    3. Analyze with AI (JSON Output)
    """
    # Detect the site
    site = "amazon" if "amazon" in url else "flipkart" if "flipkart" in url else None
    
    if not site:
        return {"error": "Unsupported website. Please use Amazon or Flipkart."}

   # ... (Keep the site detection logic at the top)

    # Initialize variables so they exist outside the 'with' block
    title, price, reviews = "", "", []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent="...")
        page = context.new_page()

        try:
            # Change "networkidle" to "domcontentloaded"
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_selector(SELECTORS[site]["price"], timeout=20000)
            
            # Store data in our local variables
            title = page.locator(SELECTORS[site]["title"]).first.inner_text().strip()
            price = page.locator(SELECTORS[site]["price"]).first.inner_text().strip()
            reviews = page.locator(SELECTORS[site]["reviews"]).all_text_contents()[:5]
            
            # The 'with' block will close the browser automatically when we exit it
        except Exception as e:
            return {"error": f"Scraping failed: {str(e)}"}

    # --- OUTSIDE the 'with' block now (The Event Loop is gone) ---
    
    analysis_data = {
        "sentiment_score": 8,
        "top_3_pros": ["Great Camera", "Fast Performance", "Premium Feel"],
        "top_3_cons": ["Expensive", "Slow Charging", "No Charger in Box"],
        "verdict": "A solid flagship choice for power users (Demo Mode)."
    }

    analysis_data.update({
        "product_name": title,
        "price": price,
        "platform": site.capitalize()
    })

    return analysis_data