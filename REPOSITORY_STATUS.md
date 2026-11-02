# Shared repository status

GitHub repository: https://github.com/Satobloc/Storyo
Development branch: `integration/v0.9-grammar-boundary`
Draft pull request: https://github.com/Satobloc/Storyo/pull/1

The development branch contains the neutral grammar model, Plotto adapter, graph-boundary guard, Plotto Studio v5.2 HTML importer, source-faithful Bio-Tragic Loop and Vignette Expansion templates, graph diagnostics, and bounded reference-path traversal. The importer maps 1,462 conflict entries, 1,853 variants, 92 A/B/C master clauses, and 11,068 references while keeping corpus text external.

All 11,068 imported source offsets were checked against parenthesized source spans. The text-free graph audit records 3,427 nodes, 11,068 references, 332 weakly connected components, and a largest component of 3,096 nodes. The complete local test suite passes 15 tests. A GitHub Actions matrix is configured for Python 3.10, 3.11, 3.12, and 3.13; all four hosted matrix jobs pass on Python 3.10, 3.11, 3.12, and 3.13.

The complete v0.8 Nellibeth pilot archive is retained in the companion development bundle; the GitHub branch currently carries its provenance note rather than every archive file. The default branch `main` remains unchanged pending review. No merge has been performed.
