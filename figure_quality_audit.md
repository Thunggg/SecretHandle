# Figure quality audit

Audit date: 2026-10-03. Source inspected: the final compiled `main.pdf`, rendered at 2× resolution into `figure_previews/`.

| Figure | Page | Source | Visual audit | Status |
|---|---:|---|---|---|
| SecretHandle architecture | 11 | `figures/tikz_architecture.tex` | Trust groups, authoritative sources, mint, agent, resolver, target, redactor, confirmation, and keystore are distinct. Protected, ordinary, and adversarial paths use both color and line-style encoding. Arrow labels do not cover node text; all nodes are inside the page box. | Pass |
| Threat and control boundary | 13 | `figures/tikz_threat_privacy_robustness.tex` | Accepted and rejected target paths are separated; the raw-secret path and redacted return path are visible. The repaired layout removes the earlier source/gate overlap. | Pass |
| Method pipeline | 17 | `figures/tikz_method_pipeline.tex` | Six numbered stages follow a two-row snake layout. The malicious-instruction and rejection branches are visually separate, with no label collision. | Pass |
| Formal dependency graph | 21 | `figures/tikz_theory_diagram.tex` | Assumptions, lemmas, theorems, propositions, design consequence, and empirical oracles occupy distinct tiers. A deliberate vertical gap prevents the caption from touching the graphic. | Pass |
| Planned experimental setup | 29 | `figures/tikz_experimental_setup.tex` | Sources, factors, attacks, conditions, protected oracles, metrics, and reproducibility controls are separated. Control arrows terminate at box borders and do not cross text. | Pass |
| Conceptual PGFPlots trends | 33 | `figures/pgfplots_placeholder_results.tex` | Axes, legends, and tick labels are legible. Short component labels avoid the previous x-axis collision. Caption prominently states that coordinates are illustrative placeholders, not results. | Pass |

Checks applied to every figure:

- Native TikZ/PGFPlots vector output; no raster screenshots are used as manuscript figures.
- No external icon font is required; semantic roles are encoded with standard geometric shapes, hatching, line styles, and labels.
- Captions are descriptive and state the interpretation or limitation needed to read the figure safely.
- Graphics remain within the Elsevier preprint text block, with no cropping, off-page content, or arrowheads hidden under text.
- Color is redundant with dashing, hatching, shape, or position where it carries security meaning.

Result: **all six final figures passed rendered-page inspection.**
