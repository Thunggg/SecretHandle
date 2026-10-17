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

- `du2025mobileattacks`: upgraded from abstract-only to **full-text verified** (arXiv HTML v3, Sec. IV-C "Clipboard / OTP Harvesting"). The manuscript's OTP exfiltration/forwarding motivation is directly supported: the paper has the agent switch from WhatsApp to the system Messages app, extract the **Alipay verification code**, and send it to the attacker. **Note a version/title drift:** v3 (2026-07-07) retitles the work to *Exploiting Mobile LLM Agents as Confused Deputies via Non-App-Controlled Channels* while the arXiv metadata title still shows the v1/v2 title; the entry stays keyed by the stable arXiv ID.
- `debenedetti2025camel`, `costa2025fides`, `shi2025progent`: re-checked against the **official arXiv pages** (v2, v2, and v3 respectively). Version drift recorded (Progent is now v3, 2026-05-14; CaMeL v2, 2025-06-24; Fides v2, 2025-09-03); titles and author order unchanged. Kept at **abstract-only verified** because the manuscript uses only high-level one-sentence summaries fully entailed by the abstracts; there is no nuanced comparison requiring section-level detail.

Known limitations:

- Tectonic/BibTeX reports empty page fields for several proceedings entries where official pages do not supply stable pagination; this is metadata completeness, not a missing citation.
- The arXiv-to-published upgrade pass (2026-10-17) is done: 10 entries (AutoDroid, AgentDojo, InjecAgent, indirect prompt injection, OSWorld, AndroidWorld, AITW, AppAgent, Mobile-Agent v1/v2) moved from `@article` arXiv preprint to `@inproceedings` at their published venues (MobiCom'24, NeurIPS D&B'23/'24, Findings of ACL'24, AISec'23, ICLR'25, CHI'25, ICLR'24 LLM-Agents workshop). The remaining fast-moving cluster (CaMeL, Fides, Progent, FinePrint, EIA, AEIA, ScreenAgent, Mobile-Agent-v3, mobile-attack measurement, anonymization) plus `chen2024spabench` and `chong2024casper` still have no confirmed archival venue and stay as arXiv until one is established; `toyama2021androidenv` is a technical report with no published version.
- Official Android pages are versioned web documentation; access dates are included, but a release snapshot should be archived with the artifact.

Result: **consistent for a research draft; the closest-work comparison and the mobile-OTP-attack motivation are full-text verified, one miscited role (AutoDroid) was corrected, all four remaining fast-moving arXiv entries were re-checked against their current versions (with drift recorded), and 10 arXiv entries were upgraded to their published archival venues. The residual arXiv-only cluster is limited to works with no confirmed published venue as of 2026-10-17 and is logged in `citation_search_log.md`.**
