import re, json, uuid, os

def parse_audit_log(log_file_path, output_json_path):
    nodes = []
    # Гибкий regex для поиска меток, игнорирующий мусорные символы
    found_re = re.compile(r"✅\s*НАЙДЕНО:\s*(?P<code>.+?)\s*\|\s*Стр\.\s*(?P<page>\d+)\s*\|\s*Файл:\s*(?P<file>.+)")
    context_re = re.compile(r"\[Context\]:\s*\.\.\.(?P<text>.+?)\.\.\.")
    
    if not os.path.exists(log_file_path):
        print(f"Error: {log_file_path} not found.")
        return

    # Читаем файл, пробуя разные кодировки (UTF-16 и UTF-8)
    content = ""
    for enc in ['utf-16', 'utf-8-sig', 'utf-8', 'cp1251']:
        try:
            with open(log_file_path, 'r', encoding=enc) as f:
                content = f.read()
            if "НАЙДЕНО" in content:
                print(f"[*] Файл успешно прочитан в кодировке {enc}")
                break
        except: continue

    lines = content.splitlines()
    current = None
    
    for line in lines:
        line = line.strip()
        m_found = found_re.search(line)
        if m_found:
            code = m_found.group("code").strip()
            # Классификация улик
            if "UNIX" in code: cls = "Jurisdiction Forgery (UN->UNIX)"
            elif "555" in code: cls = "Digital Twin / Metadata Forgery"
            elif "455" in code: cls = "Fiscal Anomaly"
            else: cls = "Primary Identity Mapping"
            
            current = {
                "node_id": f"EV-{str(uuid.uuid4())[:8].upper()}",
                "target": code,
                "classification": cls,
                "source": {"file": m_found.group("file").strip(), "page": int(m_found.group("page"))}
            }
            nodes.append(current)
            continue
        
        m_ctx = context_re.search(line)
        if m_ctx and nodes:
            nodes[-1]["forensic_context"] = m_ctx.group("text").strip()

    registry = {
        "registry_meta": {
            "caseId": "CASE-MACHERET-1997-2026",
            "protocol": "TI-ULA-CORE-v1.3.1",
            "total_nodes": len(nodes)
        },
        "evidence_nodes": nodes
    }
    
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    print(f"✅ Реестр успешно материализован. Собрано узлов: {len(nodes)}")

if __name__ == "__main__":
    parse_audit_log("final_audit_report.txt", "evidence_registry.json")