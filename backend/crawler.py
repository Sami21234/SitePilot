# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin, urlparse
# import time

# # creating a valid URL checker to ensure we only crawl relevant pages and avoid unnecessary resources

# def is_valid_url(url, base_domain):
#     parsed = urlparse(url)      # breaks the URL into parts (scheme, netloc, path, etc)
#     return(
#         parsed.scheme in ("http", "https")
#         and parsed.netloc == base_domain
#         and not any(            # checks if the URL ends with any of the specified extensions, which are typically associated with non-HTML resources
#             url.endswith(ext)
#             for ext in [".pdf", ".jpg", ".png", ".zip", ".css", ".js"]
#         )
#     )

# # creating a function to clean the texts by removing unnecessary tags and elements that do not contribute to the main content of the page

# def clean_text(soup):
#     for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
#         tag.decompose()     # removing unwanted tags with its all children 

#     main = soup.find("main") or soup.find("article")    # trying to find the main content of the page, if not found then we will use the whole text of the page
#     if main:
#         text = main.get_text(separator=" ", strip=True)
#     else:
#         text = soup.get_text(separator=" ", strip=True)

#     lines = [line.strip() for line in text.splitlines() if line.strip()]        # splitting the text into lines
#     return " ".join(lines)

# # creating a function to crawl the website and extract the text content from each page file

# def crawl_website(start_url, max_pages=20):
#     visited = set()        # to keep track of visited(processed) URLs

#     to_visit = [start_url]     # to keep track of URLs to be visited (initially contains the starting URL)

#     results = []       # to store the results (URL and extracted text)

#     base_domain = urlparse(start_url).netloc        # extracting the base domain from the starting URL (example --> If start_url is https://books.toscrape.com/catalogue, base_domain becomes books.toscrape.com)
    
#     while to_visit and len(visited) < max_pages:     # loop until there are URLs to visit and we haven't reached the maximum page limit
#         url = to_visit.pop(0)     # get the next URL to visit (FIFO order)

#         if url in visited:
#             continue       # if the URL has already been visited, skip it

#         try:
#             response = requests.get(url, timeout=10, headers={
#                 "User-Agent": "Mozilla/5.0 (compatible; SitePilot/1.0)"
#             })
        
#             if response.status_code != 200:
#                 continue
                
#             content_type = response.headers.get("Content-Type", "")
        
#             if "text/html" not in content_type:
#                 continue
            
#             soup = BeautifulSoup(response.text, "html.parser")      # Converts the raw HTML text into a searchable BeautifulSoup objects (tree sturcture)
#             text = clean_text(soup)     # Passing that object into the clean_text function created earlier to get clean content text
        
#             if len(text) < 100:
#                 continue
        
#             results.append({
#                 "url": url,
#                 "text": text,
#                 "title": soup.title.string if soup.title else ""
#             })
        
#             visited.add(url)        # Adding the URL to the visited set so it won't be requested again
#             print(f"[Crawled {url} - {len(text)} characters]")      # printing the statement about the crawled url and its characters
        
#             for link in soup.find_all("a", href=True):
#                 absolute = urljoin(url, link["href"])
#                 absolute = absolute.split("#")[0]       # (e.g., page.html#section1 becomes page.html) so the crawler doesn't treat them as separate pages
#                 absolute = absolute.rstrip("/")     # removes trailing slashes so, example.com and example.com/ are treated as the exact same URL.

#                 if absolute not in visited and is_valid_url(absolute, base_domain):
#                     to_visit.append(absolute)     # If the discovered link hasn't been visited yet and passes the domain/file checks, it is added to the back of the to_visit queue.
            
#             time.sleep(0.5)
        
#         except Exception as e:
#             print(f"[Error] {url}: {e}")
#             continue

#     print(f"\n[Done] Crawled {len(results)} pages from {base_domain}")
#     return results

# if __name__ == "__main__":      # This block only runs if executed this file directly (not if imported it elsewhere)
#     pages = crawl_website("https://books.toscrape.com", max_pages=5)
#     for page in pages:
#         print(f"\nURL: {page['url']}")
#         print(f"Title: {page['title']}")
#         print(f"Text preview: {page['text'][:200]}")



# import time
# from urllib.parse import urljoin, urlparse

# from bs4 import BeautifulSoup
# import requests

# # Creating a valid URL checker to ensure we only crawl relevant pages and avoid unnecessary resources
# def is_valid_url(url, base_domain):
#     parsed = urlparse(url)  # Breaks the URL into parts (scheme, netloc, path, etc)
#     return (
#         parsed.scheme in ("http", "https")
#         and parsed.netloc == base_domain
#         and not any(  # Checks if the URL ends with specified non-HTML extensions
#             url.endswith(ext)
#             for ext in [".pdf", ".jpg", ".png", ".zip", ".css", ".js"]
#         )
#     )

# # Creating a function to clean text by removing unnecessary HTML structural tags
# def clean_text(soup):
#     # Only remove things that NEVER contain readable text content
#     for tag in soup(["script", "style"]):
#         tag.decompose() 

#     # Look for common content wrappers
#     main = soup.find("main") or soup.find("article") or soup.find("div", class_="page_inner")
#     if main:
#         text = main.get_text(separator=" ", strip=True)
#     else:
#         text = soup.get_text(separator=" ", strip=True)

#     # Split into structural blocks, clean up empty lines
#     lines = [line.strip() for line in text.splitlines() if line.strip()]
#     return " ".join(lines)

