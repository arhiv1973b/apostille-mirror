# Archival mirror \u2014 ASP extract SN2026003728

**Document:** Extras de pe actul de schimbare a numelui \u0219i/sau prenumelui  
**Act:** SN2026003728 \u00b7 Reg. 26327379 \u00b7 Issued 09.11.2026  
**Change:** MACERET \u2192 MACHERET (ALEXEI) \u00b7 IDNP 2000001159655

## Legal model

| Layer | Rule |
|-------|------|
| **raw/** | Byte-identical ASP-signed PDF only. Never modify. |
| **web/** | Static archival viewer. Marked `[ARCHIVAL FALLBACK MIRROR]`. |
| **Verification** | Qualified e-signature \u2192 [msign.gov.md](https://msign.gov.md). QR portal link is convenience only and may expire. |

Official ASP materials do **not** print a fixed \u201cQR expires in N days\u201d on this extract type. In practice, public download links for some ASP electronic extracts have been limited (e.g. **15 days** for certain email-delivery channels). MCabinet-held signed PDFs remain valid under **Law 124/2022**; authenticity is proven by MSign, not by the temporary QR URL.

## Setup

1. Copy original PDF to `raw/SN2026003728_original.pdf`
2. `sha256sum raw/SN2026003728_original.pdf | tee SHA256SUMS.txt`
3. Paste hash into `web/index.html` and `manifest.json`
4. QR monitor:
   ```bash
   python3 scripts/check_qr_link.py --url \"https://YOUR-QR-URL\" --mirror-dir mirror/SN2026003728 --history
   ```
