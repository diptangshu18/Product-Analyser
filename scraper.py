import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import openai

# Load secret API key from .env
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def scrape_and_analyze(url: str):
    """
    Partner A's Role: Scrape data + AI Summary
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print(f"Scraping: {url}")
        page.goto(url, timeout=60000)
        
        # Grabbing basic info
        title = page.title()
        # Note: Selectors like '.review-text' may need adjustment for Amazon/Flipkart
        reviews = page.locator(".review-text").all_text_contents()[:3] 
        
        browser.close()

        # AI Integration (The Buzzword Step)
        prompt = f"Summarize these reviews for {title} in 2 sentences: {reviews}"
        ai_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "product_name": title,
            "ai_summary": ai_response.choices[0].message.content,
            "status": "Success"
        }