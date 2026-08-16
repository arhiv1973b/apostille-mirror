import json
import os
import shutil

# --- Конфигурация путей ---
BASE_DIR = r"H:\ACTOR_DEV_ENV"
VB_EVENTS_PATH = os.path.join(BASE_DIR, r"evidence_registry\victoriabank_events.json")
TIMELINE_PATH = os.path.join(
    BASE_DIR, r"apostille-mirror\FORENSIC_TIMELINE_20260615.json"
)
GRAPH_PATH = os.path.join(BASE_DIR, "entity_graph.json")


def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    return None


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def sync_pipeline():
    print(f"[*] Чтение CAS-реестра: {VB_EVENTS_PATH}")
    vb_data = load_json(VB_EVENTS_PATH)
    if not vb_data or "events" not in vb_data:
        print(
            "[!] Ошибка: Неверный формат или файл victoriabank_events.json не найден."
        )
        return

    events = vb_data["events"]

    # --- 1. Интеграция в Таймлайн (reconstruct-timeline) ---
    print(f"[*] Обработка хронологии: {TIMELINE_PATH}")
    timeline = load_json(TIMELINE_PATH) or []

    if os.path.exists(TIMELINE_PATH):
        backup_path = TIMELINE_PATH + ".bak"
        shutil.copy2(TIMELINE_PATH, backup_path)
        print(f"    [+] Создан бэкап таймлайна: {backup_path}")

    # Индексируем существующие источники для дедупликации
    existing_sources = {item.get("Source", "") for item in timeline}
    added_to_timeline = 0

    for event in events:
        # Формируем уникальную ссылку на источник в рамках CAS
        source_ref = f"victoriabank_events.json#{event['id']}"

        if source_ref not in existing_sources:
            timeline.append(
                {
                    "Timestamp": event["timestamp"],
                    "Type": "FINANCIAL_EVENT",
                    "Detail": event["title"],
                    "Source": source_ref,
                }
            )
            added_to_timeline += 1

    # Сортировка по времени (ISO 8601 корректно сортируется как строка)
    timeline.sort(key=lambda x: x.get("Timestamp", ""))
    save_json(timeline, TIMELINE_PATH)
    print(f"    [+] Добавлено событий в таймлайн: {added_to_timeline}")

    # --- 2. Инициализация и обновление Графа Сущностей (build-entity-graph) ---
    print(f"[*] Обновление графа сущностей: {GRAPH_PATH}")
    graph = load_json(GRAPH_PATH) or {"nodes": [], "edges": []}

    def add_node(node_id, label, node_type):
        if not any(n.get("id") == node_id for n in graph["nodes"]):
            graph["nodes"].append({"id": node_id, "label": label, "type": node_type})

    def add_edge(source, target, relation, ref_id):
        edge_id = f"{source}--{target}--{ref_id}"
        if not any(e.get("id") == edge_id for e in graph["edges"]):
            graph["edges"].append(
                {
                    "id": edge_id,
                    "source": source,
                    "target": target,
                    "relation": relation,
                    "reference": ref_id,
                }
            )

    # Базовые узлы для текущего контекста
    add_node("ACTOR_MACHERET", "Alexei Macheret", "PERSON")
    add_node("ORG_VICTORIABANK", "Victoriabank", "ORGANIZATION")

    added_edges = 0
    for event in events:
        # Связываем персону и организацию через конкретный инцидент
        add_edge(
            source="ACTOR_MACHERET",
            target="ORG_VICTORIABANK",
            relation="FINANCIAL_INTERACTION",
            ref_id=event["id"],
        )
        added_edges += 1

    save_json(graph, GRAPH_PATH)
    print(
        f"    [+] Добавлено/обновлено узлов: {len(graph['nodes'])}, новых связей: {added_edges}"
    )
    print("[*] Интеграция успешно завершена.")


if __name__ == "__main__":
    sync_pipeline()
