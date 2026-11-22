"""Builds the Pinterest RSS feeds from pin-schedule.json.
Only pins whose publish time has passed are included, so the feeds grow
3 pins a day. Run by .github/workflows/pinterest-feed.yml on a timer."""
import json, os, datetime, html
from email.utils import format_datetime
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://sheihab.github.io/wearhue/"
FEEDS = {"Colours for your skin tone": "feed-skin.xml", "What colours go together": "feed-match.xml", "Outfit colour palettes": "feed-style.xml"}
now = datetime.datetime.now(datetime.timezone.utc)
pins = json.load(open(os.path.join(HERE, "pin-schedule.json")))
for board, fn in FEEDS.items():
    mine = [p for p in pins if p["board"] == board]
    live = [p for p in mine if datetime.datetime.fromisoformat(p["time"]) <= now] or mine[:1]  # never empty
    live = sorted(live, key=lambda p: p["time"], reverse=True)[:50]
    items = ""
    for p in live:
        t = datetime.datetime.fromisoformat(p["time"])
        link = f'{p["link"]}?utm_source=pinterest&amp;utm_medium=pin&amp;utm_campaign={p["id"]}'
        e = html.escape
        items += f"""  <item>
   <title>{e(p["title"])}</title>
   <link>{link}</link>
   <guid isPermaLink="false">wearhue-{p["id"]}</guid>
   <pubDate>{format_datetime(t)}</pubDate>
   <description><![CDATA[<img src="{p["image"]}" alt="{e(p["title"])}"/><p>{p["description"]}</p>]]></description>
   <category>{e(p["keywords"])}</category>
   <enclosure url="{p["image"]}" type="image/png" length="0"/>
   <media:content url="{p["image"]}" medium="image" type="image/png"/>
  </item>
"""
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:atom="http://www.w3.org/2005/Atom">
 <channel>
  <title>Wearhue: {html.escape(board)}</title>
  <link>{SITE}</link>
  <atom:link href="{SITE}{fn}" rel="self" type="application/rss+xml"/>
  <description>Colour guides from Wearhue: find the clothing colours that suit your skin tone.</description>
  <language>en</language>
{items} </channel>
</rss>
"""
    open(os.path.join(HERE, fn), "w").write(xml)
    print(fn, len(live), "pins live")
