import os
import requests
import json

# Получаем ключ из среды или жестко заданный (удалил для безопасности в итоговом коде)
API_KEY = "AIzaSyB7IN_3u9ffBf8pt60xy4DX1m6Zy8y1PKo"
# Список доступных моделей для проверки
LIST_URL = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

def check():
    try:
        resp = requests.get(LIST_URL).json()
        models = [m['name'] for m in resp.get('models', [])]
        return models
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    print(check())
