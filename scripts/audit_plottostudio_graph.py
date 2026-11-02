"""Print text-free structural diagnostics for a supplied Plotto Studio HTML file."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from storyo.graph_audit import summarize_reference_graph
from storyo.plottostudio_importer import import_plottostudio_html


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("html", help="Path to a user-supplied Plotto Studio v5.2 HTML file")
    parser.add_argument("--top-n", type=int, default=15)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = summarize_reference_graph(import_plottostudio_html(args.html), top_n=args.top_n)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
