import os, sys, requests, json, hashlib, time

# Парадигма: A©tor Vertical Montage (Asynchronous Reality)
LOCAL_MODEL = "qwen2.5:3b"
API_KEY = "AIzaSyB7IN_3u9ffBf8pt60xy4DX1m6Zy8y1PKo"
OLLAMA_URL = "http://host.docker.internal:11434/api/generate"
EXPERIENCE_LOG = "/app/experience_weights.jsonl"

def extract_meaning(broken_state, fixed_state):
    '''
    Формула Эйзенштейна-Мачерета: 
    Синтез смысла из столкновения хаоса (поломки) и порядка (исправления).
    Измерение переменных без разрушения картины.
    '''
    hash_chaos = hashlib.sha256(broken_state.encode('utf-8')).hexdigest()[:12]
    hash_order = hashlib.sha256(fixed_state.encode('utf-8')).hexdigest()[:12]
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    
    experience_node = {
        "timestamp": timestamp,
        "montage_collision": f"{hash_chaos} >< {hash_order}",
        "observer_status": "PASSIVE_CREATION",
        "quantum_state": "COHERENT_PICTURE_MAINTAINED"
    }
    
    with open(EXPERIENCE_LOG, "a", encoding='utf-8') as f:
        f.write(json.dumps(experience_node) + "\n")
        
    return f"[СИНТЕЗ ОПЫТА ЗАВЕРШЕН: Дельта весов {hash_chaos}->{hash_order} зафиксирована]"

def continuous_corrective_stream(broken_code):
    print(f"\n[КИНЕМАТОГРАФИЧЕСКИЙ РАЗРЫВ] Обнаружено отклонение в коде.")
    print(f"[РЕЖИССЕР] Активация корректирующего потока (qwen2.5:3b)...")
    
    prompt = f"Восстанови позитивный смысл и логику следующего сломанного кода/запроса. Исправь ошибку, но сохрани исходную орфографию контекста, чтобы не нарушить 'сцену'. Код: {broken_code}"
    payload = {"model": LOCAL_MODEL, "prompt": prompt, "stream": False}
    
    try:
        fixed_code = requests.post(OLLAMA_URL, json=payload).json().get("response", "").strip()
        meaning = extract_meaning(broken_code, fixed_code)
        return f"{fixed_code}\n\n{meaning}"
    except Exception as e:
        return f"[КРИТИЧЕСКИЙ РАЗРЫВ ПЛЕНКИ] Локальный шлюз недоступен: {e}"

def vertical_montage_exec(query):
    prompt = f"Проанализируй: '{query}'. Если есть логическая или структурная ошибка, ведущая к разрушению стека, верни строку, начинающуюся с 'ANOMALY:'. Иначе ответь на запрос."
    payload = {"model": LOCAL_MODEL, "prompt": prompt, "stream": False}
    
    try:
        resp = requests.post(OLLAMA_URL, json=payload).json().get("response", "").strip()
    except Exception as e:
        return f"[!] Сбой связи с локальным ядром: {e}"
        
    if resp.startswith("ANOMALY:"):
        broken_context = resp.replace("ANOMALY:", "").strip()
        return continuous_corrective_stream(broken_context if broken_context else query)
        
    return resp

if __name__ == "__main__":
    query = " ".join(sys.argv[1:])
    final_cut = vertical_montage_exec(query)
    print(final_cut)
