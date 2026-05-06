#!/bin/bash
EMAILS="srindependencejl.dgs@gmail.com chisinauprotocol@state.gov fieldoffice.moldova@coe.int"
SUBJECT="URGENT: Lethal Condition Report - Group I Disabled Subject - Case tw571ryb"

MSG="To: $EMAILS
From: arhiv240@gmail.com
Subject: $SUBJECT
X-Priority: 1 (Highest)

ATTENTION: UN Strategic Oversight / DGS / U.S. State Dept.

Subject Alexei Macheret (A©tor, IDNP 2000001159655) reports a CRITICAL escalation:
1. STATUS: Confirmed Disability Group I (Sever/Severe)[cite: 4].
2. ASSET THEFT: 25,210,256.15 MDL siphoned via FinComBank identity manipulation[cite: 1, 10].
3. STRANGULATION: MICB has blocked the remaining 298.15 MDL, leaving the subject with ZERO survival funds[cite: 5].
4. JUDICIAL SABOTAGE: Judge Maria Muruianu (Case 2-3062/26) has intentionally blocked access to justice using linguistic discrimination[cite: 2, 6, 7].

This is a mechanical proof of intentional physical liquidation of a protected person under ECHR Art. 3.
All evidence is sealed at: https://github.com/arhiv1973b/apostille-mirror/

Action Required: Immediate humanitarian intervention and release of IMF/UN linked assets.
A©tor"

echo "$MSG" | msmtp --account=default $EMAILS
