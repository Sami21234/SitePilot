import requests
from bs4 import BeautifulSoup
from urlib.parse import urljoin, urlparse
import time

# creating a valid URL checker to ensure we only crawl relevant pages and avoid unnecessary resources

def is_valid_url(url, base_domain):
    parsed = urlparse(url)
    return(
        parsed.scheme in ("http", "https")
        and parsed.netloc == base_domain
        and not any(
            url.endswith(ext)
            for ext in [".pdf", ".jpg", ".png", ".zip", ".css", ".js"]
        )
    )

# creating a function to clean the texts by removing unnecessary tags and elements that do not contribute to the main content of the page

def clean_text(soup):
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()     # removing unwanted tags with its all children 

    main = soup.find("main") or soup.find("article")
    if main:
        text = main.get_text(separator=" ", strip=True)
    else:
        text = soup.get_text(separator=" ", strip=True)

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return " ".join(lines)