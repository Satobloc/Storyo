"""Minimal adapter boundary for Plotto-like records, not a Plotto corpus import.

The adapter consumes normalized records supplied by a separate importer. It
preserves Plotto's source-specific terms as metadata and does not infer causality.
"""
from __future__ import annotations
from typing import Any, Mapping
from .grammar import (Grammar, NodeDefinition, Reference, ReferenceGroup,
                      GroupMode, SegmentAddress, Transformation, TransformKind)


class PlottoAdapter:
    adapter_id = "storyo.adapter.plotto"
    adapter_version = "0.1.0"

    _transform_map = {
        "change": TransformKind.CHANGE,
        "transpose": TransformKind.TRANSPOSE,
        "add": TransformKind.ADD,
        "remove": TransformKind.REMOVE,
        "substitute": TransformKind.SUBSTITUTE,
    }

    def import_records(self, records: Mapping[str, Any]) -> Grammar:
        source_artifacts = records.get("source_artifacts", {})

        def source_address(record: Mapping[str, Any]):
            spec = record.get("source")
            if not spec:
                return None
            artifact_id = str(spec["artifact_id"])
            if artifact_id not in source_artifacts:
                raise ValueError(f"Missing source artifact: {artifact_id}")
            return SegmentAddress.from_text(
                artifact_id, str(source_artifacts[artifact_id]),
                int(spec["start"]), int(spec["end"]),
                selector=str(spec.get("selector", "exact-span")),
                section_path=tuple(spec.get("section_path", ()))
            )

        nodes = tuple(NodeDefinition(
            node_id=str(x["id"]), node_type=str(x.get("type", "conflict")),
            label=str(x.get("label", "")), source=source_address(x),
            attributes={"plotto": dict(x.get("attributes", {}))}
        ) for x in records.get("nodes", []))
        refs = []
        for x in records.get("references", []):
            transforms = tuple(Transformation(
                transform_id=str(t.get("id", f"{x['id']}:{i}")),
                kind=self._transform_map.get(str(t.get("operation", "")).lower(), TransformKind.CUSTOM),
                target_role=t.get("target_role"), replacement_role=t.get("replacement_role"),
                payload={k: v for k, v in t.items() if k not in {"id", "operation", "target_role", "replacement_role"}}
            ) for i, t in enumerate(x.get("transformations", [])))
            refs.append(Reference(
                reference_id=str(x["id"]), source_node=str(x["from"]), target_node=str(x["to"]),
                direction=str(x.get("direction", "unspecified")),
                status=str(x.get("status", "unreviewed")), source=source_address(x), transformations=transforms,
                attributes={"source_system": "Plotto", **dict(x.get("attributes", {}))}
            ))
        groups = tuple(ReferenceGroup(
            group_id=str(g["id"]), mode=GroupMode(g["mode"]),
            member_reference_ids=tuple(map(str, g.get("members", []))),
            required=bool(g.get("required", False)), notes=str(g.get("notes", ""))
        ) for g in records.get("groups", []))
        grammar = Grammar(
            grammar_id="plotto.import", grammar_version="0.1.0",
            source_name="Plotto", source_version=str(records.get("source_version", "unspecified")),
            nodes=nodes, references=tuple(refs), groups=groups,
            metadata={"adapter": self.adapter_id, "adapter_version": self.adapter_version,
                      "import_status": "normalized-records-only", "causal_promotion": "prohibited-by-default"}
        )
        grammar.validate()
        return grammar
