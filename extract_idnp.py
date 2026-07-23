import json
import re
import os

# Конфигурация путей
TARGET_DIR = r"H:\ACTOR_DEV_ENV\apostille-mirror"
INDEX_FILE = os.path.join(TARGET_DIR, "Cloud_Heavy_Index.json")
OUTPUT_FILE = os.path.join(TARGET_DIR, "IDNP_Anomalies_Map.json")

def analyze_idnp_nodes():
    print("✦ Инициализация модуля форензик-анализа ИДНП...")
    
    if not os.path.exists(INDEX_FILE):
        print(f"[ОШИБКА] Базовый индекс не найден: {INDEX_FILE}")
        return

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Регулярные выражения для поиска 13-значных номеров и ключевых слов
    # Настроено на стандарты локальных удостоверений личности
    idnp_pattern = re.compile(r'\b\d{13}\b')
    keyword_pattern = re.compile(r'(?i)(иднп|idnp|buletin|pasaport|identitate|удостоверение)')

    suspect_nodes = []

    print("Сканирование метаданных...")
    for file in data:
        name = file.get('name', '')
        
        # Фильтрация по наличию 13-значного кода или триггерных слов в имени файла
        if idnp_pattern.search(name) or keyword_pattern.search(name):
            suspect_nodes.append({
                "id": file.get('id'),
                "name": name,
                "url": file.get('url'),
                "mimeType": file.get('mimeType')
            })

    # Материализация выборки
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(suspect_nodes, f, ensure_ascii=False, indent=2)

    print(f"✓ Сканирование завершено.")
    print(f"✓ Обнаружено узлов, связанных с идентификационными данными: {len(suspect_nodes)}")
    print(f"✦ Суб-карта сгенерирована: {OUTPUT_FILE}")

if __name__ == '__main__':
    analyze_idnp_nodes()
