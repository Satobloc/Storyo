"""Import Plotto Studio v5.x DATA records without redistributing its corpus.

The importer reads a user-supplied Plotto Studio HTML file, extracts its JSON
DATA object, and builds an in-memory STORYO Grammar. It does not export source
plot text, and does not infer causal dependencies or ambiguous group semantics.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from .grammar import Grammar, GroupMode, NodeDefinition, Reference, ReferenceGroup, SegmentAddress
from .plotto_adapter import PlottoAdapter


class PlottoStudioImportError(ValueError):
    pass


def _extract_data(html: str) -> dict[str, Any]:
    match = re.search(r"\bconst\s+DATA\s*=\s*", html)
    if not match:
        raise PlottoStudioImportError("Could not find `const DATA =` in the supplied HTML")
    start = match.end()
    in_string = False
    escaped = False
    depth = 0
    for index in range(start, len(html)):
        char = html[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        else:
            if char == '"':
                in_string = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    try:
                        data = json.loads(html[start:index + 1])
                    except json.JSONDecodeError as exc:
                        raise PlottoStudioImportError(f"DATA object is not valid JSON: {exc}") from exc
                    if not isinstance(data, dict) or not isinstance(data.get("entries"), list):
                        raise PlottoStudioImportError("DATA object lacks an entries array")
                    return data
    raise PlottoStudioImportError("DATA object appears to be truncated")


def import_plottostudio_html(path: str | Path) -> Grammar:
    """Read Plotto Studio HTML and return a provenance-preserving Grammar.

    Node IDs are stable within this source version: plotto:entry:<id>,
    plotto:entry:<id>:variant:<key>, and explicit unresolved-variant IDs.
    A link without a target variant points to the conflict-level node. A link
    naming a missing target variant points to a placeholder that records the
    unresolved source pointer, rather than silently falling back to the entry.
    """
    path = Path(path)
    raw = path.read_bytes()
    html = raw.decode("utf-8")
    data = _extract_data(html)
    dataset_sha = hashlib.sha256(raw).hexdigest()
    entries = data["entries"]
    by_id = {int(entry["id"]): entry for entry in entries}
    source_artifacts: dict[str, str] = {}
    nodes: list[dict[str, Any]] = []
    references: list[dict[str, Any]] = []
    groups: list[dict[str, Any]] = []
    unresolved_targets: dict[tuple[int, str], str] = {}

    for entry in entries:
        entry_id = int(entry["id"])
        nodes.append({
            "id": f"plotto:entry:{entry_id}", "type": "conflict",
            "attributes": {"entry_id": entry_id, "category": entry.get("category", "")}
        })
        for variant in entry.get("variants", []):
            key = str(variant.get("key", ""))
            artifact_id = f"plotto-studio-v5.2:entry:{entry_id}:variant:{key or 'default'}"
            source_text = str(variant.get("text", ""))
            source_artifacts[artifact_id] = source_text
            nodes.append({
                "id": f"plotto:entry:{entry_id}:variant:{key}", "type": "variant",
                "source": {"artifact_id": artifact_id, "start": 0, "end": len(source_text),
                           "selector": "whole-variant"},
                "attributes": {"entry_id": entry_id, "variant_key": key,
                               "category": entry.get("category", "")}
            })

    # Plotto Studio's A/B/C masterwords are separate source nodes,
    # not automatically connected to conflict entries by inferred edges.
    for clause_family, clauses in data.get("master", {}).items():
        for clause in clauses:
            clause_id = int(clause["id"])
            artifact_id = f"plotto-studio-v5.2:master:{clause_family}:{clause_id}"
            clause_text = str(clause.get("text", ""))
            source_artifacts[artifact_id] = clause_text
            nodes.append({
                "id": f"plotto:master:{clause_family}:{clause_id}",
                "type": "master-clause",
                "source": {"artifact_id": artifact_id, "start": 0, "end": len(clause_text),
                           "selector": "whole-master-clause"},
                "attributes": {"master_family": str(clause_family), "clause_id": clause_id}
            })

    # References are processed only after all real variant nodes are known.
    node_ids = {node["id"] for node in nodes}
    grouped: dict[tuple[str, int, str, str], list[str]] = defaultdict(list)
    for entry in entries:
        entry_id = int(entry["id"])
        for variant in entry.get("variants", []):
            key = str(variant.get("key", ""))
            source_node = f"plotto:entry:{entry_id}:variant:{key}"
            artifact_id = f"plotto-studio-v5.2:entry:{entry_id}:variant:{key or 'default'}"
            source_text = str(variant.get("text", ""))
            for link_index, link in enumerate(variant.get("links", [])):
                target_entry = int(link["target"])
                target_variant = str(link.get("variant", ""))
                if target_entry not in by_id:
                    target_node = f"plotto:unresolved-entry:{target_entry}"
                    if target_node not in node_ids:
                        nodes.append({"id": target_node, "type": "unresolved-target",
                                      "attributes": {"requested_entry_id": target_entry}})
                        node_ids.add(target_node)
                elif target_variant:
                    target_node = f"plotto:entry:{target_entry}:variant:{target_variant}"
                    if target_node not in node_ids:
                        target_node = f"plotto:unresolved-variant:{target_entry}:{target_variant}"
                        if target_node not in node_ids:
                            nodes.append({"id": target_node, "type": "unresolved-target",
                                          "attributes": {"requested_entry_id": target_entry,
                                                         "requested_variant": target_variant}})
                            node_ids.add(target_node)
                else:
                    target_node = f"plotto:entry:{target_entry}"

                start = int(link.get("start", 0))
                close = source_text.find(")", start)
                if start < 0 or start >= len(source_text) or source_text[start] != "(" or close < 0:
                    raise PlottoStudioImportError(
                        f"Cannot resolve parenthesized source span for entry {entry_id} "
                        f"variant {key} link {link_index} at offset {start}"
                    )
                ref_id = f"plotto:ref:{entry_id}:{key}:{link_index}"
                ref = {
                    "id": ref_id, "from": source_node, "to": target_node,
                    "direction": str(link.get("direction", "unspecified")),
                    "status": str(link.get("status", "unreviewed")),
                    "source": {"artifact_id": artifact_id, "start": start, "end": close + 1,
                           "selector": "parenthesized-reference"},
                    "attributes": {"entry_id": entry_id, "source_variant": key,
                                 "target_entry_id": target_entry,
                                 "target_variant": target_variant,
                                "notation": str(link.get("notation", "")),
                                 "source_link_index": link_index},
                    "transformations": []
                }
                for op_index, operation in enumerate(link.get("operations", [])):
                    ref["transformations"].append({
                        "id": f"{ref_id}:op:{op_index}",
                        "operation": str(operation.get("op", "custom")),
                        **{k: v for k, v in operation.items() if k != "op"}
                    })
                references.append(ref)
                group_key = (source_node, start, str(link.get("direction", "unspecified")),
                             str(link.get("notation", "")))
                grouped[group_key].append(ref_id)

    # Multiple targets emitted from one source notation are preserved as a
    # group, but their logical operator is deliberately left uncertain.
    for index, (key, member_ids) in enumerate(sorted(grouped.items(), key=lambda item: item[0])):
        if len(member_ids) > 1:
            groups.append({"id": f"plotto:group:{index}", "mode": "uncertain",
                           "members": member_ids, "required": False,
                           "notes": "Multiple targets share one source notation; operator semantics not inferred."})

    normalized = {
        "source_version": "Plotto Studio v5.2",
        "source_artifacts": source_artifacts,
        "nodes": nodes,
        "references": references,
        "groups": groups,
        "metadata": {"source_html_sha256": dataset_sha}
    }
    grammar = PlottoAdapter().import_records(normalized)
    return Grammar(
        grammar_id="plotto-studio.v5.2", grammar_version="0.1.0",
        source_name="Plotto Studio", source_version="v5.2",
        nodes=grammar.nodes, references=grammar.references, groups=grammar.groups,
        metadata={**grammar.metadata,
                  "source_html_sha256": dataset_sha,
                  "entry_count": len(entries),
                  "variant_count": sum(len(e.get("variants", [])) for e in entries),
                  "master_clause_counts": {k: len(v) for k, v in data.get("master", {}).items()},
                  "corpus_text_exported": False,
                  "source_data_embedded": False}
    )
