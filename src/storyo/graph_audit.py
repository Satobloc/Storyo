"""Text-free structural diagnostics for an imported reference grammar."""
from __future__ import annotations
from collections import Counter, deque
from typing import Any
from .grammar import Grammar


def summarize_reference_graph(grammar: Grammar, top_n: int = 15) -> dict[str, Any]:
    """Return reproducible graph counts without exporting source corpus text."""
    grammar.validate()
    if top_n < 0:
        raise ValueError("top_n must be non-negative")
    nodes = {node.node_id: node for node in grammar.nodes}
    outgoing: Counter[str] = Counter()
    incoming: Counter[str] = Counter()
    undirected = {node_id: set() for node_id in nodes}
    pair_types: Counter[str] = Counter()
    self_loops = 0
    for ref in grammar.references:
        outgoing[ref.source_node] += 1
        incoming[ref.target_node] += 1
        undirected[ref.source_node].add(ref.target_node)
        undirected[ref.target_node].add(ref.source_node)
        pair_types[f"{nodes[ref.source_node].node_type}->{nodes[ref.target_node].node_type}"] += 1
        self_loops += ref.source_node == ref.target_node
    unseen = set(nodes)
    component_sizes = []
    while unseen:
        root = unseen.pop()
        queue = deque([root])
        size = 0
        while queue:
            current = queue.popleft()
            size += 1
            for neighbor in undirected[current]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    queue.append(neighbor)
        component_sizes.append(size)
    def top_degree(counter):
        ranked = sorted(counter.items(), key=lambda item: (-item[1], item[0]))[:top_n]
        return [{"node_id": node_id, "degree": degree, "node_type": nodes[node_id].node_type}
                for node_id, degree in ranked]
    return {
        "grammar": {"id": grammar.grammar_id, "version": grammar.grammar_version,
                    "source": grammar.source_name, "source_version": grammar.source_version},
        "interpretation_guard": "Reference-network topology only; no causal or world-dependency meaning is inferred.",
        "counts": {
            "nodes": len(nodes),
            "node_types": dict(sorted(Counter(n.node_type for n in grammar.nodes).items())),
            "references": len(grammar.references),
            "reference_directions": dict(sorted(Counter(r.direction for r in grammar.references).items())),
            "reference_statuses": dict(sorted(Counter(r.status for r in grammar.references).items())),
            "transformations": dict(sorted(Counter(t.kind.value for r in grammar.references for t in r.transformations).items())),
            "groups": len(grammar.groups),
            "group_modes": dict(sorted(Counter(g.mode.value for g in grammar.groups).items())),
            "reference_endpoint_node_types": dict(sorted(pair_types.items())),
            "self_loops": self_loops,
        },
        "connectivity": {
            "weak_component_count": len(component_sizes),
            "largest_weak_component_nodes": max(component_sizes, default=0),
            "isolated_node_count": sum(1 for n in nodes if not outgoing[n] and not incoming[n]),
            "largest_component_sizes": sorted(component_sizes, reverse=True)[:top_n],
        },
        "degree": {
            "nodes_with_outgoing_references": sum(1 for n in nodes if outgoing[n]),
            "nodes_with_incoming_references": sum(1 for n in nodes if incoming[n]),
            "highest_out_degree": top_degree(outgoing),
            "highest_in_degree": top_degree(incoming),
        },
    }
