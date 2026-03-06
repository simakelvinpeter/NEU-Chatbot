"""
NEU Website Crawler — BeautifulSoup + requests
Scrapes key sections of neu.edu.tr and saves clean paragraph chunks to JSON.

Usage:
    cd backend
    python scraper/neu_crawler.py

Output:
    backend/scraper/neu_scraped_data.json
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import time
import re
import os

# ─── Config ──────────────────────────────────────────────────────────────────

DOMAIN = "neu.edu.tr"
MAX_PAGES = 300          # hard cap
DEPTH_LIMIT = 2          # follow links this many levels deep
DELAY = 0.8              # seconds between requests
REQUEST_TIMEOUT = 12

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "neu_scraped_data.json")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

# Priority seed URLs — cover every major topic students ask about
SEED_URLS = [
    # Core
    "https://neu.edu.tr/?lang=en",
    "https://neu.edu.tr/about-us/?lang=en",
    "https://neu.edu.tr/about-us/our-university-in-numbers/?lang=en",
    "https://neu.edu.tr/about-us/vision-mission-our-values/?lang=en",
    "https://neu.edu.tr/contact/?lang=en",

    # Admissions
    "https://neu.edu.tr/students/international-student-office/?lang=en",
    "https://neu.edu.tr/students/international-students-admission/?lang=en",
    "https://neu.edu.tr/students/scholarships/?lang=en",
    "https://neu.edu.tr/students/foundation-program/?lang=en",
    "https://neu.edu.tr/students/english-preparatory-school/?lang=en",

    # Academic
    "https://neu.edu.tr/academic/faculties/?lang=en",
    "https://neu.edu.tr/academic/applied-schools/?lang=en",
    "https://neu.edu.tr/academic/vocational-schools/?lang=en",
    "https://neu.edu.tr/academic/institute-of-graduate-studies/?lang=en",
    "https://neu.edu.tr/academic/grand-library/?lang=en",
    "https://neu.edu.tr/academic/academic-calendar/?lang=en",

    # Campus life
    "https://neu.edu.tr/campus-life/dormitories/?lang=en",
    "https://neu.edu.tr/campus-life/transportation/?lang=en",
    "https://neu.edu.tr/campus-life/canteens-and-cafeterias/?lang=en",
    "https://neu.edu.tr/campus-life/health/?lang=en",
    "https://neu.edu.tr/campus-life/sports/?lang=en",
    "https://neu.edu.tr/campus-life/student-clubs/?lang=en",
    "https://neu.edu.tr/campus-life/museums/?lang=en",
    "https://neu.edu.tr/campus-life/life-in-north-cyprus/?lang=en",
    "https://neu.edu.tr/campus-life/other-services/?lang=en",
    "https://neu.edu.tr/campus-life/ataturk-culture-and-congress-centre/?lang=en",

    # Students
    "https://neu.edu.tr/students/accommodation/?lang=en",
    "https://neu.edu.tr/students/summer-school/?lang=en",
    "https://neu.edu.tr/students/double-major-and-minor-major-programs/?lang=en",
    "https://neu.edu.tr/students/student-residence-permit/?lang=en",
    "https://neu.edu.tr/students/follow-up-and-coordination-unit/about-follow-up-and-coordination-unit/?lang=en",

    # Research
    "https://neu.edu.tr/research/center-of-excellence/?lang=en",
    "https://neu.edu.tr/research/desam-research-institute/?lang=en",
    "https://neu.edu.tr/research/laboratories/?lang=en",

    # Rankings
    "https://neu.edu.tr/about-us/rankings-accreditations-equivalences-memberships/?lang=en",

    # Hospital (external but NEU-owned)
    "https://neareasthospital.com/kurumsal/",
]

# URL patterns to skip
SKIP_PATTERNS = re.compile(
    r"\.(pdf|jpg|jpeg|png|gif|svg|zip|doc|docx|xls|xlsx|mp4|mp3|avi|ico|woff|woff2|ttf|css|js)$"
    r"|/wp-admin/"
    r"|/wp-json/"
    r"|/feed/"
    r"|/xmlrpc"
    r"|/login"
    r"|/register"
    r"|/cart"
    r"|/checkout"
    r"|action="
    r"|/page/\d"
    r"|replytocom=",
    re.IGNORECASE,
)

# Tags whose content should be stripped
STRIP_TAGS = ["script", "style", "nav", "footer", "header", "aside",
              "noscript", "iframe", "form", "button", "svg", "img"]

# ─── Helpers ─────────────────────────────────────────────────────────────────

def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    if not parsed.scheme.startswith("http"):
        return False
    if DOMAIN not in parsed.netloc:
        return False
    if SKIP_PATTERNS.search(url):
        return False
    return True


def clean_text(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_chunks(soup: BeautifulSoup, url: str, title: str) -> list[dict]:
    """
    Extract meaningful paragraph-level chunks from a page.
    Each chunk is a dict with url, title, and content.
    """
    for tag in soup(STRIP_TAGS):
        tag.decompose()

    # Try main content area first
    main = (
        soup.find("main")
        or soup.find("article")
        or soup.find("div", class_=re.compile(r"content|entry|post|page", re.I))
        or soup.find("body")
    )

    chunks = []
    if not main:
        return chunks

    # Collect paragraphs and headings
    current_heading = title or ""
    buffer = []

    for elem in main.find_all(["h1", "h2", "h3", "h4", "p", "li", "td", "th"]):
        tag_name = elem.name
        text = elem.get_text(separator=" ", strip=True)
        text = clean_text(text)

        if not text or len(text) < 20:
            continue

        if tag_name in ("h1", "h2", "h3", "h4"):
            # Flush current buffer as a chunk
            if buffer:
                chunk_text = " ".join(buffer)
                if len(chunk_text) > 60:
                    chunks.append({
                        "url": url,
                        "title": title,
                        "section": current_heading,
                        "content": chunk_text,
                    })
            current_heading = text
            buffer = []
        else:
            buffer.append(text)
            # Flush when buffer gets big enough
            if sum(len(t) for t in buffer) > 800:
                chunk_text = " ".join(buffer)
                chunks.append({
                    "url": url,
                    "title": title,
                    "section": current_heading,
                    "content": chunk_text,
                })
                buffer = []

    # Flush remainder
    if buffer:
        chunk_text = " ".join(buffer)
        if len(chunk_text) > 60:
            chunks.append({
                "url": url,
                "title": title,
                "section": current_heading,
                "content": chunk_text,
            })

    return chunks


def get_internal_links(soup: BeautifulSoup, base_url: str) -> list[str]:
    links = []
    for tag in soup.find_all("a", href=True):
        full = urljoin(base_url, tag["href"].strip())
        # Normalise: strip fragments and trailing slash variations
        full = full.split("#")[0].rstrip("/")
        if full and is_valid_url(full) and full not in links:
            links.append(full)
    return links


# ─── Crawler ─────────────────────────────────────────────────────────────────

def crawl():
    session = requests.Session()
    session.headers.update(HEADERS)

    visited: set[str] = set()
    # Queue items: (url, depth)
    queue: list[tuple[str, int]] = [(u.rstrip("/"), 0) for u in SEED_URLS]

    all_chunks: list[dict] = []
    pages_scraped = 0

    print(f"Starting NEU crawler — max {MAX_PAGES} pages, depth {DEPTH_LIMIT}")
    print(f"Output → {OUTPUT_FILE}\n")

    while queue and pages_scraped < MAX_PAGES:
        url, depth = queue.pop(0)

        # Normalise
        url = url.split("#")[0].rstrip("/")
        if url in visited:
            continue
        if not is_valid_url(url):
            continue

        visited.add(url)

        try:
            resp = session.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            if resp.status_code != 200:
                print(f"  [skip {resp.status_code}] {url}")
                continue

            content_type = resp.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                continue

            resp.encoding = "utf-8"
            soup = BeautifulSoup(resp.text, "html.parser")

            title = soup.title.get_text(strip=True) if soup.title else url

            chunks = extract_chunks(soup, url, title)
            all_chunks.extend(chunks)
            pages_scraped += 1

            print(f"  [{pages_scraped:3d}] {len(chunks):3d} chunks  {url}")

            # Follow links if depth allows
            if depth < DEPTH_LIMIT:
                for link in get_internal_links(soup, url):
                    if link not in visited:
                        queue.append((link, depth + 1))

            time.sleep(DELAY)

        except requests.exceptions.Timeout:
            print(f"  [timeout] {url}")
        except Exception as exc:
            print(f"  [error] {url} — {exc}")

    print(f"\nDone. Scraped {pages_scraped} pages → {len(all_chunks)} chunks")

    # Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"Saved to {OUTPUT_FILE}")
    return all_chunks


if __name__ == "__main__":
    crawl()
