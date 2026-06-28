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
def ok(text):
    t=text.lower()
    return any(g in t for g in GOOD) and not any(b in t for b in BAD)
def cat(text):
    t=text.lower()
    if any(w in t for w in ["restaurant","culver","coffee","cafe","burger","chicken"]): return "Restaurants"
    if any(w in t for w in ["housing","homes","subdivision","apartments","residential"]): return "Housing"
    if any(w in t for w in ["hotel","resort"]): return "Hotels"
    if any(w in t for w in ["road","highway","interchange","infrastructure"]): return "Infrastructure"
    if any(w in t for w in ["retail","store","shopping","publix","aldi","target"]): return "Retail"
    return "Development"
def city(text):
    for c in CITIES:
        if c.lower() in text.lower(): return c + ("" if c=="Polk County" else ", FL")
    return "Polk County, FL"
def img(category):
    return {"Restaurants":"images/restaurant-card.svg","Housing":"images/housing-card.svg","Infrastructure":"images/road-card.svg","Hotels":"images/hotel-card.svg","Retail":"images/road-card.svg","Development":"images/road-card.svg"}.get(category,"images/road-card.svg")
def feed(q): return "https://news.google.com/rss/search?q="+quote_plus(q)+"&hl=en-US&gl=US&ceid=US:en"

def main():
    stories=[]; seen=set()
    for q in QUERIES:
        parsed=feedparser.parse(feed(q))
        for e in parsed.entries[:12]:
            title=clean(e.get("title","")); summary=clean(e.get("summary","")); link=e.get("link","#")
            text=title+" "+summary
            if not title or not ok(text): continue
            key=title.lower()
            if key in seen: continue
            seen.add(key)
            category=cat(text)
            stories.append({"title":title,"category":category,"city":city(text),"date":(e.get("published","")[:16] or datetime.now(timezone.utc).date().isoformat()),"summary":summary[:150] or "Positive growth and development update for Polk County, Florida.","url":link,"image":img(category)})
    if not stories:
        stories = json.loads((DATA/"stories.json").read_text())
    DATA.mkdir(exist_ok=True)
    (DATA/"stories.json").write_text(json.dumps(stories[:12], indent=2), encoding="utf-8")
    (DATA/"last-updated.json").write_text(json.dumps({"updated":datetime.now(timezone.utc).isoformat()}, indent=2), encoding="utf-8")
if __name__=="__main__": main()
