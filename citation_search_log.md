# Citation search log

Search date: 2026-10-03. Canonical topic: Android OS-minted, destination/task-bound opaque secrets for mobile AI agents.

## Sources searched

- arXiv official abstract and metadata pages/API for exact IDs and author order.
- ACM Digital Library/DOI and DBLP for published systems and security papers.
- USENIX and NDSS official proceedings pages and full text.
- ACL Anthology for PAPILLON and PrivacyRestore.
- RFC Editor for HOTP, TOTP, HMAC, OAuth resource indicators, DPoP, and OAuth security BCP.
- W3C for WebAuthn.
- NIST for SP 800-63B.
- Android Developers and AOSP official documentation for SMS, Autofill, Credential Manager, clipboard sensitivity, Android 15 OTP/screen-share protection, Keystore/StrongBox, key attestation, accessibility, WebView, and Protected Confirmation.
- General web search was used for discovery; final entries point to an official archive, proceedings page, DOI, standards body, or platform documentation.

## Representative queries

- `site:arxiv.org/abs/2602.10139 Anonymization-Enhanced Privacy mobile GUI agents`
- `site:arxiv.org/abs/2510.27140 mobile agent OTP forwarding Alipay prompt injection`
- `site:arxiv.org/abs/2503.18813 CaMeL agent security`
- `site:arxiv.org/abs/2505.23643 FIDES agent security`
- `site:arxiv.org/abs mobile GUI agents AndroidWorld AppAgent AutoDroid benchmark`
- `site:arxiv.org prompt injection AgentDojo InjecAgent AirGapAgent IsolateGPT Progent`
- `site:aclanthology.org PAPILLON privacy LLM prompt sanitization`
- `site:developer.android.com SMS Retriever User Consent OTP Credential Manager autofill StrongBox`
- `site:developer.android.com EXTRA_IS_SENSITIVE clipboard`
- `site:source.android.com protected confirmation hardware-backed keystore`
- `site:rfc-editor.org RFC 4226 RFC 6238 RFC 8707 RFC 9449`
- `site:usenix.org TaintDroid Capsicum Android mandatory access control`

## Inclusion criteria

1. Direct support for mobile GUI-agent operation, privacy, attack, isolation, capability, Android mediation, authentication, destination/audience binding, or the planned benchmark.
2. Existence and metadata verified at an official scholarly archive, proceedings site, DOI publisher, standards body, or platform owner.
3. The cited claim is no stronger than the verified abstract/section.
4. Duplicate arXiv/conference versions are collapsed to one appropriate entry.

## Exclusion criteria

- Unverifiable title, author order, venue, or identifier.
- Discovery pages or marketing posts as the only source.
- A neighboring topic with no concrete claim in the manuscript.
- Duplicate version, superseded source, or a system that cannot support the intended claim.
- A named seed whose exact scholarly metadata or claim was not verified.

## Seed resolution

- arXiv:2602.10139 resolved to Zhao, Zou, Li, and Liu, *Anonymization-Enhanced Privacy Protection for Mobile GUI Agents: Available but Invisible*.
- arXiv:2510.27140 resolved to Du et al., *Measuring the Security of Mobile LLM Agents under Adversarial Prompts from Untrusted Third-Party Channels*.
- arXiv:2503.18813 resolved to Debenedetti et al., *Defeating Prompt Injections by Design* (CaMeL).
- arXiv:2505.23643 resolved to Costa et al., *Securing AI Agents with Information-Flow Control* (Fides).
- arXiv:2504.11703 resolved to Shi et al., *Progent: Securing AI Agents with Privilege Control*.
- arXiv:2504.11281 resolved to Chen et al., *The Obvious Invisible Threat...*.
- EIA resolved to arXiv:2409.11295.
- AirGapAgent resolved to CCS 2024, DOI 10.1145/3658644.3690350.
- IsolateGPT resolved to the NDSS 2025 official proceedings page.
- AutoDroid, AndroidWorld, AppAgent, Mobile-Agent/v2/v3, SPA-Bench, AndroidEnv, AITW, AgentDojo, and InjecAgent were resolved through official arXiv/proceedings metadata.

## Literature clusters

1. Mobile placeholders and inference-time privacy.
2. Mobile GUI agents and reproducible benchmarks.
3. Prompt injection, information-flow control, privileges, and agent isolation.
4. Capability systems and Android information-flow/access-control foundations.
5. OTP/authentication standards and audience/sender-bound tokens.
6. Official Android source, identity, redaction, and hardware-key mechanisms.

