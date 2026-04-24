from scraper.engine import scrape_and_analyze
import json

# STEP 1: Paste the Flipkart URL here
TEST_URL = "https://www.amazon.in/dp/B0CHX1W1XY"

def start_test():
    print(f"🚀 Starting AI Analysis for: {TEST_URL}")
    print("⏳ This might take 10-20 seconds... (Opening hidden browser)")
    
    try:
        result = scrape_and_analyze(TEST_URL)
        
        # Check if the engine returned an error
        if "error" in result:
            print("❌ TEST FAILED!")
            print(f"Error Details: {result['error']}")
        else:
            print("✅ TEST SUCCESSFUL!")
            print(json.dumps(result, indent=4))
            
    except Exception as e:
        print(f"🔥 Script crashed: {e}")

if __name__ == "__main__":
    start_test()