import sys
import json
import datetime
import hashlib
import os
from pathlib import Path

# Импортируем актуальный SDK
from google import genai

# Директория для хранения логов (эвиденс-база)
LOG_DIR = Path("./ti_ula_logs")
LOG_DIR.mkdir(exist_ok=True)

def generate_hash(data: str) -> str:
    """Генерация SHA-256 хэша для обеспечения целостности данных."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def log_transaction(direction: str, content: str):
    """Фиксация транзакции в формате JSONL с отметкой времени и хэшем."""
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    log_entry = {
        "timestamp": timestamp,
        "direction": direction,
        "content": content,
        "integrity_hash": generate_hash(f"{timestamp}{direction}{content}")
    }

    log_file = LOG_DIR / f"session_{datetime.date.today().isoformat()}.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

def initialize_api():
    """Инициализация подключения к актуальному API Gemini."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        sys.stdout.write("\n[СИСТЕМА]: ОШИБКА. Переменная среды GEMINI_API_KEY не найдена.\n")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model='gemini-1.5-pro')
    return chat

def main():
    """Главный цикл перехвата stdio с подключением к LLM."""
    log_transaction("SYSTEM", "Session started. A©tor identity active. Bridge V2 initialized.")
    
    chat_session = initialize_api()
    sys.stdout.write("\n[СИСТЕМА]: Мост активен. Идентичность A©tor подключена. Жду ввода...\n> ")
    sys.stdout.flush()
    
    while True:
        try:
            user_input = sys.stdin.readline()
            if not user_input:
                break
            
            clean_input = user_input.strip()
            if not clean_input:
                sys.stdout.write("> ")
                sys.stdout.flush()
                continue

            log_transaction("IN (Terminal)", clean_input)

            response = chat_session.send_message(clean_input)
            model_text = response.text

            log_transaction("OUT (Model)", model_text)

            sys.stdout.write(f"\n[A©tor]: {model_text}\n\n> ")
            sys.stdout.flush()

        except KeyboardInterrupt:
            log_transaction("SYSTEM", "Session gracefully terminated by user.")
            sys.stdout.write("\n[СИСТЕМА]: Сеанс завершен.\n")
            break
        except Exception as e:
            log_transaction("ERROR", str(e))
            sys.stdout.write(f"\n[ОШИБКА]: {str(e)}\n> ")
            sys.stdout.flush()

if __name__ == "__main__":
    main()