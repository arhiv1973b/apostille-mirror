#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, time
try:
    import requests
except ImportError:
    print("ERROR: 'requests' not installed. Run: pip3 install requests")
    sys.exit(1)

if len(sys.argv) < 2:
    print("Usage: python3 link_tester.py <urls_file>")
    sys.exit(1)

urls_file = sys.argv[1]
with open(urls_file, "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

results = []
print(f"Testing {len(urls)} URLs...\n")
for u in urls:
    try:
        t0 = time.time()
        r = requests.head(u, allow_redirects=True, timeout=10)
        elapsed = time.time() - t0
        status = "OK" if r.ok else "FAIL"
        results.append({"url":u, "status_code":r.status_code, "ok":r.ok, "time_s":round(elapsed,3)})
        print(f"[{status}] {r.status_code} | {u[:50]:50s} | {round(elapsed,3)}s")
    except Exception as e:
        results.append({"url":u, "error":str(e)[:100]})
        print(f"[ERROR] {u[:50]:50s} | {str(e)[:30]}")

with open("report_link_results.json","w",encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\nResults saved to report_link_results.json")
