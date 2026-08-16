import hashlib
import json
import os
from datetime import datetime

# Файлы для фиксации
FILES_TO_HASH = [
    r"evidence_registry\victoriabank_events.json",
    r"apostille-mirror\FORENSIC_TIMELINE_20260615.json",
    r"entity_graph.json",
    r"legal_analysis\victoriabank_blockade_analysis.md",
]


def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def generate_manifest():
    manifest = {"timestamp": datetime.now().isoformat(), "files": {}}
    base_dir = r"H:\ACTOR_DEV_ENV"

    for rel_path in FILES_TO_HASH:
        full_path = os.path.join(base_dir, rel_path)
        if os.path.exists(full_path):
            manifest["files"][rel_path] = calculate_sha256(full_path)
        else:
            print(f"[!] Файл не найден: {full_path}")

    manifest_path = os.path.join(base_dir, "state_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)
    print(f"[+] Манифест состояния успешно сгенерирован: {manifest_path}")


if __name__ == "__main__":
    generate_manifest()
