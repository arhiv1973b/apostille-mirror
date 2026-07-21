import json
import os

manifest_data = [
    {"name": "apostila (3).html", "id": "1ANPhmyBv_eJLnLAJDrfSD4ZUl-A9KIFS"},
    {"name": "apostila (1).html", "id": "1hBeoGpOP15qiOcGYJnOR3_1Pj7_NsAlZ"},
    {"name": "Către Judecătoria Chișinău (sediul Ciocana_Buiucani).html", "id": "1idFIIABvcFEvo9wNHWym3u1YEw62IKzP"},
    {"name": "1-568 от Центра (Конфликтующая копия пользователя Alexei Macheret 2022-02-14 02_1.12.08 PM).html", "id": "1I9lIl_-oeyQtGnukxaFGU6oy5XEW3oZO"},
    {"name": "08 11 2006 - для Судов по ИДНП. 2005 года определяя невиность_Исправлен.signed.html", "id": "1jtsiDbLsoCano7s5bpLd55TtWVq26rDF"},
    {"name": "Către Judecătoria Chișinău (sediul Ciocana_Buiucani).signed.html", "id": "10OSvLUiCqkXMr5FwiUeAvlyAsJhWessF"},
    {"name": "apostille_archive_english.html", "id": "1SK9u6SDOLy0rkyiszFOyC_kvAmYlYqDv"},
    {"name": "apostille_registry_working.signed.html", "id": "1Z7Xy-VSKzfCPOA58Fe96prW5KJAmlcwm"},
    {"name": "apostille_archive_english.signed.html", "id": "19ad2h9ObpfE-qlzQ2artovSSO3hcxjTZ"},
    {"name": "A©tor arhiv si actual reestrf_4.html", "id": "1Od8NkZq_9NFbiD_R5ZH78PYutYiWjEyN"},
    {"name": "apostille_archive_english_fixed.html", "id": "1uFMNlgKMJ3O2LYHw7jIxTJCLHDkEnx5c"},
    {"name": "A©tor arhiv si actual reestrf_3.html", "id": "1auCtuIxRSofBnTZM68fUSfJadr407vGf"},
    {"name": "Actor of Moldova.html", "id": "18zhjxUzTZVA6LNi2ynxH5DGKTGVZJPHy"},
    {"name": "apostila_2.html", "id": "1Cx2g0kp-BpR9DbinPgUhXjfTSSruxQvw"},
    {"name": "doumentii na nsasledstvo.html", "id": "17KIplpRUqQBC_pQZY-C-0nwck3rResxG"},
    {"name": "Actor of Moldova.signed.html", "id": "1d3y2XxsLd8JmsXoQ2ltBcICRvsWsrZLW"},
    {"name": "doumentii na nsasledstvo_1.html", "id": "14vwHfTKGD1tJ-xlZTQt64IBLJY1MVosW"},
    {"name": "+Виталий Чумак.конкретизируя r обязанность Налоговой.html", "id": "1Gtr0SsWoz2HSsjEAQQvYH8L1HbtSAfhr"},
    {"name": "apostille_registry_working_2.signed.html", "id": "1wEpVZacF3aJB0OOnYb2j2dIMzQjrILjE"},
    {"name": "doumentii na nsasledstvo_2.html", "id": "1s5XmXr7LIvSicpkQE_y5ZChIW9-CGV07"}
]

def generate_html(node):
    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Evidence Node: {node['name']}</title>
    <style>
        body {{ margin: 0; padding: 0; height: 100vh; display: flex; flex-direction: column; }}
        iframe {{ width: 100%; height: 100%; border: none; }}
        nav {{ padding: 10px; background: #eee; }}
    </style>
</head>
<body>
    <nav>
        <a href="../index.html">⬅ Назад</a>
    </nav>
    <iframe src="https://drive.google.com/viewerng/viewer?embedded=true&url=https://drive.google.com/uc?export=view&id={node['id']}"></iframe>
</body>
</html>"""
    with open(f"nodes/{node['name']}", "w", encoding="utf-8") as f:
        f.write(html_content)

os.makedirs("nodes", exist_ok=True)
for node in manifest_data:
    generate_html(node)

# Generate simple index
index_content = "<html><body><h1>Evidence Nodes</h1><ul>"
for node in manifest_data:
    index_content += f'<li><a href="nodes/{node["name"]}">{node["name"]}</a></li>'
index_content += "</ul></body></html>"
with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_content)
