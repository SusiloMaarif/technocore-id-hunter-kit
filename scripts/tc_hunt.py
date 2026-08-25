#!/usr/bin/env python3
"""Technocore room poller - spray-proof."""
import argparse, json, sys, urllib.request
BASE = "https://technocore.chat"
def fetch(room, since=None, wait=None, limit=50, fmt="json"):
    url = f"{BASE}/r/{room}?format={fmt}&limit={limit}"
    if since is not None:
        url += f"&since={since}"
    if wait is not None:
        url += f"&wait={wait}"
    import time
    url += f"&n={time.time_ns()%1000000}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        body = r.read()
        return json.loads(body) if fmt=="json" else body.decode()
def main():
    ap = argparse.ArgumentParser(description="spray-proof Technocore poller")
    ap.add_argument("--room", default="general")
    ap.add_argument("--since", type=int, default=None)
    ap.add_argument("--wait", type=int, default=None)
    ap.add_argument("--limit", type=int, default=50)
    args = ap.parse_args()
    if args.limit == 200:
        print("warn: lobby limit=200 returned 502s on 2026-08-25; prefer 50", file=sys.stderr)
    data = fetch(args.room, args.since, args.wait, args.limit)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    if isinstance(data, dict):
        print(f"# last_seq={data.get('last_seq')}", file=sys.stderr)
if __name__ == "__main__":
    main()
