import json
import os
from datetime import datetime

def update_matrix():
    print("A©TOR · Monitoring silence from international nodes (Fix: utf-8-sig)...")
    file_path = 'response_matrix.json'
    try:
        # Читаем с поддержкой BOM, если он появится
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        
        data['last_sync'] = datetime.now().isoformat()
        for node in data['nodes']:
            if node['status'] == "SILENCE":
                node['days_since_notice'] += 1
                node['last_event'] = f"SILENCE_LOGGED_DAY_{node['days_since_notice']}"
        
        # Сохраняем в чистом utf-8
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print("✅ Matrix updated successfully (v1.0.1).")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update_matrix()