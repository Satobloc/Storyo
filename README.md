# STORYO v0.9 development workspace

This workspace contains the v0.9 grammar-boundary prototype, the author-supplied Bio-Tragic Loop and Vignette Expansion source documents, and a complete local copy of the prior v0.8 Nellibeth pilot package under `archive/v0.8/`. The GitHub branch currently contains the v0.8 provenance note only; the complete package is retained in this companion bundle pending a separate repository import decision.

## Semantic boundary

A source-defined grammar reference is not automatically a fictional-world causal dependency. Reference paths, world-dependency paths, presentation paths, and source-realization mappings remain distinct. An adapter may import a reference, but it may not silently promote it into canon or causality.

## Structure

- `src/storyo/`: neutral grammar interfaces, graph boundaries, Plotto adapter/importer, reference-path traversal, and graph diagnostics.
- `tests/`: executable tests for provenance, importer mapping, and semantic separation.
- `docs/`: architecture, design decisions, author-origin frameworks, typed framework templates, and integration audits.
- `archive/v0.8/`: complete v0.8 pilot copy in this local bundle; the GitHub branch currently contains only its provenance note.

## Plotto Studio integration

The importer reads the embedded `const DATA` object from a user-supplied Plotto Studio v5.2 HTML file. It imports entry/variant/master-clause nodes, reference directions and statuses, transformation records, exact source spans, and unresolved target pointers. It validates every reference offset against its parenthesized source span, and deliberately does not copy or redistribute the corpus text. See [`docs/integrations/plotto-studio-v5.2.md`](docs/integrations/plotto-studio-v5.2.md), the text-free graph audit, and `scripts/audit_plottostudio_graph.py`.

## Author-origin framework templates

The Bio-Tragic Loop and Vignette Expansion source documents are preserved verbatim and represented as independently loadable typed templates, referenced by `structural-templates.v0.1.json`. The representation keeps the macro narrative skeleton separate from the vignette-development workflow, preserves author-asserted relations as template-scoped statements, and does not promote them into world causality. See [`docs/frameworks/README.md`](docs/frameworks/README.md).

## Run tests

Python 3.10+, standard library only:

```bash
python -m unittest discover -s tests -v
```

## Scope

This is an interface and source-integration milestone, not a complete story-generation engine. Plotto is an optional structural resource, not STORYO's governing ontology. The v0.8 Nellibeth graph remains provisional and sparse; its sensitivity outputs are conditional on the currently represented dependencies.
