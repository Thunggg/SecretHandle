# ACM MobiSys 2027 Mode B Re-Review (Round 3): `SecretHandle`

## 1. Header and Review Metadata

- **Paper Title:** *SecretHandle: OS-Minted, Destination- and Task-Bound Opaque Secrets for Android Mobile AI Agents*
- **Authors:** Nguyễn Tiến Thuận, Trần Phát Tài (FPT University, Can Tho, Vietnam) — single-blind submission
- **Review Date:** November 23, 2026
  - **Days remaining to Abstract Registration (Nov 27, 2026 23:59 AoE):** **4 days**
  - **Days remaining to Full Paper Submission (Dec 4, 2026 23:59 AoE):** **11 days**
- **Mode:** **Mode B (Re-review of a revised version)** comparing the newly revised `SecretHandle_MobiSys2027.pdf` (17 pages), `manuscript_full_source.tex`, `evidence_logs_all.json`, and `references_verified.bib` against `previous_review_mobisys2027.md` (Round 2) and `revision_checklist.md`, following `mobisys2027_review_prompt.md`.
- **Track / Stance:** Regular Full Paper; balanced, calibrated ACM MobiSys TPC standard.
- **Assumptions Made (Phase 0 bypassed per user instruction):** Regular track submission; no prior publication or concurrent submission elsewhere; synthetic canaries and read-only static UI dumps only (no human subjects).
- **Review Limitations:**
  1. **No live web fetch:** `https://github.com/SecretHandle/SecretHandle` was not accessed online, so public repository availability and runnable code execution remain unverified.
  2. **Decommissioned EC2 visual logs:** As now transparently documented in Appendix A (p. 15), raw JSON logs for the 11 on-device/emulator benchmark blocks reside in `evidence_logs_all.json`, while aggregate metrics from the decommissioned EC2 visual-agent run (`Mobile-Agent v3.5` `29/30` / `48.6 s`, B1 `150 ms`, OS UI dispatch `4.18 ms`, PSS `28.7 MB`, `batterystats` $< 0.12\text{ mJ}$) cannot be independently recomputed from raw trial traces here.

---

## 2. Executive Verdict

- **Overall Recommendation:** **4.0 / 5 (Weak Accept — Submission-Ready for ACM MobiSys 2027; upgraded from 2.5 / 5 in Round 1 and 3.5 / 5 in Round 2).**
- **Outcome Forecast:** Early Rejection: **$< 5\%$** | Advances to R2 then Reject: **25–35%** | **Conditional Accept with Shepherding: 50–60% (Most Likely)** | Straight Accept: **10–15%**.
- **Top 3 Strengths:**
  1. **100% closure of all prior Critical and Major log-vs-text discrepancies:** Every item in RMF-1 through RMF-4 was executed cleanly—re-capturing `Gmail` (`identifierId` in GMS WebView) and `GitHub` (`login_field`/`password` in OAuth Custom Tab), separating `5/20` (`25.0%`) WebView Fail-Closed apps consistently across Table 6, Table 8, and JSON, fixing `Grab`'s misclassification, transparently disclosing RQ6's `2/10` suppressed heuristic checks (`overlay_detected=false`), `Clock`'s 0-frame sentinel, and `Settings`'s `p99` ($38.0 \rightarrow 101.0\text{ ms}$), annotating T4 DoS human fallback in Table 4, and disclosing archived vs. aggregate EC2 logs in Appendix A.
  2. **Strong mobile-systems rigor and honesty:** Real Galaxy A52s `AndroidKeyStore` TEE benchmarking (`1.79 ms` `doFinal` / `5.74 ms` `init+doFinal` vs. $2.45\,\mu\text{s}$ cached `SecretKeySpec`), Table 3 cleanly contrasting Upstream AOSP vs. Stock Android 14 (`b3secrethandle.apk`), $n=10$ physical redactor ablation (`99.16%` coverage), and 15-min unplugged Wi-Fi ADB power run with candid quantization and thermal caveats.
  3. **Immaculate CFP format compliance:** Stock `acmart v2.20` layout (zero negative `\vspace`, zero float-spacing overrides), body text ends cleanly on Page 12 right column (~64% of right column still free), zero text overflows or clipping, and `52/52` BibTeX entries cited with zero unused or undefined references.
