#!/bin/bash
# Скрипт интеграции поиска в дорожную карту
# Протокол: STAGED_ASSEMBLY v2.0

TARGET="./mirrors/evidence-roadmap.html"

# Вставляем стили и структуру перед закрывающим тегом </body>
# Используем временный файл для сборки
cat > roadmap_patch.html << 'EOF'
<style>
    #ti-ula-search-container { font-family: monospace; padding: 20px; background: #000; color: #0f0; border: 1px solid #0f0; margin: 20px 0; }
    #search-input { width: 100%; padding: 10px; background: #111; border: 1px solid #0f0; color: #0f0; margin-bottom: 10px; }
    .evidence-item { padding: 5px; border-bottom: 1px dotted #333; display: flex; justify-content: space-between; }
    .evidence-item:hover { background: #111; }
    .evidence-link { color: #0f0; text-decoration: none; }
    .evidence-link:hover { text-decoration: underline; }
    .file-size { color: #555; font-size: 0.8em; }
</style>

<div id="ti-ula-search-container">
    <h3>[ TERMINAL ] TI-ULA EVIDENCE SEARCH</h3>
    <input type="text" id="search-input" placeholder="Введите имя файла или фрагмент доказательства..." oninput="searchEvidence()">
    <div id="results-count"></div>
    <div id="search-results"></div>
</div>
EOF
cat >> roadmap_patch.html << 'EOF'
<script>
let evidenceData = [];

// Загрузка индекса
fetch('evidence_index.json')
    .then(response => response.json())
    .then(data => {
        evidenceData = data;
        console.log("TI-ULA: Индекс загружен, объектов:", evidenceData.length);
    });

function searchEvidence() {
    const query = document.getElementById('search-input').value.toLowerCase();
    const resultsContainer = document.getElementById('search-results');
    const countContainer = document.getElementById('results-count');
    
    if (query.length < 2) {
        resultsContainer.innerHTML = '';
        countContainer.innerHTML = '';
        return;
    }

    const filtered = evidenceData.filter(item => 
        item.name.toLowerCase().includes(query)
    );

    countContainer.innerHTML = `Найдено совпадений: ${filtered.length}`;
    
    resultsContainer.innerHTML = filtered.slice(0, 50).map(item => `
        <div class="evidence-item">
            <a href="https://drive.google.com/file/d/${item.id}/view" target="_blank" class="evidence-link">
                > ${item.name}
            </a>
            <span class="file-size">${(item.size / 1024 / 1024).toFixed(2)} MB</span>
        </div>
    `).join('');
    
    if (filtered.length > 50) {
        resultsContainer.innerHTML += '<div style="color:#555; padding: 10px;">...показаны первые 50 результатов. Уточните запрос.</div>';
    }
}
</script>
EOF
# Внедряем патч перед </body> (если он есть) или просто в конец файла
if grep -q "</body>" "$TARGET"; then
    sed -i '/<\/body>/e cat roadmap_patch.html' "$TARGET"
else
    cat roadmap_patch.html >> "$TARGET"
fi

rm roadmap_patch.html
echo -e "\e[32m[ OK ] Поисковый движок интегрирован в $TARGET\e[0m"
echo -e "\e[36m--- TI-ULA ОБНОВЛЕНИЕ ЗАВЕРШЕНО ---\e[0m"
