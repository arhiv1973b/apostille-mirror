# Git LFS — original PDF SN2026003728

A©TOR_KEY="# [⚖ A©tor Declaration]"

## Why LFS
- Original ASP PDF is **1 653 420** bytes, SHA-256 `eaab385cfd10739bf3f7a76169b6dbb5fa115052dfcc494d3d4bc5a3515e5afd`.
- Agent API cannot upload binary safely; **Git LFS** is the correct channel for immutable evidence.
- Repo stays small; pointer file in git, blob in LFS storage.

## One-time setup (phone / PC / iSH)

```sh
# 1) Install LFS (once per machine)
# macOS:  brew install git-lfs
# Debian/Ubuntu:  sudo apt install git-lfs
# iSH / Alpine:   apk add git-lfs
git lfs install

# 2) Clone or update repo
cd apostille-mirror
git pull origin master

# 3) Confirm attributes (already on master)
cat .gitattributes | head

# 4) Place the ORIGINAL file you already sent (byte-identical)
mkdir -p mirror/SN2026003728/raw
cp "Macheret Alexei .pdf" mirror/SN2026003728/raw/SN2026003728_original.pdf

# 5) Verify hash BEFORE push
sha256sum mirror/SN2026003728/raw/SN2026003728_original.pdf
# MUST equal:
# eaab385cfd10739bf3f7a76169b6dbb5fa115052dfcc494d3d4bc5a3515e5afd

# 6) Track + push via LFS
git lfs track "mirror/**/raw/*.pdf"   # optional if .gitattributes already present
git add .gitattributes
git add mirror/SN2026003728/raw/SN2026003728_original.pdf
git status   # should show LFS pointer, not full binary diff
git commit -m "A©TOR_KEY immutable ASP PDF SN2026003728 via Git LFS"
git push origin master

# optional court branch
git checkout -b mirror/a-ctor-key-sn2026003728-court-fallback
git push -u origin mirror/a-ctor-key-sn2026003728-court-fallback
```

## After successful push

Public raw (LFS-aware clients / GitHub UI):

`https://github.com/arhiv1973b/apostille-mirror/blob/master/mirror/SN2026003728/raw/SN2026003728_original.pdf`

Download:

`https://github.com/arhiv1973b/apostille-mirror/raw/master/mirror/SN2026003728/raw/SN2026003728_original.pdf`

## Check LFS on server

```sh
git lfs ls-files
git lfs env
```

## Drive backup (already uploaded)
https://drive.google.com/file/d/18BUzuTiLkopSu51cwd4Arx3bzX_EuD4W/view

## Rule
Never re-export or re-sign the PDF. Only the ASP-signed bytes + this SHA-256 are authoritative; MSign verifies the signature (Legea 124/2022).