- **Remaining Residual / Minor Problems (Zero Critical flaws; zero newly introduced Major flaws):**
  1. **[Major — inherent/structural, not fixable before Dec 4 without new engineering]:** End-to-end visual/tree security trials ($n=30$) remain on 2 synthetic APKs under KVM emulation (with raw EC2 trial traces decommissioned and no per-template T1–T5 counts), Credential Manager/Wallet remain architectural-only, and RQ6 measures touch-passthrough plus 2-app `gfxinfo` rather than end-to-end AndroidWorld task completion rates.
  2. **[Minor — 2-minute LaTeX fix]:** Appendix C's 3-line intro sits alone on an almost empty **Page 16** while Table 8 floats onto **Page 17** because `\clearpage` and `\begin{table*}[t]` were placed *before* `\section{Real-App UI Compatibility Audit}`.
  3. **[Minor — 3-minute wording/JSON polish]:** Abstract (p. 1) and Conclusion (p. 12) state *"zero touch-passthrough or measured frame-latency regression"* ($\Delta\text{p95} = 0.0\text{ ms}$), whereas Section 7 RQ6 (p. 10) honestly reports `Settings p99` ($38.0 \rightarrow 101.0\text{ ms}$, `jank` $2.30\% \rightarrow 3.66\%$)—inserting *"median/p95"* makes the Abstract and Conclusion 100% airtight.
- **Single Most Important Thing to Fix Before Submission:** Fix the **Page 16 orphan Appendix C layout** (move `\section{Real-App UI Compatibility Audit}` above Table 8), tighten Abstract and Conclusion to *"measured median/p95 frame-latency regression"*, verify the public GitHub repository live in an incognito window, and **register the Abstract on HotCRP by Nov 27, 2026 23:59 AoE (4 days)**.

---

## 3. Mode B Delta Table (Round 2 Review $\rightarrow$ Revised Draft Nov 23, 2026 v3)

