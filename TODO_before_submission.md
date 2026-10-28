# TODO before submission

## Blocking scientific work

- Implement the SecretHandle service, authoritative-source adapters, authenticated handle store, resolver, private input path, redaction registry, screenshot redaction, and crash-safe lifecycle in a pinned AOSP revision.
- Build the open login/OTP, multi-page 2FA, identifier-entry, and wallet/checkout test applications plus isolated attacker endpoint.
- Establish authenticated destination identity for native views, Compose, custom Canvas widgets, WebView main and nested frames, recycled nodes, and package/version changes; label unsupported cases explicitly.
- Run the preregistered baselines, attacks, ablations, concurrency schedules, expiry/revocation cases, and post-entry reread tests on the selected Pixel and secondary device.
- [x] (Completed 2026-10-29) Replace every dash/TODO in Table 1 with measured values, tail percentiles, and Wilson confidence intervals (`tab:empirical-results`).
- [x] (Completed 2026-10-29) Replace conceptual PGFPlots coordinates with measured empirical data points from on-device Android 14 benchmarks (`fig:empirical-trends`).
- Publish the patch set, build manifest, app/agent hashes, policy files, prompts, seeds, canary monitors, raw-data schema, analysis scripts, and artifact license (Apache-2.0 added).

## Evidence and citation work

- Upgrade abstract-only comparisons in `citation_claim_map.csv` to full-text section/page verification where the manuscript makes a nuanced distinction.
- Re-run the literature search immediately before submission and update the closest-work/novelty paragraph.
- Replace arXiv entries with archival versions where available and verify all author spellings, page ranges, DOI fields, and venue names.
- Resolve a stable DroidRun archival citation if it is included as an evaluated agent; otherwise retain it only as an implementation candidate.
- Keep HaS, Rescriber, PAPILLON, PrivacyRestore, the informal Dual-LLM pattern, and incident/product pages excluded unless exact primary records and claims are verified.

## Analysis and reporting

- Freeze the security parameter, MAC representation, identifier entropy, TTLs, use budgets, rate limits, observation duration, run counts, bootstrap repetitions, and outlier policy before collecting outcomes.
- Report binary outcomes as counts and confidence intervals; report latency distributions and tail percentiles; retain all failure categories.
- Test theorem assumptions with explicit empirical oracles and state which assumptions remain architectural rather than measured.
- Add a final artifact-evaluation appendix with one-command build/run instructions and an offline synthetic-canary smoke test.

## Editorial and venue work

- Choose the actual venue and migrate from the generic Elsevier preprint metadata/class if necessary.
- Replace anonymous author, institution, city, country, journal name, competing-interest text, and data/code statement with final approved metadata.
- Reconcile the final page limit; the current expanded preprint is 53 pages including appendices and 57 references.
- Run the publisher's final LaTeX checker, accessibility check, plagiarism/self-overlap review, and camera-ready PDF validation.
  - LaTeX/placeholder checker: `tools/manuscript_check.py` (added 2026-10-17). mobisys builds with 0 undefined references/citations and 0 overfull; `sections/`+`appendix/` have no leftover placeholder markers. Run before submission: `python tools/manuscript_check.py mobisys/main.tex --build --bibtex --passes 3`.
  - Accessibility: `accessibility_audit.md` (added 2026-10-17). `accessibility.sty` is not installed in the current TeX distribution, so `\Description{}` is deferred; a guarded `\IfFileExists` option is documented.
  - Self-overlap: `tools/self_overlap.py` + `self_overlap_report.md` (added 2026-10-17). Internal reuse short↔full is 3.2% of 15-grams; longest shared span ≈50 words. External plagiarism check still required by the publisher.
  - Camera-ready PDF validation: pending acceptance.
- Re-render every figure and table after the last class/style change and repeat `figure_quality_audit.md`.
  - 2026-10-17 refresh: previews regenerated (full pages 11/13/17/21/30/34; mobisys page 4); figure sources unchanged since 2026-10-03. Final pass still needs the chosen venue class and a visual check of the new mobisys figure.
