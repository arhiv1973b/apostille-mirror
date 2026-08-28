import json
import subprocess


def read_git_json(filepath):
    try:
        res = subprocess.run(
            ["git", "show", f"d4e1da34291bcf92d29fe2af51d2b29c89634a6f:{filepath}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return json.loads(res.stdout) if res.returncode == 0 else None
    except Exception:
        return None


print("Чтение структуры связей (edges)...")
edges_data = read_git_json("registry_chunks/edges.json")
edges = edges_data.get("edges", []) if edges_data else []

print("Чтение узлов доказательств (nodes)...")
vis_nodes = []
vis_edges = []
keywords = ["1-568", "fincombank", "nbm", "jus_cogens", "venice"]

# Читаем чанки (1-7)
for i in range(1, 8):
    chunk = read_git_json(f"registry_chunks/registry_chunk_{i}.json")
    if not chunk:
        continue

    for node in chunk.get("evidence_nodes", []):
        node_id = node.get("node_id")
        doc_ref = node.get("document_ref", "").lower()

        # Определяем категорию и цвет
        color = "#4a4a4a"  # Default
        if "1-568" in doc_ref:
            color = "#cc0000"  # Detention (Красный)
        elif "fincombank" in doc_ref or "nbm" in doc_ref:
            color = "#ff8c00"  # Blockade (Оранжевый)
        elif "jus_cogens" in doc_ref or "venice" in doc_ref:
            color = "#0000cc"  # Jus Cogens (Синий)

        # Добавляем узел, если он ключевой
        if color != "#4a4a4a":
            label = f"[{node_id}]\n{node.get('document_ref', 'Unknown')[:30]}..."
            vis_nodes.append(
                f"{{id: '{node_id}', label: '{label}', color: '{color}', shape: 'box'}}"
            )

# Формируем связи только для найденных ключевых узлов
node_ids = [n.split("id: '")[1].split("'")[0] for n in vis_nodes]
for edge in edges:
    if edge["source"] in node_ids or edge["target"] in node_ids:
        vis_edges.append(
            f"{{from: '{edge['source']}', to: '{edge['target']}', label: '{edge.get('relation', '')}'}}"
        )

html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>TI-ULA Evidence Graph: CASE-MACHERET-1997-2026</title>
  <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style type="text/css">
    body {{ background-color: #1e1e1e; color: white; font-family: sans-serif; margin: 0; }}
    #mynetwork {{ width: 100vw; height: 100vh; border: none; }}
    #legend {{ position: absolute; top: 10px; left: 10px; background: rgba(0,0,0,0.7); padding: 15px; border-radius: 5px; }}
  </style>
</head>
<body>
<div id="legend">
    <h3>CASE-MACHERET-1997-2026</h3>
    <p><span style="color:#cc0000;">■</span> Detention (Root Cause: 1-568/98)</p>
    <p><span style="color:#ff8c00;">■</span> Financial Blockade (Fincombank)</p>
    <p><span style="color:#0000cc;">■</span> Jus Cogens / Erga Omnes</p>
</div>
<div id="mynetwork"></div>
<script type="text/javascript">
  var nodes = new vis.DataSet([{",".join(vis_nodes)}]);
  var edges = new vis.DataSet([{",".join(vis_edges)}]);
  var container = document.getElementById('mynetwork');
  var data = {{ nodes: nodes, edges: edges }};
  var options = {{ edges: {{ arrows: 'to', color: '#aaaaaa' }}, physics: {{ stabilization: false, barnesHut: {{ springLength: 200 }} }} }};
  var network = new vis.Network(container, data, options);
</script>
</body>
</html>
"""

with open("evidence_map.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print("Успех! Граф сохранен в файл: evidence_map.html. Откройте его в любом браузере.")
