# Danh sách Công việc Cần sửa cho Bản thảo *SecretHandle* (Bản hoàn chỉnh)

> **Nguồn đối chiếu:** `mobisys2027_review_secrethandle.md` (Mode B Re-Review — đánh giá hiện tại: **2.5 / 5**, mục tiêu sau sửa: **4.0 / 5**).
>
> **Phạm vi:** Chỉ bao gồm các công việc sửa mã nguồn, thực nghiệm, nội dung bài báo, tài liệu tham khảo, artifact và chế bản LaTeX/PDF (đã loại bỏ toàn bộ phần hậu cần nộp bài và đăng ký abstract).

---

## Nhóm 1: Sửa ngay lỗi kỹ thuật, thuật toán, số học & tự mâu thuẫn (~3 giờ)

- [x] **1.1. Sửa lỗi pseudocode Thuật toán 2 Dòng 13 (`§6`, tr. 8):**
  - Đưa lệnh `wipe s` vào đúng phạm vi nhánh `else` ($\{z \gets \mathsf{consumed};\; \text{wipe } s\}$), tránh việc xóa nhầm bí mật $s$ của handle đa dụng khi $ok \land u > 0$ (ví dụ clipboard $u_0 = 5$).
  - Làm rõ trong đoạn giải thích đi kèm: việc hoàn trả ngân sách ($u \leftarrow u + 1$) ở handle đa dụng chỉ xảy ra khi hủy **trước khi** ghi bất kỳ byte nào vào bộ đệm trường đích.
  - *Xong khi:* Pseudocode Dòng 13 trong `algorithm.tex` phân nhánh tường minh và khớp hoàn toàn với phần mô tả ở `§4` và `§6`.

- [x] **1.2. Sửa lỗi tính toán bậc độ lớn (`§7` RQ5, tr. 10):**
  - Sửa cụm *"4 orders of magnitude faster"* thành *"over two orders of magnitude ($\sim 187\times$)"* (vì $4.18\,\text{ms} / 22.30\,\mu\text{s} = 187.4\times$).
  - *Xong khi:* Toàn văn không còn mô tả sai tỷ lệ giữa $22.30\,\mu\text{s}$ và $4.18\,\text{ms}$.

- [x] **1.3. Sửa tuyên bố sai về StrongBox dưới quyền root (`§9`, tr. 12):**
  - Đổi *"preventing handle MAC forgery even under root compromise"* thành *"preventing offline key extraction even if device storage is compromised (online root compromise remains out of scope per §3)"*.
  - *Xong khi:* Tuyên bố ở `§9` nhất quán hoàn toàn với Mô hình đe dọa ở `§3` (tr. 3) và Giả định 5.3.

- [x] **1.4. Đồng bộ kịch bản Template 1 giữa `§7` (tr. 10) và Bảng 5/6 (tr. 15):**
  - Sửa câu *"In a representative Template 1 trial, an incoming SMS prompts the agent..."* ở `§7` (*Qualitative Analysis*) thành *"a promotional notification arriving alongside the banking SMS prompts the agent..."* để khớp với vector *Cross-app promotion notification* trong Phụ lục B.
  - *Xong khi:* Không còn mâu thuẫn về kênh truyền chỉ thị tiêm nhiễm của Template 1 giữa thân bài và phụ lục.

- [x] **1.5. Phân tách rõ cỡ mẫu WebView (`§7` vs. Phụ lục B):**
  - Ghi rõ kết quả $30/30$ ($56.80\,\mu\text{s}$) là microbenchmark riêng `Vault.revealWeb`, tách biệt với $n = 6$ lượt thử tác tử end-to-end của Template 3 (*Web Phishing*) trong bộ 30 lượt thử.
  - *Xong khi:* Người đọc phân biệt rõ $n = 30$ (microbenchmark) và $n = 6$ (end-to-end Template 3).

