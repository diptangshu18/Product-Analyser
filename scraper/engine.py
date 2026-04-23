from playwright.sync_api import sync_playwright

def scrape_product(url: str):
    """
    Partner A's logic: 
    Opens a browser, visits the URL, and returns raw data.
    """
    with sync_playwright() as p:
        # We use headless=True so the browser runs in the background
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Go to the URL provided by the user
            page.goto(url, timeout=60000)
            product_title = page.title()
            
            # This is the 'Contract' format we agreed on
            return {
                "status": "success",
                "title": product_title,
                "url": url
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
        finally:
            browser.close()