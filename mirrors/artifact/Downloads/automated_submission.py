#!/usr/bin/env python3
"""
CASE-MACHERET-1997-2026 - Automated Submission Script
Run this on your local machine to submit to IPFS and Email
"""

import os
import sys
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# ============== CONFIGURATION ==============
# Fill in your credentials here

# For Pinata (get from https://www.pinata.cloud/ → API Keys)
PINATA_JWT = "YOUR_PINATA_JWT_HERE"

# For Email (SMTP)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "your_email@gmail.com"
SMTP_PASSWORD = "your_app_password"

# For OHCHR
OHCHR_EMAIL = "cat@ohchr.org"
VICTIM_EMAIL = "arhiv240@gmail.com"

# Files to upload
FILES_TO_UPLOAD = [
    "ECHR_complaint_filled.md",
    "UN_COMMUNICATION_SHORT.md", 
    "OHCHR_EMAIL_DRAFT.txt"
]

# ==========================================

def upload_to_pinata(filepath, jwt):
    """Upload file to IPFS via Pinata"""
    import requests
    
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    
    headers = {
        "Authorization": f"Bearer {jwt}"
    }
    
    with open(filepath, 'rb') as f:
        files = {'file': (os.path.basename(filepath), f)}
        response = requests.post(url, files=files, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        cid = data.get('IpfsHash', '')
        print(f"✅ Uploaded {filepath} → CID: {cid}")
        return cid
    else:
        print(f"❌ Failed to upload {filepath}: {response.text}")
        return None

def send_email_to_ohchr(subject, body, smtp_email, smtp_password):
    """Send email to OHCHR"""
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_email
        msg['To'] = OHCHR_EMAIL
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent to {OHCHR_EMAIL}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def load_email_template():
    """Load OHCHR email template"""
    with open("OHCHR_EMAIL_DRAFT.txt", "r", encoding="utf-8") as f:
        return f.read()

def main():
    print("=" * 50)
    print("CASE-MACHERET-1997-2026 - Automated Submission")
    print("=" * 50)
    
    # Check if credentials are set
    if PINATA_JWT == "YOUR_PINATA_JWT_HERE":
        print("\n⚠️  Pinata JWT not configured. Skipping IPFS upload.")
        do_pinata = input("Configure now? (y/n): ")
        if do_pinata.lower() == 'y':
            PINATA_JWT = input("Enter Pinata JWT: ")
    else:
        do_pinata = "y"
    
    # Upload to IPFS
    if do_pinata == "y":
        print("\n📤 Uploading to IPFS...")
        cids = {}
        for filename in FILES_TO_UPLOAD:
            if os.path.exists(filename):
                cid = upload_to_pinata(filename, PINATA_JWT)
                if cid:
                    cids[filename] = cid
            else:
                print(f"⚠️  File not found: {filename}")
        
        if cids:
            print("\n📋 IPFS CIDs:")
            for fname, cid in cids.items():
                print(f"  {fname}: https://ipfs.io/ipfs/{cid}")
    
    # Send OHCHR email
    print("\n📧 Sending OHCHR email...")
    if SMTP_EMAIL == "your_email@gmail.com":
        print("⚠️  SMTP not configured. Skipping email.")
    else:
        subject = "Individual Communication - Moldova - Jus Cogens - CASE-MACHERET-1997-2026"
        body = load_email_template()
        send_email_to_ohchr(subject, body, SMTP_EMAIL, SMTP_PASSWORD)
    
    print("\n✅ Submission complete!")
    print("\nNext steps:")
    print("1. ECHR: https://echr.coe.int/application")
    print("2. Check your email for confirmation")

if __name__ == "__main__":
    main()
