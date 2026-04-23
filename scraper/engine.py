import os
import json
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import openai

# Load environment variables (API Keys)
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- SELECTOR REGISTRY ---
# Centralized location to manage website changes
SELECTORS = {
    "amazon": {
        "title": "#productTitle",
        "price": ".a-price-whole",
        "reviews": ".review-text-content"
    },
    "flipkart": {
        "title": ".B_NuCI",
        "price": "._30jeq3",
        "reviews": "._6K-7Co"
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

    with sync_playwright() as p:
        # Launch Browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()
        
        try:
            # 1. SCRAPE PHASE
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # Using our Selector Registry
            title = page.inner_text(SELECTORS[site]["title"]).strip()
            price = page.inner_text(SELECTORS[site]["price"]).strip()
            # Grab top 5 reviews for AI context
            reviews = page.locator(SELECTORS[site]["reviews"]).all_text_contents()[:5]

            browser.close()

            # 2. AI ANALYZER PHASE (Structured JSON)
            prompt = f"""
            Analyze these reviews for {title} (Price: {price}). 
            Return a JSON object with:
            1. 'sentiment_score' (0-10)
            2. 'top_3_pros' (list)
            3. 'top_3_cons' (list)
            4. 'verdict' (one sentence)
            Reviews: {reviews}
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )

            # Parse AI response and add metadata
            analysis_data = json.loads(response.choices[0].message.content)
            analysis_data.update({
                "product_name": title,
                "price": price,
                "platform": site.capitalize()
            })

            return analysis_data

        except Exception as e:
            if 'browser' in locals():
                browser.close()
            return {"error": f"Scraping or AI analysis failed: {str(e)}"}