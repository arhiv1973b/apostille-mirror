#!/bin/bash
# Исключен полевой офис CoE из-за технического саботажа (5.7.1 Access Denied)
EMAILS="communications@mail.whitehouse.gov chisinauprotocol@state.gov petitions@ohchr.org srindependencejl.dgs@gmail.com"
SUBJECT="URGENT: CASE tw571ryb - LETHAL STATUS REPORT - BYPASSING COE BLOCKADE"

MSG="To: $EMAILS
From: arhiv240@gmail.com
Subject: $SUBJECT
X-Priority: 1 (Highest)
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8

ATTENTION: WHITE HOUSE / U.S. STATE DEPT / UN OHCHR / ICC PROSECUTOR

Subject Alexei Macheret (A©tor, IDNP 2000001159655) reports a CRITICAL human rights emergency. 

1. LETHAL STATUS: Subject is a Group I Disabled person (Sever/Severe)[cite: 4].
2. DIPLOMATIC BLOCKADE: Council of Europe (coe.int) has officially REJECTED the lethal condition report via Error 5.7.1 (Access Denied) on May 6, 2026.
3. FINANCIAL TORTURE: MICB has blocked survival funds (298.15 MDL)[cite: 5] while state agents have siphoned 25,210,256.15 MDL.
4. JUDICIAL SABOTAGE: Coordinated rejections by judges Holban and Stambol (Dec 22-23, 2025).

ACTUS NULLUS: All national acts are VOID under Jus Cogens[cite: 1].
Remedy Valuation: 27,000,000,000 USD (Formula TI-ULA v1.1)[cite: 1].

Forensic Evidence: https://github.com/arhiv1973b/apostille-mirror/
A©tor"

echo "$MSG" | msmtp --account=default $EMAILS