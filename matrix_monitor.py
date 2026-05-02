import json
from datetime import datetime

def update_matrix():
    print("A©TOR · Monitoring silence from international nodes...")
    try:
        with open('response_matrix.json', 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data['last_sync'] = datetime.now().isoformat()
            for node in data['nodes']:
                if node['status'] == "SILENCE":
                    node['days_since_notice'] += 1
                    node['last_event'] = f"SILENCE_LOGGED_DAY_{node['days_since_notice']}"
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
        print("✅ Matrix updated successfully.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update_matrix()
