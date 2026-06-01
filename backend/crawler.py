
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlsplit, urlunsplit
import time


def normalize_url(url):
    # Remove fragment (#section)
    url = url.split("#")[0]

    parts = urlsplit(url)

    path = parts.path.rstrip("/")

    # Convert /index.html -> /
    if path.endswith("/index.html"):
        path = path[:-11]

    return urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            path,
            "",  # remove query string
            ""
        )
    )


# creating a valid URL checker to ensure we only crawl relevant pages and avoid unnecessary resources

def is_valid_url(url, base_domain):
    parsed = urlparse(url)      # breaks the URL into parts (scheme, netloc, path, etc)

    if parsed.scheme not in ("http", "https"):
        return False

    if parsed.netloc != base_domain:
        return False

    blocked_extensions = (
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".svg",
        ".webp",
        ".zip",
        ".rar",
        ".css",
        ".js",
        ".ico"
    )

 # checks if the URL ends with any of the specified extensions, which are typically associated with non-HTML resources

    return not url.lower().endswith(blocked_extensions)

# creating a function to clean the texts by removing unnecessary tags and elements that do not contribute to the main content of the page

def clean_text(soup):
    # Remove non-content(unwanted) tags with its all children
    for tag in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header",
        "aside"
    ]):
        tag.decompose()

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    lines = [       # splitting the text into lines
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    return " ".join(lines)

# creating a function to crawl the website and extract the text content from each page file

def crawl_website(start_url, max_pages=20):

    start_url = normalize_url(start_url)

    visited = set()     # to keep track of visited(processed) URLs
    queue = [start_url]     # to keep track of URLs to be visited (initially contains the starting URL)
    results = []        # to store the results (URL and extracted text)

    base_domain = urlparse(start_url).netloc        # extracting the base domain from the starting URL (example --> If start_url is https://books.toscrape.com/catalogue, base_domain becomes books.toscrape.com)

    while queue and len(visited) < max_pages:       # loop until there are URLs to visit and we haven't reached the maximum page limit

        url = normalize_url(queue.pop(0))       # get the next URL to visit (FIFO order)

        if url in visited:
            continue        # if the URL has already been visited, skip it

        print(f"\n[Attempting] {url}")

        try:
            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                }
            )

            print("Status Code:", response.status_code)

            if response.status_code != 200:
                print(
                    f"[Skipped] Status "
                    f"{response.status_code}"
                )
                continue

            content_type = response.headers.get(
                "Content-Type",
                ""
            )

            if "text/html" not in content_type:
                print("[Skipped] Non-HTML page")
                continue

            # Fix encoding issues
            response.encoding = (
                response.apparent_encoding
            )

            # Use response.content to avoid Â£ issue
            soup = BeautifulSoup(       
                response.content,
                "html.parser"
            )

            text = clean_text(soup)

            print(
                f"Text Length: {len(text)}"
            )

            if len(text) < 50:
                print(
                    "[Skipped] Too little text"
                )
                continue

            title = ""

            if soup.title:
                title = soup.title.get_text(
                    strip=True
                )

            results.append({
                "url": url,
                "title": title,
                "text": text
            })

            visited.add(url)

            print(
                f"[Crawled] {url} "
                f"({len(text)} chars)"
            )

            # Discover links
            for link in soup.find_all(
                "a",
                href=True
            ):

                absolute = urljoin(
                    response.url,
                    link["href"]
                )

                absolute = normalize_url(
                    absolute
                )

                if (
                    absolute not in visited     
                    and absolute not in queue
                    and is_valid_url(       
                        absolute,
                        base_domain
                    )
                ):
                    queue.append(
                        absolute
                    )

            time.sleep(0.5)

        except Exception as e:
            print(
                f"[Error] {url}"
            )
            print(e)

    print(
        f"\n[Done] Crawled "
        f"{len(results)} pages "
        f"from {base_domain}"
    )

    return results


if __name__ == "__main__":      # This block only runs if executed this file directly (not if imported it elsewhere)

    pages = crawl_website(
        "https://books.toscrape.com",
        max_pages=5
    )

    for page in pages:

        print("\n" + "=" * 80)

        print("URL:", page["url"])

        print("TITLE:",
              page["title"])

        print("TEXT PREVIEW:")

        print(
            page["text"][:300]
        )