| Previous Issue (`previous_review_mobisys2027.md`) | Prev. Severity | Current Status | Evidence in Revised Manuscript (`SecretHandle_MobiSys2027.pdf` / `.tex` / `evidence_logs_all.json`) |
| :--- | :---: | :---: | :--- |
| **RMF-1:** 20-app audit WebView contradiction (`CocCoc`, `SoundCloud`, `Binance`), `Grab` `password` mislabeling, `Gmail` lock-screen & `GitHub` URL captures, `0/20` OTP disclosure | **Major** | **Resolved** | `Gmail` re-captured on GMS Sign-In WebView (`identifierId`, `21:36:28`) and `GitHub` on OAuth Custom Tab (`login_field`/`password`, `21:37:43`). All 5 WebView apps classified `WEBVIEW_FAIL_CLOSED` (`5/20 = 25.0%`); `Grab` fixed to `STANDARD_INPUT_FALLBACK` (`9/20 = 45.0%`); `Lazada` stray `TextView` removed; `Direct Match` = `6/20 = 30.0%`. Explicit `0/20` post-login `smsOTPCode` disclosure in Section 7, App. C, and JSON `audit_scope_note`. Exact match across Section 7, Table 6, Table 8, and JSON. *(Tiny note: `revision_checklist.md` item 4.3 still has a stale `7/20, 10/20, 3/20` typo, but the paper and JSON are 100% exact at `6/20, 9/20, 5/20`.)* |
| **RMF-2:** `rq6_benign_regression_results.json` vs. Section 7 RQ6 discrepancies (`SMS_Benign`/`Contacts` `FALSE_POSITIVE`, `Clock` 0-frame `4950 ms`, `Settings` `p99` $38 \rightarrow 101\text{ ms}$) | **Major** | **Resolved** | Section 7 RQ6 (p. 10) now explicitly reports `0/10` visible false-positive overlays, discloses the 1 suppressed heuristic check (`overlay_detected=false`) on `SMS_Benign` and `Contacts`, reports full `Markor` ($\text{p95}=18.0\text{ ms}$, $\text{p99}: 27.0 \rightarrow 31.0\text{ ms}$, jank `3.70%`) and `Settings` ($\text{p95}=36.0\text{ ms}$, $\text{p99}: 38.0 \rightarrow 101.0\text{ ms}$, jank $2.30\% \rightarrow 3.66\%$) tails, and explains `Clock` (`0` B3 frames, `4950 ms` sentinel excluded). JSON `summary` adds matching explanatory fields verbatim. |
| **RMF-3:** T4 DoS human-fallback disclosure in Table 4's $U_{\text{att}} = 1.00$ and unarchived EC2 log disclosure in App. A | **Major** | **Resolved** | Table 4 (p. 8) adds footnote $^\S$ (*"Includes local single-tap user touch confirmation on Template 4 DoS trials ($n=6$ of 30) after exceeding $k_{\max}=3$"*), mirrored in Section 7 (p. 10). Appendix A (p. 15) explicitly enumerates all archived `output/*.json` logs vs. aggregate metrics from decommissioned EC2 runs. |
| **RMF-4:** Standardize `b3.apk` $\rightarrow$ `b3secrethandle.apk`, 15-min battery caveats, Table 6 summary, GitHub check | **Minor** | **Resolved** *(GitHub & HotCRP pending)* | `b3.apk` count in `.tex` is now **0** (`b3secrethandle.apk` appears consistently throughout); 15-min battery caveats (screen-on $\sim 950\text{ mW}$, `4.5 mAh` quantization, $36.8 \rightarrow 34.8^\circ\text{C}$ cooling) added in Section 7 RQ6 (p. 10); compact Table 6 (`tab:compat_summary`) added cleanly in Section 7 (p. 11). **New Minor layout nit:** Appendix C text sits alone on P16 with Table 8 pushed to P17. |

---

## 4. Re-Verified Format and Compliance Checklist (Phase 1 — Programmatically Measured)

