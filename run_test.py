from scraper.engine import scrape_and_analyze
import json

# Use a real product link
url = "https://www.amazon.in/dp/B0CHX1W1XY" 
print("🚀 Starting AI Analysis...")
result = scrape_and_analyze(url)
print(json.dumps(result, indent=4))