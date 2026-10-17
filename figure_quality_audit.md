# Figure quality audit

Audit date: 2026-10-03. Refresh: 2026-10-17. Source: the compiled `main.pdf` and `mobisys/main.pdf`, rendered at 150 dpi into `figure_previews/`.

## Full paper (elsarticle preprint)

Page numbers refreshed 2026-10-17 (sections grew, so the last two figures shifted by one page). Figure **sources are unchanged** since 2026-10-03, so the content audit carries forward.

| Figure | Page | Source | Visual audit | Status |
|---|---:|---|---|---|
| SecretHandle architecture | 11 | `figures/tikz_architecture.tex` | Trust groups, authoritative sources, mint, agent, resolver, target, redactor, confirmation, and keystore are distinct. Protected, ordinary, and adversarial paths use both color and line-style encoding. Arrow labels do not cover node text; all nodes are inside the page box. | Pass (carried) |
| Threat and control boundary | 13 | `figures/tikz_threat_privacy_robustness.tex` | Accepted and rejected target paths are separated; the raw-secret path and redacted return path are visible. The repaired layout removes the earlier source/gate overlap. | Pass (carried) |
| Method pipeline | 17 | `figures/tikz_method_pipeline.tex` | Six numbered stages follow a two-row snake layout. The malicious-instruction and rejection branches are visually separate, with no label collision. | Pass (carried) |
| Formal dependency graph | 21 | `figures/tikz_theory_diagram.tex` | Assumptions, lemmas, theorems, propositions, design consequence, and empirical oracles occupy distinct tiers. A deliberate vertical gap prevents the caption from touching the graphic. | Pass (carried) |
| Planned experimental setup | 30 | `figures/tikz_experimental_setup.tex` | Sources, factors, attacks, conditions, protected oracles, metrics, and reproducibility controls are separated. Control arrows terminate at box borders and do not cross text. | Pass (carried) |
| Conceptual PGFPlots trends | 34 | `figures/pgfplots_placeholder_results.tex` | Axes, legends, and tick labels are legible. Short component labels avoid the previous x-axis collision. Caption prominently states that coordinates are illustrative placeholders, not results. | Pass (carried) — **content is a placeholder; replace/remove before submission** |

## Short paper (Emerging Ideas, `mobisys/`)

| Figure | Page | Source | Audit | Status |
|---|---:|---|---|---|
| SecretHandle architecture (condensed) | 4 | `mobisys/sections/architecture.tex` (`figure*`, inline TikZ) | Source and build verified: the 12-page XeLaTeX build reports no overfull/underfull boxes and no undefined references, and the float spans both columns without clipping reported by LaTeX. **Visual re-inspection of the regenerated preview is pending human review.** | Pass (source+build) |

## Refresh note (2026-10-17)

- Previews regenerated at 150 dpi into `figure_previews/`: `figure_01_page_11.png` … `figure_06_page_34.png` and `mobisys_figure_01_page_04.png`.
- Figure source files under `figures/` were last modified 2026-10-03 and are unchanged, so the 2026-10-03 visual findings still apply; only page positions moved.
- The `mobisys/` condensed architecture figure is new relative to the 2026-10-03 audit and has not yet been visually inspected; only source and build integrity were checked.
- The final re-render/re-audit (item #327) still requires the last class/style change (venue-dependent) and a visual pass over the regenerated previews.

## Checks applied to every figure

- Native TikZ/PGFPlots vector output; no raster screenshots are used as manuscript figures.
- No external icon font is required; semantic roles are encoded with standard geometric shapes, hatching, line styles, and labels.
- Captions are descriptive and state the interpretation or limitation needed to read the figure safely.
- Graphics remain within the text block, with no cropping, off-page content, or arrowheads hidden under text.
- Color is redundant with dashing, hatching, shape, or position where it carries security meaning.

Result: **six full-paper figures pass content inspection (carried from 2026-10-03, sources unchanged); the new short-paper figure passes source+build checks and awaits visual review.**
