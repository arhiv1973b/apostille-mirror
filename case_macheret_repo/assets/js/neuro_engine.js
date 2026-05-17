/** 
 * A©tor Authority · Neuro-Engine Core v3.0 (CATHARSIS ENGINE)
 * Protocol: Jus Cogens Erga Omnes
 * Architecture: Eisenstein / Macheret Cinematic Transmutation
 * Concept: The Wall dissolves. Manipulation is shattered. The King is Naked.
 */

const CatharsisEngine = {
    metadata: null,
    vaultBase: "https://drive.google.com/uc?export=download&id=",
    
    // Strict regex to protect against backslashes, bugs, and metadata overwriting.
    // Hashes must be pure 64-character hex strings.
    hashPattern: /^[a-fA-F0-9]{64}$/,

    async init() {
        console.log("A©tor Protocol: Initiating Catharsis Sequence...");
        await this.loadMetadata();
        this.constructTheWall();
        this.activateJusCogensVectors();
    },

    async loadMetadata() {
        try {
            // Fetch metadata. Protected source of Actual Fact.
            const response = await fetch('/neuro_metadata_massive.json');
            this.metadata = await response.json();
            console.log(`Catharsis Engine: ${this.metadata.nodes.length} nodes of Brute Fact synchronized.`);
        } catch (e) {
            console.error("Catharsis Engine: Protocol interception detected or metadata missing.", e);
        }
    },

    sanitizeHash(hash) {
        // Protects the node from manipulation, backslashes, and malicious payloads.
        if (typeof hash !== 'string') return null;
        const cleanHash = hash.replace(/[\/\\]/g, '').trim();
        return this.hashPattern.test(cleanHash) ? cleanHash : null;
    },

    resolveHash(rawHash) {
        if (!this.metadata) return null;
        const safeHash = this.sanitizeHash(rawHash);
        if (!safeHash) return null;

        const node = this.metadata.nodes.find(n => n.hash === safeHash);
        if (node) {
            return this.vaultBase + (node.file_id || node.id || node.vault_id); 
        }
        return null;
    },

    constructTheWall() {
        // Injecting the visual algorithms of Eisenstein/Macheret
        const style = document.createElement('style');
        style.textContent = `
            /* State 1: The Wall (Illusion of Burden) */
            .neuro-link, .evidence-card, .pillar {
                position: relative;
                overflow: hidden;
                transition: all 0.8s cubic-bezier(0.25, 1, 0.5, 1);
                filter: grayscale(100%) contrast(1.5);
                opacity: 0.8;
                border: 1px solid #333;
                background: #0a0a0a;
            }
            .neuro-link::after {
                content: "THE WALL [ILLUSION]";
                position: absolute;
                top: 0; left: 0; width: 100%; height: 100%;
                background: repeating-linear-gradient(45deg, #111, #111 10px, #222 10px, #222 20px);
                color: #555; display: flex; align-items: center; justify-content: center;
                font-family: monospace; letter-spacing: 2px;
                transition: opacity 0.5s ease;
                z-index: 10;
            }

            /* State 2: Contradiction / Conflict of Frames */
            .neuro-link.conflict::after {
                opacity: 0.3;
                mix-blend-mode: difference;
            }

            /* State 3: Catharsis (Jus Cogens Truth Revealed) */
            .neuro-link.catharsis {
                filter: grayscale(0%) contrast(1) drop-shadow(0 0 10px rgba(201, 168, 76, 0.6));
                opacity: 1;
                border: 1px solid #c9a84c; /* Golden truth */
                background: transparent;
                text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
            }
            .neuro-link.catharsis::after {
                opacity: 0;
                pointer-events: none;
            }
            .jus-cogens-vector {
                color: #00ff00 !important;
                text-decoration: none;
                font-weight: bold;
                letter-spacing: 1px;
            }
        `;
        document.head.appendChild(style);
    },

    activateJusCogensVectors() {
        // The algorithm: Interaction creates contradiction, shattering the wall to reveal perspective.
        const links = document.querySelectorAll('[data-hash]');
        
        // 1. Initial State: Setup the Wall
        links.forEach(el => {
            el.classList.add('neuro-link');
            const safeHash = this.sanitizeHash(el.getAttribute('data-hash'));
            const url = this.resolveHash(safeHash);
            
            if (url) {
                el.href = url;
                el.setAttribute('data-truth-url', url);
            }
        });

        // 2. The Dynamic Transmutation (Catharsis via Interaction)
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    
                    // Stage 1: Conflict (The viewer's subconscious is stimulated)
                    el.classList.add('conflict');
                    
                    // Stage 2: Transmutation / Catharsis ("The King is Naked")
                    // The illusion of the wall dissolves, revealing the clear Jus Cogens Vector.
                    setTimeout(() => {
                        el.classList.remove('conflict');
                        el.classList.add('catharsis', 'jus-cogens-vector');
                        
                        // Overwrite the visual facade with the pure, protected hash stream
                        const safeHash = this.sanitizeHash(el.getAttribute('data-hash'));
                        if (safeHash) {
                            el.innerHTML = `[ VERIFIED VECTOR ]<br><span style="font-size:0.7em; color:#fff; word-break:break-all;">${safeHash}</span>`;
                        }
                    }, 600); // 600ms delay for cinematic pacing
                    
                    observer.unobserve(el);
                }
            });
        }, { threshold: 0.3 });

        links.forEach(el => observer.observe(el));
    }
};

window.CatharsisEngine = CatharsisEngine;
document.addEventListener('DOMContentLoaded', () => CatharsisEngine.init());
