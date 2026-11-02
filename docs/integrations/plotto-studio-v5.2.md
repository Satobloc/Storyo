# Plotto Studio v5.2 integration

## Status

The first executable importer is implemented in `src/storyo/plottostudio_importer.py`. It reads a user-supplied Plotto Studio HTML file, extracts the embedded `const DATA` JSON object, and builds an in-memory STORYO `Grammar` through the neutral Plotto adapter.

The importer does **not** commit, export, or redistribute the embedded plot text. The repository contains the importer, tests, documentation, and a text-free audit summary only. The source HTML remains an external input supplied by the user.

## Source identity

The audited source was `plotto-studio-life-draw-v5-2.html` supplied in the working conversation. Its SHA-256 is:

`b6b4d38ccc75d1f612eb25a807e8f485ea6fd2c1d6553aa191cd4c8df1d85634`

The source identifies itself as Plotto Studio v5.2. The importer records this file hash in grammar metadata. A changed HTML file produces a different source fingerprint.

## Mapping

| Plotto Studio source object | STORYO representation | Notes |
|---|---|---|
| Entry ID | `conflict` node | Category retained as source metadata; no plot text copied into node labels |
| Entry variant | `variant` node | Source text represented by a content-addressed full-variant span |
| A/B/C master clause | `master-clause` node | Separate source nodes; no inferred links to conflict entries |
| Cross-reference | `Reference` | Direction, status, notation, source variant and target identifiers retained |
| Parenthesized notation | `SegmentAddress` | Exact offsets in the relevant variant text, including parentheses |
| `change` / `transpose` operation | `Transformation` | Operation kind and source parameters retained; not automatically executed |
| Multiple targets sharing one source notation | `ReferenceGroup(UNCERTAIN)` | Group existence is preserved; `choose`/`include`/`sequence` semantics are not guessed |
| Missing requested target variant | `unresolved-target` node | Explicit placeholder preserves the unresolved pointer; it is not silently redirected to the entry root |

A reference without a requested target variant points to the conflict-level node. A reference naming a particular variant points to that variant when present. When the requested variant does not exist, the importer creates a placeholder keyed by the requested entry and variant. This keeps the unresolved pointer visible and validates the graph without pretending the target variant was found.

## Audit of the supplied source

| Measure | Count |
|---|---:|
| Conflict entries | 1,462 |
| Variants | 1,853 |
| A master clauses | 15 |
| B master clauses | 62 |
| C master clauses | 15 |
| Total master clauses | 92 |
| Cross-references | 11,068 |
| Lead-up references | 5,311 |
| Carry-on references | 4,609 |
| Uncertain-direction references | 1,148 |
| Interpreted references | 10,302 |
| Partial references | 742 |
| Unresolved-target-variant references | 23 |
| Corrected-with-secondary-source references | 1 |
| `change` operations | 1,712 |
| `transpose` operations | 246 |
| Multi-target source-notation groups | 478 |
| Distinct unresolved target-variant pointers | 20 |

The in-memory import contains 3,427 nodes: 1,462 conflict nodes, 1,853 variant nodes, 92 master-clause nodes, and 20 unresolved-target placeholders. It contains 11,068 references and 478 uncertain groups.

## Important semantic limits

1. `leadup`, `carryon`, and `uncertain` are preserved as Plotto source directions. They are not renamed to causal, temporal, or epistemic dependency types.
2. The 478 multi-target groups share a source notation position. Their operator meaning is not sufficiently established by this dataset alone, so they remain `uncertain`.
3. The `change` and `transpose` operations are preserved, not applied. Their execution semantics need a separate, tested transformation engine.
4. An unresolved target variant remains unresolved. A placeholder is an integrity device, not a repaired source record.
5. The 92 master clauses are separate source nodes. The importer does not assume a particular A/B/C combination is a causal story graph.
6. The source's text and master-clause wording remain in the external HTML input. The grammar stores content hashes and offsets, not a copy of the corpus.
7. No imported reference is promoted to a STORYO world dependency or canonical story fact.

## Reproduction

With Python 3.10+ and the source HTML available locally:

```bash
PYTHONPATH=src python - <<'PY'
from storyo.plottostudio_importer import import_plottostudio_html

grammar = import_plottostudio_html("/path/to/plotto-studio-life-draw-v5-2.html")
print(len(grammar.nodes), len(grammar.references), len(grammar.groups))
print(grammar.metadata)
PY
```

Run the unit tests:

```bash
python -m unittest discover -s tests -v
```

The unit test uses a tiny inline structural fixture. The full source audit above was run against the supplied HTML file; the HTML itself is intentionally not bundled in this repository.


## Reference-network topology audit

The text-free audit reports 3,427 nodes and 11,068 directed references. The graph has 332 weakly connected components; its largest component contains 3,096 nodes. There are 331 isolated nodes. Endpoint types are mixed: 7,797 references target conflict-level nodes, 3,248 target variant nodes, and 23 target explicit unresolved-target placeholders. One self-reference is present.

These are topological properties of Plotto Studio's reference network, not measures of causal structure, narrative centrality, quality, or importance. High in-degree means only that a source-defined reference points to a node frequently.

The importer validates that every source pointer begins at an opening parenthesis and resolves to a closing parenthesis. The supplied v5.2 dataset passes this check for all 11,068 references. See `plotto-studio-v5.2-graph-audit.json` for machine-readable counts.
