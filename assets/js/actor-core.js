/**
 * A©t0r Forensic Core v15.0
 * Content Addressable Storage (CAS) Resolver & UI Engine
 */
async function initForensicHub() {
    console.log("A©t0r Hub v15.0 Active");
    try {
        const response = await fetch('dist/meta/UNIVERSAL_CAS_INDEX.json');
        const index = await response.json();
        renderRegistry(index);
        updateStats(index);
    } catch (e) {
        console.error("CAS Index Load Failed", e);
    }
}

function renderRegistry(index) {
    const container = document.getElementById('cas-explorer');
    if (!container) return;
    
    let html = '';
    for (const [hash, node] of Object.entries(index)) {
        html += <div class="cas-card">
                <div class="cas-hash">\...</div>
                <div class="cas-meta">Node: \ | ID: \</div>
                <div class="cas-links">
                    <a href="\" target="_blank" class="hash-link">GITHUB_RAW</a>
                    <a href="\" target="_blank" class="hash-link">GDRIVE_NODE</a>
                </div>
            </div>;
    }
    container.innerHTML = html;
}

function updateStats(index) {
    const count = Object.keys(index).length;
    const nodeEl = document.getElementById('node-count');
    if (nodeEl) nodeEl.innerText = "4010+ (" + count + " active)";
}

window.onload = initForensicHub;
