"""Neutral, provenance-aware interfaces for external narrative grammars."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
from typing import Any, Mapping, Protocol, Sequence

class GroupMode(str, Enum):
    CHOOSE = "choose"
    INCLUDE = "include"
    SEQUENCE = "sequence"
    ALTERNATIVE = "alternative"
    UNCERTAIN = "uncertain"

class TransformKind(str, Enum):
    CHANGE = "change"
    TRANSPOSE = "transpose"
    ADD = "add"
    REMOVE = "remove"
    SUBSTITUTE = "substitute"
    CUSTOM = "custom"

@dataclass(frozen=True)
class SegmentAddress:
    artifact_id: str
    artifact_sha256: str
    start: int
    end: int
    text_sha256: str
    selector: str = "exact-span"
    section_path: tuple[str, ...] = ()

    @classmethod
    def from_text(cls, artifact_id: str, artifact: str, start: int, end: int,
                  selector: str = "exact-span", section_path: Sequence[str] = ()) -> "SegmentAddress":
        if start < 0 or end < start or end > len(artifact):
            raise ValueError("Invalid source span")
        segment = artifact[start:end]
        return cls(artifact_id, sha256(artifact.encode("utf-8")).hexdigest(), start, end,
                   sha256(segment.encode("utf-8")).hexdigest(), selector, tuple(section_path))

    def resolve(self, artifact: str) -> str:
        if sha256(artifact.encode("utf-8")).hexdigest() != self.artifact_sha256:
            raise ValueError("Source artifact fingerprint mismatch")
        segment = artifact[self.start:self.end]
        if sha256(segment.encode("utf-8")).hexdigest() != self.text_sha256:
            raise ValueError("Source segment fingerprint mismatch")
        return segment

@dataclass(frozen=True)
class NodeDefinition:
    node_id: str
    node_type: str
    label: str = ""
    source: SegmentAddress | None = None
    attributes: Mapping[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class Transformation:
    transform_id: str
    kind: TransformKind
    target_role: str | None = None
    replacement_role: str | None = None
    payload: Mapping[str, Any] = field(default_factory=dict)
    reversible: bool = True

@dataclass(frozen=True)
class Reference:
    reference_id: str
    source_node: str
    target_node: str
    direction: str = "unspecified"
    status: str = "unreviewed"
    source: SegmentAddress | None = None
    transformations: tuple[Transformation, ...] = ()
    attributes: Mapping[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class ReferenceGroup:
    group_id: str
    mode: GroupMode
    member_reference_ids: tuple[str, ...]
    required: bool = False
    source: SegmentAddress | None = None
    notes: str = ""

@dataclass(frozen=True)
class Grammar:
    grammar_id: str
    grammar_version: str
    source_name: str
    source_version: str
    nodes: tuple[NodeDefinition, ...] = ()
    references: tuple[Reference, ...] = ()
    groups: tuple[ReferenceGroup, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        node_ids = [n.node_id for n in self.nodes]
        ref_ids = [r.reference_id for r in self.references]
        group_ids = [g.group_id for g in self.groups]
        if len(node_ids) != len(set(node_ids)):
            raise ValueError("Duplicate grammar node id")
        if len(ref_ids) != len(set(ref_ids)):
            raise ValueError("Duplicate reference id")
        if len(group_ids) != len(set(group_ids)):
            raise ValueError("Duplicate reference-group id")
        known_nodes, known_refs = set(node_ids), set(ref_ids)
        for ref in self.references:
            if ref.source_node not in known_nodes or ref.target_node not in known_nodes:
                raise ValueError(f"Dangling grammar reference: {ref.reference_id}")
        for group in self.groups:
            unknown = set(group.member_reference_ids) - known_refs
            if unknown:
                raise ValueError(f"Unknown references in group {group.group_id}: {sorted(unknown)}")

class GrammarAdapter(Protocol):
    adapter_id: str
    adapter_version: str
    def import_records(self, records: Mapping[str, Any]) -> Grammar: ...

@dataclass(frozen=True)
class GenerationReceipt:
    algorithm: str
    seed: int
    ordered_candidate_ids: tuple[str, ...]
    selected_ids: tuple[str, ...]
    policy: str

def deterministic_choose(candidate_ids: Sequence[str], seed: int) -> tuple[str, GenerationReceipt]:
    """Choose one candidate using a versioned 32-bit LCG, stable across runtimes."""
    ordered = tuple(candidate_ids)
    if not ordered:
        raise ValueError("Cannot choose from an empty candidate list")
    state = seed & 0xFFFFFFFF
    state = (1664525 * state + 1013904223) & 0xFFFFFFFF
    chosen = ordered[state % len(ordered)]
    return chosen, GenerationReceipt("storyo-lcg32-v1", seed, ordered, (chosen,), "uniform-index-v1")