## Rejected candidates

See `references_rejected.md`. The most important exclusions are the Brave Comet report (not a scholarly source and not needed for a manuscript claim), the informal Dual LLM pattern, commercial AP2/Stripe/Visa/Mastercard pages, and seed names such as HaS/Rescriber whose exact intended scholarly records were not established in this pass.

## Counts

- Candidate pool examined: more than 70 records/pages across the clusters above.
- Final verified bibliography: 57 entries.
- Every final entry is cited; every citation key resolves.
- The majority are directly tied to the locked topic; peripheral systems-security foundations support explicit design statements only.

## Re-verification pass (2026-10-17)

Re-checked the four remaining abstract-only arXiv entries against their current official pages:

- arXiv:2503.18813 (CaMeL) — v2 (2025-06-24); title/authors unchanged; claim confirmed at abstract level.
- arXiv:2505.23643 (Fides) — v2 (2025-09-03); title/authors unchanged; claim confirmed at abstract level.
- arXiv:2504.11703 (Progent) — **v3 (2026-05-14)**; title/authors unchanged; privilege-control claim confirmed.
- arXiv:2510.27140 (mobile attack measurement) — **v3 (2026-07-07)**. Full text inspected (Sec. IV-C): the paper documents the Alipay verification-code harvesting workflow that motivates the threat model. **Version/title drift:** v3 retitles the paper to *Exploiting Mobile LLM Agents as Confused Deputies via Non-App-Controlled Channels*; the arXiv metadata title still shows the v1/v2 title. The bibliography keeps the stable arXiv ID.

Open decision: for arXiv:2510.27140, choose whether the bibliography title should follow the revised v3 document title or the current arXiv metadata title; keep whichever matches the version cited at submission.

## Archival-version upgrade pass (2026-10-17)

Upgraded 10 entries from `@article` (arXiv preprint) to `@inproceedings` (published venue). All verified against official proceedings/DOI/publisher pages. arXiv IDs retained where useful via DOI/URL.

- `wen2023autodroid` → MobiCom 2024. DOI 10.1145/3636534.3649379.
- `debenedetti2024agentdojo` → NeurIPS 2024 Datasets and Benchmarks Track. OpenReview s80yaEXev6.
- `zhan2024injecagent` → Findings of ACL 2024, pp. 10471–10506. DOI 10.18653/v1/2024.findings-acl.624.
- `greshake2023indirect` → ACM AISec 2023, pp. 79–90. DOI 10.1145/3605764.3623985.
- `xie2024osworld` → NeurIPS 2024 Datasets and Benchmarks Track. OpenReview Mk2A6hJcDp.
- `rawles2024androidworld` → ICLR 2025. OpenReview 0J7Qg3qI2O.
- `rawles2023aitw` → NeurIPS 2023 Datasets and Benchmarks Track.
- `zhang2023appagent` → CHI 2025, pp. 1–17. DOI 10.1145/3706598.3713600.
- `wang2024mobileagentv2` → NeurIPS 2024.
- `wang2024mobileagent` (Mobile-Agent v1) → First International Workshop on Large Language Model Agents (at ICLR 2024).

Verified but intentionally left as `@article` (arXiv-only; no published venue confirmed):

- `toyama2021androidenv` — arXiv:2105.13231 carries no journal-ref; remains a technical report.

Deferred pending venue confirmation:

- `chong2024casper` — **resolved (2026-10-17)**: IEEE CSCloud 2025 (12th Int'l Conf on Cyber Security and Cloud Computing), pp. 122–131, DOI 10.1109/CSCloud66326.2025.00027. Note the published version revises the evaluation (4500 synthesized + 2000 real prompts; PII accuracy 92.6%, topic accuracy 92.5–94.0%) relative to the arXiv v1 (4000 prompts; 98.5%/89.9%); the manuscript cites only the qualitative "detects and removes sensitive prompt content locally," which both versions support.
- `chen2024spabench` — **resolved (2026-10-17)**: ICLR 2025 (Spotlight; earlier a NeurIPS 2024 OWA workshop poster). OpenReview OZbFRNhpwr. Key retained as `chen2024spabench`; manuscript cites it only for benchmark breadth.
- Remaining 2024–2026 arXiv-only entries (CaMeL, Fides, Progent, FinePrint, EIA, AEIA, ScreenAgent, Mobile-Agent-v3, mobile-attack measurement, anonymization) — no confirmed archival venue as of this pass.
