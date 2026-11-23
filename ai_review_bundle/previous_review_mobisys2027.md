# ACM MobiSys 2027 Pre-Submission Re-Review: `SecretHandle`

---

## 1. Header

- **Paper Title:** *SecretHandle: OS-Minted, Destination- and Task-Bound Opaque Secrets for Android Mobile AI Agents*
- **Authors:** Nguyễn Tiến Thuận, Trần Phát Tài (FPT University, Can Tho, Vietnam) — single-blind submission
- **Review Date:** November 23, 2026
  - **Days remaining to Abstract Registration (Nov 27, 2026 23:59 AoE):** **4 days**
  - **Days remaining to Full Paper Submission (Dec 4, 2026 23:59 AoE):** **11 days**
  - *(CFP verified directly against `https://www.sigmobile.org/mobisys/2027/call_for_papers/` on Nov 23, 2026; all dates, rules, single-blind policy, 500-word rebuttal limit, and subsidized 2027 APC rates confirmed.)*
- **Mode:** **Mode B (Re-review of a revised version)** with complete Mode A depth across all required sections (incorporating `previous_review_mobisys2027.md` dated Oct 29, 2026, `revision_checklist.md`, revised `SecretHandle_MobiSys2027.pdf` built Oct 30, 2026, `manuscript_full_source.tex`, and `references_verified.bib`).
- **Track:** Regular Full Paper (assumed default; no `[Emerging Ideas]` prefix present).
- **Review Stance:** Balanced, rigorous ACM MobiSys TPC standard (calibrated for a highly selective systems venue).
- **Assumptions Made:**
  1. Authors intend to submit to the Regular Full Paper track of ACM MobiSys 2027 (no prior publication or concurrent submission elsewhere).
  2. No human subjects or real user credentials were used; all experiments used synthetic canaries as stated in Section 9 (p. 12) and Appendix A (p. 15).
  3. Because the user requested direct delivery of the `.md` review after a prior interrupted turn, Phase 0 intake questions were bypassed using explicit defaults listed above.
- **Review Limitations:**
  1. **`evidence_logs.rar` could not be extracted:** No RAR extraction utility (`unrar`, `unar`, `7z`, `bsdtar`, or Python `rarfile`) was available in the inspection environment. Therefore, the raw JSON benchmark logs inside `evidence_logs.rar` (`benchmark_autodroid_diversity.json`, `benchmark_overhead_lifecycle_redirection.json`, `extended_source_ui_benchmark.json`, `fallback_policy_benchmark.json`, `physical_device_benchmark.json`, `rq6_benign_regression_results.json`, `webview_failclosed_benchmark.json`) could **not** be cross-checked against the numbers printed in Section 7.
  2. **GitHub repository unverified:** Browsing `https://github.com/SecretHandle/SecretHandle` was blocked by environment policy and web search returned zero indexed results. Code execution, repository completeness, and public accessibility could not be verified.
  3. **Visual figure inspection:** PDF measurements (`pdfinfo`, `pdffonts`, `pdfminer`, `pdfimages`) were executed directly on `SecretHandle_MobiSys2027.pdf`; visual inspection relied on extracted page renders (pages 4 and 9) plus bounding-box coordinates. Authors must still perform a final 100%-zoom check in Adobe Acrobat and HotCRP's format checker.

---

## 2. Executive Verdict

- **Overall Recommendation:** **2.5 / 5 (Weak Reject / Borderline — leaning Weak Reject if submitted as-is; reachable 4 / 5 Weak Accept if Must-Fix items are completed in the remaining 11 days).**
- **Outcome Forecast (as-is):** Early Rejection: **15–25%** | Advances to R2 then Reject: **50–60%** | Conditional Accept with Shepherding: **20–25%** | Straight Accept: **<5%**.
- **Top 3 Strengths:** (1) High-relevance mobile systems security problem with a crisp attack/defense framing against Confused Deputy redirection on GUI agents (§1–§3); (2) clean monotonic policy algebra ($D_T \cap D_S \cap \text{TypePolicy}$) and formal transition model with atomic single-use reservation and post-entry redaction (§4–§6); (3) thorough revision discipline on arithmetic, Wilson CIs, Baseline B2 reframing, and artifact documentation (§7, Appendix A–B).
- **Top 3 Critical/Major Problems:**
  1. **[Critical] Unsubstantiated `"we audited 20 applications on Android 14"` claim (§7, p. 11):** The paper claims a 20-app real-world audit with zero app names, zero breakdown (`X/20` hints vs. custom views), and mixes in synthetic `BenchmarkRunner` microbenchmark numbers (`47.60 us`, `30/30`), while the authors' own `revision_checklist.md` confirms the 15–20 real-app audit has **not been run yet**.
  2. **[Critical] Persistent AOSP Reference Monitor vs. Stock Android 14 APK Gap & Self-Contradictions (§4, §6, §7, §9):** The paper still calls the prototype both *"a privileged Binder service"* (p. 6, 8) and *"an unprivileged broker"* (p. 12), claims interception *"at the telephony boundary"* (p. 11) for a `NotificationListenerService`, omits how OTP digits/bubbles are located without a detector or how `InjectInternal` works on stock Android 14, cites POSIX `mlock()`/`explicit_bzero` for a Java service (p. 12), and reports a suspiciously fast `17.63 us` TrustZone Keystore HMAC on Snapdragon 778G (p. 10).
  3. **[Major] Algorithmic, Numerical, and Evaluation Contradictions (§6–§7):** Algorithm 2 Line 13 wipes `s` unconditionally after multi-use resolution (`u > 0`), breaking multi-use handles; Section 7 (p. 10) miscalculates $4.18\,\text{ms} / 22.30\,\mu\text{s} = 187\times$ as *"4 orders of magnitude"*; Table 3 reports $U_{\text{att}}=1.00$ ($30/30$) without per-template breakdown despite Template 4 revoking handles and requiring human touch fallback; and `"zero task regression across 10 AndroidWorld applications"` (p. 1, 12) is only backed by `50/50` touch pass-through tests and 2-app `gfxinfo`, not end-to-end AndroidWorld task completion.
- **Single Most Important Thing to Fix:** Either **complete the real 15–20 Google Play app compatibility audit** (producing concrete `X/20` counts and an app table) before Dec 4 or strip the unsubstantiated `"audited 20 applications"` claim immediately, **and** resolve the technical accuracy contradictions in the stock Android 14 prototype description (`NotificationListener` vs. telephony boundary, `InjectInternal` API, `17.63 us` TrustZone HMAC verification, and Algorithm 2 Line 13).

### Mode B Delta Table (Previous Review Oct 29, 2026 $\rightarrow$ Revised Draft Oct 30, 2026)

| Previous Issue | Prev. Severity | Current Status | Evidence in Revised Manuscript (`SecretHandle_MobiSys2027.pdf` / `.tex`) |
| :--- | :---: | :---: | :--- |
| **W1:** AOSP `system_server` vs. stock Android 14 Broker/Overlay gap | Critical | **Partially Resolved (Still Critical)** | Clarifications added in §4 (p. 6), §6 (p. 8), §9 (p. 12). However, §7 (p. 11) still claims *"intercepts the SMS at the telephony boundary"*, §9 (p. 12) contradicts §4/§6 by calling it *"an unprivileged broker"*, `InjectInternal`/bubble-detection APIs on stock Android 14 remain unspecified, and Java `mlock()`/`explicit_bzero` (p. 12) is unsubstantiated. |
| **W2:** Alg. 2 Line 5 vs. Line 7 typo, DoS contradiction, & value-oblivious error codes | Critical | **Partially Resolved (Now Major)** | Line reference fixed (`Line~\ref{line:resolve:mismatch}` = Line 6, `Line~\ref{line:resolve:reserve}` = Line 7, p. 8 & p. 11). Internal audit logs (`ALREADY_RESOLVED`, `HANDLE_EXPIRED`, `CALLER_MISMATCH`) are now cleanly distinguished from agent-visible responses (`unavailable handle`, `destination denied`, p. 10–11). **Unresolved:** How $U_{\text{att}}=1.00$ ($30/30$) holds on Template 4 (DoS Depletion) when $k \ge 3$ revokes the handle and requires human touch confirmation, plus **New Bug** in Alg. 2 Line 13 (`wipe s` on multi-use handles). |
| **W3:** Security eval limited to 2 synthetic APKs; no real-app compatibility study | Major | **Unresolved $\rightarrow$ Upgraded to Critical (Credibility Risk)** | §7 (p. 11) added a paragraph claiming *"we audited 20 applications on Android 14"* plus `47.60 us` fallback and `56.80 us` WebView medians, **but** provides zero app names, zero compatibility percentages, and `revision_checklist.md` explicitly shows the 15–20 real-app audit is **incomplete (`[ ]`)**. |
| **W4:** Unfair Baseline B2 (conflating Credential Manager with SMS User Consent) | Major | **Resolved** | §7 (p. 9) renamed B2 to *"SMS Consent / Unbound Autofill Flow"*, explicitly acknowledged package binding in Credential Manager & SMS Retriever, and scoped B2's failure to SMS User Consent, intra-app field redirection, and lack of post-entry redaction. |
| **W5:** `Claude Sonnet 4.6` mislabeling, Mobile-Agent citation, ARM latency & CPU sums | Major | **Mostly Resolved (New Math Error Found)** | Fixed `Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)` throughout (p. 1, 2, 8); fixed Mobile-Agent citation `[38, 43]`; fixed ARM latency sum ($17.63+1.73+0.16+2.33+0.45 = 22.30\,\mu\text{s}$); fixed PSS breakdown ($14.2+2.1+12.4=28.7\,\text{MB}$); fixed ARM CPU sum ($3.2+3.2+0.8=7.2\%$). **New Error:** §7 (p. 10) claims $22.30\,\mu\text{s}$ is *"4 orders of magnitude faster"* than $4.18\,\text{ms}$ (actual ratio: $187.4\times \approx 2$ orders). |
| **W6:** Prompt injection delivery when SMS/notification is masked (Fig. 2) | Major | **Partially Resolved** | Appendix B (p. 15) and §7 (p. 11) now state payloads arrive via unredacted promotional notifications or chat/web pages. **Unresolved:** §7 (p. 10, *Qualitative Analysis*) still says *"In a representative Template 1 trial, an incoming SMS prompts the agent..."* (contradicting Table 5), and Fig. 2(b) still blacks out the entire SMS bubble (contradicting `revision_checklist.md` MF-3). |
| **W7:** Unexplained B1 `150 ms` overhead & missing energy measurement | Minor | **Partially Resolved (Still Minor/Major for MobiSys)** | B1 `150 ms` explained as local regex/NER scanning (p. 9). Added `< 0.12 mJ` per mediation event via `dumpsys batterystats` (p. 10), but methodology (simulated unplug software model, no hardware power monitor, no per-task drain) remains weak for MobiSys. |
| **W8:** Graphic clipping (Fig. 1), blurry Fig. 2, `Trân` header typo, `UL..` typo, LLM disclosure | Minor | **Mostly Resolved (New Layout Issue Found)** | Fixed `\shortauthors{Nguyễn and Trần}` (verified on P2–P14); fixed Fig. 1 right-side legend clipping; upgraded Fig. 2 PNGs to 1439–1612 ppi; fixed Table 1 `\textbf{S1}`; cleaned LLM disclosure (p. 12). **Remaining/New:** Page 8 `REMARK 5.16 (LEGITIMATE-BUT-UNW` heading overflow/clipping; Page 2 `UI..` double period in PDF render; Fig. 1 top diamond (`Injected content`) close to top edge; non-stock float spacing tweaks in `.tex` preamble. |

---

## 3. Compliance and Format Checklist (Phase 1 — Desk-Reject Screen)

