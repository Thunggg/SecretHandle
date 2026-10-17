# Citation consistency report

Audit date: 2026-10-03; full-text upgrade 2026-10-17.

- Bibliography entries: **57**.
- Distinct cited keys: **57**.
- Missing keys: **0**.
- Uncited retained entries: **0**.
- Duplicate keys: **0**.
- Seed arXiv IDs checked against titles and author order: pass.
- DOI/title checks for RFCs, ACL papers, AirGapAgent, and classical systems papers: pass at metadata level.
- Android citations point to official Android Developers/AOSP pages: pass.
- Substantive arXiv claims are limited to abstract-supported statements unless the full text was directly inspected; verification levels are recorded in `citation_claim_map.csv`.
- No citation from federated learning, mechanism design, or another topic dominates the paper.
- No empirical citation is used as a theorem for SecretHandle.
- No digital/tool-agent mechanism is described as an implemented Android analog path.

## Full-text upgrades (2026-10-17)

- `zhao2026anonymization` (closest mobile-placeholder work): upgraded from abstract-only to **full-text verified** (arXiv HTML v3, Sec. 3.2 and 3.5). Confirms the manuscript claim: detection is model-based (PII detector), the placeholder mapping is session-scoped, and the interaction proxy validates element-index ranges and resolves placeholders without binding a resolved value to a destination field or origin.
- `wen2023autodroid`: **corrected**. The earlier framing as a mobile-placeholder/anonymization baseline was unsupported; AutoDroid has no privacy/placeholder or value-substitution component (its components are a functionality-aware UI representation, memory injection, and multi-granularity query optimization). It is now cited only as a mobile-agent/task-automation system. Both `mobisys/sections/{background,related_work}.tex` and `sections/{introduction,related_work}.tex` were updated; `citation_claim_map.csv` reflects the corrected role.

Known limitations:

- Tectonic/BibTeX reports empty page fields for several proceedings entries where official pages do not supply stable pagination; this is metadata completeness, not a missing citation.
- The arXiv-heavy fast-moving cluster should be upgraded to published versions and full-text claim locations before submission.
- Official Android pages are versioned web documentation; access dates are included, but a release snapshot should be archived with the artifact.

Result: **consistent for a research draft; the closest-work comparison is now full-text verified, and one miscited role (AutoDroid) was corrected. Remaining arXiv claim-location upgrades for the fast-moving cluster are still a submission TODO.**
