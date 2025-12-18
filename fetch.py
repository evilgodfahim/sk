import feedparser
import re
import requests
import os
import json

FEED_URL = "https://politepaul.com/fd/QMwGP4F4EnYO.xml"
PATTERN = re.compile(
    r"^https://sarbojonkotha\.info/sarbojonkotha-([0-9]+)-([0-9]+)/$"
)
OUTPUT_FILE = "sarbojonkotha.html"
TRACK_FILE = "last.json"

def main():
    feed = feedparser.parse(FEED_URL)

    candidates = []

    for entry in feed.entries:
        url = entry.link.strip()
        m = PATTERN.match(url)
        if m:
            x = int(m.group(1))
            y = int(m.group(2))
            candidates.append((x, y, url))

    if not candidates:
        print("No matching URLs found.")
        return

    # Sort by highest X, then highest Y
    candidates.sort(key=lambda t: (t[0], t[1]), reverse=True)

    # Pick the single best URL
    _, _, selected_url = candidates[0]

    # Check tracking JSON
    last_url = load_last_url()
    if selected_url == last_url:
        print("No new page. Skipping download.")
        return

    # New URL found, download and save
    save_page(selected_url)
    save_last_url(selected_url)


def save_page(url):
    html = requests.get(url, timeout=10).text
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved as:", OUTPUT_FILE)


def load_last_url():
    if not os.path.exists(TRACK_FILE):
        return None
    try:
        with open(TRACK_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("url")
    except:
        return None


def save_last_url(url):
    data = {"url": url}
    with open(TRACK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print("Updated tracking JSON.")


if __name__ == "__main__":
    main()