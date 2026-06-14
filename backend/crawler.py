
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin, urlparse, urlsplit, urlunsplit
# import time


# def normalize_url(url):
#     # Remove fragment (#section)
#     url = url.split("#")[0]

#     parts = urlsplit(url)

#     path = parts.path.rstrip("/")

#     # Convert /index.html -> /
#     if path.endswith("/index.html"):
#         path = path[:-11]

#     return urlunsplit(
#         (
#             parts.scheme,
#             parts.netloc,
#             path,
#             "",  # remove query string
#             ""
#         )
#     )


# # creating a valid URL checker to ensure we only crawl relevant pages and avoid unnecessary resources

# def is_valid_url(url, base_domain):
#     parsed = urlparse(url)      # breaks the URL into parts (scheme, netloc, path, etc)

#     if parsed.scheme not in ("http", "https"):
#         return False

#     if parsed.netloc != base_domain:
#         return False

#     blocked_extensions = (
#         ".pdf",
#         ".jpg",
#         ".jpeg",
#         ".png",
#         ".gif",
#         ".svg",
#         ".webp",
#         ".zip",
#         ".rar",
#         ".css",
#         ".js",
#         ".ico"
#     )

#  # checks if the URL ends with any of the specified extensions, which are typically associated with non-HTML resources

#     return not url.lower().endswith(blocked_extensions)

# # creating a function to clean the texts by removing unnecessary tags and elements that do not contribute to the main content of the page

# def clean_text(soup):
#     # Remove non-content(unwanted) tags with its all children
#     for tag in soup([
#         "script",
#         "style",
#         "nav",
#         "footer",
#         "header",
#         "aside"
#     ]):
#         tag.decompose()

#     text = soup.get_text(
#         separator=" ",
#         strip=True
#     )

#     lines = [       # splitting the text into lines
#         line.strip()
#         for line in text.splitlines()
#         if line.strip()
#     ]

#     return " ".join(lines)

# # creating a function to crawl the website and extract the text content from each page file

# def crawl_website(start_url, max_pages=20):

#     start_url = normalize_url(start_url)

#     visited = set()     # to keep track of visited(processed) URLs
#     queue = [start_url]     # to keep track of URLs to be visited (initially contains the starting URL)
#     results = []        # to store the results (URL and extracted text)

#     base_domain = urlparse(start_url).netloc        # extracting the base domain from the starting URL (example --> If start_url is https://books.toscrape.com/catalogue, base_domain becomes books.toscrape.com)

#     while queue and len(visited) < max_pages:       # loop until there are URLs to visit and we haven't reached the maximum page limit

#         url = normalize_url(queue.pop(0))       # get the next URL to visit (FIFO order)

#         if url in visited:
#             continue        # if the URL has already been visited, skip it

#         print(f"\n[Attempting] {url}")

#         try:
#             response = requests.get(
#                 url,
#                 timeout=10,
#                 headers={
#                     "User-Agent":
#                     "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
#                 }
#             )

#             print("Status Code:", response.status_code)

#             if response.status_code != 200:
#                 print(
#                     f"[Skipped] Status "
#                     f"{response.status_code}"
#                 )
#                 continue

#             content_type = response.headers.get(
#                 "Content-Type",
#                 ""
#             )

#             if "text/html" not in content_type:
#                 print("[Skipped] Non-HTML page")
#                 continue

#             # Fix encoding issues
#             response.encoding = (
#                 response.apparent_encoding
#             )

#             # Use response.content to avoid Â£ issue
#             soup = BeautifulSoup(       
#                 response.content,
#                 "html.parser"
#             )

#             text = clean_text(soup)

#             print(
#                 f"Text Length: {len(text)}"
#             )

#             if len(text) < 50:
#                 print(
#                     "[Skipped] Too little text"
#                 )
#                 continue

#             title = ""

#             if soup.title:
#                 title = soup.title.get_text(
#                     strip=True
#                 )

#             results.append({
#                 "url": url,
#                 "title": title,
#                 "text": text
#             })

