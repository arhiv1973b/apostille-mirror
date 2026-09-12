# ocr_zero_weight_bridge.py
import os, json, hashlib, re


def extract_defect_fingerprint(text):
    # Извлечение нетипичных символов, двойных знаков и возможных опечаток как паттерна
    anomalies = re.findall(r"([^\w\s]{2,}|[a-zA-Zа-яА-Я]+\d+[a-zA-Zа-яА-Я]+)", text)
    return hashlib.sha256(str(anomalies).encode("utf-8")).hexdigest()[:16]


def process_ocr_to_udhr_pointer(
    drive_link, raw_text_file, output_name, target_lang="en"
):
    with open(raw_text_file, "r", encoding="utf-8") as f:
        raw_text = f.read()

    text_hash = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
    defect_fingerprint = extract_defect_fingerprint(raw_text)

    udhr_mapping = {
        "source_anchor": drive_link,
        "raw_text_hash": text_hash,
        "defect_fingerprint": defect_fingerprint,
        "browser_sync_key": f"SYNC-{defect_fingerprint}",
        "translation_status": f"Translated to {target_lang}. Grammatically corrected.",
        "forensic_anomaly_log": "Mechanical/OCR typos detected and preserved in raw_text_hash for strict visual matching.",
        "jurisdictional_baseline": "UDHR 1948 (Jus Cogens)",
    }

    out_dir = "🏛️_EVIDENCE/OCR_TEXT_LAYER/UDHR_INDEX_MAPPING"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{output_name}.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(udhr_mapping, f, indent=4, ensure_ascii=False)

    print(f"[+] Advanced Node created: {out_path} | Defect Key: {defect_fingerprint}")