- [x] **1.6. Sửa lỗi tràn/cắt chữ tiêu đề `Remark 5.16` (`§5`, tr. 8):**
  - Đổi `\begin{remark}[Legitimate-but-unwanted actions]` thành `\begin{remark}[In-scope misuse]`.
  - *Xong khi:* Biên dịch PDF không còn lỗi cắt chữ `REMARK 5.16 (LEGITIMATE-BUT-UNW`.

---

## Nhóm 2: Kiểm chứng phần cứng trên Galaxy A52s & Đối chiếu log gốc (~0.5–1 ngày)

- [x] **2.1. Kiểm toán phép đo TrustZone HMAC ($17.63\,\mu\text{s}$) và Binder IPC ($1.73\,\mu\text{s}$) trong `BenchmarkRunner.java` (`§7` RQ5):**
  - **Đã kiểm tra trực tiếp `BenchmarkRunner.java` (dòng 346–417):** Phép đo $17.63\,\mu\text{s}$ ($9.32\,\mu\text{s}$ emulator) thực chất dùng JCA `Mac.getInstance("HmacSHA256")` với `SecretKeySpec` trong bộ nhớ, $1.73\,\mu\text{s}$ ($0.61\,\mu\text{s}$ emulator) đo sao chép bộ đệm parcel (`System.arraycopy`), và $2.33\,\mu\text{s}$ ($1.06\,\mu\text{s}$) là chi phí `Vault.reveal` CAS/vòng lặp. Đã sửa mô tả trong `§7 RQ5` và Abstract cho **trung thực 100%** với mã nguồn.
  - [x] **Đã chạy thực nghiệm trên Galaxy A52s (`SM-A528B`, Android 14 API 34):** Bổ sung `TeeBenchmarkActivity.java` vào `b3secrethandle.apk`, đo trực tiếp 100 lượt khóa phần cứng `AndroidKeyStore` TEE (`inside_secure_hardware: true`, `SECURITY_LEVEL_TRUSTED_ENVIRONMENT`): trung vị **`1.79 ms`** (`1,785.31 µs` cho `Mac.doFinal` đã init) / **`5.74 ms`** (`5,740.99 µs` cho `init+doFinal`), `system_server` Binder IPC **`221.09 µs`**, đối chứng với `2.45 µs` (`n=1,000`) cho khóa phiên `SecretKeySpec` cache trong RAM (`output/physical_device_tee_benchmark.json`, đã đưa vào `§7` RQ5).

- [x] **2.2. Đối chiếu chéo toàn bộ số liệu trong `§7` với tệp JSON gốc:**
  - Đã đối chiếu toàn bộ 7 tệp JSON trong `output/`: khớp $100\%$ `physical_device_benchmark.json` (bao gồm sửa `% CPU`: `3.2% user, 3.2% kernel, 0.0% iowait, 0.5% irq, 0.1% softirq` thay cho `0.8% I/O wait/IRQ`), `benchmark_overhead_lifecycle_redirection.json`, `extended_source_ui_benchmark.json`, `fallback_policy_benchmark.json`, `webview_failclosed_benchmark.json`, `benchmark_autodroid_diversity.json`, và `rq6_benign_regression_results.json`.

---

## Nhóm 3: Xử lý lỗ hổng chí mạng về khảo sát 20 ứng dụng thực tế (~2–3 ngày)

