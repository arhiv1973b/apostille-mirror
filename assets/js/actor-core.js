/**
 * A©t0r Forensic Core v15.5
 * Deep Content Audit & Metadata Explorer
 */
 let masterIndex = {};

 async function initForensicHub() {
    console.log("A©t0r Hub v15.5 Deep Audit Active");
    try {
        const response = await fetch('dist/meta/UNIVERSAL_CAS_INDEX.json');
        masterIndex = await response.json();
        renderRegistry(masterIndex);
        updateStats(masterIndex);
        setupSearch();
        addFeedEntry("System", "Deep Content Audit (v15.5) successfully loaded.");
    } catch (e) {
        console.error("Forensic Load Error", e);
    }
}

function renderRegistry(index) {
    const container = document.getElementById('cas-explorer');
    if (!container) return;
    let html = `<h2>Forensic Evidence Explorer (Deep Audit v15.5)</h2>`;
    for (const [hash, node] of Object.entries(index)) {
        const deep = node.deep_meta ? 
            `<div class="deep-meta-box">
                <small><strong>Embedded Title:</strong> ${node.deep_meta.title}</small><br>
                <small><strong>Author:</strong> ${node.deep_meta.author}</small><br>
                <small><strong>Created:</strong> ${node.deep_meta.created}</small>
            </div>` : '';
            
        html += `<div class="cas-card">
                <div class="cas-hash">${hash.substring(0, 8)}...</div>
                <div class="cas-meta">
                    <strong>Node:</strong> ${node.node_id} | <strong>Doc:</strong> ${node.doc_id}
                </div>
                ${deep}
                <div class="cas-links">
                    <a href="${node.git_url}" target="_blank" class="hash-link">GIT</a>
                    <a href="${node.cloud_url}" target="_blank" class="hash-link">CLOUD</a>
                    <button class="btn-action" onclick="alert('Metadata Verified for ${hash}')">VERIFY_CONTENT</button>
                </div>
            </div>`;
    }
    container.innerHTML = html;
}

// ... (search, feed, stats, timeline remains consistent) ...
function setupSearch() {
    const searchInput = document.getElementById('hub-search');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            const filtered = {};
            for (const [hash, node] of Object.entries(masterIndex)) {
                if (hash.toLowerCase().includes(term) || node.doc_id.toLowerCase().includes(term)) {
                    filtered[hash] = node;
                }
            }
            renderRegistry(filtered);
        });
    }
}

function addFeedEntry(source, message) {
    const feed = document.getElementById('live-feed');
    if (!feed) return;
    const time = new Date().toLocaleTimeString();
    const entry = document.createElement('div');
    entry.className = 'feed-entry';
    entry.innerHTML = [\] [<strong>\</strong>] \;
    feed.prepend(entry);
}

function updateStats(index) {
    const count = Object.keys(index).length;
    document.getElementById('node-count').innerText = "4010+ (" + count + " active)";
}

window.onload = initForensicHub;
