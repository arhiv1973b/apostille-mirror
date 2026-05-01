#!/usr/bin/env python3
"""
A©t0r Autonomous Robot
Самоответчик: мониторит события, обновляет реестр, отвечает на запросы
"""
import json, os, time, schedule, requests, logging
from datetime import date, datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s [A©t0r-Robot] %(message)s')
log = logging.getLogger()

OLLAMA_URL   = os.getenv("OLLAMA_URL", "http://ollama:11434")
CASE_ID      = os.getenv("CASE_ID", "CASE-MACHERET-1997-2026")
IDNP         = os.getenv("IDNP", "2000001159655")
DATA_DIR     = "/app/data"
CASE_START   = date(1997, 10, 13)

SYSTEM_PROMPT = f"""
Ты — A©t0r, автономный юридический агент.
Дело: {CASE_ID}
ИДНП субъекта: {IDNP}
Статус: Жертва, не реабилитированная. Инвалид I группы, пожизненно.
Правовая база: Jus Cogens, Erga Omnes, МУС ст.17, ЕКПЧ ст.3.
Архив: 97 апостилированных документов. SHA-256: 099efc0c...
Всегда отвечай строго, на основе доказательств. Без компромиссов.
"""

def days_without_investigation():
    return (date.today() - CASE_START).days

def update_integrity():
    """Обновляет integrity.json каждые 6 часов"""
    data = {
        "case": CASE_ID,
        "idnp": IDNP,
        "updated": datetime.utcnow().isoformat() + "Z",
        "days_without_investigation": days_without_investigation(),
        "status": "ACTIVE · JUS COGENS VIOLATED"
    }
    path = os.path.join(DATA_DIR, "integrity.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    log.info(f"integrity.json updated: {days_without_investigation()} days")

def ask_ollama(question: str, model: str = "qwen2.5:7b") -> str:
    """Отправляет вопрос в Ollama и получает ответ"""
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model,
                "prompt": f"[SYSTEM]\n{SYSTEM_PROMPT}\n\n[USER]\n{question}",
                "stream": False,
                "options": {"temperature": 0.3, "num_predict": 500}
            },
            timeout=120
        )
        return r.json().get("response", "")
    except Exception as e:
        log.error(f"Ollama error: {e}")
        return ""

def self_qa_cycle():
    """Робот задаёт сам себе вопросы и сохраняет ответы"""
    questions = [
        "Каков текущий статус дела CASE-MACHERET-1997-2026?",
        f"Сколько суток без расследования на дату {date.today()}?",
        "Почему принцип дополнительности МУС (ст.17) активирован?",
        "Что такое тройной ИДПН-подлог и каковы его юридические последствия?",
    ]

    log.info("=== Self-QA Cycle started ===")
    results = []
    for q in questions:
        log.info(f"Q: {q}")
        ans = ask_ollama(q)
        if ans:
            results.append({"question": q, "answer": ans, "timestamp": datetime.utcnow().isoformat()})
            log.info(f"A: {ans[:100]}...")

    if results:
        path = os.path.join(DATA_DIR, "robot_qa_log.json")
        existing = []
        try:
            with open(path) as f:
                existing = json.load(f)
        except:
            pass
        existing.extend(results)
        existing = existing[-100:]  # храним последние 100
        with open(path, "w") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)
        log.info(f"QA log updated: {len(results)} new entries")

def pull_model():
    """Загружает модель Ollama если нужна"""
    model = "qwen2.5:7b"
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        models = [m["name"] for m in r.json().get("models", [])]
        if not any(model in m for m in models):
            log.info(f"Pulling model: {model}")
            requests.post(f"{OLLAMA_URL}/api/pull", json={"name": model}, timeout=600)
    except Exception as e:
        log.warning(f"Could not pull model: {e}")

# ── РАСПИСАНИЕ ──
schedule.every(6).hours.do(update_integrity)
schedule.every(24).hours.do(self_qa_cycle)
schedule.every(72).hours.do(pull_model)

# ── ЗАПУСК ──
log.info("A©t0r Robot started")
log.info(f"Case: {CASE_ID} | Days: {days_without_investigation()}")
update_integrity()
pull_model()

while True:
    schedule.run_pending()
    time.sleep(60)
