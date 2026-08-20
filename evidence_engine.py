import hashlib
import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Set
from imperative_norms import ImperativeNormGuard

@dataclass(frozen=True)
class EvidenceNode:
    node_id: str
    fact_data: str
    parent_hash: Optional[str] = None
    node_type: str = "FACT" 

    def compute_hash(self) -> str:
        content = f"{self.node_id}:{self.fact_data}:{self.parent_hash}:{self.node_type}"
        return hashlib.sha256(content.encode()).hexdigest()

class EvidenceDAG:
    def __init__(self):
        self._nodes: Dict[str, EvidenceNode] = {}
        self._edges: Set[Tuple[str, str]] = set()

    def add_fact(self, node: EvidenceNode, depends_on: Optional[str] = None):
        ImperativeNormGuard.enforce(node, self._nodes)
        self._nodes[node.node_id] = node
        if depends_on: self._edges.add((depends_on, node.node_id))

graph = EvidenceDAG()

# Добавление первичных доказательств (Anchors)
graph.add_fact(EvidenceNode("DOC_NEURO_PROTOCOL_1125", "NEURO-PROTOCOL A@t0r/SC-1125-2025", node_type="DOC_ORIGINAL"))
graph.add_fact(EvidenceNode("DOC_PRESIDENTIAL_MEMO", "Nota Verbale - Presidential Memorandum", node_type="DOC_ORIGINAL"))
graph.add_fact(EvidenceNode("DOC_PASSPORT_MACERET", "Passport and Aviz for MACERET ALEXEI", node_type="DOC_ORIGINAL"))

# Факты из дела
graph.add_fact(EvidenceNode("VICTORIABANK_BLOCKADE_2026", "Блокировка счета", node_type="FACT"), depends_on="DOC_NEURO_PROTOCOL_1125")
graph.add_fact(EvidenceNode("MARKOVA_INHERITANCE_RETENTION", "Удержание депозитов", node_type="FACT"), depends_on="DOC_PRESIDENTIAL_MEMO")
