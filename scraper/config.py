# A centralized registry for multiple sites and fallback patterns
SITE_CONFIG = {
    "amazon": {
        "title": ["#productTitle", "h1#title", ".a-size-large"],
        "price": [".a-price-whole", "#priceblock_ourprice", ".a-offscreen"],
        "reviews": [".review-text-content", "[data-hook='review-body']"]
    },
    "flipkart": {
        "title": ["h1", ".VU-Z7M", ".B_NuCI"],
        "price": ["[class*='Nx9bqj']", "._30jeq3", ".div.Nx9bqj"],
        "reviews": [".Z_37Z8", ".t-ZTKy", "._2-N_i0"]
    }
}

# Generic fallback for "Universal" scraping if the site isn't listed
GENERIC_SELECTORS = {
    "title": "h1",
    "price": "[class*='price'], .price, #price",
    "reviews": "div[class*='review'], .comments"
}