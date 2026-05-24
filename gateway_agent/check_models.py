import os
import requests
import json

# Получаем ключ из среды или жестко заданный (удалил для безопасности в итоговом коде)
API_KEY = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY", "")
# Список доступных моделей для проверки
def get_list_url():
    return f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

def check():
    try:
        resp = requests.get(get_list_url()).json()
        models = [m['name'] for m in resp.get('models', [])]
        return models
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    print(check())