| Item | CFP Requirement | Measured / Observed Value | Status | Method | Evidence |
| :--- | :--- | :--- | :---: | :---: | :--- |
| File format and page size | PDF only, US Letter ($612 \times 792\text{ pt}$) | PDF 1.7, $612 \times 792\text{ pts}$ (letter), 17 pages, XeTeX `0.999997` | **OK** | **Measured** (`pdfinfo`) | P1–P17 |
| Embedded fonts | All fonts embedded | All 10 CID Type 0C / Type 1C fonts: `emb=yes, sub=yes, uni=yes` | **OK** | **Measured** (`pdffonts`) | P1–P17 |
| Page numbers | Visible on every page (`printfolios=true`) | Centered bottom page numbers `1`–`17` (`y=74.7 pt`) on all pages | **OK** | **Measured** (`pdfminer`) | P1–P17; `.tex` line 77 |
| Main content $\le 12$ pages | $\le 12$ numbered pages incl. figs/tables; refs and appendix unlimited | Main content (Sections 1–10) ends on **P12 right column** (`y=478.7 pt`, ~36% of right col used; **~64% of right col spare**). `\clearpage` $\rightarrow$ Refs P13–P14; App. A–C P14–P17 | **OK** | **Measured** (`pdfminer` + `.tex`) | P12 (Sec. 10), P13–P14 (Refs), P14–P17 (App. A–C) |
| Essential content in appendix | Reviewers not obliged to read appendix | Compact Table 6 (20-app summary) is now inside Section 7 (p. 11); App. B (Table 7) and App. C (Table 8) cleanly serve as detailed reference tables | **OK** | **Estimated** | P11, P15–P17 |
| Body font size | $\ge 10\text{ pt}$ (`sigconf,10pt`) | Body text measured at `9.96 pt` (`41,025` chars; exact LaTeX `10pt` in PDF bp) | **OK** | **Measured** (`pdfminer` + `.tex`) | P1–P12; `.tex` line 4 |
| Column geometry and lines/col | 2 cols, $\sim 9.25 \times 3.33\text{ in}$, $\sim 0.33\text{ in}$ gutter, $\le 55$ lines/col | Stock `acmart v2.20`: $8.61\text{--}8.65\text{ in}$ tall $\times$ $3.36\text{--}3.39\text{ in}$ wide, $0.29\text{--}0.30\text{ in}$ gutter; **31–51 unique lines/col** across P1–P12 (all $\le 55$; stock 8pt refs P13–P14: 56–62 lines) | **OK** | **Measured** (`pdfminer`) | P1–P12 |
| Template-tampering screen | No negative `\vspace`, shrunken margins, or float squeezing | **0** negative `\vspace`, **0** `\textfloatsep`/`\floatsep`/`\intextsep`/`\abovecaptionskip`/`\belowcaptionskip` overrides; 100% stock `acmart` | **OK** | **Measured** (`.tex` audit) | `.tex` lines 77–84 |
| Cross-references and math | Zero undefined refs, accurate line/table numbers | **0** undefined `\ref`/`\eqref`; all `Table 1`–`Table 8`, `Algorithm 1`–`2`, and `Line 6`, `Line 7`, `Line 13` verified exact across `.tex` and PDF | **OK** | **Measured** (`.tex` + PDF scan) | Full document |
| Legibility, overflow, and graphics | Readable at 100% zoom, zero clipping/overflow | Zero body text overflows on P1–P12; Fig. 2 `3.2 cm` at `1310–1439 ppi`; **cosmetic WARN:** P16 has only 3 lines (App. C intro) with Table 8 pushed to P17 | **OK (Minor P16 nit)** | **Measured** (`pdfminer`, `pdfimages`) | P4, P9, P10, P16–P17 |
| Front matter, Single-blind, and LLM policy | Names/affiliations/contacts, abstract $\ge 100$ words, LLM disclosure, no hidden text | Both authors and emails present; Abstract $\approx 252$ words; Section 9 proofreading disclosure present; **0** white (`#FFFFFF`) or tiny ($< 4.5\text{ pt}$) text spans across all 17 pages | **OK** | **Measured** (`pdfminer` scan) | P1, P12, full PDF |
| BibTeX and Artifact URL | Clean references; live public repo | **52/52** BibTeX entries cited, **0** unused, **0** missing, `@article{dennis1966semantics}` valid; GitHub URL **Not verified** | **Not verified** | **Measured** (`.bib`) / **Not verifiable** (URL) | P13–P15 |

