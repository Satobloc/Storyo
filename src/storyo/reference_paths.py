"""Bounded traversal of source-defined grammar references."""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from typing import Iterable
from .grammar import Grammar, Reference


@dataclass(frozen=True)
class ReferencePath:
    node_ids: tuple[str, ...]
    reference_ids: tuple[str, ...]

    @property
    def edge_count(self) -> int:
        return len(self.reference_ids)


def find_reference_paths(grammar: Grammar, start_node: str, target_node: str, *,
                         max_edges: int = 8, directions: Iterable[str] | None = None,
                         max_paths: int = 25) -> tuple[ReferencePath, ...]:
    """Find simple directed paths, ordered by length then reference IDs.

    Direction filters match source labels exactly. An empty bounded search is
    not proof that no relationship exists. Results remain reference paths,
    never world-causal paths.
    """
    grammar.validate()
    if max_edges < 0:
        raise ValueError("max_edges must be non-negative")
    if max_paths < 1:
        raise ValueError("max_paths must be positive")
    known = {node.node_id for node in grammar.nodes}
    if start_node not in known or target_node not in known:
        raise KeyError("Start and target must be nodes in the supplied grammar")
    if start_node == target_node:
        return (ReferencePath((start_node,), ()),)
    allowed = None if directions is None else set(directions)
    adjacency = {node_id: [] for node_id in known}
    for ref in grammar.references:
        if allowed is None or ref.direction in allowed:
            adjacency[ref.source_node].append(ref)
    for refs in adjacency.values():
        refs.sort(key=lambda ref: ref.reference_id)
    queue = deque([(start_node, (start_node,), ())])
    found = []
    shortest = None
    while queue:
        node_id, node_path, ref_path = queue.popleft()
        depth = len(ref_path)
        if depth >= max_edges or (shortest is not None and depth >= shortest):
            continue
        for ref in adjacency[node_id]:
            nxt = ref.target_node
            if nxt in node_path:
                continue
            next_refs, next_nodes = ref_path + (ref.reference_id,), node_path + (nxt,)
            if nxt == target_node:
                shortest = len(next_refs) if shortest is None else shortest
                found.append(ReferencePath(next_nodes, next_refs))
                if len(found) >= max_paths:
                    return tuple(found)
            elif shortest is None or len(next_refs) < shortest:
                queue.append((nxt, next_nodes, next_refs))
    return tuple(found)
