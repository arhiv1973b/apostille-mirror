import os
import requests
import json

LOCAL_MODEL = "qwen2.5:0.5b"
API_KEY = os.getenv("GEMINI_API_KEY")
OLLAMA_URL = "http://host.docker.internal:11434/api/generate"
# Используем V1beta и gemini-1.5-flash
LIST_MODELS_URL = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

def list_models():
    resp = requests.get(LIST_MODELS_URL).json()
    return resp

if __name__ == "__main__":
    print(json.dumps(list_models(), indent=2))
