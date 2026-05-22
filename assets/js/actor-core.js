/**
 * A©t0r Forensic Core v15.2
 * Enhanced with Search & Timeline Engine
 */
let masterIndex = {};

async function initForensicHub() {
    console.log("A©t0r Hub v15.2 Active");
    try {
        const response = await fetch('dist/meta/UNIVERSAL_CAS_INDEX.json');
        masterIndex = await response.json();
        renderRegistry(masterIndex);
        updateStats(masterIndex);
        setupSearch();
    } catch (e) {
        console.error("Forensic Load Error", e);
    }
}

function setupSearch() {
    const searchInput = document.getElementById('hub-search');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            const filtered = {};
            for (const [hash, node] of Object.entries(masterIndex)) {
                if (hash.toLowerCase().includes(term) || 
                    node.doc_id.toLowerCase().includes(term) || 
                    node.node_id.toLowerCase().includes(term)) {
                    filtered[hash] = node;
                }
            }
            renderRegistry(filtered);
        });
    }
}

function renderRegistry(index) {
    const container = document.getElementById('cas-explorer');
    if (!container) return;
    
    let html = '<h2>CAS Evidence Explorer</h2>';
    const entries = Object.entries(index);
    
    if (entries.length === 0) {
        html += '<p style="color: #e74c3c;">No nodes matching search criteria.</p>';
    } else {
        for (const [hash, node] of entries) {
            html += 
                <div class="cas-card">
                    <div class="cas-hash">\...</div>
                    <div class="cas-meta">
                        <strong>Node:</strong> \ | 
                        <strong>Doc:</strong> \ | 
                        <strong>Status:</strong> \
                    </div>
                    <div class="cas-links">
                        <a href="\" target="_blank" class="hash-link">GITHUB_MIRROR</a>
                        <a href="\" target="_blank" class="hash-link">GDRIVE_CLOUD</a>
                    </div>
                </div>
            ;
        }
    }
    container.innerHTML = html;
}

function updateStats(index) {
    const count = Object.keys(index).length;
    const nodeEl = document.getElementById('node-count');
    if (nodeEl) nodeEl.innerText = "4010+ (" + count + " indexed)";
}

window.onload = initForensicHub;
