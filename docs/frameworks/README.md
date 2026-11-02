# Author-origin structural templates

`structural-templates.v0.1.json` is a small catalog index for two independently loadable template files: `bio-tragic-loop.v0.1.json` and `vignette-expansion.v0.1.json`. Both formalize source documents preserved verbatim under `docs/user-frameworks/`.

## Bio-Tragic Loop

The model is represented at macro scale. It preserves the five named layers, their ten named phases, the seven suggested variable nodes, and the nine-beat abstract flow summary and five-part emotional spine as separate structures. The source's five interdependency statements are retained as `author_stated_interdependency` relations, with reciprocal components split into explicit directed records where appropriate. The dependency-lattice statement is retained separately as an author assertion. The revelation rule is retained as an author-asserted template invariant.

The phase descriptions and variable-node reconfiguration questions are retained. The JSON does not map every abstract-flow beat onto one or more detailed phases. Such a crosswalk would require an interpretive decision, so the abstract flow and detailed phase structure remain separately addressable.

## Vignette Expansion

The model is represented as a module-development workflow. The eight numbered steps remain workflow steps, not fictional-world chronology. The five named module functions are slots, not a mandatory reading sequence. The source describes the modular spine as a network of interlocking segments, not a linear story. The three internal micro-stages retain their own order. Each numbered step retains its goal, action list, and expected output. Link types remain distinct: direct (narrative) and resonant (thematic/metaphoric). Meta Weaving remains optional.

## Typed loading and validation

`src/storyo/frameworks.py` loads the JSON catalog into typed immutable records. It checks unique identifiers, relation endpoints, template scope, and source-file SHA-256 fingerprints. It rejects a relation typed as `causal`, because a reusable framework relation is not automatically a dependency in a particular fictional world.

Run the checks with:

```bash
python -m unittest discover -s tests -v
```

These are source-faithful structural templates, not claims that either framework is a universal narrative law. The machine-readable representation is an implementation layer and does not replace the original wording.