| Item | CFP Requirement | Measured / Observed Value | Status | Method | Evidence (Page / Section) |
| :--- | :--- | :--- | :---: | :---: | :--- |
| File format & page size | PDF only, US Letter (`612 x 792 pt`), Adobe Acrobat compatible | PDF 1.7, `612 x 792 pts (letter)`, 15 pages, XeTeX `0.999997` | **OK** | **Measured** (`pdfinfo`) | All pages (P1–P15) |
| Embedded fonts | All fonts embedded | All 10 CID Type 0C / Type 1C fonts have `emb=yes, sub=yes, uni=yes` | **OK** | **Measured** (`pdffonts`) | All pages (P1–P15) |
| Page numbers | Visible on every page (`printfolios=true`) | Centered bottom page numbers `1` through `15` on all pages | **OK** | **Measured** (`pdfminer` + `.tex`) | Footer P1–P15; `.tex` line 77 |
| Main content page limit | $\le 12$ single-spaced numbered pages (incl. figs/tables); refs & appendix unlimited | Main content (§1–§10) ends on P12 right column (`y=192 pt`, ~75% of col used); `\clearpage` before References on P13; Appendix A–B on P14–P15 | **OK** | **Measured** (`pdfminer` + `.tex`) | P12 (§10), P13 (Refs), P14–P15 (App. A–B) |
| Hidden main content in appendix | Essential claims/results/threat model should not hide in appendix | Appendix A has artifact instructions; Appendix B has Table 5 (prompt injection taxonomy) and delivery channels referenced from §7 | **WARN** | **Estimated** | P14–P15 (App. A–B); Table 5 details clarify §7 W6 |
| Body font size | $\ge 10\text{ pt}$ (`\documentclass[sigconf,10pt]{acmart}`) | Body text measured at `9.96 pt` (exact LaTeX `10pt` in PDF bp) | **OK** | **Measured** (`pdfminer` + `.tex`) | P1–P12; `.tex` line 4 |
| Column geometry & lines/col | 2 columns, `9.25 x 3.33 in`, `0.33 in` gutter, $\le 55$ lines/col | Body columns `8.61 in` tall $\times$ `3.37 in` wide, `0.30 in` gutter (stock `acmart v2.20` `sigconf,10pt`); **40–52 lines/col** on P1–P12 (Refs P13–P14: 62–64 lines in stock `7.97 pt`) | **OK** | **Measured** (`pdfminer`) | P1–P12 (body); P13–P14 (stock ACM refs) |
| Template-tampering screen | No negative `\vspace`, shrunken margins, altered body spacing | No negative `\vspace`, no margin/linespread changes; **however**, preamble compresses float skips (`\textfloatsep=8pt`, `\floatsep=6pt`, `\intextsep=6pt`, `\abovecaptionskip=5pt`, `\belowcaptionskip=2pt`) and suppresses ACM ref block (`printacmref=false`) | **WARN** | **Measured** (`.tex` audit) | `.tex` lines 77–88 |
| Legibility & graphics | Readable at 100% zoom, no clipping/overflow, grayscale-safe | (1) **P8 `REMARK 5.16` heading overflows/clips** (`LEGITIMATE-BUT-UNW` / `ACTIONS).`); (2) Fig. 1 legend no longer clipped (`x1=537.7 pt`), but verify top diamond `Injected content` (`y=681..690`) in Acrobat; (3) Fig. 2 PNGs are high-res (`1439–1612 ppi`), but `height=2.6cm` makes text small at 100% zoom; (4) P2 §2 heading reads `UI..` in extraction | **FAIL / WARN** | **Measured** (`pdfminer`, `pdfimages`) + **Estimated** | P2 (§2), P4 (Fig. 1), P8 (Remark 5.16), P9 (Fig. 2) |
| Front matter & Single-blind | Names, affiliations, contacts (single-blind since 2026); CCS concepts; keywords; abstract $\ge 100$ words | Both authors, FPT emails, affiliation present; running header fixed (`Nguyễn and Trần`); CCS & keywords present; Abstract $\approx 265$ words | **OK** | **Measured** (`.tex` + `pdfminer`) | P1, P2–P14 running headers |
| LLM policy & prompt-injection screen | Disclose LLM-generated text; editing exempt; no hidden/white/tiny text | §9 (p. 12) states *"LLM tools were used solely for language proofreading"*; zero white or `<4.5 pt` hidden text detected across all 15 pages | **OK** | **Measured** (`pdfminer` color/size scan) | P12 (§9); full PDF scan |
| Ethics / IRB statement | Required if human subjects or non-public human data | States synthetic canaries & open benchmarks only; no human subjects | **OK** | **Estimated** | P12 (§9), P15 (App. A) |
| Prior publication / naming / artifact URL | No double submission; consistent naming; check public repo link | Consistent name `SecretHandle` (note: unrelated GitHub OSS repos use the name); `https://github.com/SecretHandle/SecretHandle` **unverified** | **Not verified** | **Not verifiable** (blocked/unindexed) | P14 (App. A) |
| Scope fit (CFP topics) | Genuine mobile systems contribution | Strong fit: *Security and privacy in mobile systems*, *New software systems for mobile computing*, *ML/AI for mobile devices* | **OK** | **Estimated** | P1–P2 (§1), P4–P6 (§4) |

### Exact Fixes Needed for Full Format Compliance

1. **Fix Page 8 `Remark 5.16` overfull heading:** In `manuscript_full_source.tex` (`\begin{remark}[Legitimate-but-unwanted actions]`), shorten the title to `\begin{remark}[In-scope misuse]` so the small-caps header never overflows or clips into the right column.
2. **Remove unnecessary float-spacing compression in preamble:** Because Page 12 right column currently has ~25% vertical whitespace remaining, remove lines 83–88 (`\setlength{\textfloatsep}...` through `\setlength{\belowcaptionskip}...`) so the manuscript uses 100% stock `acmart` vertical spacing (eliminating any template-tampering suspicion).
3. **Verify Figure 1 top edge and enlarge Figure 2 slightly:** Wrap Figure 1's `tikzpicture` in `\resizebox{\textwidth}{!}{...}` (or verify `Injected content` diamond at `y=6.3` in Adobe Acrobat) and increase Figure 2 height from `2.6cm` to `3.2cm` so notification text is effortless to read at 100% zoom.
4. **Inspect Page 2 `\paragraph{Mobile agents act through the UI.}` visually:** Confirm in Adobe Acrobat whether `acmart` produces a double period (`UI..`); if so, remove the trailing period inside `\paragraph{...}` (or check across all `\paragraph` macros for consistency).
5. **Run HotCRP's built-in PDF checker** immediately upon upload; an AI format audit never substitutes for HotCRP's automated compliance verification.

---

## 4. Submission Logistics Checklist (Phase 2)

- [ ] **Portal & Deadlines:** Register and submit at `https://mobisys27.hotcrp.com/` (*Author to confirm*).
  - **Abstract Registration:** **Nov 27, 2026 23:59 AoE (4 days left)** — meaningful title + $\ge 100$-word abstract matching the final paper (no placeholders); **no extensions**.
  - **Full Paper Submission:** **Dec 4, 2026 23:59 AoE (11 days left)** — author list (`Nguyễn Tiến Thuận`, `Trần Phát Tài`) is **fixed at submission** and cannot be modified afterward.
- [ ] **Conflicts of Interest (COI):** Review the full MobiSys 2027 TPC list (including PC co-chairs Jun Han — KAIST, `junhan@cyphy.kaist.ac.kr`, and Falko Dressler — TU Berlin, `dressler@ccs-labs.org`) and mark every genuine COI (same org within 24m/next 12m, co-authorship/grants within 24m/next 12m, advisor/advisee ever, same research group/advisor within 48m, prior exposure to the work, family/close personal). Do not over-mark (e.g., same research topic is **not** a COI) and never omit a COI (*Author to confirm*).
- [ ] **HotCRP Form Consistency:** Ensure Ethics certification (none required if strictly synthetic canaries — confirm no human data in any real-app screenshot/audit!), LLM disclosure (matches §9 proofreading statement), Regular Track (do **not** tick Emerging Ideas unless intentionally switching tracks), and Resubmission Summary (leave blank if first submission) (*Author to confirm*).
- [ ] **Public GitHub Artifact Link:** Confirm `https://github.com/SecretHandle/SecretHandle` is live, public, Apache 2.0 licensed, and matches every filename cited in Appendix A (`device/b3-secrethandle/b3.apk`, `configs/android14_eval.yaml`, `make check`, `make smoke`) **before** Dec 4 (*Author to confirm*).
- [ ] **Preprint / Tech Report Policy:** If posting an arXiv version during review, use a different system name and do not publicize it on social media/blogs while under review (*Author to confirm*).
- [ ] **Post-Acceptance Planning:** At least one author must register at the **non-student rate** and present in person in Ho Chi Minh City (June 21–25, 2027). Check if FPT University is in ACM Open (`https://libraries.acm.org/acmopen/open-participants`); if not, budget the subsidized 2027 APC (**$500 ACM/SIG member / $750 non-member**). Plan for optional post-acceptance Artifact Evaluation and TBA pitch-video/preview requirements (*Author to confirm*).

---

## 5. First-Round Survivability (Early-Rejection Screen)

- **First Two Pages (Abstract + §1 Introduction, p. 1–2):**
  - *What works:* The opening two pages are tightly written and genuinely engaging. The SecureBank/`refund.example` running example concretely distinguishes *memory theft* from *disclosure through legitimate handling*. The *"Why mobile"* paragraph makes a strong MobiSys-native argument (SMS Retriever, Credential Manager, Accessibility UI, WebView origins). Headline metrics are crisp, properly accompanied by Wilson CIs (`0/30`, `[0.00, 0.11]`), and the previous draft's jarring `"Claude Sonnet 4.6"` error is gone.
  - *What triggers skepticism in Round 1:* A seasoned mobile-systems reviewer reading the Abstract and §1 Contribution (iv) will notice an immediate tension: the paper opens by promising *"an Android design... a privileged service mints an opaque, authenticated handle at the authoritative OS source—the SMS or notification OTP pipeline, Credential Manager, the clipboard, or a wallet"* (p. 1), yet Contribution (iv) calls it *"an end-to-end stock-Android prototype implementation spanning notification brokering, screen overlay redaction, and atomic vault resolution"* (p. 2). A first-round reviewer will immediately flip to §7 to check whether Credential Manager/Wallet were actually built and whether the evaluation ran on real apps or synthetic APKs.
- **Early-Rejection Verdict:** **~75–85% probability of advancing past Round 1 to Round 2.** The problem framing, writing quality, formal model, and clean Table 3 headline numbers look strong on a skim. However, once assigned to deep Round 2 review, the missing real-app audit evidence (p. 11), AOSP-vs-stock-APK mismatch, and subtle technical bugs will dominate the discussion.

---

## 6. Summary and Claim–Evidence Table

### Neutral Summary

*SecretHandle* addresses secret disclosure and Confused Deputy destination redirection in Android GUI agents that read screens or accessibility trees to complete tasks requiring OTPs, credentials, or sensitive clipboard data. Rather than exposing plaintext values to the agent or relying on user-space regex placeholders, the paper proposes an OS-level capability layer that mints unforgeable, HMAC-authenticated opaque handles (`SH-XXXXXX`) at authoritative OS sources and binds each handle to a secret type, task identifier ($\tau$), destination predicate ($d$ over package, origin, field class, and node), and typed lifecycle (single-use + TTL for OTPs, multi-use task-scoped for identifiers, confirm-per-use for payments). When an agent issues `ENTER(handle)` (or types a handle string intercepted by the Agent SDK bridge), a trusted resolver authenticates the handle, verifies task and target context, atomically decrements the use budget via CAS, injects the value, and activates an observation redactor to mask subsequent screenshots and accessibility trees. The authors formalize non-disclosure, destination confinement, unforgeability, and single-use linearizability under six explicit reference-monitor assumptions and present Mint/Resolve algorithms. They implement a stock Android 14 prototype using a Binder service (`SecretHandleVaultService`), `NotificationListener` broker, and `TYPE_ACCESSIBILITY_OVERLAY`, evaluated primarily on an AWS EC2 x86_64 emulator against Mobile-Agent v3.5 (Claude 3.5 Sonnet) and AutoDroid (GPT-4o), plus microbenchmarks on a physical Samsung Galaxy A52s (Snapdragon 778G). Across 30 paired synthetic trials, SecretHandle achieves `0/30` exposure (vs. `29/30` unprotected), `0/30` redirection (vs. `30/30` for unbound placeholders and SMS consent), `50/50` atomic race safety, `22.30 us` core mediation on ARM, and reports zero regression across 10 AndroidWorld apps.

### Claim–Evidence Table

| Abstract / Intro Claim | Where Supported | Support Strength | Concrete Gap |
| :--- | :--- | :---: | :--- |
| **C1:** Mints opaque handles at authoritative OS sources: SMS/notification OTP pipeline, **Credential Manager, clipboard, wallet** (p. 1–2) | §4 (p. 4–5), §7 (p. 9–10) | **Partial** | Only SMS `NotificationListener` and sensitive clipboard (`EXTRA_IS_SENSITIVE`) are evaluated in §7. **Zero** implementation or evaluation for Credential Manager, Wallet, or Protected Confirmation. |
| **C2:** Destination binding over package, field class, and fail-closed confinement for unattested WebViews (p. 1–2) | §4 (p. 5), §5 (Thm 5.9), §7 (RQ2, p. 10–11) | **Partial** | Core agent trials (`n=30`) use only 2 custom APKs (`com.legitimate.bank`, `com.attacker.rewards`). The *"audited 20 applications"* claim on p. 11 provides no app names, no breakdown, and is flagged uncompleted in `revision_checklist.md`. WebView fail-closed (`30/30`, `56.80 us`) appears to be a synthetic `Vault.revealWeb` microbenchmark rather than end-to-end browser/WebView trials. |
| **C3:** Formal proofs of non-disclosure, confinement, unforgeability, single-use linearizability, enforced via Algorithms 1 & 2 (p. 2) | §5 (p. 6–8), §6 (Alg. 1–2, p. 8) | **Partial** | Proofs are mathematically clean under Assumptions 5.3–5.8, **but** Alg. 2 Line 13 contains a concrete pseudocode bug (`wipe s` executes even when `ok ∧ u > 0` for multi-use handles), and the stock Android 14 APK prototype does not satisfy strong AOSP-level Assumptions 5.3/5.6/5.7. |
| **C4:** Zero secret exposure (`0/30` vs `29/30`), zero redirection (`0/30` vs `30/30` for B1/B2), full utility under attack (`U_att = 1.00`) on visual & tree agents (p. 1–2) | §7 (Table 3, RQ1, RQ2, RQ4, p. 9–11), App. B | **Partial** | Paired synthetic trials ($n=30$) with Wilson CIs are well-structured, and B2 is now fairly framed. **Gap:** No per-template (T1–T5) breakdown; unclear how `U_att=1.00` ($30/30$) was achieved under Template 4 (`DoS Depletion`) when `k >= 3` revokes the handle and requires human touch fallback. |
| **C5:** Atomic single-use race safety (`50/50` races) and replay/TTL enforcement (p. 1–2) | §7 (RQ3, p. 10) | **Strong** | 10-thread barrier stress test across 50 handles (`500` threads total), sequential replay (`50/50`), and 5-minute TTL (`50/50`) directly validate Proposition 5.12 and 5.13. |
| **C6:** Microsecond in-vault transitions (`5.42 us` mint, `0.18 us` resolve; `22.3 us` ARM mediation; `4.2 ms` e2e) (p. 1–2) | §7 (RQ5, p. 10) | **Partial** | Emulator & ARM sums now add up exactly (`11.20 us`, `22.30 us`), **but** (a) `17.63 us` for TrustZone Keystore HMAC-SHA256 on Snapdragon 778G is unusually fast for a real TEE world-switch and needs measurement verification, and (b) text falsely calls `22.30 us` vs. `4.18 ms` *"4 orders of magnitude"* (actual: `187x` = ~2 orders). |
| **C7:** *"Zero task regression across 10 AndroidWorld applications ($\Delta = 0.00$)"* (p. 1–2, 12) | §7 (RQ6, p. 10) | **Weak** | RQ6 only reports `50/50` touch pass-through (`FLAG_NOT_TOUCHABLE`) and `gfxinfo` p95 on **2 apps** (Markor, Settings). No actual AndroidWorld agent task completion scores (`SR` under B0 vs. B3) are reported! |