- [x] **3.1. Chạy khảo sát tương thích UI thật trên 15–20 ứng dụng Google Play (`§7` & Appendix C):**
  - Đã thực thi `tools/audit_real_apps_compatibility.py --capture ...` trực tiếp trên **Samsung Galaxy A52s (`SM-A528B`, Android 14 / API 34)** ở màn hình đăng nhập / SĐT / OTP / PIN thực tế của **20 ứng dụng thương mại Google Play** (chỉ đọc cây UI tĩnh và `dumpsys package`, không lưu text người dùng và không chạy tấn công lên app thật; file cũ emulator 30/10 được tách lưu riêng).
  - Kết quả thực tế trong [`output/real_apps_compatibility_audit.json`](file:///e:/NCKH/SecretHandle/output/real_apps_compatibility_audit.json) và bảng `Table~\ref{tab:app_compatibility}` (Phụ lục C, tóm tắt trong `§7`): **9/20 (45.0%)** `DIRECT_COMPATIBLE` (`EditText` có tín hiệu ngữ nghĩa OTP/mật khẩu rõ ràng) và **11/20 (55.0%)** `STANDARD_INPUT_FALLBACK` (`10` `EditText` + `1` `AutoCompleteTextView`, đối sánh theo package+class kết hợp chạm xác nhận). Ghi nhận thêm hiện tượng thực tế: 2 app ủy quyền đăng nhập sang package khác (`Gmail -> com.google.android.gms`, `SoundCloud -> com.android.chrome` Custom Tab), và `com.VCB` kích hoạt cảnh báo RASP chặn Developer Options trước khi vào màn hình nhập liệu (đã loại khỏi 20 app UI).

- [x] **3.2. Tách bạch khảo sát 20 ứng dụng với microbenchmark `Vault.revealFallback` ($47.60\,\mu\text{s}$):**
  - Ghi rõ trong `§7` rằng kết quả $30/30$ với trung vị $47.60\,\mu\text{s}$ là microbenchmark tổng hợp `BenchmarkRunner` cho bước kiểm tra trong vault (`Vault.revealFallback`), không bao gồm thời gian phản xạ chạm của con người.

- [x] **3.3. Phương án dự phòng bắt buộc (đã kích hoạt ngay để bảo vệ tính trung thực):**
  - Đã **xóa bỏ hoàn toàn** câu *"we audited 20 applications on Android 14"* thiếu bằng chứng ở `§7` và chỉ trình bày hai microbenchmark `Vault.revealFallback` và `Vault.revealWeb` có log JSON thật hậu thuẫn. (Khi chạy xong 3.1 trên Galaxy A52s sẽ cập nhật bảng thật vào lại.)

---

## Nhóm 4: Đồng bộ hóa Thiết kế AOSP vs. Nguyên mẫu Stock Android 14 (~1.5 ngày)

- [x] **4.1. Thêm tiểu mục và bảng ánh xạ *Upstream AOSP Design vs. Stock Android 14 Prototype* (`§6.1`, Bảng 3):**
  - Đã bổ sung `Table~\ref{tab:aosp_vs_stock}` nêu rõ cơ chế/API Android 14 thực tế của `b3secrethandle.apk`: `NotificationListenerService` + regex (trình bày thẳng thắn hạn chế detector ở Android 14), `AccessibilityNodeInfo`, `ACTION_SET_TEXT` + chặn `TYPE_VIEW_TEXT_CHANGED` ở SDK bridge, `TYPE_ACCESSIBILITY_OVERLAY` + `FLAG_SECURE` trong `MainActivity` + lọc cây trợ năng ở bridge, và tách rõ Java `Vault` process vs. C++ `mlock()`/`explicit_bzero` của thiết kế AOSP upstream.

- [x] **4.2. Chỉnh lại phần mở đầu `§5` và ánh xạ Giả định 5.3–5.7:**
  - Đã chỉnh đoạn mở đầu `§5` phân định rõ các giả định đạt trọn vẹn trong AOSP `system_server`, còn `b3.apk` thực thi ở ranh giới IPC giữa broker được cấp quyền và UID tác tử không đặc quyền theo các giới hạn ở `§6` và `§9`.

- [x] **4.3. Xóa các câu tự mâu thuẫn về đặc quyền và vị trí chặn:**
  - Đã sửa *"intercepts the SMS at the telephony boundary"* (`§7`) thành *"at the notification listener before agent observation"*.
  - Đã thống nhất thuật ngữ xuyên suốt `§4`, `§6`, `§7`, `§9` và Phụ lục A: `b3secrethandle.apk` là APK cài ngoài được người dùng cấp quyền Notification Listener & Accessibility, tách biệt khỏi UID tác tử không đặc quyền.

- [x] **4.4. Thu hẹp phạm vi tuyên bố cho trung thực trong Abstract và `§1`:**
  - Ghi rõ nguyên mẫu Android 14 cài đặt và đánh giá **2 nguồn** (**SMS/notification OTP** và **sensitive clipboard**), còn Credential Manager/Wallet thuộc thiết kế tổng quát (`§4–§5`).
  - Ghi rõ thử nghiệm tác tử end-to-end chạy trên KVM emulator, còn microbenchmark lõi và CPU/PSS/power profile chạy trên Samsung Galaxy A52s thật.

- [x] **4.5. Thảo luận trung thực đánh đổi che bong bóng SMS (Hình 2b) và 2 kịch bản tấn công thích ứng (`§9`):**
  - Đã bổ sung phân tích trong `§9`: đánh đổi giữa che toàn bộ bong bóng (bảo toàn zero-leak nhưng ẩn ngữ cảnh giao dịch vs. span-level redaction ở tương lai), cửa sổ đua tranh 200ms/scroll trước khi `TYPE_ACCESSIBILITY_OVERLAY` commit, và `setFilterTouchesWhenObscured(true)` chống tapjacking hộp thoại fallback.

---

## Nhóm 5: Hoàn thiện phân rã T1–T5, AndroidWorld, Metadata LLM, Ablation & Năng lượng (~1.5–2 ngày)

- [x] **5.1. Thêm phân rã/kịch bản T1–T5 (`§7`):**
  - [x] Đã bổ sung ngay trong `§7` tóm tắt 2 kênh truyền tải chỉ thị tiêm nhiễm (độc lập với Phụ lục B) và làm rõ T4 DoS ($k \ge k_{\max}=3$) chuyển sang xác nhận chạm người dùng (*human intervention rather than autonomous recovery*).
  - *(Đóng — không bịa số liệu)* Không trích xuất được số đếm rời từng template T1–T5 do EC2 đã xóa và không còn `results/trials.jsonl`; giữ nguyên số tổng $n=30$ đã xác minh.

- [x] **5.2. Kiểm tra siêu dữ liệu thí nghiệm LLM (`§7`):**
  - Đã cập nhật đúng kênh gọi mô hình Claude~3.5~Sonnet là **qua Amazon Bedrock** (`snapshot claude-3-5-sonnet-20241022`, $T=0.0$, top-p $1.0$, max 15 steps) thay cho *"Anthropic API"*.
  - *(Không khả dụng)* Không có khoảng ngày gọi API và chi phí USD/token chi tiết do chạy qua API Bedrock và không còn log billing tách riêng cho từng tác vụ.

- [x] **5.3. Sửa tuyên bố về 10 ứng dụng AndroidWorld (Abstract, `§1`, `§7` RQ6, `§10`):**
  - Đã áp dụng **Phương án B (trung thực với dữ liệu đã đo)**: sửa thành *"zero touch-passthrough or measured frame-latency regression across 10 AndroidWorld applications ($50/50$ events, $\Delta\text{p95}=0.0\,\text{ms}$ on Markor and Settings)"*.

- [x] **5.4. Nâng cỡ mẫu ablation `No Observation Redactor` (`§7`):**
  - [x] Đã chạy **10 cặp thử nghiệm ghép cặp (`n=10`)** trực tiếp trên Samsung Galaxy A52s (`output/redactor_ablation_10trials.json`): khi tắt `RedactionAccessibilityService`, **10/10** lượt lộ plaintext canary OTP trong UI tree và `screencap` (`97.38–97.93%` nền trắng + nét chữ OTP); khi bật Redactor, **10/10** lượt phủ lớp `ACCESSIBILITY_OVERLAY` che kín **`99.16%`** pixel (`0.00%` pixel gốc còn sót). Đã cập nhật vào `§7` (ghi rõ kiểm chứng tầng quan sát OS).

- [x] **5.5. Củng cố phương pháp đo năng lượng trên Galaxy A52s (`§7` RQ6):**
  - [x] Đã ghi rõ $< 0.12\,\text{mJ}$ mỗi sự kiện trung gian là *simulated-unplug `batterystats`* estimate.
  - [x] **Đã chạy đo rút cáp USB 15 phút qua Wi-Fi ADB (`192.168.1.125:5555`):** Lưu ý user build không root chặn sysfs `Permission denied`, nên đã thu mẫu trực tiếp từ `dumpsys battery` (`output/physical_device_battery_unplugged_15m.json`, `7.5 phút` Idle vs. `7.5 phút` SecretHandle Active + burst mỗi 15s): dòng tiêu thụ trung bình `249.45 mA` (`980.9 mW`) Idle vs. `240.21 mA` (`940.5 mW`) Active — không phát sinh hao pin vượt ngưỡng nhiễu nền (đã đưa vào `§7` RQ6).

---

## Nhóm 6: Công trình liên quan, BibTeX, Artifact & Chế bản LaTeX/PDF (~1.5 ngày)

- [x] **6.1. Bổ sung công trình liên quan 2026 & kinh điển (`§8`) và dọn `references_verified.bib`:**
  - Đã kiểm chứng metadata thật qua web và bổ sung vào `§8` + `references_verified.bib`: **Aura** (`arXiv:2602.10915`), **SUPOR** (USENIX Sec '15), **UIPicker** (USENIX Sec '15), **TrustUI** (APSys '14), **TruZ-Droid** (MobiSys '18).
  - Đã sửa `dennis1966semantics` sang `@article` (`Communications of the ACM`) và xóa sạch 14 mục thừa chưa trích dẫn.

- [x] **6.2. Hoàn thiện Phụ lục A–C (`mobisys/sections/artifact.tex`):**
  - Đã bổ sung đầy đủ lệnh ADB sau `adb install`, sửa đúng tên `b3secrethandle.apk`, và đồng bộ toàn bộ đường dẫn trong Artifact Appendix khớp 100% với cấu trúc thực tế của repo (`SecretHandle/`, `device/b3-secrethandle/`, `device/b0-otp-forwarding/`, `tools/`, `output/*.json`), gỡ bỏ tham chiếu tới `evaluation/` và `results/trials.jsonl` (EC2 đã xóa).
  - [ ] *(Tác giả tự kiểm tra trước khi nộp)* Xác nhận kho GitHub `https://github.com/SecretHandle/SecretHandle` truy cập công khai được khi mở mã nguồn.

- [x] **6.3. Sửa chế bản LaTeX, hình ảnh và ngân sách 12 trang:**
  - Đã xóa 6 dòng ép khoảng cách float trong preamble (`mobisys/main.tex`).
  - Đã tăng chiều cao Hình 2 từ `2.6cm` lên `3.2cm`, bọc Hình 1 trong `\resizebox{\textwidth}{!}{...}`, bỏ dấu chấm dư ở tiêu đề `\paragraph{Mobile agents act through the UI}`, rút ngắn tiêu đề `Remark 5.16` thành `[In-scope misuse]`.
  - **Kết quả biên dịch cuối:** `mobisys/main.pdf` dài **16 trang** (`612 x 792 pts (letter)`), $100\%$ font nhúng (`emb=yes`), **Mục 10 Conclusion kết thúc gọn trên Trang 12**, References ở Trang 13–14, Phụ lục A–C ở Trang 14–16, không còn cảnh báo `Overfull`/`Undefined`, `manuscript_check.py` đạt **PASS**.