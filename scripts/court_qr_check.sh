#!/usr/bin/env sh
# A©TOR_KEY="# [⚖ A©tor Declaration]"
set -eu
ACTOR_KEY='# [⚖ A©tor Declaration]'
MIRROR_DIR="${MIRROR_DIR:-mirror/SN2026003728}"
COURT_DIR="$MIRROR_DIR/court"
mkdir -p "$COURT_DIR"
URL1=""; URL2=""; URL3=""
if [ "${1:-}" = "--from-file" ] && [ -n "${2:-}" ]; then
  i=0
  while IFS= read -r line || [ -n "$line" ]; do
    line=$(printf '%s' "$line" | tr -d '\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    [ -z "$line" ] && continue
    i=$((i+1))
    case $i in 1) URL1=$line ;; 2) URL2=$line ;; 3) URL3=$line ;; esac
  done < "$2"
else
  URL1=${1:-}; URL2=${2:-}; URL3=${3:-}
fi
if [ -z "$URL1" ] || [ -z "$URL2" ] || [ -z "$URL3" ]; then
  echo "Need 3 QR URLs" >&2; exit 2
fi
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 A©tor-Court-QR/1.0'
check_one(){ curl -sS -L -o /dev/null -w '%{http_code}' --connect-timeout 10 --max-time 20 -A "$UA" "$1" 2>/dev/null || echo 000; }
export URL1 URL2 URL3 NOW ACTOR_KEY COURT_DIR
python3 - <<'PY'
import json, os, urllib.parse
urls = [os.environ["URL1"], os.environ["URL2"], os.environ["URL3"]]
now, actor, court = os.environ["NOW"], os.environ["ACTOR_KEY"], os.environ["COURT_DIR"]
def parts(u):
    p = urllib.parse.urlparse(u)
    return {"url": u, "host": p.netloc, "path": p.path or "/", "query": p.query or None,
            "query_params": dict(urllib.parse.parse_qsl(p.query)) if p.query else {}}
links = []
for i, u in enumerate(urls, 1):
    d = parts(u); d["page"] = i; d["status"] = "PARSED"; links.append(d)
qr = {"ACTOR_KEY": actor, "act_number": "SN2026003728", "registration_number": "26327379",
      "issue_date": "2026-11-09", "updated_at": now, "qr_links": links,
      "portals_from_document_text": ["https://msign.gov.md", "https://mcabinet.gov.md"],
      "legal_basis_facts": ["Legea RM nr. 124/2022", "Legea RM nr. 100/2001"]}
open(f"{court}/qr_sources.json", "w", encoding="utf-8").write(json.dumps(qr, ensure_ascii=False, indent=2)+"\n")
print("wrote qr_sources.json")
PY
CHECKS=""
for n in 1 2 3; do eval "u=\$URL$n"; code=$(check_one "$u"); echo "QR$n HTTP $code"; CHECKS="$CHECKS$n|$code|$u\n"; done
export CHECKS
python3 - <<'PY'
import json, os
from pathlib import Path
court = Path(os.environ["COURT_DIR"]); now = os.environ["NOW"]; actor = os.environ["ACTOR_KEY"]
log_path = court / "court_status_log.json"
prev = json.loads(log_path.read_text(encoding="utf-8")) if log_path.exists() else {}
checks = prev.get("checks") or []
for line in os.environ.get("CHECKS", "").strip().split("\n"):
    if not line.strip(): continue
    n, code, url = line.split("|", 2)
    checks.append({"page": int(n), "url": url, "http_status": int(code) if code.isdigit() else None,
                   "ok": code.isdigit() and 200 <= int(code) < 400, "checked_at": now})
log = {"ACTOR_KEY": actor, "act_number": "SN2026003728", "generated_at": now,
       "hypothesis_risk": "By hearing date ASP/EVO QR may be unavailable. Pre-hearing checks only.",
       "checks": checks,
       "original_pdf": {"path": "raw/SN2026003728_original.pdf",
         "sha256": "eaab385cfd10739bf3f7a76169b6dbb5fa115052dfcc494d3d4bc5a3515e5afd", "bytes": 1653420}}
log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print("wrote court_status_log.json")
PY
