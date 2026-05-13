#!/usr/bin/env python3
"""Detect tech stack from a website's HTML. Takes domain as argument."""
import sys, json, re
from urllib.request import urlopen, Request
from urllib.error import URLError

domain = sys.argv[1] if len(sys.argv) > 1 else ""
if not domain:
    print("")
    sys.exit(0)

try:
    req = Request(f"https://{domain}", headers={"User-Agent": "Mozilla/5.0"})
    html = urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
except Exception:
    print("")
    sys.exit(0)

techs = []
checks = [
    (r"react", "React"),
    (r"next[\-/]", "Next.js"),
    (r"vue\.js|vuejs", "Vue.js"),
    (r"angular", "Angular"),
    (r"svelte", "Svelte"),
    (r"tailwindcss|tailwind", "Tailwind"),
    (r"bootstrap", "Bootstrap"),
    (r"jquery", "jQuery"),
    (r"wordpress|wp-content", "WordPress"),
    (r"shopify", "Shopify"),
    (r"webflow", "Webflow"),
    (r"gatsby", "Gatsby"),
    (r"nuxt", "Nuxt"),
    (r"remix", "Remix"),
    (r"vercel", "Vercel"),
    (r"cloudflare", "Cloudflare"),
    (r"google.*analytics|gtag", "Google Analytics"),
    (r"segment\.com|analytics\.js", "Segment"),
    (r"intercom", "Intercom"),
    (r"stripe\.js|stripe\.com", "Stripe"),
    (r"hubspot", "HubSpot"),
    (r"sentry", "Sentry"),
]

html_lower = html.lower()
for pattern, name in checks:
    if re.search(pattern, html_lower) and name not in techs:
        techs.append(name)

print(", ".join(techs) if techs else "Unknown")
