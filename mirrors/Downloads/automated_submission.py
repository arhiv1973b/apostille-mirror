#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemkick/A©t0r Automated IPFS Deployment Script
Project: CASE-MACHERET-1997-2026
"""

import os
import sys
import requests
import re

# === КОНФИГУРАЦИЯ ===
DATABASE_PATH = r"C:\Users\arhiv\База Данных.txt"

def get_pinata_jwt():
    """Dynamically extract Pinata JWT from local database file."""
    if os.path.exists(DATABASE_PATH):
        try:
            with open(DATABASE_PATH, "r", encoding="utf-8") as f:
                content = f.read()
                # Look for Pinata JWT pattern (usually a long string)
                # We'll look for a line containing 'Pinata' and 'JWT' or similar
                # Or just search for a bearer token pattern
                match = re.search(r"Pinata.*?JWT[:\s]+([a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+)", content, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
                
                # Fallback: search for any long JWT-like string if Pinata keyword is nearby
                match = re.search(r"([a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+)", content)
                if match:
                    return match.group(1).strip()
        except Exception as e:
            print(f"[-] Error reading {DATABASE_PATH}: {e}")
    
    # Fallback to environment variable
    return os.getenv("PINATA_JWT")

PINATA_JWT = get_pinata_jwt()

# Список 6 основных файлов для анкоринга
FILES_TO_UPLOAD = [
    "ECHR_complaint_filled.md",
    "UN_JUS_COGENS_PROTOCOL.md",
    "UN_COMMUNICATION_SHORT.md",
    "ECHR_FORM_PREPARED.md",
    "TUNNEL_PREPARATION.md",
    "A©tor_PGP_PublicKey.asc"
]

PINATA_API_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"

def check_config():
    if not PINATA_JWT or not PINATA_JWT.strip():
        print("[-] Ошибка: Pinata JWT-токен не найден в базе данных и не задан в переменных окружения.")
        print(f"[*] Проверьте путь: {DATABASE_PATH}")
        sys.exit(1)

def upload_to_ipfs(file_path):
    if not os.path.exists(file_path):
        print(f"[-] Файл не найден: {file_path}. Пропустите или проверьте путь.")
        return None

    print(f"[*] Загрузка {file_path} в IPFS...")
    
    headers = {
        "Authorization": f"Bearer {PINATA_JWT.strip()}"
    }

    try:
        with open(file_path, "rb") as f:
            file_data = {
                "file": (os.path.basename(file_path), f)
            }
            
            # Добавляем метаданные
            options = {
                "pinataMetadata": {
                    "name": os.path.basename(file_path),
                    "keyvalues": {
                        "project": "CASE-MACHERET-1997-2026",
                        "author": "A©t0r"
                    }
                }
            }
            
            response = requests.post(
                PINATA_API_URL, 
                headers=headers, 
                files=file_data
            )
            
            if response.status_code == 200:
                result = response.json()
                cid = result.get("IpfsHash")
                print(f"[+] Успешно! Файл: {file_path} -> CID: {cid}")
                return cid
            else:
                print(f"[-] Ошибка загрузки {file_path}: Статус {response.status_code} - {response.text}")
                return None
                
    except Exception as e:
        print(f"[-] Исключение при обработке {file_path}: {str(e)}")
        return None

def main():
    print("=== Инициализация деплоя улик A©t0r (CASE-MACHERET-1997-2026) ===")
    check_config()
    
    results = {}
    
    # Ensure we are in the project root to find files
    os.chdir(r"H:\ACTOR_DEV_ENV\apostille-mirror")
    
    for file_name in FILES_TO_UPLOAD:
        cid = upload_to_ipfs(file_name)
        if cid:
            results[file_name] = cid
            
    print("\n=== СВОДНАЯ ТАБЛИЦА ДЛЯ IPFS_DEPLOYMENT.md ===")
    print("| File | IPFS CID | Status |")
    print("| --- | --- | --- |")
    for file_name, cid in results.items():
        print(f"| {file_name} | `{cid}` | [DEPLOYED] |")
        
    if len(results) == len(FILES_TO_UPLOAD):
        print("\n[+] Все файлы успешно загружены. Скопируйте CIDs и обновите манифесты.")
    else:
        print(f"\n[!] Загружено только {len(results)} из {len(FILES_TO_UPLOAD)} файлов. Проверьте логи ошибок выше.")

if __name__ == "__main__":
    main()