#             visited.add(url)

#             print(
#                 f"[Crawled] {url} "
#                 f"({len(text)} chars)"
#             )

#             # Discover links
#             for link in soup.find_all(
#                 "a",
#                 href=True
#             ):

#                 absolute = urljoin(
#                     response.url,
#                     link["href"]
#                 )

#                 absolute = normalize_url(
#                     absolute
#                 )

#                 if (
#                     absolute not in visited     
#                     and absolute not in queue
#                     and is_valid_url(       
#                         absolute,
#                         base_domain
#                     )
#                 ):
#                     queue.append(
#                         absolute
#                     )

#             time.sleep(0.5)

#         except Exception as e:
#             print(
#                 f"[Error] {url}"
#             )
#             print(e)

#     print(
#         f"\n[Done] Crawled "
#         f"{len(results)} pages "
#         f"from {base_domain}"
#     )

#     return results


# if __name__ == "__main__":      # This block only runs if executed this file directly (not if imported it elsewhere)

#     pages = crawl_website(
#         "https://books.toscrape.com",
#         max_pages=5
#     )

#     for page in pages:

#         print("\n" + "=" * 80)

#         print("URL:", page["url"])

#         print("TITLE:",
#               page["title"])

#         print("TEXT PREVIEW:")

#         print(
#             page["text"][:300]
#         )


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlsplit, urlunsplit
import time


def normalize_url(url):
    """Remove fragments, trailing slashes, and index.html suffixes."""
    url = url.split("#")[0]
    parts = urlsplit(url)
    path = parts.path.rstrip("/")
    if path.endswith("/index.html"):
        path = path[:-11]
    return urlunsplit((parts.scheme, parts.netloc, path, "", ""))


def is_valid_url(url, base_domain):
    """
    Returns True only if the URL is on the same domain
    and points to an HTML page, not a binary file.
    """
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    if parsed.netloc != base_domain:
        return False
    blocked_extensions = (
        ".pdf", ".jpg", ".jpeg", ".png", ".gif",
        ".svg", ".webp", ".zip", ".rar", ".css",
        ".js", ".ico", ".xml", ".json"
    )
    return not url.lower().endswith(blocked_extensions)


def clean_text(soup):
    """
    Extracts clean meaningful text from any website.
    Strategy: remove noise tags first, then get all remaining text.
    No hardcoded class names — works universally.
    """
    import re

    # Step 1: Remove definite non-content tags
    for tag in soup(["script", "style", "noscript",
                     "iframe", "nav", "header",
                     "footer", "aside"]):
        tag.decompose()

    # Step 2: Get all remaining text from body
    body = soup.find("body")
    if body is None:
        text = soup.get_text(separator=" ", strip=True)
    else:
        text = body.get_text(separator=" ", strip=True)

    # Step 3: Replace multiple spaces and newlines with single space
    text = re.sub(r'\s+', ' ', text).strip()

    # Step 4: Truncate to prevent embedding model overload
    return text[:5000]


def detect_js_framework(url):
    """
    Fetches the page once and checks for JavaScript framework
    fingerprints. Returns True if Playwright is needed.
    """
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        html = response.text

        js_signals = [
            'id="root"',
            'id="app"',
            'id="__next"',
            "data-reactroot",
            "ng-version",
            "__nuxt",
        ]

        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        text_length = len(soup.get_text(strip=True))

        has_js_signals = any(sig in html for sig in js_signals)
        is_empty = text_length < 200

        return has_js_signals or is_empty

    except Exception:
        return False


