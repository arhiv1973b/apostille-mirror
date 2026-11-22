#!/usr/bin/env sh
# A©TOR_KEY="# [⚖ A©tor Declaration]"
# Push immutable ASP PDF via Git LFS
# Usage:
#   sh scripts/push_pdf_lfs.sh "/path/to/Macheret Alexei .pdf"
set -eu
EXPECTED=eaab385cfd10739bf3f7a76169b6dbb5fa115052dfcc494d3d4bc5a3515e5afd
SRC=${1:-}
DEST=mirror/SN2026003728/raw/SN2026003728_original.pdf

if [ -z "$SRC" ] || [ ! -f "$SRC" ]; then
  echo "Usage: $0 /path/to/original.pdf" >&2
  exit 2
fi

command -v git-lfs >/dev/null 2>&1 || command -v git >/dev/null 2>&1 || {
  echo "git required" >&2; exit 1
}
git lfs install
mkdir -p mirror/SN2026003728/raw
cp "$SRC" "$DEST"

HASH=$(sha256sum "$DEST" | awk '{print $1}')
if [ "$HASH" != "$EXPECTED" ]; then
  echo "HASH MISMATCH" >&2
  echo "got:      $HASH" >&2
  echo "expected: $EXPECTED" >&2
  exit 1
fi
echo "OK hash $HASH"

git add .gitattributes "$DEST" 2>/dev/null || git add "$DEST"
git status
echo "Next: git commit -m 'A©TOR_KEY immutable ASP PDF SN2026003728 via Git LFS' && git push"
