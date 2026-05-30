import requests
from bs4 import BeautifulSoup
from urlib.parse import urljoin, urlparse
import time

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