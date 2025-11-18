import feedparser
import re
import requests
import os

FEED_URL = "https://politepol.com/fd/QMwGP4F4EnYO.xml"

PATTERN = re.compile(
    r"^https://sarbojonkotha\.info/sarbojonkotha-([0-9]+)-([0-9]+)/$"
)

OUTPUT_FILE = "sarbojonkotha.html"   # always this name

def main():
    feed = feedparser.parse(FEED_URL)

    candidates = []

    for entry in feed.entries:
        url = entry.link.strip()
        m = PATTERN.match(url)
        if m:
            x = int(m.group(1))   # first number
            y = int(m.group(2))   # second number
            candidates.append((x, y, url))

    if not candidates:
        print("No matching URLs found.")
        return

    # Sort by highest X, then highest Y
    candidates.sort(key=lambda t: (t[0], t[1]), reverse=True)

    # Pick the single best URL
    _, _, selected_url = candidates[0]

    save_page(selected_url)


def save_page(url):
    html = requests.get(url, timeout=10).text

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print("Saved as:", OUTPUT_FILE)


if __name__ == "__main__":
    main()