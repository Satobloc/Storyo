"""Typed loading and validation for author-origin structural templates.

Template relations describe a reusable author-defined framework. They are not
world dependencies and must not be promoted into a fictional world's graph.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Any, Mapping


@dataclass(frozen=True)
class TemplateElement:
    element_id: str
    kind: str
    label: str
    attributes: Mapping[str, Any]


@dataclass(frozen=True)
class TemplateRelation:
    relation_id: str
    source_id: str
    target_id: str
    relation_type: str
    source_statement: str
    claim_status: str
    scope: str


@dataclass(frozen=True)
class StructuralTemplate:
    template_id: str
    title: str
    template_kind: str
    scale: str
    source_file: str
    source_sha256: str
    elements: tuple[TemplateElement, ...]
    relations: tuple[TemplateRelation, ...]
    source_assertions: tuple[Mapping[str, Any], ...]
    source_structures: Mapping[str, Any]
    interpretation_guard: str

    def validate(self, source_root: str | Path | None = None) -> None:
        element_ids = [x.element_id for x in self.elements]
        relation_ids = [x.relation_id for x in self.relations]
        if len(element_ids) != len(set(element_ids)):
            raise ValueError(f"Duplicate element id in {self.template_id}")
        if len(relation_ids) != len(set(relation_ids)):
            raise ValueError(f"Duplicate relation id in {self.template_id}")
        known = set(element_ids)
        for relation in self.relations:
            if relation.source_id not in known or relation.target_id not in known:
                raise ValueError(f"Dangling template relation: {relation.relation_id}")
            if relation.scope != "template":
                raise ValueError("Template relations must remain scoped to the template")
            if relation.relation_type == "causal":
                raise ValueError("Template relations cannot be promoted as world-causal edges")
        if not re.fullmatch(r"[0-9a-f]{64}", self.source_sha256):
            raise ValueError(f"Invalid source SHA-256 for {self.template_id}")
        if source_root is not None:
            source_path = Path(source_root) / self.source_file
            actual = sha256(source_path.read_bytes()).hexdigest()
            if actual != self.source_sha256:
                raise ValueError(f"Source fingerprint mismatch for {self.template_id}")


def load_template_catalog(path: str | Path,
                          source_root: str | Path | None = None) -> tuple[StructuralTemplate, ...]:
    """Load a template catalog and optionally verify source-file fingerprints."""
    catalog_path = Path(path)
    raw = json.loads(catalog_path.read_text(encoding="utf-8"))
    items = list(raw.get("templates", []))
    for relative_path in raw.get("template_files", []):
        template_path = catalog_path.parent / relative_path
        payload = json.loads(template_path.read_text(encoding="utf-8"))
        if "template" in payload:
            items.append(payload["template"])
        else:
            items.extend(payload.get("templates", []))
    templates = []
    for item in items:
        elements = tuple(TemplateElement(
            element_id=str(x["element_id"]), kind=str(x["kind"]),
            label=str(x["label"]),
            attributes={k: v for k, v in x.items()
                        if k not in {"element_id", "kind", "label"}}
        ) for x in item.get("elements", []))
        relations = tuple(TemplateRelation(
            relation_id=str(x["relation_id"]), source_id=str(x["source_id"]),
            target_id=str(x["target_id"]), relation_type=str(x["relation_type"]),
            source_statement=str(x.get("source_statement", "")),
            claim_status=str(x.get("claim_status", "unspecified")),
            scope=str(x.get("scope", "template"))
        ) for x in item.get("relations", []))
        template = StructuralTemplate(
            template_id=str(item["template_id"]), title=str(item["title"]),
            template_kind=str(item["template_kind"]), scale=str(item["scale"]),
            source_file=str(item["source_file"]), source_sha256=str(item["source_sha256"]),
            elements=elements, relations=relations,
            source_assertions=tuple(item.get("source_assertions", [])),
            source_structures=dict(item.get("source_structures", {})),
            interpretation_guard=str(item.get("interpretation_guard", ""))
        )
        template.validate(source_root)
        templates.append(template)
    ids = [x.template_id for x in templates]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate structural template id")
    return tuple(templates)
