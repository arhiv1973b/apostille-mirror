document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('dynamic-evidence-grid');
    const fallbackMessage = 'Manifest unavailable. Static evidence index remains available.';

    const renderFallback = () => {
        if (grid) {
            grid.innerHTML = `
                <div class="ev-card">
                    <div class="ev-card-icon">⚠️</div>
                    <div class="ev-card-title">Fallback mode</div>
                    <div class="ev-card-body">${fallbackMessage}</div>
                </div>
            `;
        }
    };

    fetch('manifest.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Manifest request failed: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const evidenceNodes = Array.isArray(data?.evidenceNodes) ? data.evidenceNodes : [];
            const forensicData = data?.forensicData || {};

            if (grid) {
                if (evidenceNodes.length === 0) {
                    renderFallback();
                    return;
                }

                grid.innerHTML = evidenceNodes.map(node => `
                    <div class="ev-card">
                        <div class="ev-card-icon">${node.icon || '•'}</div>
                        <div class="ev-card-title">${node.title || 'Evidence node'}</div>
                        <div class="ev-card-body">
                            ${node.num ? `<span class="num">${node.num}</span>` : ''}
                            ${node.body || ''}
                        </div>
                    </div>
                `).join('');
            }

            const updateField = (id, value, className = '') => {
                const el = document.getElementById(id);
                if (el && value !== undefined && value !== null) {
                    el.textContent = value;
                    if (className) el.className = 'val ' + className;
                }
            };

            updateField('f-subject', forensicData.subject, 'gold');
            updateField('f-theftAmount', forensicData.theftAmount, 'red');
            updateField('f-subjects', forensicData.subjects, 'red');
            updateField('f-method', forensicData.method);
            updateField('f-timestamp', forensicData.timestamp, 'green');
            updateField('f-merkleRoot', forensicData.merkleRoot, 'green');
        })
        .catch(err => {
            console.error('Error loading manifest:', err);
            renderFallback();
        });
});
