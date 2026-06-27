import json, re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus
import feedparser

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

GOOD = ["restaurant","opening","coming soon","development","housing","homes","subdivision","apartments","hotel","retail","shopping","store","road","highway","interchange","infrastructure","construction","grand opening","planned","approved","breaks ground"]
BAD = ["crime","arrest","shooting","murder","killed","fatal","deadly","lawsuit","scandal","charged","jail","prison","threat","missing","death","dies","homicide","politics","election"]
CITIES = ["Auburndale","Lakeland","Winter Haven","Davenport","Haines City","Bartow","Lake Wales","Mulberry","Polk City","Lake Alfred","Fort Meade","Frostproof","Polk County"]
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

def clean(s): return re.sub(r"\s+", " ", s or "").strip()
def positive(text):
    t=text.lower()
    return any(g in t for g in GOOD) and not any(b in t for b in BAD)
def category(text):
    t=text.lower()
    if any(w in t for w in ["restaurant","culver","coffee","cafe","burger","chicken"]): return "Restaurants"
    if any(w in t for w in ["housing","homes","subdivision","apartments","residential"]): return "Housing"
    if any(w in t for w in ["road","highway","interchange","infrastructure"]): return "Infrastructure"
    if "hotel" in t or "resort" in t: return "Hotels"
    if any(w in t for w in ["retail","store","shopping","publix","aldi","target"]): return "Retail"
    return "Development"
def city(text):
    for c in CITIES:
        if c.lower() in text.lower(): return c + ("" if c=="Polk County" else ", FL")
    return "Polk County, FL"
def image(cat):
    return {"Restaurants":"images/culvers.svg","Housing":"images/housing.svg","Infrastructure":"images/roads.svg","Hotels":"images/hotel.svg","Retail":"images/roads.svg","Development":"images/roads.svg"}.get(cat,"images/roads.svg")
def feed_url(q): return "https://news.google.com/rss/search?q="+quote_plus(q)+"&hl=en-US&gl=US&ceid=US:en"

def main():
    stories=[]; seen=set()
    for q in QUERIES:
        feed=feedparser.parse(feed_url(q))
        for e in feed.entries[:12]:
            title=clean(e.get("title","")); summary=clean(e.get("summary","")); link=e.get("link","#")
            text=title+" "+summary
            if not title or not positive(text): continue
            key=title.lower()
            if key in seen: continue
            seen.add(key)
            cat=category(text)
            stories.append({"title":title,"category":cat,"city":city(text),"date":(e.get("published","")[:16] or datetime.now(timezone.utc).date().isoformat()),"summary":summary[:220] or "Positive growth and development update for Polk County, Florida.","url":link,"image":image(cat)})
    culvers={"title":"Culver’s Opening in Auburndale","category":"Restaurants","city":"Auburndale, FL","date":"May 14, 2025","summary":"Construction is underway on US 92 West for Auburndale’s newest Culver’s location.","url":"https://whatnow.com/orlando/restaurants/culvers-opening-in-auburndale/","image":"images/culvers.svg"}
    if not any("culver" in s["title"].lower() for s in stories): stories.insert(0, culvers)
    DATA.mkdir(exist_ok=True)
    (DATA/"stories.json").write_text(json.dumps(stories[:40], indent=2), encoding="utf-8")
    (DATA/"last-updated.json").write_text(json.dumps({"updated":datetime.now(timezone.utc).isoformat()}, indent=2), encoding="utf-8")
if __name__=="__main__": main()
