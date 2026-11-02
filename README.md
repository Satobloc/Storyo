# STORYO

Narrative structure, modular composition, and controlled story morphogenesis.

This repository is the shared STORYO / Plotto Studio workspace. The first development milestone establishes a neutral, provenance-aware grammar interface and a narrow Plotto adapter boundary while preserving the prior v0.8 Nellibeth pilot as an independently versioned baseline.

## Non-negotiable semantic boundary

A source-defined grammar reference is not automatically a fictional-world causal dependency. Reference paths, world-dependency paths, presentation paths, and source-realization mappings remain distinct. An adapter may import a reference, but it may not silently promote it into canon or causality.

## Initial structure

- `src/storyo/`: neutral grammar interfaces, graph boundaries, and Plotto adapter.
- `tests/`: executable tests for provenance and semantic separation.
- `docs/`: architecture and design decisions, including the author-origin Bio-Tragic Loop and Vignette Expansion frameworks.
- `archive/v0.8/`: preserved Nellibeth pilot snapshot and validation artifacts.

Python 3.10+, standard library only. Run `python -m unittest discover -s tests -v` from the repository root.

This is an interface milestone, not a complete story-generation engine. It does not import or redistribute the Plotto corpus.