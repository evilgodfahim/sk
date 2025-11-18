import feedparser
import re
import requests
import os
from datetime import datetime

FEED_URL = "https://politepol.com/fd/QMwGP4F4EnYO.xml"

PATTERN = re.compile(
    r"^https://sarbojonkotha\.info/sarbojonkotha-[0-9]+-[0-9]+/$"
)

def main():
    feed = feedparser.parse(FEED_URL)

    os.makedirs("pages", exist_ok=True)

    for entry in feed.entries:
        url = entry.link.strip()

        if PATTERN.match(url):
            save_page(url)

def save_page(url):
    html = requests.get(url, timeout=10).text

    slug = url.rstrip("/").split("/")[-1]      # example: sarbojonkotha-12-1
    filename = f"pages/{slug}.html"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print("Saved:", filename)

if __name__ == "__main__":
    main()
