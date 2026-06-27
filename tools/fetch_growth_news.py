import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

import feedparser

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

POSITIVE = [
    "restaurant", "opening", "coming soon", "development", "housing", "homes",
    "subdivision", "apartments", "hotel", "retail", "shopping", "store",
    "road", "highway", "interchange", "infrastructure", "construction",
    "business expansion", "grand opening", "breaks ground", "planned", "approved"
]

NEGATIVE = [
    "crime", "arrest", "arrested", "shooting", "murder", "killed", "fatal",
    "deadly", "crash kills", "lawsuit", "scandal", "charged", "jail",
    "prison", "threat", "missing", "death", "dies", "homicide", "fraud",
    "politics", "election"
]

CITY_PATTERNS = [
    "Auburndale", "Lakeland", "Winter Haven", "Davenport", "Haines City",
    "Bartow", "Lake Wales", "Mulberry", "Polk City", "Lake Alfred",
    "Fort Meade", "Frostproof", "Poinciana", "Polk County"
]

QUERIES = [
    'Polk County FL new restaurant development housing highway hotel retail',
    'site:whatnow.com/orlando Polk County restaurant Auburndale Lakeland Davenport',
    'Auburndale FL new restaurant development',
    'Lakeland FL new restaurant development housing hotel retail',
    'Winter Haven FL development restaurant hotel housing',
    'Davenport FL development housing restaurant hotel retail',
    'Haines City FL development restaurant housing',
    'Polk County FL road highway interchange construction'
]

def clean(text):
    return re.sub(r"\s+", " ", text or "").strip()

def is_positive(text):
    t = text.lower()
    if any(bad in t for bad in NEGATIVE):
        return False
    return any(good in t for good in POSITIVE)

def category_for(text):
    t = text.lower()
    if any(w in t for w in ["restaurant", "culver", "coffee", "cafe", "chicken", "taco", "burger"]):
        return "Restaurants"
    if any(w in t for w in ["housing", "homes", "subdivision", "apartments", "residential"]):
        return "Housing"
    if any(w in t for w in ["road", "highway", "interchange", "fdot", "infrastructure"]):
        return "Roads"
    if "hotel" in t or "resort" in t:
        return "Hotels"
    if any(w in t for w in ["retail", "store", "shopping", "publix", "aldi", "target"]):
        return "Retail"
    return "Development"

def city_for(text):
    for city in CITY_PATTERNS:
        if city.lower() in text.lower():
            return city
    return "Polk County"

def google_news_url(query):
    return "https://news.google.com/rss/search?q=" + quote_plus(query) + "&hl=en-US&gl=US&ceid=US:en"

def main():
    stories = []
    seen = set()

    for query in QUERIES:
        feed = feedparser.parse(google_news_url(query))
        for entry in feed.entries[:12]:
            title = clean(entry.get("title", ""))
            summary = clean(entry.get("summary", ""))
            url = entry.get("link", "#")
            text = f"{title} {summary}"
            if not title or not is_positive(text):
                continue
            key = title.lower()
            if key in seen:
                continue
            seen.add(key)
            stories.append({
                "title": title,
                "category": category_for(text),
                "city": city_for(text),
                "date": entry.get("published", "")[:16] or datetime.now(timezone.utc).date().isoformat(),
                "summary": summary[:220] if summary else "Positive growth and development update for Polk County, Florida.",
                "url": url,
                "source": "Google News"
            })

    # Always keep the known Culver's lead near top if not present
    culvers = {
        "title": "Culver’s Opening in Auburndale",
        "category": "Restaurants",
        "city": "Auburndale",
        "date": "2025-05-14",
        "summary": "Culver’s is planned for Auburndale, adding another restaurant option along the city’s growing commercial corridor.",
        "url": "https://whatnow.com/orlando/restaurants/culvers-opening-in-auburndale/",
        "source": "What Now Orlando"
    }
    if not any("culver" in s["title"].lower() for s in stories):
        stories.insert(0, culvers)

    DATA.mkdir(exist_ok=True)
    (DATA / "stories.json").write_text(json.dumps(stories[:40], indent=2), encoding="utf-8")
    (DATA / "last-updated.json").write_text(json.dumps({
        "updated": datetime.now(timezone.utc).isoformat(),
        "source": "GitHub Actions + Google News RSS queries"
    }, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
