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
        # 1. Применяем императивную норму ПЕРЕД добавлением
        ImperativeNormGuard.enforce(node, self._nodes)
        
        # 2. Если норма пройдена, добавляем
        self._nodes[node.node_id] = node
        if depends_on: self._edges.add((depends_on, node.node_id))

# Инициализация графа фактами дела
graph = EvidenceDAG()

# Узел: Финансовая блокада
graph.add_fact(EvidenceNode(
    node_id="VICTORIABANK_BLOCKADE_2026",
    fact_data="Искусственная генерация задолженности -11.98 MDL при балансе 0.00 MDL",
    node_type="FACT"
))

# Узел: Наследство
graph.add_fact(EvidenceNode(
    node_id="MARKOVA_INHERITANCE_RETENTION",
    fact_data="Удержание депозитов Марковой Г.И.",
    node_type="FACT"
))
