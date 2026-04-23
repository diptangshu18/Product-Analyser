from fastapi import FastAPI
from scraper.engine import scrape_product # Importing Partner A's work

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to EchoCommerce API", "version": "1.0"}

@app.get("/analyze")
def analyze_product(url: str):
    """
    Partner B's route:
    Takes a URL from the user and passes it to the scraper.
    """
    print(f"Analyzing: {url}")
    
    # Call the scraper function from Partner A
    result = scrape_product(url)
    
    # In the future, Partner B will add NLP analysis here
    return result