# # Creating a function to crawl the website and extract text content sequentially
# def crawl_website(start_url, max_pages=20):
#     visited = set()         # To keep track of visited (processed) URLs
#     to_visit = [start_url]  # Uniformly renamed queue to 'to_visit' for clarity
#     results = []            # To store final results (URL, title, and extracted text)

#     base_domain = urlparse(start_url).netloc  # Extracting core domain (e.g., books.toscrape.com)
    
#     while to_visit and len(visited) < max_pages:  # Loop until queue is empty or page limit is met
#         url = to_visit.pop(0)                     # Get next URL to visit (FIFO queue order)

#         if url in visited:
#             continue                              # Skip if the URL has already been processed

#         try:
#             # Realigned all indentation levels properly to exactly 12 spaces inside this block
#             response = requests.get(url, timeout=10, headers={
#                 "User-Agent": "Mozilla/5.0 (compatible; SitePilot/1.0)"
#             })
        
#             if response.status_code != 200:
#                 print(f"[Skipped] {url} returned HTTP status code: {response.status_code}")
#                 continue
                
#             content_type = response.headers.get("Content-Type", "")
        
#             if "text/html" not in content_type:
#                 print(f"[Skipped] {url} is not HTML (Content-Type: {content_type})")
#                 continue
            
#             soup = BeautifulSoup(response.text, "html.parser")
#             text = clean_text(soup)
            
#             # 🔍 TEMPORARY DEBUG PRINT: Check if text filtering is erasing the page body
#             print(f"[Debug] URL: {url} | Cleaned text character count: {len(text)}")
        
#             if len(text) < 100:
#                 print(f"[Skipped] {url} text length is too short ({len(text)} chars).")
#                 continue
        
#             results.append({
#                 "url": url,
#                 "text": text,
#                 "title": soup.title.string if soup.title else ""
#             })
        
#             visited.add(url)
#             print(f"[Crawled] {url} - {len(text)} characters")
        
#             for link in soup.find_all("a", href=True):
#                 absolute = urljoin(url, link["href"])
#                 absolute = absolute.split("#")[0]       # Strip anchor fragments
#                 absolute = absolute.rstrip("/")         # Remove trailing slashes for standard string matching

#                 if absolute not in visited and is_valid_url(absolute, base_domain):
#                     to_visit.append(absolute)            # Safely append back to the target queue
            
#             time.sleep(0.5)
        
#         except Exception as e:
#             print(f"[Error] {url}: {e}")
#             continue

#     print(f"\n[Done] Crawled {len(results)} pages from {base_domain}")
#     return results

# if __name__ == "__main__":
#     # Added explicit trailing slash to standard home domain to prevent domain mismatch skips
#     pages = crawl_website("https://books.toscrape.com/", max_pages=5)
#     for page in pages:
#         print(f"\nURL: {page['url']}")
#         print(f"Title: {page['title']}")
#         print(f"Text preview: {page['text'][:200]}")

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time


def normalize_url(url):
    url = url.split("#")[0]

    if url.endswith("/index.html"):
        url = url[:-11]

    return url.rstrip("/")


def is_valid_url(url, base_domain):
    parsed = urlparse(url)

    return (
        parsed.scheme in ("http", "https")
        and parsed.netloc == base_domain
        and not any(
            url.lower().endswith(ext)
            for ext in [
                ".pdf",
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".zip",
                ".css",
                ".js",
            ]
        )
    )


def clean_text(soup):
    for tag in soup(
        [
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
        ]
    ):
        tag.decompose()

    main = soup.find("main") or soup.find("article")

    if main:
        text = main.get_text(separator=" ", strip=True)
    else:
        text = soup.get_text(separator=" ", strip=True)

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    return " ".join(lines)


def crawl_website(start_url, max_pages=20):
    start_url = normalize_url(start_url)

    visited = set()
    to_visit = [start_url]
    results = []

    base_domain = urlparse(start_url).netloc

    while to_visit and len(visited) < max_pages:

        url = normalize_url(to_visit.pop(0))

        if url in visited:
            continue

        print(f"\n[Attempting] {url}")

        try:
            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "(Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 "
                        "(KHTML, like Gecko) "
                        "Chrome/120.0 Safari/537.36"
                    )
                },
            )

            print("Status Code:", response.status_code)

            if response.status_code != 200:
                print(f"[Skipped] Status {response.status_code}")
                continue

            content_type = response.headers.get(
                "Content-Type", ""
            )

            if "text/html" not in content_type:
                print("[Skipped] Non-HTML page")
                continue

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            text = clean_text(soup)

            print("Text Length:", len(text))

            if len(text) < 100:
                print("[Skipped] Too little content")
                continue

            title = (
                soup.title.get_text(strip=True)
                if soup.title
                else ""
            )

            results.append(
                {
                    "url": url,
                    "title": title,
                    "text": text,
                }
            )

            visited.add(url)

            print(
                f"[Crawled] {url} "
                f"({len(text)} chars)"
            )

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
                    and absolute not in to_visit
                    and is_valid_url(
                        absolute,
                        base_domain
                    )
                ):
                    to_visit.append(absolute)

            time.sleep(0.5)

        except Exception as e:
            print(f"[Error] {url}")
            print(e)

    print(
        f"\n[Done] Crawled "
        f"{len(results)} pages "
        f"from {base_domain}"
    )

    return results


if __name__ == "__main__":

    pages = crawl_website(
        "https://books.toscrape.com",
        max_pages=5
    )

    for page in pages:
        print("\n" + "=" * 80)
        print("URL:", page["url"])
        print("TITLE:", page["title"])
        print("TEXT PREVIEW:")
        print(page["text"][:300])