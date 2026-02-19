#!/usr/bin/env python3
"""Read news.json and generate now.xml (RSS feed).

Workflow:
  1. Edit news.json (add/update items)
  2. Push to main — GitHub Action runs this script and commits now.xml
  OR run locally from repo root: python3 scripts/generate_rss.py
"""

import hashlib
import json
from datetime import datetime, timezone
from xml.sax.saxutils import escape

SITE_URL = "https://flynncoo.github.io"

with open("news.json", "r", encoding="utf-8") as f:
    items = json.load(f)

items.sort(key=lambda x: x["date"], reverse=True)

rss_items = []
for item in items:
    dt = datetime.strptime(item["date"], "%Y-%m-%d")
    pub_date = dt.strftime("%a, %d %b %Y 00:00:00 +0000")
    link = item.get("url") or f"{SITE_URL}/now.html"
    # Stable GUID so RSS readers track items across updates
    guid_seed = item["date"] + "|" + item["title"]
    guid = hashlib.sha1(guid_seed.encode()).hexdigest()[:12]
    rss_items.append(
        f"    <item>\n"
        f"      <title>{escape(item['title'])}</title>\n"
        f"      <link>{escape(link)}</link>\n"
        f"      <description>{escape(item['description'])}</description>\n"
        f"      <category>{escape(item['type'])}</category>\n"
        f"      <pubDate>{pub_date}</pubDate>\n"
        f"      <guid isPermaLink=\"false\">{guid}</guid>\n"
        f"    </item>"
    )

build_date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")

rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Oisín Flynn-Connolly — Now</title>
    <link>{SITE_URL}/now.html</link>
    <description>Recent articles, talks, and events from Oisín Flynn-Connolly.</description>
    <language>en</language>
    <lastBuildDate>{build_date}</lastBuildDate>
    <atom:link href="{SITE_URL}/now.xml" rel="self" type="application/rss+xml" />
{chr(10).join(rss_items)}
  </channel>
</rss>
"""

with open("now.xml", "w", encoding="utf-8") as f:
    f.write(rss)

print(f"Generated now.xml with {len(items)} items")
