import json
import re
import os
from collections import Counter

# Конфигурация путей
TARGET_DIR = r'H:\ACTOR_DEV_ENV\apostille-mirror'
MAP_FILE = os.path.join(TARGET_DIR, 'IDNP_Anomalies_Map.json')

def find_discrepancies():
    print('✦ Инициализация модуля форензик-анализа ИДНП...')
    
    if not os.path.exists(MAP_FILE):
        print(f'[ОШИБКА] Суб-карта не найдена: {MAP_FILE}')
        return

    with open(MAP_FILE, 'r', encoding='utf-8') as f:
        nodes = json.load(f)

    # Ищем строгие 13-значные последовательности
    idnp_pattern = re.compile(r'\b\d{13}\b')
    idnp_counter = Counter()
    
    print('Извлечение идентификаторов...')
    for node in nodes:
        name = node.get('name', '')
        matches = idnp_pattern.findall(name)
        for match in matches:
            idnp_counter[match] += 1

    print('\n==================================================')
    print('✦ [РЕЗУЛЬТАТЫ ЧАСТОТНОГО АНАЛИЗА ИДНП] ✦')
    print('==================================================')
    
    if not idnp_counter:
        print('В именах файлов 13-значные номера не найдены. Аномалии скрыты глубже.')
    else:
        for idnp, count in idnp_counter.items():
            print(f' -> Выявлен ИДНП: {idnp} | Встречается в узлах: {count} раз(а)')

        if len(idnp_counter) > 1:
            print('\n[КРИТИЧЕСКОЕ ВНИМАНИЕ] Обнаружено расщепление идентификатора!')
            print('Найдено несколько уникальных 13-значных номеров. Зафиксирован факт вероятной подмены.')
        else:
            print('\n[СТАТУС] Изолирован единый идентификатор. Базовый номер стабилен в именах файлов.')

if __name__ == '__main__':
    find_discrepancies()
