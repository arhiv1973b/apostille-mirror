const tileGrid = document.getElementById('tileGrid');
const searchBox = document.getElementById('searchBox');
const modal = document.getElementById('modal');
const modalIframe = document.getElementById('modalIframe');

async function loadRegistry() {
    try {
        const response = await fetch('EVIDENCE_REGISTRY_INDEX.json');
        const data = await response.json();
        renderTiles(data.evidence_nodes || []);
    } catch (e) { console.error("Ошибка загрузки реестра:", e); }
}

function renderTiles(nodes) {
    tileGrid.innerHTML = '';
    nodes.forEach(node => {
        try {
            const tile = document.createElement('div');
            tile.className = 'tile';
            tile.innerHTML = `<h3>${node.node_id || 'N/A'}</h3>
                              <p>${node.document_ref || 'Без описания'}</p>
                              <small>Hash: ${node.hash_sha256?.substring(0,16) || '...'}</small>`;
            
            tile.onclick = () => openModal(node.drive_iframe_src);
            tileGrid.appendChild(tile);
        } catch (e) { console.warn("Ошибка рендеринга узла:", e); }
    });
}

function openModal(src) {
    if (!src) return;
    // URL Transformation to preview
    const previewUrl = src.replace(/\/view.*$/, '/preview').replace(/\/edit.*$/, '/preview');
    modalIframe.src = previewUrl;
    modal.style.display = 'block';
}

document.querySelector('.close').onclick = () => { modal.style.display = 'none'; modalIframe.src = ''; };

// Live Search
searchBox.oninput = (e) => {
    const val = e.target.value.toLowerCase();
    document.querySelectorAll('.tile').forEach(tile => {
        const text = tile.innerText.toLowerCase();
        tile.style.display = text.includes(val) ? '' : 'none';
    });
};

loadRegistry();
