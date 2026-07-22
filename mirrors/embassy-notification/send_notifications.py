#!/usr/bin/env python3
# SECURITY AUDIT: 2026-03-16
# - Body template corrected: apostilles 1997-2026 (not 2021-2023)
# - Member states: 129 (not 126)
# - Proper respondent: Ministry of Finance (not Ministry of Justice)
# - Claimant identified: Macheret Alexei Artur
# - CC petition date: 24.10.2019 reg.Nr.100cg (not 2009)
# - Turkey email fixed in embassies.csv
# - All entries remain Status=Draft until manually changed to Active
"""
Diplomatic Notification Sender
Sends legal case notifications to embassies of Hague Convention member states
"""

import csv
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ============================================
# CONFIGURATION - Edit these values
# ============================================
SMTP_SERVER = "smtp.office365.com"  # Outlook/Office 365
SMTP_PORT = 587
SMTP_USER = "arhiv1973b@outlook.com"  # Your Outlook email
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")  # App password or regular password

# Email templates
SUBJECT = "Legal Case: Macheret Alexei Artur v. Republic of Moldova — Jus Cogens Violations — Hague Convention 1961"

BODY_TEMPLATE = """Excellency,

We respectfully bring to your attention a serious case of human rights violations and systematic institutional fraud by the Republic of Moldova, a member state of the Hague Convention of 1961.

CASE REFERENCE
==============
Macheret Alexei Artur v. Republic of Moldova
Claimant: Macheret Alexei Artur (IDNP: 2000001159655), Group 1 disability holder
Proper Respondent: Ministry of Finance of the Republic of Moldova (Serviciul Fiscal de Stat)
Improper Intervening Party: Ministry of Justice / ARIJ (acknowledged debt, substituted debtor)
Claim Amount: EUR 500,000
Period: 1997-2026
GitHub: https://github.com/arhiv1973b/apostille-legal-case

CASE SUMMARY
============
A civil lawsuit has been filed against the Republic of Moldova for:

1. Systematic violation of fair trial rights (ECHR Art. 6) — confirmed by Chisinau Court of Appeal, 27.11.2019, case No. 10r-1009/19
2. Prohibition of inhuman treatment (ECHR Art. 3) — denial of accessible justice to Group 1 disability holder
3. Denial of effective remedy (ECHR Art. 13) — improper respondent substitution: Ministry of Justice redirected payment to State Tax Service without notification (payment order No. 0600013037, 01.10.2021)
4. Apostille authentication violations (Hague Convention 1961, Art. 3) — 90 apostilles issued 1997-2026, 14.4% bearing unclear or defective signatures; apostille No. 5OTZ38FVFN8R2 (29.12.2021) — field 10 (digital signature) empty in violation of mandatory form
5. Peremptory norm violations — Vienna Convention Art. 53 and 64 (jus cogens)
6. Language discrimination — Constitutional Court petition filed 24.10.2019 (registered: No. 100cg) refused on language grounds, violating Law No. 60 of Moldova (equal rights of persons with disabilities)
7. Criminal conviction on basis of invalid normative act — judgment 1a-42/09 (03.02.2009), rehabilitation proceedings blocked by General Prosecutor (reference URIUST/19/MDA/3, ECHR case No. 41929/11)

DEBTOR SUBSTITUTION — KEY VIOLATION
=====================================
ARIJ/Ministry of Justice acknowledged overpayment of 50 lei (letter No. 12-25/1988, 02.09.2021) but redirected execution to State Tax Service (SFS) without notifying the claimant. Ministry of Finance then issued notification of execution. Three different state bodies involved in a single obligation — constituting institutional fraud under Vienna Convention Art. 49 and denial of effective remedy under ECHR Art. 13.

DOCUMENTATION
=============
All case documents (EN / RU / RO):
https://arhiv1973b.github.io/apostille-legal-case/
https://github.com/arhiv1973b/apostille-legal-case

LEGAL BASIS
===========
- European Convention on Human Rights (Art. 3, 6, 13)
- Hague Convention of 1961 (Apostille), Art. 3
- Vienna Convention on the Law of Treaties 1969 (Art. 26, 49, 53, 64)
- Law No. 60 of the Republic of Moldova (rights of persons with disabilities)
- UN Human Rights Committee reference URIUST/19/MDA/3

REQUEST
=======
We respectfully request:
1. Review of this case documentation
2. Support for human rights and rule-of-law monitoring in Moldova
3. Diplomatic communication to the Government of Moldova regarding systematic violations
4. If violations are confirmed — diplomatic intervention through available channels

Respectfully,
Macheret Alexei Artur
Claimant / Actor
Date: 2026
Contact: arhiv240@gmail.com

---
This notification is addressed to member states of the Hague Convention of 1961 (129 states)
Case reference: https://arhiv1973b.github.io/apostille-legal-case/
"""

# Embassy database (CSV format)
EMBASSY_DB = "embassies.csv"


def load_embassies():
    """Load embassy contacts from CSV"""
    embassies = []
    try:
        with open(EMBASSY_DB, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("Email") and row.get("Email").strip():
                    embassies.append(row)
    except FileNotFoundError:
        print(f"Warning: {EMBASSY_DB} not found")
    return embassies


def send_email(to_email, country, from_email):
    """Send notification email to embassy"""
    if not SMTP_PASSWORD:
        print(f"⚠️ SMTP password not set. Would send to {country}: {to_email}")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = SUBJECT

        msg.attach(MIMEText(BODY_TEMPLATE, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        print(f"✓ Sent to {country}: {to_email}")
        return True
    except Exception as e:
        print(f"✗ Failed to send to {country}: {e}")
        return False


def main():
    """Main function"""
    print("=" * 60)
    print("DIPLOMATIC NOTIFICATION SENDER")
    print("=" * 60)
    print(f"Started: {datetime.now()}")
    print(f"From: {SMTP_USER}")
    print()

    embassies = load_embassies()
    print(f"Loaded {len(embassies)} embassy contacts with emails")

    if not SMTP_PASSWORD:
        print("\n⚠️ SMTP_PASSWORD not set!")
        print("Set environment variable:")
        print("  export SMTP_PASSWORD='your-password'")
        print("\nRun script again after setting password")
        return

    # Show embassies that will be notified
    print("\nEmbassies that will receive notification:")
    for embassy in embassies:
        print(f"  - {embassy.get('Country', 'Unknown')}: {embassy.get('Email', 'N/A')}")

    print("\n" + "=" * 60)

    # Send confirmation
    confirm = input(f"Send to {len(embassies)} embassies? (yes/no): ")
    if confirm.lower() != "yes":
        print("Cancelled.")
        return

    success = 0
    failed = 0

    for embassy in embassies:
        email = embassy.get("Email", "").strip()
        country = embassy.get("Country", "Unknown")

        if email and send_email(email, country, SMTP_USER):
            success += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print(f"COMPLETED: {success} sent, {failed} failed")
    print("=" * 60)


if __name__ == "__main__":
    main()
