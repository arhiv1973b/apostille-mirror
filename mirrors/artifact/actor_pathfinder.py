import networkx as nx
import hashlib
import json
import datetime

class JusCogensNode:
    def __init__(self, id, title, doc_date, apo_date, content):
        self.id = id
        self.title = title
        self.doc_date = self.parse_date(doc_date)
        self.apo_date = self.parse_date(apo_date)
        self.content = content
        
        # Расчет временного разрыва
        self.delay_days = (self.apo_date - self.doc_date).days if self.doc_date and self.apo_date else 0
        self.integrity_weight = self.evaluate_integrity()

    def parse_date(self, date_str):
        for fmt in ('%d.%m.%Y', '%Y-%m-%d', '%d-%m-%Y'):
            try: return datetime.datetime.strptime(date_str.strip(), fmt)
            except: continue
        return None

    def evaluate_integrity(self):
        # Базовая логика: задержка более 365 дней снижает вес узла на 50%
        # Разрыв в 6354 дня обнуляет доверие (Toxic)
        weight = 1.0
        if self.delay_days > 365: weight *= 0.5
        if self.delay_days > 5000: weight *= 0.1
        return weight

# Инициализация графа Сектора 9
G = nx.DiGraph()

# Данные LUPAŞCU SESSION (Загрузка аномалий)
nodes_data = [
    ("ROOT_JC", "Jus Cogens Base", "24.07.1997", "24.07.1997", "Original Ratification"),
    ("IMWM44AZGX6N6", "Lupașcu Entry", "12.03.2024", "26.03.2024", "Session Record"),
    ("DR4Y1584JW9F4", "Temporal Breach", "13.10.1998", "15.03.2016", "Evidence Suppression"),
    ("DLTP7B8ZHWGQ7", "System Mimicry", "20.01.2026", "20.01.2026", "Forgery Analog"),
    ("4J20E98WFY7J2", "Identity Ghost", "28.03.2026", "28.03.2026", "Vacuum Node")
]

audit_log = []
total_weight = 0

for id, title, d_date, a_date, content in nodes_data:
    node = JusCogensNode(id, title, d_date, a_date, content)
    G.add_node(node.id, title=node.title, delay=node.delay_days, weight=node.integrity_weight)
    
    status = "⚠️ TOXIC/ANOMALY" if node.integrity_weight < 0.6 else "✅ VERIFIED"
    audit_log.append(f"{status} | {node.id} | Delay: {node.delay_days} days | Weight: {node.integrity_weight}")
    total_weight += node.integrity_weight

integrity_index = (total_weight / len(nodes_data)) * 100

# Сохранение финального отчета
with open("audit_report.txt", "w") as f:
    f.write(f"--- A©TŌR COURT REPORT (LUPAŞCU SESSION) | {datetime.date.today()} ---\n")
    for line in audit_log:
        f.write(line + "\n")
    f.write(f"\n--- GLOBAL INTEGRITY INDEX: {integrity_index:.2f}% ---\n")

print(f"--- [A©tōr] Расчет завершен. Индекс целостности: {integrity_index:.2f}% ---")
