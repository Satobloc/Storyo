"""Typed graph boundary: reference, world dependency, and presentation stay apart."""
from dataclasses import dataclass
from enum import Enum

class DependencyKind(str, Enum):
    CAUSAL = "causal"
    EPISTEMIC = "epistemic"
    MOTIVATIONAL = "motivational"
    INTERPRETIVE = "interpretive"
    THEMATIC = "thematic"
    INSTITUTIONAL = "institutional"

@dataclass(frozen=True)
class WorldDependency:
    dependency_id: str
    source_facet: str
    target_facet: str
    kind: DependencyKind
    necessity: str = "unspecified"
    confidence: float | None = None

@dataclass(frozen=True)
class PresentationLink:
    link_id: str
    earlier_segment: str
    later_segment: str
    rationale: str = ""

def import_references_as_dependencies(_references):
    """Forbidden implicit conversion. Promotion requires explicit author review."""
    raise TypeError("Grammar references require explicit author-reviewed mapping before entering the world graph")
