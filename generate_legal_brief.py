import json
import os
from datetime import datetime

BASE_DIR = r"H:\ACTOR_DEV_ENV"
VB_EVENTS_PATH = os.path.join(BASE_DIR, r"evidence_registry\victoriabank_events.json")
LEGAL_DIR = os.path.join(BASE_DIR, "legal_analysis")
OUTPUT_MD = os.path.join(LEGAL_DIR, "victoriabank_blockade_analysis.md")


def generate_brief():
    if not os.path.exists(LEGAL_DIR):
        os.makedirs(LEGAL_DIR)

    with open(VB_EVENTS_PATH, "r", encoding="utf-8") as f:
        events_data = json.load(f)

    events = events_data.get("events", [])

    md_content = f"""# LEGAL ANALYSIS: FINANCIAL BLOCKADE EPISODE
**Date Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Project:** CASE-MACHERET-1997-2026
**Subject:** Victoriabank Infrastructure Restrictions

## 1. FACTUAL BASIS (EVIDENCE REGISTRY)
This analysis is based on cryptographically secured events from the Centralized Authority for Source-of-truth (CAS) registry: `victoriabank_events.json`.

"""
    for e in events:
        md_content += f"*   **Event ID:** `{e['id']}`\n"
        md_content += f"    *   **Timestamp:** {e['timestamp']}\n"
        md_content += f"    *   **Detail:** {e['title']}\n"

    md_content += """
## 2. LEGAL QUALIFICATION (THEORY OF CONTINUING CONSEQUENCES)
Within the established legal model (`detention → non-rehabilitation → continuing-consequences`), the documented financial events constitute a deprivation of basic socio-economic integration. 

The denial of financial services without transparent legal justification serves as a structural extension of the primary non-rehabilitation phase.

## 3. APPLICABLE INTERNATIONAL OBLIGATIONS
*   **ECHR Article 3 (Prohibition of Torture/Degrading Treatment):** State toleration or initiation of financial exclusion mechanisms that precipitate destitution or severe psychological distress engages the threshold of degrading treatment.
*   **ECHR Article 5 (Right to Liberty and Security):** The financial blockade restricts the physical and logistical autonomy of the individual, serving as a de facto continuation of punitive restrictions on liberty.
*   **Jus Cogens & Erga Omnes:** The systemic failure to rehabilitate and the ongoing deprivation of rights violates non-derogable international norms.

## 4. INTEGRATION INTO ENTITY GRAPH
*   **Primary Node:** ACTOR_MACHERET
*   **Adverse Node:** ORG_VICTORIABANK
*   **Edge:** FINANCIAL_INTERACTION (Coercive/Restrictive)
"""

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"[+] Юридический меморандум успешно сгенерирован: {OUTPUT_MD}")


if __name__ == "__main__":
    generate_brief()
