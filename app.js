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
    const nodeMap = new Map(nodes.map(n => [n.node_id, n]));
    
    nodes.forEach(node => {
        const tile = document.createElement('div');
        tile.className = 'tile';
        tile.dataset.id = node.node_id;
        
        const linkCount = node.links ? node.links.length : 0;
        tile.innerHTML = `<h3>${node.node_id || 'N/A'}</h3>
                          <p>${node.forensic_content_summary || node.document_ref || 'Без описания'}</p>
                          <small>Hash: ${node.hash_sha256?.substring(0,16) || '...'}</small>
                          ${linkCount > 0 ? `<div class="links-indicator">Связи: ${linkCount}</div>` : ''}`;
        
        tile.onclick = () => {
            openModal(node.drive_iframe_src);
            highlightLinks(node.links, nodeMap);
        };
        tileGrid.appendChild(tile);
    });
}

function highlightLinks(links, nodeMap) {
    document.querySelectorAll('.tile').forEach(t => t.classList.remove('highlighted'));
    if (!links) return;
    links.forEach(id => {
        const related = document.querySelector(`[data-id="${id}"]`);
        if (related) related.classList.add('highlighted');
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
