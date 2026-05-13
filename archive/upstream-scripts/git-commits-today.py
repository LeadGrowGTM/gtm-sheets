#!/usr/bin/env python3
"""Output today's git commits as a JSON array."""
import subprocess, json, re, datetime, sys

repo = sys.argv[1] if len(sys.argv) > 1 else "."
date = datetime.date.today().isoformat()

out = subprocess.run(
    ["git", "-C", repo, "log",
     f"--since={date}T00:00:00", "--pretty=format:%h|%an|%ad|%s",
     "--date=short", "--shortstat"],
    capture_output=True, text=True
).stdout.strip().split("\n")

commits, i = [], 0
while i < len(out):
    if "|" in out[i]:
        h, a, d, m = out[i].split("|", 3)
        c = {"hash": h, "author": a, "date": d, "message": m,
             "files_changed": "0", "insertions": "0", "deletions": "0"}
        i += 1
        while i < len(out) and not out[i].strip():
            i += 1
        if i < len(out) and "file" in out[i]:
            s = out[i]
            for k, p in [("files_changed", r"(\d+) file"),
                         ("insertions", r"(\d+) ins"),
                         ("deletions", r"(\d+) del")]:
                x = re.search(p, s)
                if x:
                    c[k] = x.group(1)
            i += 1
        commits.append(c)
    else:
        i += 1

print(json.dumps(commits))
