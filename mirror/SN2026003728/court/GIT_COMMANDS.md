# Court fallback branch — mobile Git

A©TOR_KEY="# [⚖ A©tor Declaration]"

```sh
cd apostille-mirror
git checkout master && git pull
git checkout -b mirror/a-ctor-key-sn2026003728-court-fallback

mkdir -p mirror/SN2026003728/raw
cp "/path/to/Macheret Alexei .pdf" mirror/SN2026003728/raw/SN2026003728_original.pdf
sha256sum mirror/SN2026003728/raw/SN2026003728_original.pdf
# expect: eaab385cfd10739bf3f7a76169b6dbb5fa115052dfcc494d3d4bc5a3515e5afd

# after iPhone QR scan — urls.txt one URL per line:
sh scripts/court_qr_check.sh --from-file urls.txt

git add mirror/SN2026003728/ scripts/court_qr_check.sh
git commit -m 'A©TOR_KEY="# [⚖ A©tor Declaration]" court-fallback SN2026003728'
git push -u origin mirror/a-ctor-key-sn2026003728-court-fallback
```
