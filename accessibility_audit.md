# Accessibility Audit

Audit date: 2026-10-17.

## Scope

Applies to all manuscript figures (mobisys and full paper). The `accessibility` LaTeX package is not installed in the current TeX environment, so `\Description{}` is not used; we document an equivalent accessibility posture.

## Findings

| Item | Status | Notes |
|---|---|---|
| Vector graphics (TikZ/PGFPlots) | Pass | All figures are vector; no raster screenshots as manuscript figures. |
| Color-redundant encoding | Pass | Security meaning encoded via shape/dashing/hatching/position in addition to color (per figure_quality_audit.md). |
| Descriptive captions | Pass | Captions describe interpretation, limitations, and semantics of visual elements. |
| Alt text provision | Deferred | `\Description{}` not injected due to missing `accessibility.sty`. A guarded conditional is recommended if/when the package becomes available. |
| PDF tagging | Deferred | PDF/UA tagging depends on venue preflight; not required for current submission class. |
| Reading order/figure placement | Pass | Figures placed with clear captions, labels; no hidden arrowheads. |

## Recommendation

If the venue requires PDF accessibility/tagging at camera-ready, add:

```latex
\IfFileExists{accessibility.sty}{\usepackage{accessibility}}{\newcommand{\Description}[1]{}}
```

Then add `\Description{...}` for each figure (e.g., mobisys architecture, threat/control boundary). Alternatively, provide alt text in the submission system if requested.
