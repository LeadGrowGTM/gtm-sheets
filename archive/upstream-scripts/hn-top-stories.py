#!/usr/bin/env python3
"""Fetch top N Hacker News stories with details.

Requires N+1 API calls — can't be done with a single HTTP source.
Also extracts domain from URL and computes hours since posted.

Usage: python3 hn-top-stories.py [count]
"""
import json, sys, time
from urllib.request import urlopen
from urllib.parse import urlparse

count = int(sys.argv[1]) if len(sys.argv) > 1 else 10

# Step 1: Fetch top story IDs (one call)
ids = json.loads(urlopen("https://hacker-news.firebaseio.com/v0/topstories.json").read())

# Step 2: Fetch details for each (N calls — this is why we need a script)
stories = []
for story_id in ids[:count]:
    item = json.loads(urlopen(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json").read())
    if not item or item.get("type") != "story":
        continue

    url = item.get("url", "")
    domain = urlparse(url).netloc.removeprefix("www.") if url else "news.ycombinator.com"
    posted_ts = item.get("time", 0)
    hours_ago = round((time.time() - posted_ts) / 3600, 1) if posted_ts else 0

    stories.append({
        "title": item.get("title", ""),
        "url": url or f"https://news.ycombinator.com/item?id={story_id}",
        "domain": domain,
        "score": str(item.get("score", 0)),
        "author": item.get("by", ""),
        "comments": str(item.get("descendants", 0)),
        "hours_ago": str(hours_ago),
        "hn_link": f"https://news.ycombinator.com/item?id={story_id}",
    })

print(json.dumps(stories))