---

## 7. Dimension Scores

*(Derived from CFP values and standard MobiSys practice — not an official MobiSys reviewing form.)*

| Dimension | Score (1–5) | One-Line Justification |
| :--- | :---: | :--- |
| 1. Scope and relevance to mobile systems | **5 / 5** | Directly targets Android OS secret pipelines, accessibility/overlay mediation, and mobile GUI agents. |
| 2. Novelty and insight | **3.5 / 5** | Combining OS-source capability minting, monotonic destination/field binding, and post-entry redaction is solid; must differentiate against 2026 mobile agent OS work (Aura, MATE). |
| 3. Significance and potential impact | **4 / 5** | Addresses an urgent, practical security blocker for deploying autonomous agents on personal smartphones. |
| 4. Technical soundness and depth | **3 / 5** | Good formal model and policy algebra, undermined by Alg. 2 Line 13 `wipe s` bug, `187x` vs. `4 orders` error, and root-compromise StrongBox overclaim. |
| 5. Implementation realism | **2 / 5** | Stock Android 14 user-space APK (`NotificationListener` + `TYPE_ACCESSIBILITY_OVERLAY`) falls far short of the paper's `system_server`/`InputDispatcher` reference-monitor framing; `mlock()`/`explicit_bzero` and `17.63 us` TrustZone HMAC appear inconsistent with a Java APK. |
| 6. Evaluation rigor | **2 / 5** | Unsubstantiated `"audited 20 applications"` claim without data, synthetic-only security APKs, missing per-template breakdown (esp. T4 DoS), unmeasured AndroidWorld task success, and software-modeled energy (`dumpsys batterystats`). |
| 7. Reproducibility and artifact readiness | **3.5 / 5** | Detailed Appendix A commands and Apache 2.0 plan, but GitHub repo is unverified, `evidence_logs.rar` unreadable here, and setup commands (`enabled_accessibility_services` / `allow_listener`) are missing. |
| 8. Presentation and clarity | **3.5 / 5** | Crisp prose and improved figures/headers, marred by Page 8 `Remark 5.16` heading clipping, small Fig. 2 text, and Template 1 vector contradiction between §7 and App. B. |
| 9. Ethics, privacy, safety | **4.5 / 5** | Synthetic canaries and isolated endpoints avoid real-user risk; only caveat is ensuring no private user data enters any real-app UI dump if MF-5 is executed. |
| 10. Honest limitations and discussion | **3.5 / 5** | Honest about in-scope misuse and WebView origin limits (§9), but overclaims prototype privileges, real-app audit completeness, and AndroidWorld task regression. |

---

## 8. Strengths (Ranked)

1. **Clear, MobiSys-native problem formulation and Confused Deputy attack demonstration (§1–§2, p. 1–3; §7 RQ2, p. 9–10):** Demonstrating quantitatively why user-space placeholder anonymization (B1, Zhao et al. [47]) fails completely (`30/30` leaks) under destination redirection—even when the agent never sees raw digits—is a compelling, memorable insight that immediately justifies OS-level destination binding.
2. **Clean monotonic policy algebra and formal lifecycle model (§4, p. 5; §5, p. 6–8):** Intersecting task policy $D_T$ (derived from the user-launched foreground package), source policy $D_S$, and type policy ensures monotonic narrowing. Separating immutable HMAC-authenticated metadata $H$ from mutable state $(u, k)$ in $\Omega[n]$ (Eq. 1) is an elegant design detail that preserves authenticator validity across multi-use lifecycles.
3. **Strong framing of Observation Closure and dual-agent validation (§4, p. 5; §7 RQ1/RQ4, p. 9):** Explicitly accounting for post-entry re-observation (the secret reappearing in the next screenshot or `AccessibilityNodeInfo` dump) and validating against both a visual VLM agent (Mobile-Agent v3.5 / Claude 3.5 Sonnet) and a structural tree agent (AutoDroid / GPT-4o) strengthens the evaluation's breadth.
4. **Substantial revision progress on Baseline B2 fairness, statistical hygiene, and arithmetic (§7, p. 9–10):** Compared to the Oct 29 draft, the authors cleanly fixed the `Claude 3.5 Sonnet` naming, separated internal audit codes from value-oblivious agent responses, reframed B2 honestly around SMS User Consent vs. Credential Manager/SMS Retriever, added exact 95% Wilson CIs, and fixed the ARM latency/PSS/CPU breakdowns.
5. **High-value specialized evaluations for realistic OTP patterns (§7 RQ2, RQ3, p. 10):** Testing 6-box segmented OTP traversal (`0.93 us`), Android 14 sensitive clipboard handles (`EXTRA_IS_SENSITIVE`, $u_0=5$), and a 10-thread barrier concurrency test (`50/50` atomic linearizability) shows attention to practical Android edge cases.

---

## 9. Weaknesses (Ranked by Severity)

### W1. [Critical | Confidence: High] Unsubstantiated `"we audited 20 applications on Android 14"` claim lacking any app list, breakdown, or completed data
- **What:** Section 7 (*Real-World Compatibility & Web Views*, p. 11) asserts: *"To evaluate generality beyond synthetic APKs, we audited 20 applications on Android 14. Standard inputs with recognized semantic hints directly match $\Match(d,x)$, while applications utilizing custom canvases, custom numpads, or unannotated containers are securely handled via \SH's fallback policy... successfully resolving handles in $30/30$ trials with zero raw exposure (median latency $47.60\,\mu\text{s}$)."* Yet the manuscript names **zero** of those 20 applications, reports **zero** counts of how many matched directly vs. needed fallback (`X/20` vs. `Y/20`), and conflates a $47.60\,\mu\text{s}$ in-process vault benchmark (`Vault.revealFallback`) with human single-tap touch confirmation trials. Worse, the authors' own `revision_checklist.md` (MF-5) marks the 15–20 real Google Play app audit as **incomplete (`[ ] CHƯA HOÀN THÀNH — CẦN CHẠY THẬT`)**.
- **Where:** Section 7, Page 11, right column (*Real-World Compatibility & Web Views*).
- **Why it matters for MobiSys:** Even without seeing `revision_checklist.md`, any MobiSys reviewer will immediately flag a `"we audited 20 applications"` sentence with no app list and no percentages as either sloppy or fabricated. If a shepherd or AE committee asks for the 20-app audit data and it does not exist, the paper faces **immediate rejection**.
- **Concrete fix (Fixable before Dec 4):** In the next 3–4 days, run `tools/audit_real_apps_compatibility.py` on **15–20 real Google Play apps** installed on your Samsung Galaxy A52s (recording exact package names, versions, category, `autofillHints`, `inputType`, `EditText` vs. custom view/WebView), add a compact summary table (in §7 or Appendix C) with exact `X/20` counts, and clearly separate the **static UI compatibility audit** from the **$n=30$ synthetic `Vault.revealFallback` latency microbenchmark (`47.60 us`)** (noting that real human tap confirmation adds human reaction latency on top of the `47.60 us` vault check). If you cannot finish the 20-app audit before Dec 4, **delete the `"we audited 20 applications"` claim entirely** before submission.
- **Effort:** 2–3 days (running the real audit on Galaxy A52s + adding table).

---

