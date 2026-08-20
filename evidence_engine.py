import hashlib
import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Set

@dataclass(frozen=True)
class EvidenceNode:
    node_id: str
    fact_data: str
    parent_hash: Optional[str] = None

    def compute_hash(self) -> str:
        content = f"{self.node_id}:{self.fact_data}:{self.parent_hash}"
        return hashlib.sha256(content.encode()).hexdigest()

class EvidenceDAG:
    def __init__(self):
        self._nodes: Dict[str, EvidenceNode] = {}
        self._edges: Set[Tuple[str, str]] = set()

    def add_fact(self, node: EvidenceNode, depends_on: Optional[str] = None):
        self._nodes[node.node_id] = node
        if depends_on: self._edges.add((depends_on, node.node_id))
