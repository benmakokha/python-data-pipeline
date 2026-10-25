import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://books.toscrape.com/"

def fetch_html(url: str) -> str:
    """Fetches raw HTML content from a target URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve URL {url}: {e}")
        return None

def parse_items(html_content: str) -> list[dict]:
    """Parses raw HTML and extracts structured item data."""
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, "lxml")
    items = []

    # Locate each article container on the page
    articles = soup.find_all("article", class_="product_pod")

    for article in articles:
        title = article.h3.a["title"]
        relative_url = article.h3.a["href"]
        full_url = BASE_URL + relative_url.replace("../", "")
        
        # Extract price string
        price = article.find("p", class_="price_color").text

        items.append({
            "title": title,
            "company_or_source": "BooksToScrape",
            "location": price,  # Storing price in location field for testing
            "url": full_url,
            "description": f"Price: {price}"
        })

    logger.info(f"Successfully parsed {len(items)} items.")
    return items
