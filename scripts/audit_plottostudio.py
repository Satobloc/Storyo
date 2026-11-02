"""Print a text-free structural audit of a supplied Plotto Studio HTML file."""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from storyo.plottostudio_importer import import_plottostudio_html


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("html", help="Path to a user-supplied Plotto Studio v5.2 HTML file")
    args = parser.parse_args()
    grammar = import_plottostudio_html(args.html)
    payload = {
        "source": grammar.source_name,
        "source_version": grammar.source_version,
        "source_html_sha256": grammar.metadata["source_html_sha256"],
        "nodes": len(grammar.nodes),
        "node_types": dict(Counter(n.node_type for n in grammar.nodes)),
        "references": len(grammar.references),
        "directions": dict(Counter(r.direction for r in grammar.references)),
        "statuses": dict(Counter(r.status for r in grammar.references)),
        "transformations": dict(Counter(t.kind.value for r in grammar.references for t in r.transformations)),
        "groups": len(grammar.groups),
        "group_modes": dict(Counter(g.mode.value for g in grammar.groups)),
        "master_clause_counts": grammar.metadata["master_clause_counts"],
        "corpus_text_exported": grammar.metadata["corpus_text_exported"],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
