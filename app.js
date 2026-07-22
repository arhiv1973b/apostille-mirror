document.addEventListener('DOMContentLoaded', () => {
    fetch('manifest.json')
        .then(response => response.json())
        .then(data => {
            // Render evidence grid
            const grid = document.getElementById('dynamic-evidence-grid');
            if (grid) {
                grid.innerHTML = data.evidenceNodes.map(node => `
                    <div class="ev-card">
                        <div class="ev-card-icon">${node.icon}</div>
                        <div class="ev-card-title">${node.title}</div>
                        <div class="ev-card-body">
                            ${node.num ? `<span class="num">${node.num}</span>` : ''}
                            ${node.body}
                        </div>
                    </div>
                `).join('');
            }

            // Render forensic data
            const updateField = (id, value, className = '') => {
                const el = document.getElementById(id);
                if (el) {
                    el.textContent = value;
                    if (className) el.className = 'val ' + className;
                }
            };

            updateField('f-subject', data.forensicData.subject, 'gold');
            updateField('f-theftAmount', data.forensicData.theftAmount, 'red');
            updateField('f-subjects', data.forensicData.subjects, 'red');
            updateField('f-method', data.forensicData.method);
            updateField('f-timestamp', data.forensicData.timestamp, 'green');
            updateField('f-merkleRoot', data.forensicData.merkleRoot, 'green');
        })
        .catch(err => console.error('Error loading manifest:', err));
});
