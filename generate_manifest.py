import datetime
import json
import datetime
import hashlib
import sys

def create_manifest(query, output_file):
    try:
        with open('mirrors/evidence_index.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Критическая ошибка: mirrors/evidence_index.json не найден.")
        return

    selected = [item for item in data if query.lower() in item['name'].lower()]
    if not selected:
        print(f"По запросу '{query}' объектов не найдено.")
        return

    manifest = {
        "meta": {
            "title": f"Evidence Packet: {query}",
            "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
            "issuer": "A©tor",
            "case_id": "CASE-MACHERET-1997-2026",
            "jurisdiction": ["ECHR", "UN", "MD"],
            "object_count": len(selected)
        },
        "evidence_chain": []
    }

    for item in selected:
        entry_string = f"{item['id']}|{item['name']}|{item['size']}"
        entry_hash = hashlib.sha256(entry_string.encode()).hexdigest()
        manifest["evidence_chain"].append({
            "name": item['name'],
            "uri": f"https://drive.google.com/file/d/{item['id']}/view",
            "integrity_id": f"sha256:{entry_hash}",
            "size_bytes": item['size']
        })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"[ OK ] Манифест '{output_file}' сформирован ({len(selected)} объектов).")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 generate_manifest.py 'КЛЮЧЕВОЕ_СЛОВО'")
    else:
        q = sys.argv[1]
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"MANIFEST_{q}_{timestamp}.json"
        create_manifest(q, filename)