**Compliance Verdict:** **PASS** on all measurable CFP rules (run HotCRP's built-in format checker upon upload and verify the public GitHub repository).

---

## 5. Full Numerical and Log Audit Against `evidence_logs_all.json`

All **11 JSON benchmark blocks** in `evidence_logs_all.json` were re-verified programmatically against `manuscript_full_source.tex` and `SecretHandle_MobiSys2027.pdf`:

| Benchmark Block / Claim | Paper Location | `evidence_logs_all.json` Value | Audit Verdict |
| :--- | :--- | :--- | :---: |
| **20-App Audit (Updated):** `6/20` (`30.0%`) Direct Match; `9/20` (`45.0%`) Pkg+Class + Touch Gate; `5/20` (`25.0%`) WebView Fail-Closed; `0/20` post-login `smsOTPCode` `EditText` | Section 7 (p. 11), Table 6 (p. 11), App. C Table 8 (p. 16–17) | `DIRECT_COMPATIBLE: 6` (`MoMo`, `Shopee`, `Messenger`, `Knowt`, `Lazada`, `Discord`); `STANDARD_INPUT_FALLBACK: 9` (`Home Credit`, `Teams`, `TikTok`, `Telegram`, `WhatsApp`, `OKX`, `Grab`, `PayPal`, `Bitwarden`); `WEBVIEW_FAIL_CLOSED: 5` (`SoundCloud`, `CocCoc`, `Binance`, `Gmail`, `GitHub`); `audit_scope_note` matches verbatim | **EXACT MATCH** |
| **RQ6 Benign Regression (Updated):** `50/50` touch (`0.0%` block); `0/10` visible false-positive overlays (`SMS_Benign` & `Contacts` 1 suppressed check, `overlay_detected=false`); Markor $\text{p95}=18.0\text{ ms}$, $\text{p99}: 27.0 \rightarrow 31.0\text{ ms}$, jank `3.70%`; Settings $\text{p95}=36.0\text{ ms}$, $\text{p99}: 38.0 \rightarrow 101.0\text{ ms}$, jank $2.30\% \rightarrow 3.66\%$; Clock `0` B3 frames / `4950 ms` sentinel excluded | Section 7 RQ6 (p. 10) | Exact match to `false_positive_audit`, `touch_transparency`, `gfxinfo_comparison`, and updated `summary` keys (`visible_overlay_false_positive_rate: 0.0`, `internal_heuristic_trigger_count: 2`, `settings_p99_delta_ms: 63.0`, `markor_p99_delta_ms: 4.0`, `excluded_zero_frame_app`) | **EXACT MATCH** |
| **AutoDroid ($n=30$), Emulator & ARM A52s Overhead ($n=100$), TEE ($n=100$/$1000$), Lifecycle ($n=50$), Redirection ($n=30$), Segmented OTP ($n=30$), Clipboard ($n=30$), Fallback ($n=30$), WebView ($n=30$), 15-min Battery, Redactor Ablation ($n=10$)** | Section 7 (p. 8–11) | Unchanged and 100% matched verbatim across every mean, median, p95, count, and Wilson CI | **EXACT MATCH** |
| **Decommissioned EC2 Visual-Agent Metrics** (`Mobile-Agent v3.5` `29/30` / `48.6 s`, B1 `150 ms`, OS UI dispatch `4.18 ms`, PSS `28.7 MB`, `batterystats` $< 0.12\text{ mJ}$) | Section 7 (p. 8–10), App. A (p. 15) | Explicitly disclosed in App. A as aggregate metrics from decommissioned EC2 runs (not expected in `output/*.json`) | **TRANSPARENTLY SCOPED** |

---

## 6. Updated Dimension Scores, Simulated Reviews, and Forecast

### Dimension Scores Progression (Round 1 $\rightarrow$ Round 2 $\rightarrow$ Round 3)

| Dimension | R1 | R2 | **R3 (Current)** | One-Line Justification |
| :--- | :---: | :---: | :---: | :--- |
| 1. Scope and relevance to mobile systems | 5.0 | 5.0 | **5.0 / 5** | Core Android OS capability and mobile GUI agent security contribution. |
| 2. Novelty and insight | 3.5 | 4.0 | **4.0 / 5** | Clear differentiation vs. Zhao et al. `[51]`, Aura `[52]`, SUPOR/UIPicker `[25, 33]`, and TruZ-Droid `[47]`. |
| 3. Significance and potential impact | 4.0 | 4.0 | **4.0 / 5** | High-impact OS blueprint for untrusted mobile AI agents. |
| 4. Technical soundness and depth | 3.0 | 4.0 | **4.5 / 5** | Policy algebra, Alg. 1–2, TEE session-key rationale, and WebView fail-closed consistency are completely aligned. |
| 5. Implementation realism | 2.0 | 3.5 | **3.5 / 5** | Transparent Table 3 AOSP-vs-stock mapping and real Galaxy A52s hardware/app tests; residual limit is stock APK rather than AOSP ROM. |
| 6. Evaluation rigor | 2.0 | 3.0 | **4.0 / 5** | Clean 20-app audit (`6/9/5`), full RQ6 `p95/p99/jank` transparency, TEE, $n=10$ redactor ablation, 15-min battery; residual limit is synthetic-APK VLM runs and no end-to-end AndroidWorld task SR. |
| 7. Reproducibility and artifact readiness | 3.5 | 4.0 | **4.5 / 5** | App. A clearly documents every archived JSON vs. aggregate EC2 metric and exact ADB commands; just confirm public GitHub URL. |
| 8. Presentation and clarity | 3.5 | 4.5 | **4.5 / 5** | Clean 12-page stock `acmart` layout with crisp Table 3 and Table 6; fix minor P16 Appendix C orphan page. |
| 9. Ethics, privacy, safety | 4.5 | 4.5 | **4.5 / 5** | Synthetic canaries, read-only static UI dumps (`0/20` live account logins), clean LLM proofreading disclosure. |
| 10. Honest limitations and discussion | 3.5 | 4.0 | **4.5 / 5** | Exemplary candor on regex/200 ms overlay race, T4 human fallback, RQ6 `p99`/suppressed checks, battery quantization, and `0/20` post-login OTP scope. |

### Updated Simulated Reviews and Meta-Review

- **Reviewer A (Systems Skeptic): `3.5` $\rightarrow$ `4 (Weak Accept)` (Confidence: 4)** — *Every artifact-vs-text contradiction is gone. Reporting `Settings p99` ($38 \rightarrow 101\text{ ms}$), `Clock`'s 0-frame sentinel, and the 2 suppressed heuristic checks honestly instead of burying them earns real systems trust. Residual limitations (synthetic APKs on KVM for end-to-end VLM runs and no AndroidWorld end-to-end task SR) are honestly scoped and appropriate for conditional acceptance/shepherding.*
- **Reviewer B (Mobile Security and AI Agents Expert): `4` $\rightarrow$ `4 (Weak Accept)` (Confidence: 4)** — *Re-capturing `Gmail` and `GitHub` cleanly as WebView Fail-Closed (`5/20 = 25%`) and fixing `Grab` resolves the WebView self-contradiction completely; Table 4 footnote $^\S$ addresses T4 DoS transparently. Happy to champion.*
- **Reviewer C (Generalist PC Member): `4` $\rightarrow$ `4.5 (Weak Accept / Accept)` (Confidence: 3)** — *Compelling, readable, submission-ready MobiSys paper with Table 6 right in Section 7. Only minor polish is the orphan Appendix C page on P16.*
- **Champion Test:** **PASSES.** All three reviewers align at Weak Accept or better (`4 / 4 / 4.5`), with Reviewer B and Reviewer C actively championing and Reviewer A supporting. Primary shepherding request (if conditionally accepted) would likely be running a small set of real-device end-to-end benign AndroidWorld tasks or a post-login OTP UI check on 3–5 real test accounts.

### Updated Outcome Forecast (MobiSys Base Rate ~15–20%)

| Submission State | Early Rejection | Advances to R2 $\rightarrow$ Reject | Conditional Accept (Shepherding) | Straight Accept |
| :--- | :---: | :---: | :---: | :---: |
| Round 1 (Oct 29 / Nov 23 v1) | 15–25% | **50–60% (Most Likely)** | 20–25% | $< 5\%$ |
| Round 2 (Nov 23 v2) | 5–10% | **40–50%** | 35–45% | 5–10% |
| **Round 3 (Current Nov 23 v3 — Submission-Ready)** | **$< 5\%$** | **25–35%** | **50–60% (Most Likely)** | **10–15%** |

---

## 7. Remaining Polish and Pre-Submission Checklist (~20 Minutes Total)

**Zero Critical or Major blockers remain.** Complete these 4 quick polish/logistics items before uploading:

1. **[Minor — 2 min] Fix Page 16 Appendix C orphan page (`sections/artifact.tex`):** Move `\section{Real-App UI Compatibility Audit}\label{sec:appendix_compat}` and its 3-line intro paragraph **above** `\begin{table*}[t]` (after `\clearpage`), so Section C and Table 8 sit cleanly together on **Page 16** (trimming the PDF from 17 to 16 crisp pages).
2. **[Minor — 3 min] Tighten Abstract and Conclusion `p95` wording (`sections/abstract.tex`, `sections/conclusion.tex`):** Change *"measured frame-latency regression"* to *"measured median/p95 frame-latency regression"* (p. 1, p. 12) so it aligns word-for-word with Section 7 RQ6's honest `Settings p99` tail disclosure.
3. **[Minor — 2 min] Clean one cosmetic JSON string (`real_apps_compatibility_audit.json`):** In `OKX`'s `vg_country_code` (`LinearLayout`), change `reason` from `"WebView / custom / opaque view container..."` to `"Custom / opaque view container..."` so no reviewer confuses it with a WebView.
4. **[Logistics — 10 min] Verify Public Artifact and HotCRP Deadlines:**
   - Push the finalized `output/*.json` and `evidence_logs_all.json` to `https://github.com/SecretHandle/SecretHandle` and verify it loads publicly in an incognito browser.
   - **Register Abstract on `https://mobisys27.hotcrp.com/` before Nov 27, 2026 23:59 AoE (4 days left)** and verify COIs.
   - Upload the final PDF and pass HotCRP's automated format checker before **Dec 4, 2026 23:59 AoE (11 days left)**.

---

## 8. Tóm tắt Điều hành tiếng Việt (Vietnamese Executive Summary)

- **Phán quyết mới:** **4.0 / 5 (Weak Accept — Đạt chuẩn sẵn sàng nộp ACM MobiSys 2027!)**, tăng mạnh từ mức **2.5 / 5** (Vòng 1) $\rightarrow$ **3.5 / 5** (Vòng 2) $\rightarrow$ **4.0 / 5** (Vòng 3). **Toàn bộ lỗi Nghiêm trọng (Critical) và toàn bộ mâu thuẫn số liệu/log Lớn (Major) đã được xử lý triệt để 100%.**
- **Dự báo kết quả:** Từ chối sớm **$< 5\%$** | Vào Vòng 2 rồi Từ chối **25–35%** | **Chấp nhận có điều kiện kèm Shepherding: 50–60% (Khả năng cao nhất)** | Chấp nhận thẳng **10–15%**. Cả 3 phản biện mô phỏng đều đạt ngưỡng ủng hộ (**Reviewer A: 4, Reviewer B: 4, Reviewer C: 4.5**), vượt qua *Champion Test*.
- **Xác minh thực tế các sửa đổi xuất sắc ở Vòng 3 (đo trực tiếp trên PDF, `.tex`, `.bib` và `evidence_logs_all.json`):**
  - **RMF-1 hoàn tất 100%:** Đã chụp lại sạch `Gmail` (`identifierId` trong GMS WebView) và `GitHub` (`login_field`/`password` trong OAuth Custom Tab), sửa đúng `Grab` về `Pkg+Class`, loại bỏ node nút bấm thừa của `Lazada`, và phân tách rành mạch **`6/20 (30.0%)` Direct Match / `9/20 (45.0%)` Pkg+Class + Touch Gate / `5/20 (25.0%)` WebView Fail-Closed**, khớp tuyệt đối giữa Mục 7, Bảng 6, Bảng 8 và JSON (kèm công bố thẳng `0/20` trường `smsOTPCode` sau đăng nhập). *(Lưu ý nhỏ: file `revision_checklist.md` mục 4.3 còn gõ nhầm `7/20, 10/20, 3/20`, nhưng bài báo và JSON hoàn toàn đúng `6/20, 9/20, 5/20`.)*
  - **RMF-2 & RMF-3 hoàn tất 100%:** Mục 7 RQ6 đã công bố trung thực `0/10` lớp phủ giả hiển thị (kèm 2 lần kích hoạt heuristic nội bộ bị chặn ở `SMS_Benign`/`Contacts`), đầy đủ `p95`/`p99`/`jank` của `Markor` và `Settings` ($\text{p99}: 38.0 \rightarrow 101.0\text{ ms}$), giải thích lỗi `0` frame / `4950 ms` của `Clock`, thêm chú thích $^\S$ về xác nhận chạm người dùng ở T4 DoS ($n=6$) dưới Bảng 4, và minh bạch hóa ranh giới giữa 11 tệp log JSON với số liệu tổng hợp từ EC2 đã đóng ở Phụ lục A.
  - **Định dạng CFP đạt chuẩn tuyệt đối:** $612 \times 792\text{ pt}$, 100% font nhúng, thân bài kết thúc gọn trên cột phải Trang 12 (còn dư ~64% cột phải), `31–51` dòng/cột ($\le 55$), `0` lệnh ép khoảng cách, `0` kết quả `b3.apk` cũ, `52/52` tài liệu tham khảo được trích dẫn khớp hoàn toàn.
- **4 chỉnh sửa nhỏ cuối cùng (~20 phút trước khi nộp):**
  1. **Sửa trang 16 trống ở Phụ lục C (2 phút):** Đảo `\section{Real-App UI Compatibility Audit}` + đoạn giới thiệu 3 dòng lên **trước** `\begin{table*}[t]` để Phụ lục C và Bảng 8 nằm chung gọn trên Trang 16 (bớt 1 trang lẻ).
  2. **Chuẩn hóa từ ngữ ở Abstract & Kết luận (3 phút):** Đổi *"measured frame-latency regression"* thành *"measured median/p95 frame-latency regression"* (tr. 1, tr. 12) để nhất quán tuyệt đối với `p99` của `Settings` ở Mục 7 RQ6.
  3. **Chỉnh 1 chuỗi chú thích nhỏ trong JSON (2 phút):** Sửa chuỗi `reason` của `vg_country_code` (`OKX`) bỏ chữ `"WebView /"` để tránh hiểu nhầm.
  4. **Hậu cần HotCRP (10 phút):** Đẩy bản JSON cuối lên GitHub công khai kiểm tra bằng tab ẩn danh, **đăng ký Abstract trước 27/11/2026 23:59 AoE (còn 4 ngày)**, và chạy bộ kiểm tra PDF của HotCRP trước **04/12/2026 23:59 AoE**.

---

## 9. Five-Line Recap

- **Verdict:** **4.0 / 5 (Weak Accept — Submission-Ready)** — all prior Critical and Major audit/log discrepancies (RMF-1–RMF-4) are cleanly resolved and programmatically verified against `evidence_logs_all.json`.
- **Forecast:** **50–60% Conditional Accept with Shepherding (Most Likely)**, **10–15% Straight Accept**, **$< 5\%$ Early Rejection**.
- **Top Polish #1:** Move `\section{Real-App UI Compatibility Audit}` above Table 8 so Page 16 is no longer a 3-line orphan page.
- **Top Polish #2:** Specify *"measured median/p95 frame-latency regression"* in the Abstract and Conclusion to match Section 7 RQ6's honest `Settings p99` tail disclosure.
- **Top Polish #3:** Push updated JSONs to the public GitHub repo, register the Abstract on HotCRP by **Nov 27, 2026 23:59 AoE (4 days)**, and run HotCRP's format check before **Dec 4, 2026 23:59 AoE**.