import os
import json
import glob

# Paths relative to the script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_DIR = os.path.join(SCRIPT_DIR, '..', 'extracted_data')
OUTPUT_MASTER_FILE = os.path.join(SCRIPT_DIR, '..', 'master_evidence_db.json')

master_db = {
    "art_3_torture_psychiatry": [],
    "art_5_arbitrary_detention": [],
    "information_blockade_evidence": [],
    "continuing_consequences_civil_execution": []
}

success_count = 0

for filepath in glob.iglob(os.path.join(TARGET_DIR, "**/*.json_extracted"), recursive=True):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for key in master_db.keys():
                if key in data and isinstance(data[key], list):
                    master_db[key].extend(data[key])
            success_count += 1
    except Exception as e:
        print(f"[!] Ошибка парсинга JSON в файле {filepath}: {e}")

with open(OUTPUT_MASTER_FILE, 'w', encoding='utf-8') as f:
    json.dump(master_db, f, ensure_ascii=False, indent=2)

print(f"Агрегация завершена. Успешно обработано файлов-экстрактов: {success_count}")
print(f"Сводная база сохранена в: {OUTPUT_MASTER_FILE}")
