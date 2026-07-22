import json
import os

# Base directory for the evidence index
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Paths to input data, configurable if moved
MANIFEST_PATH = os.path.join(os.environ.get('USERPROFILE', ''), 'Downloads', 'Downolde', 'cloud_id_manifest_full (1).json')
PDF_LIST_PATH = os.path.join(os.environ.get('USERPROFILE', ''), 'Downloads', 'Downolde', 'all_pdfs.txt')
OUTPUT_INDEX_PATH = os.path.join(BASE_DIR, 'evidence_index.json')

def build_index():
    index = {"manifest": {}, "files": []}
    
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
            try:
                index["manifest"] = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error decoding manifest: {e}")
            
    if os.path.exists(PDF_LIST_PATH):
        with open(PDF_LIST_PATH, 'r', encoding='utf-8') as f:
            index["files"] = [line.strip() for line in f if line.strip()]
            
    with open(OUTPUT_INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"Index successfully built at: {OUTPUT_INDEX_PATH}")

if __name__ == "__main__":
    build_index()
