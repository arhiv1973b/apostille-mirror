#!/usr/bin/env python3
"""A\u00a9tor \u2014 QR / public portal link monitor for ASP extracts."""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 A\u00a9tor-QR-Monitor/1.0"
)

def curl_check(url: str, timeout: int = 20) -> dict:
    result = {
        "qr_url": url,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "last_status": None,
        "last_ok": False,
        "content_type": None,
        "error": None,
        "ms": None,
        "final_url": None,
    }
    curl = shutil.which("curl")
    if not curl:
        result["error"] = "curl not found"
        return result
    cmd = [
        curl, "-sS", "-L", "-o", "/dev/null",
        "-w", "%{http_code}|%{content_type}|%{time_total}|%{url_effective}|%{errormsg}",
        "--connect-timeout", "10", "--max-time", str(timeout),
        "-A", UA,
        "-H", "Accept: text/html,application/xhtml+xml,application/pdf,*/*;q=0.8",
        url,
    ]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
        line = (p.stdout or "").strip().splitlines()[-1] if p.stdout else ""
        parts = line.split("|")
        while len(parts) < 5:
            parts.append("")
        code_s, ctype, ttotal, final, errmsg = parts[:5]
        if code_s.isdigit():
            result["last_status"] = int(code_s)
        result["content_type"] = ctype or None
        try:
            result["ms"] = int(float(ttotal) * 1000)
        except ValueError:
            pass
        result["final_url"] = final or None
        if result["last_status"] in (200, 206):
            result["last_ok"] = True
        elif result["last_status"] in (401, 403, 404, 410, 451):
            result["last_ok"] = False
            result["error"] = f"HTTP {result['last_status']} (likely expired or restricted)"
        else:
            result["last_ok"] = False
            result["error"] = errmsg or f"HTTP {result['last_status']}"
        if result["last_status"] in (0, None):
            result["last_ok"] = False
            result["error"] = errmsg or (p.stderr or "").strip() or "connection failed"
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"
        result["last_ok"] = False
    return result

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", default="")
    ap.add_argument("--mirror-dir", default="")
    ap.add_argument("--history", action="store_true")
    args = ap.parse_args()
    out = curl_check(args.url)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    out_path = args.out or (str(Path(args.mirror_dir) / "status.json") if args.mirror_dir else "status.json")
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    prev = {}
    if path.exists():
        try:
            prev = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            prev = {}
    out["first_seen_ok"] = prev.get("first_seen_ok")
    out["first_fail_at"] = prev.get("first_fail_at")
    if out["last_ok"] and not out.get("first_seen_ok"):
        out["first_seen_ok"] = out["checked_at"]
    if not out["last_ok"] and not out.get("first_fail_at"):
        out["first_fail_at"] = out["checked_at"]
    if out["last_ok"]:
        out["first_fail_at"] = None
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.history:
        hist = path.with_name("status_history.jsonl")
        with hist.open("a", encoding="utf-8") as f:
            f.write(json.dumps(out, ensure_ascii=False) + "\n")
    return 0 if out["last_ok"] else 1

if __name__ == "__main__":
    sys.exit(main())
