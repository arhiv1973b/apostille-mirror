#!/bin/bash
TO="fieldchisinau@coe.int"
SUBJECT="FORMAL NOTICE: UN Case tw571ryb Registered - A©tor (IDNP 655) - Council of Europe Monitoring Request"
LOGFILE="/mnt/h/Загрузки/MACHERET_SITE_DEPLOY/coe_notification_log_$(date +%Y%m%d).txt"

MSG="To: $TO
From: arhiv240@gmail.com
Subject: $SUBJECT
Content-Type: text/plain; charset=UTF-8

To the Head of the Council of Europe Office in Chisinau,

This is a formal notice that on May 3, 2026, the UN OHCHR officially registered case tw571ryb regarding Alexei Macheret (A©tor), IDNP 2000001159655.

The case involves 8,170 days of systematic justice denial and documented torture (Case No. 1-568/98), violating Jus Cogens and ECHR Art. 3. 

Considering the ongoing monitoring of judicial reforms in the Republic of Moldova by the Council of Europe, we formally request your attention to this case as a litmus test for the rule of law.

Full Evidence Archive: https://arhiv1973b.github.io/apostille-mirror/
UN Reference: tw571ryb

A©tor (Macheret Alexei Artur)
CASE-MACHERET-1997-2026"

if echo "$MSG" | msmtp --account=default "$TO"; then
    echo "[SUCCESS] $(date) -> Notification sent to CoE" | tee -a "$LOGFILE"
else
    echo "[FAILED] $(date) -> CoE Dispatch error" | tee -a "$LOGFILE"
fi