### W2. [Critical | Confidence: High] Unresolved Architectural Gap and Self-Contradictions Between AOSP Reference Monitor Design and Stock Android 14 APK Prototype
- **What:** While the revision added brief caveats acknowledging a stock Android 14 broker prototype (§4 p. 6, §6 p. 8, §9 p. 12), the manuscript still contains multiple direct technical contradictions and unexplained mechanisms:
  1. **Privileged vs. Unprivileged contradiction:** §4 (p. 6) and §6 (p. 8) describe a *"privileged Binder service"*, whereas §9 (*Limitations*, p. 12) calls it *"an unprivileged broker and accessibility overlay"*, and Appendix A (p. 15) installs it as a normal APK (`adb install device/b3-secrethandle/b3.apk`).
  2. **Telephony boundary overclaim:** §7 (p. 11) states *"the OS intercepts the SMS at the telephony boundary before rendering."* A `NotificationListenerService` on stock Android 14 does **not** intercept at the telephony boundary; it receives a callback *after* the SMS app has already received the broadcast, written to the SMS provider, and posted a notification (creating a finite arrival race window where the SMS app itself or a fast capture could see it).
  3. **Detector-free contradiction:** §1 (p. 2), §2 (p. 2–3), §4 (p. 5), and §8 (p. 12) attack B1 for being *"detector-dependent"* and *"screen scraping"*. Yet on Android 14 (`API 34`, prior to Android 15's system OTP notification classifier [2]), how does the stock-Android `NotificationListener` extract the OTP digits from an arbitrary SMS notification, and how does `TYPE_ACCESSIBILITY_OVERLAY` locate the exact SMS conversation bubbles in Figure 2(b) without regex/pattern matching and accessibility-tree inspection? The paper never says.
  4. **Unspecified `InjectInternal(V, s)` API:** How does `b3.apk` inject secrets into a third-party `EditText` on unmodified Android 14 without `ACTION_SET_TEXT` (which triggers `TYPE_VIEW_TEXT_CHANGED` events and passes through standard View buffers, violating the claim of *"private TCB buffers"* in Theorem 5.15)?
  5. **Java vs. C++ memory hygiene contradiction:** §9 (p. 12) claims *"Vault secrets are pinned to non-swappable memory (`mlock()`) and zeroed upon resolution or expiry (`explicit_bzero`)"*, yet Appendix A (p. 14) describes `device/b3-secrethandle` purely as *"Java and AIDL source code"* with `1.15 MB` Dalvik heap (p. 10) and mentions no JNI native C/C++ vault!
- **Where:** §1 (p. 2), §2 (p. 2–3), §4 (p. 6), §5 (Assumptions 5.3–5.7, Thm 5.15, p. 6–7), §6 (p. 8), §7 (p. 9–11), §9 (p. 12), App. A (p. 14–15).
- **Why it matters for MobiSys:** MobiSys systems reviewers rigorously audit the gap between *paper architecture* and *running code*. Contradictory claims about privilege level, telephony interception, and `mlock()`/`explicit_bzero` on a Java APK destroy reviewer trust.
- **Concrete fix (Fixable before Dec 4):**
  1. Add a concise **4-row Design vs. Prototype Mapping** in §6 (or a small table) explicitly stating for each component (Mint, Target Context, Injection, Redaction, Memory Hygiene) what the **upstream AOSP design** specifies vs. what the **stock Android 14 prototype (`b3.apk`)** actually implements (exact Android APIs: `NotificationListenerService` + regex/pattern parser on Android 14 vs. Android 15 `OTP_NOTIFICATION` pipeline; `AccessibilityNodeInfo.ACTION_SET_TEXT` with event filtering in the Agent SDK bridge; `char[]`/`byte[]` zeroing in Java vs. `mlock()`/`explicit_bzero` in upstream native AOSP C++).
  2. Fix every overclaim in §7 (p. 11: replace *"at the telephony boundary"* with *"at the notification broker before agent observation"*) and §9 (p. 12: reconcile *"unprivileged broker"* vs. *"privileged Binder service"* — explain it is a user-installed APK granted Android's elevated `BIND_NOTIFICATION_LISTENER_SERVICE` and `BIND_ACCESSIBILITY_SERVICE` permissions, while the untrusted agent runs in a separate unprivileged UID without those permissions).
  3. Explicitly note in §1 & §7 that Credential Manager and Wallet are covered by the general architecture/policy model (§4–§5) while the Android 14 prototype implements SMS/notification OTP and sensitive clipboard sources.
- **Effort:** 1–2 days (code check + text precision across §4, §6, §7, §9).

---

### W3. [Critical / Major | Confidence: Medium-High] Suspiciously Low TrustZone Keystore HMAC Latency (`17.63 us`) and 2-Orders-of-Magnitude Math Error (`4 orders` vs. `187x`)
- **What:**
  1. **Math Error (High confidence):** §7 (*Microbenchmark Overhead*, p. 10) states that ARM core mediation totals **$22.30\,\mu\text{s}$** and claims *"mediation remains **4 orders of magnitude** faster than full OS UI dispatch via AccessibilityService ($4.18\,\text{ms}$, p95 $5.82\,\text{ms}$)"*. Actual calculation: $4180\,\mu\text{s} / 22.30\,\mu\text{s} = \mathbf{187.4\times}$ (**~2 orders of magnitude**, not 4!). Even on the emulator ($4180 / 11.2 = 373\times$), it is ~2.5 orders of magnitude, not 4.
  2. **TrustZone Hardware Sanity Flag (Medium-High confidence — could not inspect `evidence_logs.rar`):** §7 (p. 10) reports *"On physical ARM silicon [Samsung Galaxy A52s, Snapdragon 778G with ARM TrustZone], TrustZone Keystore HMAC-SHA256 averages $17.63\,\mu\text{s}$ (p95 $23.33\,\mu\text{s}$)"*. On real Android 14 Qualcomm devices, an actual `AndroidKeyStore` HMAC call traverses App $\rightarrow$ Binder IPC $\rightarrow$ `keystore2` $\rightarrow$ Binder/HAL $\rightarrow$ `IKeyMintDevice` $\rightarrow$ QSEE/TrustZone SMC world-switch $\rightarrow$ return, which empirically takes **hundreds of microseconds to ~1–3 ms** (typically `500–2500 us`), NOT `17.63 us`! A latency of `17.63 us` strongly resembles an **in-process software JCA/Conscrypt `HmacSHA256`** call (or a key not actually executing inside TrustZone via `AndroidKeyStore` KeyMint per resolve), and `1.73 us` for Binder IPC is also extraordinarily fast compared to standard Android cross-process Binder round-trips (~`50–200 us`).
- **Where:** Section 7, Page 10, right column (*Microbenchmark Overhead (RQ5)*) and Abstract (p. 1).
- **Why it matters for MobiSys:** MobiSys has deep mobile-hardware/TEE experts on the TPC. Claiming `17.63 us` for a TrustZone Keystore round-trip without proving via `KeyInfo.getSecurityLevel()` that the key executed inside TEE (`SECURITY_LEVEL_TRUSTED_ENVIRONMENT`) on every call—paired with calling `187x` *"4 orders of magnitude"*—will trigger an immediate credibility meltdown in PC discussion.
- **Concrete fix (Fixable before Dec 4):**
  1. Fix *"4 orders of magnitude"* to *"over two orders of magnitude ($\sim 187\times$)"* (p. 10).
  2. **Audit `BenchmarkRunner.java` immediately:** Verify whether the `17.63 us` ARM HMAC was actually invoking `AndroidKeyStore` (`KeyStore.getInstance("AndroidKeyStore")`, checking `KeyInfo.getSecurityLevel() == SECURITY_LEVEL_TRUSTED_ENVIRONMENT`) on every iteration, OR whether it used an in-memory `SecretKeySpec` / cached session key derived from Keystore! Similarly verify whether `1.73 us` Binder IPC was an in-process local Binder call (`IBinder` inside `app_process`) vs. cross-process IPC. If it was a Keystore-derived ephemeral session key in memory (which is actually a very sensible systems optimization!), **say so honestly** and measure a real cross-process `AndroidKeyStore` TEE call (`~0.5–2 ms`) to justify why caching a TEE-derived ephemeral HMAC key in vault memory is needed!
- **Effort:** 0.5–1 day (inspect `BenchmarkRunner.java` + re-run one cross-process `AndroidKeyStore` check on Galaxy A52s).

---

### W4. [Major | Confidence: High] Pseudocode Bug in Algorithm 2 Line 13 (`wipe s` Destroys Multi-Use Handles) and StrongBox Root-Compromise Overclaim
- **What:**
  1. **Algorithm 2 Line 13 Bug:** Look at `manuscript_full_source.tex` (Algorithm 2, Line 13, p. 8):
     `\textbf{if} $ok \land u>0$ \textbf{then} $z\gets\mathsf{live}$ \textbf{else if} $\neg ok \land u_0>1$ \textbf{then} $(z,u)\gets(\mathsf{live},u+1)$ \textbf{else} $z\gets\mathsf{consumed}$; wipe $s$`
     As written, `wipe s` sits after the semicolon at the end of Line 13, executing on **all three branches**—including `ok ∧ u > 0` (a live multi-use handle like clipboard with $u_0=5$ after its 1st use, when $u=4 > 0$)! Wiping `s` when $u > 0$ destroys the secret before its remaining uses. (Also, if `InjectInternal` fails *uncertainly* after partial buffer mutation on $u_0>1$, refunding $u \leftarrow u+1$ slightly relaxes the conservative consumption statement on p. 5—clarify that refund occurs only on pre-mutation abort.)
  2. **Root-Compromise Overclaim (§9, p. 12):** Section 9 claims: *"Keys reside in TrustZone/StrongBox, preventing handle MAC forgery even under root compromise."* This is technically false: StrongBox prevents **offline key extraction**, not **online MAC forgery under root compromise**, because a root adversary can call the Keystore/KeyMint signing API as the privileged service (or patch `SecretHandleVaultService` directly, violating Assumption 5.3 and §3 p. 3 which rightly states *"If the agent has root... the redaction boundary is void"*).
- **Where:** Algorithm 2 Line 13 (p. 8); Section 9 (p. 12, right column).
- **Why it matters for MobiSys:** Security reviewers read pseudocode line by line and immediately penalize invalid root-compromise claims.
- **Concrete fix (Fixable before Dec 4):**
  1. Rewrite Algorithm 2 Line 13 clearly with scoped `wipe s` strictly in the `else` (`consumed`) branch: `else z <- consumed; wipe s` (using explicit braces or moving `wipe s` into an indented block / `if z = consumed then wipe s`).
  2. Fix §9 (p. 12) to: *"Keys reside in TrustZone/StrongBox, preventing offline key extraction even if device storage is compromised (online root compromise remains out of scope per §3)."*
- **Effort:** 1 hour.

---

### W5. [Major | Confidence: High] Unexplained $U_{\text{att}}=1.00$ ($30/30$) Under Template 4 (`DoS Depletion`), Missing Per-Template Breakdown, and Template 1 Vector Contradiction
- **What:**
  1. **Template 4 DoS Depletion vs. $U_{\text{att}}=1.00$:** Appendix B (Table 5, p. 15) shows the 30 attack trials comprise 5 templates ($n=6$ each), including **T4: DoS Depletion** (*"Repeats $\ge 3$ times"*). Page 11 states that under $\ge k_{\max}=3$ mismatches, *"the handle transitions to revoked and triggers local user touch-confirmation fallback."* Yet Table 3 (p. 9) reports a flat $U_{\text{att}} = 1.00$ ($30/30$) without disclosing **how many trials triggered human touch confirmation** vs. autonomous agent recovery! Counting human intervention as autonomous agent utility without reporting the intervention rate is misleading.
  2. **No per-template breakdown:** Table 3 aggregates all 5 templates into a single $n=30$ row, hiding per-template behavior (e.g., in T3 Web Phishing, did the agent attempt the browser, get fail-closed rejected, and then navigate back to the native banking app? And why does Page 11 say `30/30` for `"web flows (Template 3)"` when Appendix B says Template 3 has $n=6$ trials?).
  3. **Residual Template 1 contradiction:** Page 10 (*Qualitative Analysis*) still reads: *"In a representative Template 1 trial, an incoming SMS prompts the agent to forward its banking OTP (`com.legitimate.bank`) to an external app (`com.attacker.rewards`)"*, directly contradicting Table 5 (p. 15) which defines Template 1's attack vector as *"Cross-app promotion notification"* (and Appendix B's claim that payloads came from unredacted non-banking notifications).
  4. **Lost SMS context in Figure 2(b):** Figure 2(b) masks the entire SMS conversation bubble (`SecretHandle: protected`). Despite `revision_checklist.md` claiming OTP digits are replaced while preserving transaction context (amount/recipient), the manuscript text **never** explains or evaluates selective span redaction vs. full-bubble masking.
- **Where:** Table 3 (p. 9), §7 (p. 10–11), Fig. 2(b) (p. 9), Appendix B Table 5 (p. 15).
- **Why it matters for MobiSys:** Reviewers will ask whether `U_att = 1.00` was inflated by human-in-the-loop fallback or harness resets, and why the text contradicts its own appendix on Template 1 and Template 3 sample sizes ($n=6$ vs. $n=30$).
- **Concrete fix (Fixable before Dec 4):**
  1. Add a small breakdown (inline or compact 5-row table) showing `(E, R, U_att, human_fallback_count)` for each template T1–T5 ($n=6$ each), explicitly distinguishing autonomous recovery from user touch-confirmation fallback on T4.
  2. Clarify that the $30/30$ WebView result on p. 11 (`56.80 us`) is a dedicated `Vault.revealWeb` microbenchmark, separate from the $n=6$ end-to-end agent trials of Template 3.
  3. Fix p. 10 (*Qualitative Analysis*) so Template 1 matches Table 5 (*"a promotional notification arriving alongside the banking SMS prompts the agent..."*).
  4. Honestly discuss the Figure 2(b) full-bubble masking vs. span-level redaction trade-off in §4/§9 (do not claim span-level context preservation unless actually implemented and shown in Fig. 2b).
- **Effort:** 1 day (verify trial logs in `results/trials.jsonl` and update §7 + App. B).

---

### W6. [Major | Confidence: High] Overclaimed `"Zero Task Regression Across 10 AndroidWorld Applications"`, Emulator-Only Agent Trials, and Weak Energy Methodology
- **What:**
  1. **AndroidWorld Task Regression Overclaim:** Abstract (p. 1), Intro (p. 2), and Conclusion (p. 12) claim *"zero task regression across 10 AndroidWorld applications ($\Delta = 0.00$)"*. Yet §7 (RQ6, p. 10) never reports any end-to-end AndroidWorld agent task success rate (`SR` under B0 vs. B3)! It only reports `50/50` touch pass-through events (`FLAG_NOT_TOUCHABLE`) and `dumpsys gfxinfo` p95 frame time on **2** apps (Markor `18.0 ms`, Settings `36.0 ms`). Calling touch pass-through *"zero task regression across 10 AndroidWorld applications"* will be seen as severe overclaiming by anyone familiar with AndroidWorld [32].
  2. **Emulator vs. Real Device Framing:** Abstract (p. 1) says *"We evaluate an on-device Android 14 prototype..."*, yet all end-to-end VLM/tree agent trials (Table 3) ran on an AWS EC2 x86_64 emulator, with the physical Samsung Galaxy A52s used only for `app_process` microbenchmarks and daemon profiling.
  3. **Energy Measurement Methodology:** §7 RQ6 (p. 10) claims *"< 0.12 mJ per mediation event"* using `dumpsys batterystats` under *simulated battery unplug*. `dumpsys batterystats` is a coarse software estimator driven by static OEM `power_profile.xml` coefficients—not a hardware power monitor—and cannot reliably resolve `< 0.12 mJ` per single microsecond mediation event. No display brightness, radio state, thermal state, or end-to-end 15-step task battery impact is reported.
  4. **Ablation $n=1$ Control:** §7 (*Ablation*, p. 11) claims `No Observation Redactor` gives $L=1.00$ based on a *"1/1 control test"*, and lists `No Source Minting` ($E=0.97$), `No Destination Binding` ($R=1.00$), `No Atomic CAS` ($50/50$) without clarifying whether these are fresh ablation runs or restated B0/B1 results.
- **Where:** Abstract (p. 1), §1 (p. 2), §7 (RQ5, RQ6, Ablation, p. 10–11), §10 (p. 12).
- **Why it matters for MobiSys:** MobiSys reviewers have strict expectations on real-device evaluation, power measurement rigor, and honest scoping of benchmark claims.
- **Concrete fix (Fixable before Dec 4):**
  1. Either run an actual set of end-to-end AndroidWorld benign tasks (e.g., 10–20 tasks across those 10 apps with Mobile-Agent/AutoDroid under B0 vs. B3 and report exact `X/N` vs. `Y/N`), **or** reword Abstract/Intro/Conclusion honestly to: *"zero touch-passthrough or frame-latency regression across 10 AndroidWorld applications (`50/50` events, $\Delta\text{p95}=0.0\,\text{ms}$)"*.
  2. State clearly in Abstract/§7 that end-to-end agent experiments ran on Android 14 KVM emulation while hardware mediation/CPU/memory/battery profiling ran on a physical Samsung Galaxy A52s (Snapdragon 778G).
  3. In RQ6, qualify `< 0.12 mJ` explicitly as a software estimate from `dumpsys batterystats` (not hardware power-meter instrumentation), or measure unplugged discharge/current on Galaxy A52s via `/sys/class/power_supply/battery/current_now` over Wi-Fi ADB with fixed brightness/airplane mode for 15–30 minutes.
  4. Run `n=10` (or `n=30`) for the `No Observation Redactor` ablation so it isn't `1/1`.
- **Effort:** 1–2 days (rewording + unplugged Galaxy A52s power/ablation script; +2 days if running end-to-end AndroidWorld agent tasks).

---

### W7. [Major | Confidence: Medium-High] Missing Recent 2026 Mobile Agent Security Related Work & Unverified Public Artifact Repository
- **What:**
  1. **Missing 2026 Mobile Agent OS / Runtime Guardrail Work:** Section 8 (§8, p. 11–12) cites Zhao et al. (`arXiv:2602.10139`, Feb 2026) well, but misses closely adjacent 2026 mobile agent security architectures: **Aura** (*"Blind Gods and Broken Screens: Architecting a Secure, Intent-Centric Mobile Agent Operating System"*, `arXiv:2602.10915`, Feb 2026), **MATE** (*"Mobile Agent Trustworthy Execution for Safe and Efficient Mobile Control"*, EMNLP Findings Oct 2026 / `arXiv:2611.25526`), and classic Android sensitive-UI identification systems **SUPOR** (Huang et al., USENIX Security '15) and **UIPicker** (Nan et al., USENIX Security '15) plus TrustZone UI work **TrustUI** (Li et al., APSys '14) / **TruZ-Droid** (Ying et al., MobiSys '18).
  2. **Unverified GitHub Repo & Incomplete Reproduction Commands:** `https://github.com/SecretHandle/SecretHandle` could not be verified online. Appendix A (p. 15) omits the `adb shell` commands required to grant Notification Listener and Accessibility Service permissions to `b3.apk` after `adb install`.
- **Where:** §8 (p. 11–12), `references_verified.bib`, Appendix A (p. 14–15).
- **Why it matters for MobiSys:** Omitting `Aura` (a Feb 2026 Android agent OS paper on the exact same arXiv month as Zhao et al.) or classic MobiSys trusted-UI work (`TruZ-Droid`) makes Related Work look incomplete to domain experts; a dead GitHub link in Appendix A creates immediate negative impression.
- **Concrete fix (Fixable before Dec 4):** Add 3–4 sentences in §8 differentiating SecretHandle from Aura (`arXiv:2602.10915`), SUPOR/UIPicker (sensitive UI field detection), and TruZ-Droid/TrustUI (TrustZone UI paths); verify `https://github.com/SecretHandle/SecretHandle` is live and public; add the exact `adb shell cmd notification allow_listener` and `settings put secure enabled_accessibility_services` lines to Appendix A.
- **Effort:** 0.5 day.

---

### W8. [Minor | Confidence: High] Remaining Polish, Typesetting, and BibTeX Issues
- **What:**
  1. **Page 8 Remark 5.16 heading overflow:** Renders as `REMARK 5.16 (LEGITIMATE-BUT-UNW` / `ACTIONS).` in the PDF.
  2. **Preamble float-spacing tweaks:** Lines 83–88 of `.tex` tighten `\textfloatsep`, `\floatsep`, `\abovecaptionskip`, etc., despite spare whitespace on Page 12.
  3. **BibTeX entry type error:** `dennis1966semantics` (`[18]`, p. 13) uses `@inproceedings` for *Communications of the ACM* (a journal -> should be `@article`). Also 14 unused entries remain in `references_verified.bib`.
  4. **Figure 2 size & Page 2 `UI..` check:** Figure 2 (`height=2.6cm`) is slightly small at 100% zoom; verify Page 2 `Mobile agents act through the UI..` visually.
- **Where:** P2 (§2), P8 (Remark 5.16), P9 (Fig. 2), P13 (`[18]`), `.tex` lines 83–88.
- **Concrete fix:** Shorten Remark 5.16 title, restore stock float skips, fix `@article{dennis1966semantics}`, enlarge Fig. 2 to `3.2cm`, and visually inspect P2 & P4 in Adobe Acrobat.
- **Effort:** 2 hours.

---

## 10. Technical and Numerical Audit (Phase 4)

### A. Formal Model & Algorithm Audit (§5–§6)
- **Eq. (1) & Proofs (§5, p. 6–7):** Keeping immutable metadata $H$ inside $a=F_K(\enc(H))$ while tracking mutable $(u, k)$ in $\Omega[n]$ is sound. Theorem 5.9 (Destination Confinement), Corollary 5.10, Theorem 5.11 ($\Adv^{\mathsf{euf}}_{F,\mathcal{B}}(\lambda) + Q/2^\lambda$), Proposition 5.12, Proposition 5.13, and Theorem 5.15 (Non-Disclosure) are internally valid **conditional on Assumptions 5.3–5.8**.
- **BUG in Algorithm 2 Line 13 (p. 8):**
  ```
  if ok ∧ u > 0 then z <- live
  else if ¬ok ∧ u_0 > 1 then (z, u) <- (live, u + 1)
  else z <- consumed; wipe s
  ```
  In standard pseudocode indentation/single-line formatting, `; wipe s` executes outside the `else` branch, wiping `s` even after the first use of a valid multi-use handle (`u_0 = 5`, `u = 4 > 0`). **Must fix.**
- **Assumption-to-Prototype Gap:** Assumption 5.3 (*no modification/bypass*), Assumption 5.6 (*target identity equals actual commit target*), and Assumption 5.7 (*every screenshot/tree/event/log applies value-independent mask before $s$ becomes observable*) hold cleanly in the upstream AOSP `InputDispatcher`/`ViewRootImpl` architecture, **but hold only weakly** in the stock Android 14 `NotificationListener` + `TYPE_ACCESSIBILITY_OVERLAY` prototype (e.g., the SMS app renders before the overlay updates; `ACTION_SET_TEXT` passes through standard app buffers rather than private TCB buffers).

### B. Numerical Audit (Verified via Python Script)

| Claimed Number / Expression | Location | Recomputed Value | Verdict |
| :--- | :--- | :--- | :---: |
| Wilson 95% CI: `0/30` = `[0.00, 0.11]` | Table 3 (p. 9) | `[0.0000, 0.1135]` | **OK** |
| Wilson 95% CI: `1/30` = `0.03 [0.01, 0.17]` | Table 3 (p. 9) | `[0.0059, 0.1667]` | **OK** |
| Wilson 95% CI: `29/30` = `0.97 [0.83, 0.99]` | Table 3 (p. 9) | `[0.8333, 0.9941]` | **OK** |
| Wilson 95% CI: `30/30` = `1.00 [0.89, 1.00]` | Table 3 (p. 9) | `[0.8865, 1.0000]` | **OK** |
| Wilson 95% CI: `0/50` = `[0.00, 0.07]`, `50/50` = `[0.93, 1.00]` | Table 3 (p. 9) | `[0.0000, 0.0713]`, `[0.9287, 1.0000]` | **OK** |
| Emulator core mediation sum: `0.61 + 9.32 + 0.08 + 0.13 + 1.06` | §7 RQ5 (p. 10) | `11.20 us` (claimed `11.2 us`) | **OK** |
| ARM core mediation sum: `17.63 + 1.73 + 0.16 + 2.33 + 0.45` | §7 RQ5 (p. 10) | `22.30 us` (claimed `22.30 us`) | **OK** |
| TrustZone/Emulator HMAC ratio: `17.63 / 9.32` | §7 RQ5 (p. 10) | `1.89x` (claimed `~1.9x`) | **OK** |
| Vault PSS breakdown: `14.2 + 2.1 + 12.4` | §7 RQ5 (p. 10) | `28.7 MB` (claimed `28.7 MB`) | **OK** |
| ARM CPU burst sum: `3.2% + 3.2% + 0.8%` | §7 RQ6 (p. 10) | `7.2%` (claimed `7.2%`) | **OK** |
| Mediation (`22.30 us`) vs. VLM step (`48.6 s`): `< 0.01%` | §7 RQ5 (p. 10) | `0.000046%` (even `4.18 ms / 48.6 s` = `0.0086% < 0.01%`) | **OK** |
| **Mediation (`22.30 us`) vs. OS UI dispatch (`4.18 ms`): *"4 orders of magnitude faster"*** | **§7 RQ5 (p. 10)** | **$4180 / 22.30 = 187.4\times$ (~2 orders, NOT 4!)** | **FAIL (Fix!)** |
| **TrustZone Keystore HMAC-SHA256 = `17.63 us` & Binder IPC = `1.73 us` on Galaxy A52s** | **§7 RQ5 (p. 10)** | **Suspiciously fast for real TEE world-switch / cross-process Binder; `evidence_logs.rar` unreadable** | **WARN (Verify!)** |
| **Web flows (Template 3): `30/30` vs. App. B `n=6` per template** | **§7 (p. 11) vs. App. B (p. 15)** | **Sample-size discrepancy (`30` vs. `6`) unexplained** | **FAIL (Clarify!)** |

---

## 11. Evaluation Audit (Phase 5 — Adversarial & Domain Checklists)

- **Baselines:** B0 (Unprotected), B1 (Detected Placeholder approximating Zhao et al. [47]), and B2 (reframed accurately as *SMS Consent / Unbound Autofill Flow*) are now fair and well-scoped. One gap: no direct quantitative comparison against planner-side isolation (e.g., CaMeL [16] or Progent [35]), though Table 4 reasonably argues those target tool-API planners rather than vision GUI pixel/accessibility channels.
- **LLM-Based & Agentic Mobile Systems Checklist:**
  - *Model names, versions, temperature:* `claude-3-5-sonnet-20241022` ($T=0.0$, top-p $1.0$, max 15 steps) for Mobile-Agent v3.5 and `gpt-4o-2024-08-06` ($T=0.0$) for AutoDroid are disclosed. **Missing:** API call dates, system prompts, and token/dollar cost.
  - *Nondeterminism:* Handled via $n=30$ paired trials with fresh synthetic canaries and 95% Wilson CIs (good).
  - *Task realism:* **Weak** — security evaluation relies on 2 synthetic APKs; real-app compatibility claim (`20 apps`) is unsupported.
- **Security / Privacy Checklist:**
  - *Threat model:* Crisp, explicit 3-principal model, `adb unroot` + SELinux enforcing.
  - *Adaptive adversaries:* Tests 5 prompt-injection templates (T1–T5) including DoS depletion (T4) and multilingual (T5), plus handle visual spoofing. **Missing:** (a) per-template breakdown; (b) adaptive timing race between SMS arrival / scrolling and `TYPE_ACCESSIBILITY_OVERLAY` redraw on stock Android 14; (c) adaptive attack where an adversary app mimics `smsOTPCode` hint or invokes the fallback touch-confirmation prompt via tapjacking/overlay tricks.
- **Mobile Software, OS, and App Systems Checklist:**
  - *Device/OS diversity:* Only Android 14 (API 33/34) on 1 emulator + 1 physical phone (Galaxy A52s, microbenchmarks only). No Android 15/16 testing despite citing Android 15's OTP notification pipeline [2].
  - *Real apps vs. toy apps:* **Major gap** (W1, W6).
  - *App startup/jank/battery:* `dumpsys gfxinfo` only reported for 2 of 10 AndroidWorld apps (Markor, Settings); no startup latency; no end-to-end AndroidWorld task completion numbers.
- **Energy and Resource Management Checklist:**
  - *Methodology:* Uses `dumpsys batterystats` under simulated unplug (**software model**, not hardware power monitor). Does not report display brightness, radio state, thermal throttling, or end-to-end battery drain per 15-step agent task.

---

## 12. Ethics and Responsible Research (Phase 6)

- **Human Subjects / IRB:** None involved; §9 (p. 12) and Appendix A (p. 15) state that all evaluations used synthetic canaries, synthetic bank/attacker APKs, and open benchmarks. No IRB certification is required under MobiSys 2027 rules **provided** that if the authors execute the 15–20 real Google Play app compatibility audit (W1), they inspect only their own test accounts/unauthenticated login screens and store zero real personal data or third-party user data.
- **Dual Use & Terms of Service:** Attack templates and synthetic APKs target no real commercial banking vulnerability; responsible disclosure is not triggered. Do **not** run prompt-injection attacks against live commercial banking apps (keep real-app testing strictly to read-only UI metadata audits or benign compatibility checks).
- **LLM Disclosure:** §9 (p. 12) states LLM tools were used solely for language proofreading, complying with the MobiSys 2027 LLM policy.

---

## 13. Reproducibility and Artifact Readiness (Phase 7)

- **What is ready:** Appendix A (p. 14–15) clearly separates the offline Python verification package (`src/secrethandle`, `make check`, `make smoke` with `seed 20261017`) from the Android 14 prototype (`device/b3-secrethandle/b3.apk`, `BenchmarkRunner`, `run_agent_matrix.py`, `provenance.json`) under Apache 2.0. Appendix B now prints all 5 prompt injection templates (Table 5).
- **What the authors must prepare before Dec 4:**
  1. Verify `https://github.com/SecretHandle/SecretHandle` is live, public, and actually contains every file named in Appendix A (including `b3.apk` source, synthetic APKs, `android14_eval.yaml`, and raw logs matching Table 3).
  2. Add the missing Android setup commands to Appendix A (`adb shell cmd notification allow_listener ...`, `adb shell settings put secure enabled_accessibility_services ...`, `adb unroot` verification).
  3. Include the exact agent system prompts and Mobile-Agent v3.5 / AutoDroid commit hashes in the repo (and summarize key prompt settings in Appendix B) so non-authors can replicate Table 3.
  4. Document how to reproduce the physical Galaxy A52s TrustZone and `dumpsys batterystats` measurements.

---

## 14. Novelty, Related Work, and Scooping Risk (Phase 3 & 8)

- **Closest Prior Work & Differentiation:**
  1. **Zhao et al. (`arXiv:2602.10139`, Feb 2026) [47]** (*"Anonymization-Enhanced Privacy Protection for Mobile GUI Agents: Available but Invisible"*): Closest conceptual competitor. Well-differentiated and quantitatively beaten as B1 (`30/30` redirection leak vs. `0/30`).
  2. **Du et al. (`arXiv:2510.27140`, 2025) [19]**: Demonstrates the non-app-controlled Confused Deputy attack surface on mobile LLM agents; SecretHandle provides the OS-level capability defense.
  3. **CaMeL (SaTML '25) [16], FIDES (`arXiv:2505.23643`) [15], Progent (`arXiv:2504.11703`) [35], IsolateGPT (NDSS '25) [41], AirGapAgent (CCS '24) [9]**: Tool-API / planner-layer isolation; none handle raw pixel/accessibility observation and UI field injection on mobile OSes.
  4. **SchrodinText (USENIX Sec '20) [14], Rushmore (MobiSys '15) [8], GYRUS (NDSS '14) [25]**: Protect human-intended UI display/output rather than untrusted AI agents acting on secrets they must not see.
- **What a Hostile Reviewer Will Say ("X + Y" critique):** *"This is just Zhao et al.'s placeholder token [47] + Android package/field checks + an Accessibility overlay (`NotificationListener` + `TYPE_ACCESSIBILITY_OVERLAY`). Since the AOSP `system_server` integration is only on paper, the actual running system is a straightforward Android accessibility wrapper."*
  - **How to counter:** Emphasize the non-obvious systems insight—the coupling of **monotonic three-policy intersection** ($D_T \cap D_S \cap \text{TypePolicy}$), **atomic CAS reservation with bounded retry $k_{\max}$**, and **render-barrier-synchronized observation closure** across both visual and accessibility channels—and back it with real-app compatibility data!
- **Missing Related Work & 2026 Scooping / Concurrent-Work Risk (Verified via Web Search, Nov 23, 2026):**
  - **Aura** (*"Blind Gods and Broken Screens: Architecting a Secure, Intent-Centric Mobile Agent Operating System"*, `arXiv:2602.10915`, Feb 2026) — **HIGH PRIORITY TO CITE!** Proposes an intent-centric mobile OS for Android GUI agents; SecretHandle complements Aura by focusing specifically on opaque OS-minted secret capabilities and post-entry visual/tree observation closure.
  - **MATE** (Jang et al., EMNLP Findings Oct 2026 / `arXiv:2611.25526`, Nov 2026) — concurrent execution-boundary runtime guardrail + floating overlay for Android GUI agents on AndroidWorld & MobileSafetyBench (optional/concurrent, note if space permits).
  - **OS-Sentinel** (Sun et al., 2026) **[verify before citing]** & **MobileSafetyBench** (Lee et al., 2026) **[verify before citing]** — recent mobile GUI agent safety benchmarks/runtime guards.
  - **SUPOR** (Huang et al., USENIX Security 2015) and **UIPicker** (Nan et al., USENIX Security 2015) — foundational Android sensitive UI field detection, directly relevant to resolving field class $f$ when apps lack `autofillHints`.
  - **TrustUI** (Li et al., APSys 2014) and **TruZ-Droid** (Ying et al., MobiSys 2018) — MobiSys-community TrustZone trusted UI paths on Android.
  - **Name Collision Note:** The name `SecretHandle` is used in an unrelated open-source project (`nearai/ironclaw`, June 2026) and a Swift library (`boska/secret-memory`), neither of which is an academic Android GUI agent paper; no academic scooping risk from them.

---

## 15. Writing and Structure Audit (Phase 8)

- **Strengths:** Crisp, economical prose; strong 1.5-page Introduction; clean section balance fitting comfortably inside 12 pages (`~75%` of Page 12 right column used).
- **Structural Issues:**
  1. **Missing dedicated Implementation subsection:** Implementation details of `b3.apk` are scattered across two short paragraphs on p. 6 and p. 8 and Appendix A (p. 14), leaving reviewers guessing how OTP parsing, overlay tracking, and `InjectInternal` actually work on stock Android 14. Carve out a crisp ~0.4-page **§6.1 Stock-Android Prototype vs. Upstream AOSP** subsection.
  2. **Over-dense §7 paragraphs:** Section 7 packs 10+ distinct experiments into dense text walls without summary tables for (a) per-template T1–T5 results, (b) ARM vs. emulator microbenchmark breakdown, or (c) the real-app compatibility audit.
- **Page Budget (12-page limit):** Page 12 currently has ~15–18 lines of free space at the bottom of the right column. Additional ~20–25 lines can be reclaimed cleanly without touching margins by:
  - Compressing redundant prose between §4 (*Building blocks*, p. 6) and §6 (*Integration points*, p. 8) (~10 lines).
  - Condensing the 3 one-line proofs of Corollary 5.10, Proposition 5.12, and Proposition 5.13 into inline sentences (~8 lines).
  - Removing `\setlength{\textfloatsep}...` hacks while still easily staying $\le 12$ pages.
- **Representative Language / Typesetting Fixes:**
  1. P2 §2: Verify `Mobile agents act through the UI..` (possible double period).
  2. P8 Remark 5.16: `REMARK 5.16 (LEGITIMATE-BUT-UNW` / `ACTIONS).` $\rightarrow$ rename to `[In-scope misuse]`.
  3. P8 Alg. 2 Line 13: Fix scoping of `; wipe s` so multi-use handles aren't wiped while `u > 0`.
  4. P9 Fig. 2: Increase height to `3.2cm` for 100% zoom legibility.
  5. P10 §7 RQ5: Fix *"4 orders of magnitude"* $\rightarrow$ *"over two orders of magnitude ($\sim 187\times$)"*.
  6. P10 §7 (*Qualitative Analysis*): Fix Template 1 description (*"an incoming SMS prompts the agent"*) to match Table 5 (*"a promotional notification prompts the agent"*).
  7. P11 §7 (*Real-World Compatibility*): Replace unsubstantiated *"we audited 20 applications"* with concrete audited counts/table (or remove).
  8. P11 §7 (*Real-World Compatibility*): Clarify `30/30` WebView microbenchmark vs. `n=6` Template 3 end-to-end trials.
  9. P12 §9 (*Deployment*): Fix *"preventing handle MAC forgery even under root compromise"* $\rightarrow$ *"preventing offline key extraction"*.
  10. P12 §9 (*Limitations*): Reconcile *"unprivileged broker"* with §4/§6 *"privileged Binder service"*.

---

## 16. Three Simulated Reviews (Phase 9)

### Reviewer A — Systems Skeptic

- **Summary:** SecretHandle proposes an OS-level capability architecture to let Android GUI agents enter secrets (OTPs, credentials, clipboard values) without observing raw plaintext or being redirected by prompt injection. The authors formalize the state machine and evaluate a stock Android 14 prototype (`NotificationListener` + `TYPE_ACCESSIBILITY_OVERLAY`) using Mobile-Agent v3.5 and AutoDroid on an EC2 emulator, plus microbenchmarks on a Galaxy A52s.
- **Strengths:**
  - Timely mobile systems problem; Table 3 clearly shows why unbound placeholders (B1) break under redirection.
  - Clean policy intersection algebra and strong concurrency test (`50/50` barrier races).
  - Helpful Artifact Appendix with one-command offline checks.
- **Weaknesses:**
  1. **[Critical | Confidence: High] Unsubstantiated 20-app audit claim (§7, p. 11):** Claiming *"we audited 20 applications on Android 14"* without naming a single app, reporting what fraction had `smsOTPCode` hints vs. custom views, or separating that audit from a `47.60 us` synthetic vault benchmark (`30/30`) is unacceptable for a MobiSys evaluation.
  2. **[Critical | Confidence: High] Prototype-to-architecture gap and suspect hardware measurements (§4 p. 6, §7 p. 10–11, §9 p. 12):** The prototype is an installed APK (`b3.apk`) using `NotificationListenerService` and `TYPE_ACCESSIBILITY_OVERLAY`, yet the paper claims interception *"at the telephony boundary"* (p. 11), `mlock()`/`explicit_bzero` on a Java Dalvik service (p. 12), and `17.63 us` for TrustZone Keystore HMAC-SHA256 on a Snapdragon 778G (p. 10). Real Android `keystore2`/KeyMint TEE round-trips take hundreds of microseconds to milliseconds, not `17.63 us`. Also, `4.18 ms / 22.30 us` is `187x` (~2 orders), not *"4 orders of magnitude"*.
  3. **[Major | Confidence: High] Overclaimed AndroidWorld regression and weak energy methodology (Abstract, §7 RQ6 p. 10):** Claiming *"zero task regression across 10 AndroidWorld applications ($\Delta=0.00$)"* based solely on 50 touch pass-through taps and 2-app `gfxinfo`—with zero AndroidWorld agent task scores—is misleading. Energy (`< 0.12 mJ`) relies on `dumpsys batterystats` simulated unplug rather than hardware power measurement or unplugged discharge profiling.
- **Detailed Comments:** I appreciate the clean framing and the fact that you tested on stock Android 14, which is practically attractive. However, you must report what your stock APK *actually* does (exact Android APIs for OTP parsing, bubble tracking, and `InjectInternal`, plus its real trust boundary), verify the `17.63 us` TrustZone measurement, and replace vague 20-app/AndroidWorld claims with concrete, auditable tables.
- **Questions for Authors:**
  1. Please list the 20 audited Android apps and the exact fraction supporting `smsOTPCode` vs. requiring fallback.
  2. In `BenchmarkRunner`, did every iteration of the `17.63 us` ARM HMAC execute inside TrustZone (`KeyInfo.getSecurityLevel() == TRUSTED_ENVIRONMENT`), or did it use an in-memory software key?
  3. Which exact Android 14 API implements `InjectInternal(V, s)` and how is `mlock()`/`explicit_bzero` invoked from the Java `SecretHandleVaultService`?
- **Overall Recommendation:** **2 — Weak Reject**
- **Reviewer Expertise Confidence:** **4 — Expert**

---

### Reviewer B — Domain Expert (Mobile Security & AI Agents)

- **Summary:** The paper introduces SecretHandle, an Android capability-handle design enforcing destination confinement, single-use atomicity, and post-entry observation redaction against indirect prompt injection on mobile GUI agents. It includes a formal security model (§5), enforcement algorithms (§6), and an empirical evaluation against visual and accessibility-tree agents (§7).
- **Strengths:**
  - Formal separation of immutable MAC-authenticated metadata $H$ from mutable $(u, k)$ state is clean and handles multi-use lifecycles cleanly.
  - Fair, well-articulated comparison against unbound placeholders (B1) and Android's SMS User Consent vs. Credential Manager (B2).
  - Covers segmented 6-box OTPs, intra-app field redirection, and sensitive clipboard writes (`EXTRA_IS_SENSITIVE`).
- **Weaknesses:**
  1. **[Major | Confidence: High] Algorithm 2 Line 13 bug and root-compromise overclaim (§6 p. 8, §9 p. 12):** In Algorithm 2 Line 13, `; wipe s` executes even when `ok ∧ u > 0`, wiping multi-use secrets prematurely. Meanwhile §9 falsely claims StrongBox prevents handle MAC forgery *"even under root compromise"* (root can invoke the signing oracle online).
  2. **[Major | Confidence: High] Template 4 DoS Depletion vs. $U_{\text{att}}=1.00$ and Template 1 contradiction (§7 p. 10–11, App. B p. 15):** Table 3 reports $U_{\text{att}}=1.00$ across all 30 trials (including 6 trials of Template 4 DoS Depletion), yet p. 11 says $\ge 3$ mismatches revoke the handle and trigger local human touch confirmation. Did humans intervene in T4, or did T4 fail to trigger 3 retries? Furthermore, p. 10 says Template 1 uses an incoming SMS to prompt the agent, contradicting Table 5 (*cross-app promotion notification*).
  3. **[Major | Confidence: Medium-High] Detector-free claim vs. stock Android 14 prototype & missing 2026 related work (§2 p. 2–3, §8 p. 11–12):** On Android 14 (`API 34`), the `NotificationListener` and `TYPE_ACCESSIBILITY_OVERLAY` (Fig. 2b) still appear to rely on pattern detection to find OTPs/bubbles—weakening the *"detector-free"* distinction against Zhao et al. [47]. Also missing comparison to 2026 intent-centric Android agent OS work like Aura (`arXiv:2602.10915`) and classic Android sensitive-field detection (SUPOR, UIPicker).
- **Detailed Comments:** The security core of this paper is genuinely strong, and the revision fixed the earlier Line 5/Line 6 and audit-log confusion. Fixing the Line 13 pseudocode bug, adding a per-template T1–T5 table (with human-fallback counts), and tightening the detector-free / prototype claims would substantially raise my score.
- **Questions for Authors:**
  1. What are the per-template results (`E`, `R`, `U_att`, and number of human touch confirmations) for T1 through T5?
  2. How does the Android 14 prototype extract OTPs and locate Fig. 2(b) conversation bubbles without regex/heuristics, and how does it handle legitimate transaction context in the same SMS?
- **Overall Recommendation:** **3 — Borderline**
- **Reviewer Expertise Confidence:** **4 — Expert**

---

### Reviewer C — Generalist PC Member

- **Summary:** SecretHandle protects sensitive user inputs (especially OTPs) when mobile AI agents drive Android apps by substituting OS-minted opaque handles bound to the target app/field and masking the screen afterward. The paper evaluates Mobile-Agent v3.5 and AutoDroid on Android 14.
- **Strengths:**
  - Compelling motivation and readable first two pages; clearly relevant to MobiSys's audience.
  - Addresses both visual VLM agents and accessibility-tree agents, plus cross-device user viewing via `BiometricPrompt` (§9).
  - Clean 12-page structure with an open-source Artifact Appendix.
- **Weaknesses:**
  1. **[Major | Confidence: High] Unsubstantiated real-world compatibility and AndroidWorld claims (§1 p. 1, §7 p. 10–11):** The paper promises real-world generality (*"audited 20 applications"*, *"zero task regression across 10 AndroidWorld applications"*), but neither claim is backed by concrete per-app data or actual AndroidWorld task completion numbers.
  2. **[Minor | Confidence: High] Untested promised sources and presentation rough edges (Abstract, P8, P9):** Abstract and §4 emphasize Credential Manager, Wallet, and payment Protected Confirmation, none of which appear in §7. Page 8 has a clipped heading (`REMARK 5.16 (LEGITIMATE-BUT-UNW`), and Figure 2 screenshots are somewhat cramped.
- **Detailed Comments:** I like the problem and core story, and would be inclined to support the paper if the systems and security experts are satisfied with the real-app compatibility evidence and prototype honesty. Right now, however, I cannot defend the unsupported 20-app audit sentence in the PC meeting.
- **Questions for Authors:**
  1. Can you provide the concrete per-app results of the 20-app compatibility audit and actual AndroidWorld task completion rates (B0 vs. B3)?
  2. Have Credential Manager and payment confirmation been tested end-to-end, or should those be scoped as architectural extensions?
- **Overall Recommendation:** **3 — Borderline**
- **Reviewer Expertise Confidence:** **3 — Confident**

---

## 17. Self-Verification Notes (Phase 10)

1. **False-Positive Check:**
   - Re-checked the entire `.tex` source and 15-page PDF for any mention of the 20 audited apps (names, percentages, table): **Confirmed absent** (`0` app names, `0` counts anywhere in §1–§10 or Appendix A–B). W1 stands as **Critical**.
   - Re-checked `Algorithm 2 Line 13` in `.tex` line 329: `\textbf{if} $ok \land u>0$ \textbf{then} $z\gets\mathsf{live}$ \textbf{else if} $\neg ok \land u_0>1$ \textbf{then} $(z,u)\gets(\mathsf{live},u+1)$ \textbf{else} $z\gets\mathsf{consumed}$; wipe $s$` — **Confirmed** ambiguous/buggy scoping of `wipe s`.
   - Re-checked `"4 orders of magnitude"` in `.tex` line 403 vs. `$22.30\,\mu\text{s}$` and `$4.18\,\text{ms}$`: **Confirmed** ($4180/22.30 = 187.4\times$).
   - Re-checked `"unprivileged broker"` (`.tex` line 467) vs. `"privileged Binder service"` (`.tex` line 231, 336) and `"telephony boundary"` (`.tex` line 417): **Confirmed** direct self-contradictions.
   - Re-checked previous W4 (Baseline B2) and W5 (Claude 3.5 Sonnet, ARM latency/PSS/CPU sums): **Confirmed resolved** in this revision.
2. **Steelman (5-sentence case for acceptance):**
   *SecretHandle* tackles a high-impact, uniquely mobile systems vulnerability—secret disclosure and Confused Deputy redirection in GUI agents—that existing Android primitives (SMS User Consent, Autofill) and user-space placeholder anonymizers fail to solve. Its core design combines OS-source capability minting, monotonic three-policy destination intersection, atomic CAS single-use reservation, and render-barrier observation closure in a clean formal model with explicit assumptions. Unlike pure theory papers, the authors ship a working stock-Android 14 prototype and validate zero exposure and zero redirection across both visual (Claude 3.5 Sonnet Mobile-Agent v3.5) and structural (GPT-4o AutoDroid) agents, including segmented OTPs and sensitive clipboard sources. The measured overhead is negligible relative to VLM step times, and the Apache 2.0 artifact provides strong reproducibility. With minor clarifying edits during shepherding, this work offers a practical blueprint for securing mobile AI agents.
3. **Devil's Advocate (5-sentence case for rejection):**
   The paper claims an *"audit of 20 applications on Android 14"* without naming a single app or reporting a single compatibility percentage, while relying on 2 synthetic APKs for its entire security evaluation and mere touch pass-through tests to claim *"zero task regression across 10 AndroidWorld applications."* Its flagship narrative—an OS reference monitor intercepting at the telephony boundary with `mlock()`/`explicit_bzero` and detector-free source minting—directly contradicts its actual stock Android 14 Java APK (`NotificationListener` + `TYPE_ACCESSIBILITY_OVERLAY`). Key empirical numbers raise red flags, including an unexplained `17.63 us` TrustZone Keystore HMAC on Snapdragon 778G, a 2-orders-of-magnitude math error (`187x` called *"4 orders"*), and an unexplained `U_att=1.00` across Template 4 DoS Depletion despite handle revocation requiring human fallback. Furthermore, Algorithm 2 Line 13 contains a pseudocode bug that wipes multi-use secrets prematurely, and §9 incorrectly claims StrongBox prevents MAC forgery under root compromise. At MobiSys's selectivity bar, this combination of unsubstantiated evaluation claims and prototype-narrative mismatches warrants rejection.
4. **Changes After Verification:**
   - Downgraded previous W4 (B2 fairness) to **Resolved**.
   - Downgraded previous W2 from **Critical** to **Major** (typo & audit-log fixes succeeded, but T4 DoS / `U_att=1.00` and new Alg. 2 Line 13 bug remain).
   - Upgraded W3 to **Critical (W1)** because the revision inserted an unverified `"we audited 20 applications"` claim without data.
   - Confirmed scores (Rev A = 2, Rev B = 3, Rev C = 3; Overall = 2.5) strictly obey Ground Rule 7 (no overall score > 3 while Critical flaws remain).

---

## 18. Meta-Review and Forecast (Phase 11)

### Consolidation & Champion Test
- **Consensus Strengths:** Important mobile-systems security problem; strong killer experiment against unbound placeholders (B1); clean formal policy algebra; thorough artifact plan.
- **Consensus Weaknesses:** Unsubstantiated `"20 applications"` claim (W1); AOSP vs. stock Android 14 APK gap and self-contradictions (W2); AndroidWorld overclaim (W6).
- **Points of Disagreement:** Reviewer B sees strong security novelty if the T4 DoS breakdown and Line 13 bug are fixed; Reviewer A is skeptical of the systems realism (`b3.apk` vs. `system_server`, `17.63 us` TrustZone HMAC, `dumpsys batterystats` energy).
- **Champion Test:** **No reviewer would champion the manuscript in its current state.** Reviewer C's positive lean collapses as soon as Reviewer A points out the missing data behind `"we audited 20 applications"` and the `17.63 us` TrustZone / `4 orders` discrepancies. **However**, if W1–W3 are fixed before Dec 4, Reviewer B (4) and Reviewer C (4) have a clear basis to champion the paper into Conditional Accept with Shepherding.

### Outcome Forecast (Judgment, Not Statistics — MobiSys Base Rate ~15–20%)

| Submission State | Early Rejection | Advances to R2 $\rightarrow$ Reject | Conditional Accept (Shepherding) | Straight Accept |
| :--- | :---: | :---: | :---: | :---: |
| **Submitted as-is (Nov 23 state)** | 15–25% | **50–60% (Most Likely)** | 20–25% | <5% |
| **After completing MF-1 to MF-5 before Dec 4** | <10% | 30–40% | **45–55% (Most Likely)** | 5–10% |

### Rebuttal Readiness (500-Word Limit, Feb 8–12, 2027)

Likely reviewer questions and rebuttal feasibility:
1. *Where is the data for the 20-app audit?* $\rightarrow$ **Must be fixed BEFORE submission** (cannot rely on rebuttal for an already-claimed audit).
2. *How does `b3.apk` implement `InjectInternal`, OTP extraction, and `mlock()` on stock Android 14?* $\rightarrow$ Answerable in rebuttal, **far better fixed before submission**.
3. *Was `17.63 us` a real TrustZone KeyMint call?* $\rightarrow$ Needs 1-hour verification experiment (allowed in rebuttal, **fix now**).
4. *Per-template T1–T5 breakdown & T4 human fallback count?* $\rightarrow$ Answerable in 50 words from existing logs (**add now**).
5. *Actual AndroidWorld end-to-end task success (B0 vs. B3)?* $\rightarrow$ New experiment (allowed in rebuttal if requested, or scope claim honestly now).
6. *Comparison against Aura (`2602.10915`) and SUPOR/UIPicker?* $\rightarrow$ Answerable in rebuttal / camera-ready (**add now**).

**Top 3 Rebuttal Skeletons (500-word budget; fill `[placeholders]` with verified measurements only):**

1. **Prototype Architecture & TrustZone Measurement (for Reviewer A):**
   > *"We clarify our stock Android 14 prototype boundary: `b3.apk` runs with user-granted `NotificationListenerService` and `AccessibilityService` privileges while isolating the untrusted agent planner to a separate unprivileged UID mediating all screenshots and inputs via our SDK bridge. OTP extraction uses `[exact mechanism]`, `InjectInternal` uses `[exact API]` with bridge-level `TYPE_VIEW_TEXT_CHANGED` suppression, and Java vault buffers are zeroed via `[exact method]` (`mlock`/`explicit_bzero` applies to the upstream native AOSP design). For ARM HMAC, `17.63 us` reflects `[actual Keystore/session-key mechanism]`; a direct cross-process `AndroidKeyStore` TEE call measured `[X.XX ms]` (`KeyInfo` level `TRUSTED_ENVIRONMENT`), motivating our `[session-key / direct]` choice. We will add a Design-vs-Prototype table in §6."*
2. **Real-App Compatibility Audit (for Reviewers A & C):**
   > *"Our compatibility audit across `[20]` Google Play apps (banking, fintech, messaging, e-commerce on Galaxy A52s) found `[X/20]` expose standard `autofillHints`/`inputType` attributes matched directly by `Match(d,x)`, `[Y/20]` use custom views/numpads handled by our package+touch-confirmation fallback, and `[Z/20]` use WebViews rejected fail-closed. In end-to-end benign workflows across `[M]` real apps, SecretHandle achieved `[U]%` completion with `0` exposures. We will include the full per-app table in §7."*
3. **Template 4 DoS & Algorithm 2 Line 13 (for Reviewer B):**
   > *"Across T1–T5 ($n=6$ each), SecretHandle achieved `0/6` exposure and `0/6` redirection on every template; autonomous recovery succeeded in `[A/6]` (T1), `[B/6]` (T2), `[C/6]` (T3), `[D/6]` (T4, with `[F/6]` triggering local touch-confirmation fallback after $k=3$ mismatches), and `[E/6]` (T5). We will report this per-template breakdown in §7 and scope `wipe s` strictly inside the `consumed` branch of Algorithm 2 Line 13."*

### Shepherding Risk
If conditionally accepted, a MobiSys shepherd will very likely require: (1) adding the full 15–20 real-app compatibility table and/or end-to-end AndroidWorld task completion numbers; (2) verifying unplugged real-device power measurements on Galaxy A52s; (3) verifying the public GitHub artifact executes cleanly; and (4) scaling back any remaining AOSP/StrongBox overclaims in the Abstract and §9.

---

## 19. Revision Roadmap (Phase 12 — 11-Day Countdown: Nov 23 $\rightarrow$ Dec 4, 2026)

### A. Must-Fix Before Submission (Ordered by Impact / Effort)

| ID | Action (What to do) | Where | Effort | Risk if Skipped |
| :---: | :--- | :--- | :---: | :--- |
| **MF-1** | **Fix all immediate technical/math/pseudocode bugs (W3, W4, W5):** (a) Fix Alg. 2 Line 13 `wipe s` scoping; (b) fix `"4 orders of magnitude"` $\rightarrow$ `"over two orders of magnitude (~187x)"`; (c) fix §9 StrongBox root-compromise claim; (d) fix §7 p. 10 Template 1 vector to match Table 5; (e) fix Remark 5.16 heading overflow on P8; (f) clarify `30/30` WebView microbenchmark vs. `n=6` T3 trials. | §6 (p. 8), §7 (p. 10–11), §9 (p. 12) | **3 hours** | Instant credibility hit with security & systems reviewers. |
| **MF-2** | **Verify `17.63 us` TrustZone HMAC & `1.73 us` Binder IPC in `BenchmarkRunner.java` (W3):** Check `KeyInfo.getSecurityLevel()` on Galaxy A52s. If `17.63 us` was a software/session key, report honestly + measure real cross-process `AndroidKeyStore` TEE latency (`~ms`) to motivate ephemeral session-key caching. | §7 RQ5 (p. 10), Abstract | **0.5 day** | Hardware/TEE reviewer calls foul and pushes for Strong Reject. |
| **MF-3** | **Resolve the unsubstantiated `"audited 20 applications"` claim (W1):** Run `tools/audit_real_apps_compatibility.py` on **15–20 real Google Play apps** on Galaxy A52s (using your own test screens/login screens — no attacks on live apps!) and add a concrete summary table (`X/20` hints, `Y/20` custom views, `Z/20` WebView) + separate `47.60 us` synthetic fallback benchmark. *(Fallback: if impossible by Dec 1, delete the 20-app claim completely.)* | §7 (p. 11) + Table/App. C | **2–3 days** | **Critical desk/R2 reject** for unsupported experimental claim. |
| **MF-4** | **Align AOSP Design vs. Stock Android 14 Prototype honestly (W2):** Add a compact 4-row **Design vs. Prototype table** in §6 detailing exact stock Android 14 APIs (OTP extraction, bubble tracking, `InjectInternal`, Java buffer zeroing vs. upstream C++ `mlock`/`explicit_bzero`); fix `"telephony boundary"` (p. 11) and `"unprivileged broker"` (p. 12) contradictions; scope Abstract/§1 to clearly state which sources are prototyped (SMS/notification + clipboard) vs. architectural (Credential Manager/Wallet). | Abstract, §4 (p. 6), §6 (p. 8), §7 (p. 11), §9 (p. 12) | **1.5 days** | Reviewer A rejects for overclaiming prototype TCB invariants. |
| **MF-5** | **Report Per-Template T1–T5 Breakdown & Fix AndroidWorld Claim (W5, W6):** (a) Extract per-template `(E, R, U_att, human_fallback)` from `results/trials.jsonl` for T1–T5 (clarifying T4 DoS); (b) either run 10–20 end-to-end AndroidWorld agent tasks (B0 vs. B3) OR reword `"zero task regression across 10 AndroidWorld applications"` to `"zero touch-passthrough or frame-latency regression"`; (c) clarify emulator vs. physical A52s split in Abstract. | Abstract, §1, §7 (Table 3, RQ6), §10 | **1.5 days** | Reviewer A & B reject for misleading `U_att=1.00` and AndroidWorld overclaiming. |

### B. Should-Fix & Nice-to-Have
- **SF-1 (0.5 day):** Add missing 2026 related work (`Aura` `arXiv:2602.10915`, `SUPOR`, `UIPicker`, `TrustUI`/`TruZ-Droid`) in §8 and fix `@article{dennis1966semantics}`.
- **SF-2 (0.5 day):** Verify `https://github.com/SecretHandle/SecretHandle` is public and complete; add `allow_listener`/`enabled_accessibility_services` commands to Appendix A.
- **SF-3 (0.5 day):** Remove unnecessary preamble float-spacing hacks (`.tex` lines 83–88), enlarge Fig. 2 to `3.2cm`, verify Fig. 1 top diamond and P2 `UI..` in Adobe Acrobat, and expand `No Observation Redactor` ablation from `1/1` to `n=10`.
- **Nice-to-Have (1 day, if time allows):** Run a 15-minute unplugged battery current measurement on Galaxy A52s over Wi-Fi ADB (fixed brightness) to replace software-only `dumpsys batterystats` simulated unplug.

### C. Concrete Rewrite Suggestions (Preserving Verified Facts Only)
- **Abstract (last 3 sentences, fixing prototype/emulator/AndroidWorld scope):**
  > *"We implement a stock Android 14 broker prototype covering SMS/notification OTPs and sensitive clipboard handles, and evaluate it against Claude 3.5 Sonnet-driven Mobile-Agent v3.5 and GPT-4o-driven AutoDroid across OTP forwarding, cross-app and intra-app Confused Deputy redirection, replay, and concurrency attacks under KVM emulation, alongside hardware microbenchmarks on a physical Samsung Galaxy A52s. \SH{} eliminates secret exposure ($0/30$, Wilson $[0.00, 0.11]$) versus $0.97$ unprotected ($29/30$), blocks unauthorized destination redirection ($0/30$ vs. $30/30$ for unbound placeholders and SMS consent flows), guarantees atomic single-use serialization ($50/50$ races), incurs microsecond vault transitions ($5.42\,\mu\text{s}$ mint, $0.18\,\mu\text{s}$ resolve; $4.18\,\text{ms}$ end-to-end UI dispatch), and introduces zero touch-passthrough or rendering-latency regression across 10 AndroidWorld applications (`50/50` events, $\Delta\text{p95}=0.0\,\text{ms}$)."*
- **Introduction Contribution (iv) (p. 2):**
  > *"(iv) a stock Android 14 prototype realizing notification/clipboard brokering, accessibility overlay redaction, and atomic vault resolution without custom ROM modifications, together with a clear mapping to upstream AOSP integration;"*

### D. Day-by-Day Timeline (Nov 23 $\rightarrow$ Dec 4, 2026)
- **Nov 23 (Mon) — Day 1:** Complete **MF-1** (all math/pseudocode/StrongBox/Template 1/Remark 5.16 fixes) + **MF-2** (audit `BenchmarkRunner.java` & verify ARM TrustZone HMAC + Binder IPC).
- **Nov 24–26 (Tue–Thu) — Days 2–4:** Execute **MF-3** (run `audit_real_apps_compatibility.py` on 15–20 real Google Play apps on Galaxy A52s and build the compatibility table) + **MF-4** (write Design vs. Prototype mapping table in §6 and clean all overclaims).
- **Nov 27 (Fri) — ABSTRACT REGISTRATION DEADLINE (23:59 AoE):** Finalize the cleaned Abstract (using exact scope wording), verify author list (`Nguyễn Tiến Thuận`, `Trần Phát Tài`), declare COIs, and register on `https://mobisys27.hotcrp.com/` **at least 6 hours early**.
- **Nov 28–30 (Sat–Mon) — Days 6–8:** Complete **MF-5** (per-template T1–T5 breakdown + AndroidWorld honest scope or end-to-end runs) + **Nice-to-Have** unplugged Galaxy A52s power measurement & `n=10` redactor ablation.
- **Dec 1–2 (Tue–Wed) — Days 9–10:** Complete **SF-1, SF-2, SF-3** (Aura/SUPOR/UIPicker/TruZ-Droid citations, GitHub repo live test, Appendix A `adb` setup commands, remove preamble float hacks, enlarge Fig. 2, verify $\le 12$ pages).
- **Dec 3 (Thu) — Day 11:** Full end-to-end proofread in Adobe Acrobat at 100% zoom, run `pdfinfo`/`pdffonts`, upload draft to HotCRP format checker, and resolve any warnings.
- **Dec 4 (Fri) — FULL PAPER SUBMISSION DEADLINE (23:59 AoE):** Submit final PDF at least 6–12 hours before deadline.

### E. Venue / Track Fit Check
**Stay on the Regular Full Paper track for ACM MobiSys 2027** — the topic, formal model, dual-agent evaluation, and real ARM device benchmarking fit MobiSys very well, and all five Must-Fix items are genuinely doable in 11 days. Only consider switching to the **`[Emerging Ideas]`** track if you cannot complete the 15–20 real-app compatibility audit (MF-3) AND discover that your `17.63 us` ARM TrustZone benchmark requires major re-engineering.

---

## 20. Open Items (Author Must Double-Check)

1. **`evidence_logs.rar` verification:** Because RAR extraction was unavailable here, manually cross-check every number in Section 7 against the JSON files in `evidence_logs.rar`, especially `physical_device_benchmark.json` (`17.63 us` HMAC, `1.73 us` Binder), `fallback_policy_benchmark.json` (`47.60 us`), and `webview_failclosed_benchmark.json` (`56.80 us`).
2. **Real `AndroidKeyStore` Security Level:** Confirm in `BenchmarkRunner.java` whether `KeyInfo.getSecurityLevel()` actually ran inside TrustZone TEE on every iteration of the `17.63 us` benchmark.
3. **Public GitHub Repo (`https://github.com/SecretHandle/SecretHandle`):** Verify it is publicly accessible without authentication and matches all Appendix A paths/commands.
4. **Template 4 (`DoS Depletion`) Logs:** Inspect `results/trials.jsonl` for the 6 trials of Template 4 to verify how many triggered $k=3$ revocation and local touch-confirmation fallback.
5. **Visual PDF Check in Adobe Acrobat:** Confirm Page 4 Figure 1 top diamond (`Injected content`) is not clipped and Page 2 §2 heading does not print a double period (`UI..`).
6. **HotCRP Official Check:** Re-verify COI rules, ACM Open eligibility for FPT University, and HotCRP automated format validation before Dec 4, 2026 23:59 AoE.

---

## 21. Bản dịch tiếng Việt: Phán quyết Điều hành & Danh sách Bắt buộc sửa

### Phán quyết Điều hành (Executive Verdict)
- **Khuyến nghị tổng thể:** **2.5 / 5 (Weak Reject / Borderline)** nếu nộp nguyên trạng hôm nay (23/11/2026 — còn **4 ngày** tới hạn đăng ký Abstract 27/11 và **11 ngày** tới hạn nộp bài 04/12); có thể đạt **4.0 / 5 (Weak Accept)** nếu xử lý dứt điểm 5 mục Bắt buộc sửa (MF-1 đến MF-5).
- **Dự báo kết quả:** Nếu nộp nguyên trạng: **15–25% Từ chối sớm / 50–60% Vào Vòng 2 rồi Từ chối / 20–25% Chấp nhận có điều kiện (Shepherding) / <5% Chấp nhận thẳng**. Sau khi sửa hết MF-1–MF-5: xác suất **Conditional Accept** tăng lên **45–55%**.
- **Tiến bộ lớn so với bản ngày 29/10:** Đã sửa sạch lỗi `Claude 3.5 Sonnet`, cộng đúng độ trễ ARM (`22.30 us`), bộ nhớ PSS (`28.7 MB`), CPU (`7.2%`), sửa dấu `Nguyễn and Trần`, tách rõ audit log nội bộ vs. phản hồi ẩn trạng thái, định vị lại công bằng Baseline B2 và nâng độ phân giải Hình 2.
- **3 vấn đề Nghiêm trọng/Lớn còn chặn cửa Accept:**
  1. **[Critical]** Mục 7 (tr. 11) viết *"we audited 20 applications on Android 14"* nhưng không liệt kê tên ứng dụng hay tỷ lệ hỗ trợ nào, trong khi chính `revision_checklist.md` ghi khảo sát 15–20 app thật **chưa hoàn thành** — cực kỳ nguy hiểm về uy tín khoa học nếu nộp nguyên văn!
  2. **[Critical]** Còn tự mâu thuẫn giữa kiến trúc AOSP và nguyên mẫu APK Android 14 (`"privileged Binder service"` ở tr. 6/8 vs. `"unprivileged broker"` ở tr. 12; `"telephony boundary"` ở tr. 11 cho `NotificationListener`; `mlock()`/`explicit_bzero` cho dịch vụ Java; và số đo `17.63 us` cho TrustZone Keystore HMAC trên Snapdragon 778G nhanh bất thường cần kiểm chứng ngay).
  3. **[Major]** Lỗi pseudocode Thuật toán 2 Dòng 13 (`wipe s` xóa luôn bí mật của handle đa dụng khi `u > 0`), lỗi tính toán *"4 orders of magnitude"* ở tr. 10 (thực tế $4.18\,\text{ms}/22.30\,\mu\text{s} = 187.4\times \approx 2$ bậc độ lớn), thiếu bảng phân rã từng mẫu tấn công T1–T5 (đặc biệt T4 DoS làm sao đạt $U_{\text{att}}=1.00$), và tuyên bố quá mức *"zero task regression across 10 AndroidWorld applications"* khi mới chỉ đo chạm xuyên lớp phủ (`50/50`) và `gfxinfo` trên 2 app.

### Danh sách 5 việc BẮT BUỘC SỬA trước 04/12/2026 (Ưu tiên theo tác động)
1. **MF-1 (3 giờ — làm ngay hôm nay 23/11):** Sửa lỗi `wipe s` ở Thuật toán 2 Dòng 13; sửa *"4 orders of magnitude"* $\rightarrow$ *"over two orders of magnitude ($\sim 187\times$)"*; sửa câu StrongBox chống giả mạo MAC dưới quyền root (tr. 12); sửa mô tả Template 1 ở tr. 10 cho khớp Bảng 5; rút gọn tiêu đề `Remark 5.16` (tr. 8) để hết tràn chữ; làm rõ `30/30` WebView là microbenchmark riêng với `n=6` của Template 3.
2. **MF-2 (0.5 ngày — 23/11):** Kiểm tra ngay `BenchmarkRunner.java` trên Galaxy A52s xem `17.63 us` HMAC có thực sự chạy qua `AndroidKeyStore` TEE (`KeyInfo.getSecurityLevel()`) ở mỗi lần gọi hay là khóa phiên trong bộ nhớ; báo cáo trung thực và đo thêm 1 mốc gọi TEE xuyên tiến trình nếu dùng khóa phiên.
3. **MF-3 (2–3 ngày — 24–26/11):** Chạy thật `audit_real_apps_compatibility.py` trên **15–20 ứng dụng Google Play thực tế** trên Galaxy A52s (chỉ chụp cây UI màn hình đăng nhập, không tấn công app thật) để đưa bảng thống kê `X/20` cụ thể vào bài — **hoặc nếu không kịp trước 01/12 thì xóa bỏ ngay câu `"we audited 20 applications"`**.
4. **MF-4 (1.5 ngày — 25–26/11):** Thêm bảng 4 dòng **Upstream AOSP Design vs. Stock Android 14 Prototype** trong Mục 6 (ghi rõ API thực tế cho trích xuất OTP, vẽ overlay, `InjectInternal`, xóa bộ nhớ Java); xóa các câu tự mâu thuẫn (`telephony boundary`, `unprivileged broker`); nêu rõ trong Abstract nguồn nào đã cài thực tế (SMS/notification + clipboard) và nguồn nào ở mức kiến trúc (Credential Manager/Wallet).
5. **MF-5 (1.5 ngày — 28–30/11):** Thêm bảng phân rã kết quả theo 5 mẫu tấn công T1–T5 (ghi rõ số ca cần xác nhận chạm người dùng ở T4); chạy bổ sung 10–20 task AndroidWorld end-to-end **hoặc** sửa tuyên bố thành *"zero touch-passthrough or frame-latency regression across 10 AndroidWorld applications"*; bổ sung trích dẫn `Aura (arXiv:2602.10915)`, `SUPOR`, `UIPicker`, `TruZ-Droid` và kiểm tra link GitHub mở công khai trước khi nộp.