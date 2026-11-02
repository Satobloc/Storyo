# STORYO architecture: grammar boundary milestone

## 1. Architectural intent

STORYO is the host system for source-preserving narrative structures and controlled mutation. External plot systems are adapters or resources, not the ontology of a fictional world.

## 2. Data layers

1. **Source vault:** immutable source artifacts, checksums, exact spans, normalization and correction lineage.
2. **Reference grammar:** nodes, references, reference groups, transformations, and source-specific semantics.
3. **World model:** entities, events, facets, states, and typed dependencies belonging to one fictional world.
4. **Mutation/branch layer:** explicit operations, branch isolation, deterministic receipts, and diffs.
5. **Structural evaluation:** constraints, multi-input dependencies, sensitivity, contradiction and continuity diagnostics.
6. **Morphogenesis:** candidate fragments arising from unmet structural requirements. A candidate is not canon until explicitly promoted.
7. **Renderer:** source-preserving composition, alternate presentation orders, and realization mappings.

## 3. Distinct relationship systems

| System | Question answered | Must not be mistaken for |
|---|---|---|
| Reference | What does this external grammar point toward? | Cause in the fictional world |
| World dependency | What depends on what within this world, and how? | Reading order |
| Presentation | In what order is material shown? | World chronology |
| Realization | Which source spans express an abstract element? | The element's complete meaning |

A Plotto `carry-on` relation is retained as a Plotto reference. A world-causal edge requires separate evidence and author review.

The Plotto Studio v5.2 importer adds a source-specific integration path. It maps conflict entries, variants, A/B/C master clauses, references, transformation records, and source spans into the neutral grammar. It retains unresolved target variants as explicit placeholders. Multi-target notations are grouped as `uncertain` until their operator semantics are established. See `docs/integrations/plotto-studio-v5.2.md` for the source audit and exact mapping.

## 4. Grammar model

`Grammar` contains `NodeDefinition`, `Reference`, and `ReferenceGroup` records. Groups preserve their semantics:

- `choose`: select among members under an explicit policy;
- `include`: retain the designated members;
- `sequence`: order members;
- `alternative`: represent mutually alternative routes;
- `uncertain`: retain unresolved grouping or linkage.

These labels are not interchangeable. The adapter must not infer a group mode when the source does not supply one. For Plotto Studio's 478 multi-target notation groups, the importer records `uncertain`; it does not guess `choose`, `include`, or `sequence`.

`Transformation` records retain source-system operations such as Plotto's change/transpose/add/remove family. The host records the operation; a later execution layer must define and test its semantics before applying it to story data.

## 5. Source identity

`SegmentAddress` records artifact ID, full-artifact SHA-256, exact character offsets, segment SHA-256, selector, and optional section path. Resolution fails if the artifact fingerprint or selected text no longer matches. OCR correction or normalization must create a new derived artifact with lineage, not silently alter the source. The Plotto Studio importer hashes each entry-variant text as a source artifact and stores the exact parenthesized reference offsets. The public repository does not contain the source corpus text.

## 6. Determinism

Every generated choice should eventually carry: algorithm/version, seed, ordered candidate IDs, candidate weights, selection policy, chosen IDs, transformation sequence, and input-branch fingerprint. The initial helper implements a small versioned 32-bit LCG solely to prove a stable receipt shape. It is not yet the complete generation engine.

## 7. Author-origin frameworks

The Bio-Tragic Loop and Vignette Expansion documents are preserved verbatim under `docs/user-frameworks/`. They describe different but compatible scales:

- Bio-Tragic Loop: a macro-level progression with an asserted revelation invariant: revelation fulfills and negates an earlier promise.
- Vignette Expansion: a micro/module workflow: core, spine placement, links, internal architecture, meta-layer, outward iteration, assembly/calibration, and optional meta-weaving.

The system should represent these as named, versioned structural templates with explicit template-scoped relations and optional constraints. It must not treat their assertions as automatically proven across all narratives.

## 8. Nellibeth pilot boundary

The v0.8 dataset remains a provisional, source-specific analysis. Its 39 facets and seven dependencies are sparse. Sensitivity values are model outputs over that graph, not complete measurements of narrative importance. The complete v0.8 files are retained in the companion development bundle; the GitHub branch currently carries only the v0.8 provenance note. New grammar references must not modify the canonical v0.6 world snapshot.


## 9. Author-origin template layer

The Bio-Tragic Loop and Vignette Expansion are represented as separate typed structural templates. The former is a macro narrative skeleton with named layers, phases, suggested variable nodes, a nine-beat abstract-flow summary, a separate five-part emotional spine, and author-asserted interdependency statements. The latter is a vignette-development workflow with five module slots in a network model, eight numbered workflow steps, three internal micro-stages, two distinct link types, and an optional meta-weaving step. Workflow order is not world chronology; template relations are not world dependencies. Source fingerprints bind each machine-readable template to its verbatim source document.


## 10. Reference-path traversal

`src/storyo/reference_paths.py` provides bounded traversal over directed grammar references. Callers can constrain the search by the source system's direction labels, cap path length and result count, and receive exact node/reference IDs for each route. The traversal returns source-reference paths only. It does not turn a `carryon` label into a causal claim, and an empty bounded search is not proof that no relationship exists.
