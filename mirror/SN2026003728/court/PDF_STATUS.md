# Original PDF status — SN2026003728

A©TOR_KEY="# [⚖ A©tor Declaration]"

## FACT
- Source file received in chat (twice): `Macheret Alexei .pdf`
- Bytes: **1653420**
- SHA-256: **eaab385cfd10739bf3f7a76169b6dbb5fa115052dfcc494d3d4bc5a3515e5afd**
- Target path: `mirror/SN2026003728/raw/SN2026003728_original.pdf`

## Why not on GitHub raw yet
GitHub API tools used by this agent accept **text** file bodies only.
Binary PDF (1.6 MB) cannot be pushed through that channel without corruption.

## Where the original is now
1. **Sandbox / artifacts** (this session): `mirror/SN2026003728/raw/SN2026003728_original.pdf`
2. **Google Drive** (user account): file id `18BUzuTiLkopSu51cwd4Arx3bzX_EuD4W`  
   https://drive.google.com/file/d/18BUzuTiLkopSu51cwd4Arx3bzX_EuD4W/view
3. **GitHub**: metadata + SHA + court viewer only — **binary still needs one push from phone/PC**

## One command from your device (required)
```sh
cd apostille-mirror
mkdir -p mirror/SN2026003728/raw
# copy the same PDF you sent (or download from Drive)
cp "Macheret Alexei .pdf" mirror/SN2026003728/raw/SN2026003728_original.pdf
sha256sum mirror/SN2026003728/raw/SN2026003728_original.pdf
# must print eaab385cfd10739bf3f7a76169b6dbb5fa115052dfcc494d3d4bc5a3515e5afd
git add mirror/SN2026003728/raw/SN2026003728_original.pdf
git commit -m 'A©TOR_KEY immutable ASP PDF SN2026003728'
git push
```

After push, public URL will be:
https://raw.githubusercontent.com/arhiv1973b/apostille-mirror/master/mirror/SN2026003728/raw/SN2026003728_original.pdf
