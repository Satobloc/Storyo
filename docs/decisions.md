# Design decisions

## D-001: External grammars are pluggable resources

**Decision:** STORYO defines neutral interfaces; Plotto is an adapter, not the host ontology.

**Reason:** Plotto's source references and transformations are useful but source-specific. Their meanings cannot safely be generalized into all narrative relationships.

## D-002: Keep graph semantics separate

**Decision:** Reference paths, world dependencies, presentation paths, and realization mappings are distinct types.

**Reason:** A source suggestion is not causal proof; presentation order is not chronology; a manuscript span is not the abstract narrative element itself.

## D-003: Preserve author-origin frameworks

**Decision:** Store the Bio-Tragic Loop and Vignette Expansion texts verbatim and model them as templates, not universal laws.

**Reason:** Preserve exact provenance and allow testing or adaptation without silently universalizing their claims.

## D-004: Preserve v0.8 as a snapshot

**Decision:** Preserve v0.8 pilot data and engine files as an independently versioned snapshot in the companion development bundle; the GitHub branch currently carries only the provenance note. Do not rewrite the snapshot as part of the grammar milestone.

**Reason:** Maintain reproducibility and a clear version boundary. The v0.8 Nellibeth graph remains provisional and sparse.

## D-005: Source spans are content-addressed

**Decision:** A segment address binds to both the source artifact hash and the selected span hash.

**Reason:** Detect accidental source drift and support exact source-preserving assembly.

## D-006: Generation choices produce receipts

**Decision:** Deterministic selection returns algorithm/version, seed, ordered candidate IDs, policy, and chosen IDs.

**Reason:** Reproducibility must be inspectable, not merely described as seeded.

## D-007: Do not redistribute imported source corpora by default

**Decision:** The Plotto Studio importer reads the user-supplied HTML at runtime. The public repository contains importer code and a text-free structural audit, not the embedded plot corpus.

**Reason:** The source file's redistribution license has not been established. Source text remains external; STORYO retains hashes and source offsets for provenance.

## D-008: Preserve unresolved group operators as uncertain

**Decision:** Multiple references emitted from the same source notation position are grouped as `uncertain` unless source evidence establishes a more specific operator.

**Reason:** A set of targets does not by itself establish `choose`, `include`, or `sequence` semantics. STORYO must not manufacture logical structure from a parsing convenience.

## D-009: Preserve unresolved target variants explicitly

**Decision:** A reference to a missing target variant points to an explicit unresolved-target placeholder carrying the requested entry and variant identifiers.

**Reason:** Redirecting the pointer to an entry-level node would conceal the source's unresolved target status.


## D-010: Author-origin frameworks are typed templates, not world ontology

**Decision:** Formalize the Bio-Tragic Loop and Vignette Expansion as separate source-linked templates. Keep their internal structures and relation types distinct, and scope all template relations to the template.

**Reason:** The Bio-Tragic Loop is a macro narrative skeleton; Vignette Expansion is a modular development workflow. Their claims and ordering rules must not be silently converted into universal narrative laws, story chronology, or causal dependencies in an individual fictional world.