def crawl_with_playwright(start_url, max_pages=20):
    """
    Crawls JavaScript-rendered websites using a headless browser.
    Automatically falls back to requests if Playwright is missing.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[Warning] Playwright not installed. Falling back to requests.")
        return crawl_with_requests(start_url, max_pages)

    visited = set()
    queue = [normalize_url(start_url)]
    results = []
    base_domain = urlparse(start_url).netloc

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Block media files to speed up crawling significantly
        page.route(
            "**/*.{png,jpg,jpeg,gif,svg,webp,woff,woff2,mp4,mp3}",
            lambda route: route.abort()
        )

        while queue and len(visited) < max_pages:
            url = normalize_url(queue.pop(0))

            if url in visited:
                continue

            print(f"\n[Playwright] Attempting: {url}")

            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(1500)

                html = page.content()
                soup = BeautifulSoup(html, "html.parser")
                text = clean_text(soup)

                if len(text) < 50:
                    print(f"[Skipped] Too little text")
                    continue

                title = ""
                if soup.title:
                    title = soup.title.get_text(strip=True)

                results.append({"url": url, "title": title, "text": text})
                visited.add(url)
                print(f"[Crawled] {url} ({len(text)} chars)")

                for link in soup.find_all("a", href=True):
                    absolute = urljoin(url, link["href"])
                    absolute = normalize_url(absolute)
                    if (
                        absolute not in visited
                        and absolute not in queue
                        and is_valid_url(absolute, base_domain)
                    ):
                        queue.append(absolute)

                time.sleep(0.3)

            except Exception as e:
                print(f"[Error] {url}: {e}")
                continue

        browser.close()

    print(f"\n[Done] Crawled {len(results)} pages with Playwright")
    return results


def crawl_with_requests(start_url, max_pages=20):
    """
    Fast requests-based crawler for static HTML sites.
    """
    start_url = normalize_url(start_url)
    visited = set()
    queue = [start_url]
    results = []
    base_domain = urlparse(start_url).netloc

    while queue and len(visited) < max_pages:
        url = normalize_url(queue.pop(0))

        if url in visited:
            continue

        print(f"\n[Attempting] {url}")

        try:
            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                }
            )

            print(f"Status Code: {response.status_code}")

            if response.status_code != 200:
                print(f"[Skipped] Status {response.status_code}")
                continue

            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                print(f"[Skipped] Non-HTML: {content_type}")
                continue

            # Pass raw bytes to let BeautifulSoup detect encoding
            # from meta tags — avoids the Â£ encoding bug
            soup = BeautifulSoup(response.content, "html.parser")
            text = clean_text(soup)


            print(f"Text length: {len(text)}")

            if len(text) < 50:
                print(f"[Skipped] Too little text: {len(text)} chars")
                continue

            title = ""
            if soup.title:
                title = soup.title.get_text(strip=True)

            results.append({"url": url, "title": title, "text": text})
            visited.add(url)
            print(f"[Crawled] {url} ({len(text)} chars)")

            for link in soup.find_all("a", href=True):
                absolute = urljoin(response.url, link["href"])
                absolute = normalize_url(absolute)
                if (
                    absolute not in visited
                    and absolute not in queue
                    and is_valid_url(absolute, base_domain)
                ):
                    queue.append(absolute)

            time.sleep(0.5)

        except Exception as e:
            print(f"[Error] {url}: {e}")
            continue

    print(f"\n[Done] Crawled {len(results)} pages from {base_domain}")
    return results


def crawl_website(start_url, max_pages=20):
    """
    Smart entry point that auto-detects whether the site
    needs JavaScript rendering or can use the fast static crawler.
    """
    print(f"[Detecting] Checking if {start_url} needs JavaScript rendering...")

    needs_js = detect_js_framework(start_url)

    if needs_js:
        print("[Detected] JavaScript-rendered site — using Playwright")
        return crawl_with_playwright(start_url, max_pages)
    else:
        print("[Detected] Static site — using requests crawler")
        return crawl_with_requests(start_url, max_pages)


if __name__ == "__main__":
    print("=== Testing static site ===")
    pages = crawl_website("https://books.toscrape.com", max_pages=3)
    print(f"Pages crawled: {len(pages)}")

    for page in pages:
        print("\n" + "=" * 60)
        print(f"URL: {page['url']}")
        print(f"Title: {page['title']}")
        print(f"Text preview: {page['text'][:300]}")