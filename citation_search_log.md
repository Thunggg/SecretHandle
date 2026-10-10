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
