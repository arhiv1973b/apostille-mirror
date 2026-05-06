import re, json, uuid, os
from datetime import datetime

def parse_audit_log(log_file_path, output_json_path):
    nodes = []
    found_re = re.compile(r"✅ НАЙДЕНО: (?P<code>.+) \| Стр\. (?P<page>\d+) \| Файл: (?P<file>.+)")
    context_re = re.compile(r"\[Context\]: \.\.\.(?P<text>.+)\.\.\.")
    if not os.path.exists(log_file_path): return

    with open(log_file_path, 'r', encoding='utf-8') as f:
        current = None
        for line in f:
            m_found = found_re.search(line)
            if m_found:
                code = m_found.group("code").strip()
                if "UNIX" in code: cls = "Jurisdiction Forgery (UN->UNIX)"
                elif "555" in code: cls = "Digital Twin / Metadata Forgery"
                elif "455" in code: cls = "Fiscal Anomaly"
                else: cls = "Primary Identity Mapping"
                current = {
                    "node_id": f"EV-{str(uuid.uuid4())[:8].upper()}",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "target": code,
                    "classification": cls,
                    "source": {"file": m_found.group("file"), "page": int(m_found.group("page"))}
                }
                continue
            m_ctx = context_re.search(line)
            if m_ctx and current:
                current["forensic_context"] = m_ctx.group("text").strip()
                nodes.append(current)
                current = None

    registry = {
        "registry_meta": {"caseId": "CASE-MACHERET-1997-2026", "protocol": "TI-ULA-CORE-v1.3.0", "total_nodes": len(nodes)},
        "evidence_nodes": nodes
    }
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    parse_audit_log("final_audit_report.txt", "evidence_registry.json")