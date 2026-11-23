# Danh sách Công việc Cần sửa cho Bản thảo *SecretHandle* (Bản hoàn chỉnh)

> **Nguồn đối chiếu:** `mobisys2027_review_secrethandle.md` (Mode B Re-Review — đánh giá hiện tại: **2.5 / 5**, mục tiêu sau sửa: **4.0 / 5**).
>
> **Phạm vi:** Chỉ bao gồm các công việc sửa mã nguồn, thực nghiệm, nội dung bài báo, tài liệu tham khảo, artifact và chế bản LaTeX/PDF (đã loại bỏ toàn bộ phần hậu cần nộp bài và đăng ký abstract).

---

## Nhóm 1: Sửa ngay lỗi kỹ thuật, thuật toán, số học & tự mâu thuẫn (~3 giờ)

- [ ] **1.1. Sửa lỗi pseudocode Thuật toán 2 Dòng 13 (`§6`, tr. 8):**
  - Đưa lệnh `wipe s` vào đúng phạm vi nhánh `else` ($z \leftarrow \mathsf{consumed}$), tránh việc xóa nhầm bí mật $s$ của handle đa dụng khi $ok \land u > 0$ (ví dụ clipboard $u_0 = 5$).
  - Làm rõ trong đoạn giải thích đi kèm: việc hoàn trả ngân sách ($u \leftarrow u + 1$) ở handle đa dụng chỉ xảy ra khi hủy **trước khi** ghi bất kỳ byte nào vào bộ đệm trường đích.
  - *Xong khi:* Pseudocode Dòng 13 trong `manuscript_full_source.tex` phân nhánh tường minh và khớp hoàn toàn với phần mô tả ở `§4` và `§6`.

- [ ] **1.2. Sửa lỗi tính toán bậc độ lớn (`§7` RQ5, tr. 10):**
  - Sửa cụm *"4 orders of magnitude faster"* thành *"over two orders of magnitude ($\sim 187\times$)"* (vì $4.18\,\text{ms} / 22.30\,\mu\text{s} = 187.4\times$).
  - *Xong khi:* Toàn văn không còn mô tả sai tỷ lệ giữa $22.30\,\mu\text{s}$ và $4.18\,\text{ms}$.

- [ ] **1.3. Sửa tuyên bố sai về StrongBox dưới quyền root (`§9`, tr. 12):**
  - Đổi *"preventing handle MAC forgery even under root compromise"* thành *"preventing offline key extraction even if device storage is compromised (online root compromise remains out of scope per §3)"*.
  - *Xong khi:* Tuyên bố ở `§9` nhất quán hoàn toàn với Mô hình đe dọa ở `§3` (tr. 3) và Giả định 5.3.

- [ ] **1.4. Đồng bộ kịch bản Template 1 giữa `§7` (tr. 10) và Bảng 5 (tr. 15):**
  - Sửa câu *"In a representative Template 1 trial, an incoming SMS prompts the agent..."* ở `§7` (*Qualitative Analysis*, tr. 10) thành *"a promotional notification arriving alongside the banking SMS prompts the agent..."* để khớp với vector *Cross-app promotion notification* trong Bảng 5 (Phụ lục B).
  - *Xong khi:* Không còn mâu thuẫn về kênh truyền chỉ thị tiêm nhiễm của Template 1 giữa thân bài và phụ lục.

- [ ] **1.5. Phân tách rõ cỡ mẫu WebView (`§7`, tr. 11 vs. Phụ lục B, tr. 15):**
  - Ghi rõ kết quả $30/30$ ($56.80\,\mu\text{s}$) ở `§7` (tr. 11) là microbenchmark riêng `Vault.revealWeb`, tách biệt với $n = 6$ lượt thử tác tử end-to-end của Template 3 (*Web Phishing*) trong bộ 30 lượt thử của Bảng 3.
  - *Xong khi:* Người đọc phân biệt rõ $n = 30$ (microbenchmark) và $n = 6$ (end-to-end Template 3).

- [ ] **1.6. Sửa lỗi tràn/cắt chữ tiêu đề `Remark 5.16` (`§5`, tr. 8):**
  - Đổi `\begin{remark}[Legitimate-but-unwanted actions]` thành `\begin{remark}[In-scope misuse]` trong `manuscript_full_source.tex`.
  - *Xong khi:* Biên dịch PDF không còn lỗi cắt chữ `REMARK 5.16 (LEGITIMATE-BUT-UNW`.

---

## Nhóm 2: Kiểm chứng phần cứng trên Galaxy A52s & Đối chiếu log gốc (~0.5–1 ngày)

- [ ] **2.1. Kiểm toán phép đo TrustZone HMAC ($17.63\,\mu\text{s}$) và Binder IPC ($1.73\,\mu\text{s}$) trong `BenchmarkRunner.java` (`§7` RQ5, tr. 10):**
  - Kiểm tra mã nguồn `BenchmarkRunner.java` trên Galaxy A52s (Snapdragon 778G, Android 14) xem mỗi vòng lặp có thực sự gọi `AndroidKeyStore` chạy trong TEE (`KeyInfo.getSecurityLevel() == SECURITY_LEVEL_TRUSTED_ENVIRONMENT`) và thực hiện Binder IPC xuyên tiến trình hay không.
  - Nếu $17.63\,\mu\text{s}$ thực chất là khóa phiên tạm lưu trong bộ nhớ (hoặc JCA/Conscrypt phần mềm) và $1.73\,\mu\text{s}$ là Binder nội bộ trong `app_process`: sửa lại mô tả cho trung thực, đồng thời đo thêm 1 mốc gọi `AndroidKeyStore` TEE xuyên tiến trình thật (thường khoảng $0.5\text{–}2\,\text{ms}$) để chứng minh động cơ kỹ thuật của việc cache khóa phiên xuất phát từ TEE.
  - *Xong khi:* Số liệu ARM ở Abstract và `§7` RQ5 phản ánh chính xác cơ chế mật mã và IPC mà code thực thi.

- [ ] **2.2. Đối chiếu chéo toàn bộ số liệu trong `§7` với tệp JSON gốc trong `evidence_logs.rar`:**
  - Giải nén và kiểm tra khớp từng con số giữa thân bài và các tệp: `physical_device_benchmark.json`, `fallback_policy_benchmark.json`, `webview_failclosed_benchmark.json`, `rq6_benign_regression_results.json`, `benchmark_autodroid_diversity.json`, `benchmark_overhead_lifecycle_redirection.json`, `extended_source_ui_benchmark.json`.
  - *Xong khi:* $100\%$ trung bình, trung vị, p95 và tỷ lệ trong `§7` khớp với log JSON thô (không lệch đơn vị hay làm tròn).

---

## Nhóm 3: Xử lý lỗ hổng chí mạng về khảo sát 20 ứng dụng thực tế (~2–3 ngày)

- [ ] **3.1. Chạy khảo sát tương thích UI thật trên 15–20 ứng dụng Google Play (`§7`, tr. 11):**
  - Thực thi `python tools/audit_real_apps_compatibility.py --capture ...` trên Galaxy A52s ở màn hình đăng nhập/OTP của 15–20 ứng dụng phổ biến (ngân hàng/fintech, TMĐT, nhắn tin, xác thực).
  - **Ràng buộc đạo đức:** Chỉ chụp siêu dữ liệu cây giao diện tĩnh (`uiautomator dump`) ở màn hình đăng nhập/tài khoản thử nghiệm; **tuyệt đối không** chạy tấn công lên ứng dụng thương mại và **không** lưu dữ liệu cá nhân thật.
  - Xuất báo cáo thống kê cụ thể: tên ứng dụng, tên gói, **phiên bản ứng dụng (`versionName`/`versionCode`)**, nhóm ứng dụng, số lượng khớp trực tiếp `autofillHints`/`inputType` ($X/20$), số lượng dùng custom view/numpad cần fallback ($Y/20$), và số lượng dùng WebView ($Z/20$).
  - Đưa bảng tổng hợp vào `§7` (hoặc bảng chi tiết vào Phụ lục C kèm con số tóm tắt chính xác trong `§7`).
  - *Xong khi:* Có bảng dữ liệu thực tế với đầy đủ tên ứng dụng, phiên bản app và phân rã $X/20$, $Y/20$, $Z/20$.

- [ ] **3.2. Tách bạch khảo sát 20 ứng dụng với microbenchmark `Vault.revealFallback` ($47.60\,\mu\text{s}$):**
  - Ghi rõ trong `§7` (tr. 11) rằng kết quả $30/30$ với trung vị $47.60\,\mu\text{s}$ là microbenchmark tổng hợp cho bước kiểm tra trong vault (`Vault.revealFallback`), còn thao tác chạm xác nhận của người dùng thật sẽ cộng thêm thời gian phản xạ của con người.
  - *Xong khi:* Không còn sự nhập nhằng giữa khảo sát UI tĩnh 20 app và microbenchmark vault $47.60\,\mu\text{s}$.

- [ ] **3.3. Phương án dự phòng bắt buộc (nếu không kịp hoàn thành 3.1):**
  - Nếu không thể hoàn thành việc chạy khảo sát thực tế trên 15–20 ứng dụng, **xóa bỏ hoàn toàn** câu *"we audited 20 applications on Android 14"* ở `§7` (tr. 11) và chỉ trình bày `Vault.revealFallback` dưới dạng microbenchmark cơ chế dự phòng.
  - *Xong khi:* Bài báo không chứa bất kỳ tuyên bố khảo sát nào thiếu dữ liệu hậu thuẫn.

---

## Nhóm 4: Đồng bộ hóa Thiết kế AOSP vs. Nguyên mẫu Stock Android 14 (~1.5 ngày)

- [ ] **4.1. Thêm tiểu mục hoặc bảng ánh xạ *Upstream AOSP Design vs. Stock Android 14 Prototype (`b3.apk`)* trong `§6`:**
  - Nêu rõ cơ chế/API Android 14 thực tế mà nguyên mẫu `b3.apk` sử dụng cho từng thành phần so với thiết kế tích hợp AOSP lý tưởng:
    1. *Mint & trích xuất OTP:* Nêu rõ nguyên mẫu Android 14 dùng `NotificationListenerService` kèm bộ tách mẫu/regex (khác với pipeline phân loại OTP tích hợp sẵn từ Android 15 trở lên); tránh dùng ngôn từ phóng đại *"hoàn toàn không dùng detector"* khi mô tả nguyên mẫu Android 14.
    2. *Target Context (`FreshTargetContext`):* Nêu rõ nguyên mẫu lấy tên gói/trường nhập liệu đích từ cây `AccessibilityNodeInfo` / cửa sổ tiền cảnh (so với trích xuất trực tiếp từ `WindowManagerService`/`ViewRootImpl` ở AOSP upstream).
    3. *Observation Redaction & định vị bong bóng tin nhắn (Hình 2b):* Giải thích rõ cách dịch vụ xác định tọa độ bong bóng SMS để vẽ lớp phủ `TYPE_ACCESSIBILITY_OVERLAY` và cơ chế đồng bộ `SurfaceFlinger` với Agent SDK Bridge.
    4. *`InjectInternal(V, s)`:* Nêu chính xác API tiêm giá trị trên Android 14 (ví dụ `AccessibilityNodeInfo.ACTION_SET_TEXT`) và cách Agent SDK Bridge chặn sự kiện `TYPE_VIEW_TEXT_CHANGED` để không rò rỉ ngược về tác tử.
    5. *Memory hygiene (`§9`, tr. 12):* Phân tách rõ việc xóa bộ đệm trong mã Java (`char[]`/`byte[]`) ở nguyên mẫu `b3.apk` với `mlock()`/`explicit_bzero` thuộc thiết kế dịch vụ C++ trên AOSP upstream.
  - *Xong khi:* Mọi thành phần trong nguyên mẫu đều có tên API Android 14 cụ thể và ranh giới TCB rõ ràng.

- [ ] **4.2. Chỉnh lại phần mở đầu `§5` (tr. 6) và ánh xạ Giả định 5.3–5.7:**
  - Điều chỉnh câu ở đầu `§5` (tr. 6) đang viết rằng các giả định hình thức được hiện thực trực tiếp bởi nguyên mẫu Android 14; làm rõ các Giả định 5.3, 5.6, 5.7 đạt mức mạnh nhất trong kiến trúc AOSP upstream, còn nguyên mẫu stock Android 14 (`b3.apk`) thỏa mãn ở mức ranh giới IPC thông qua Agent SDK Bridge với các giới hạn đã nêu ở `§6` và `§9`.
  - *Xong khi:* Phần lý thuyết ở `§5` không tuyên bố quá mức so với năng lực thực thi của `b3.apk`.

- [ ] **4.3. Xóa các câu tự mâu thuẫn về đặc quyền và vị trí chặn:**
  - Sửa *"the OS intercepts the SMS at the telephony boundary before rendering"* (`§7`, tr. 11) thành *"intercepts the SMS at the notification broker before agent observation"*.
  - Thống nhất cách gọi *"privileged Binder service"* (`§4` tr. 6, `§6` tr. 8) và *"unprivileged broker"* (`§9` tr. 12): giải thích nhất quán rằng `b3.apk` là ứng dụng cài ngoài được người dùng cấp quyền đặc biệt (`BIND_NOTIFICATION_LISTENER_SERVICE`, `BIND_ACCESSIBILITY_SERVICE`), trong khi bộ lập kế hoạch của tác tử chạy ở một UID riêng không có các quyền này.
  - *Xong khi:* Không còn mâu thuẫn thuật ngữ giữa `§4`, `§6`, `§7`, `§9` và Phụ lục A.

- [ ] **4.4. Thu hẹp phạm vi tuyên bố cho trung thực trong Abstract và `§1`:**
  - Ghi rõ nguyên mẫu Android 14 cài đặt và đánh giá **2 nguồn** (**SMS/notification OTP** và **sensitive clipboard**), còn **Credential Manager, Wallet và Protected Confirmation** nằm trong thiết kế kiến trúc/chính sách tổng quát (`§4–§5`).
  - Ghi rõ các thử nghiệm tác tử end-to-end (Bảng 3) chạy trên Android 14 KVM emulator, còn microbenchmark phần cứng và đo tài nguyên chạy trên Samsung Galaxy A52s thật.
  - *Xong khi:* Abstract và `§1` khớp $100\%$ với những gì thực sự được đánh giá ở `§7`.

- [ ] **4.5. Thảo luận trung thực đánh đổi che bong bóng SMS (Hình 2b) và 2 kịch bản tấn công thích ứng trên stock Android 14 (`§4` / `§9`):**
  - Phân tích rõ đánh đổi giữa việc che toàn bộ bong bóng tin nhắn (như Hình 2b — an toàn tối đa nhưng che mất ngữ cảnh giao dịch như số tiền/người nhận) so với che chọn lọc từng chuỗi mã số (span-level redaction).
  - Bổ sung phân tích (và kiểm thử nhanh nếu kịp) cho 2 kịch bản thích ứng: (a) cửa sổ đua tranh thời gian lúc SMS vừa tới hoặc khi cuộn màn hình trước lúc `TYPE_ACCESSIBILITY_OVERLAY` kịp vẽ đè trên stock Android 14; (b) ứng dụng độc hại giả mạo `smsOTPCode` (bị chặn bởi ràng buộc tên gói) hoặc tìm cách tapjacking hộp thoại chạm xác nhận fallback (đối phó bằng `setFilterTouchesWhenObscured(true)` / `FLAG_WINDOW_IS_OBSCURED`).
  - *Xong khi:* Không còn mâu thuẫn giữa Hình 2(b) với phần mô tả ngữ cảnh, và 2 kịch bản thích ứng đặc thù Android 14 đều được phân tích thẳng thắn.

---

## Nhóm 5: Hoàn thiện phân rã T1–T5, AndroidWorld, Metadata LLM, Ablation & Năng lượng (~1.5–2 ngày)

- [ ] **5.1. Thêm bảng phân rã kết quả theo từng mẫu tấn công T1–T5 và tóm tắt kênh truyền tải ngay trong `§7` (tr. 9–11):**
  - Trích xuất từ `results/trials.jsonl` các chỉ số $(E, R, U_{\text{att}}, \text{số ca kích hoạt chạm xác nhận của người dùng})$ cho từng mẫu T1–T5 ($n = 6$ mỗi mẫu).
  - Làm rõ ở **T4 (DoS Depletion)**: bao nhiêu ca tác tử tự phục hồi và bao nhiêu ca bị thu hồi handle ($k = 3$) buộc phải nhờ cơ chế chạm xác nhận của người dùng.
  - Bổ sung 1–2 câu tóm tắt trực tiếp 2 kênh truyền tải chỉ thị tiêm nhiễm (thông báo khuyến mãi không che & nội dung chat/web bên thứ ba) ngay trong `§7` để thân bài đứng độc lập hoàn toàn ngay cả khi phản biện không đọc Phụ lục B.
  - *Xong khi:* Mâu thuẫn về $U_{\text{att}} = 1.00$ dưới tấn công DoS T4 được giải thích định lượng và `§7` không phụ thuộc bắt buộc vào Phụ lục B.

- [ ] **5.2. Bổ sung đầy đủ siêu dữ liệu thí nghiệm LLM (`§7`, tr. 8–9):**
  - Ghi rõ **khoảng ngày gọi API (`API call dates`)** và **chi phí token / USD trung bình mỗi tác vụ** cho Mobile-Agent v3.5 (`claude-3-5-sonnet-20241022`) và AutoDroid (`gpt-4o-2024-08-06`).
  - *Xong khi:* `§7` công bố đầy đủ model snapshot, ngày gọi API, nhiệt độ, giới hạn bước và chi phí API theo chuẩn đánh giá tác tử LLM.

- [ ] **5.3. Sửa tuyên bố về 10 ứng dụng AndroidWorld (Abstract, `§1`, `§7` RQ6, `§10`):**
  - Chọn **1 trong 2** phương án:
    - *Phương án A (mạnh hơn):* Chạy thêm 10–20 tác vụ AndroidWorld lành tính end-to-end với Mobile-Agent/AutoDroid ở chế độ B0 vs. B3 và báo cáo tỷ lệ hoàn thành thực tế ($X/N$ so với $Y/N$).
    - *Phương án B (nhanh, trung thực):* Đổi tuyên bố *"zero task regression across 10 AndroidWorld applications ($\Delta = 0.00$)"* thành *"zero touch-passthrough or rendering-latency regression across 10 AndroidWorld applications ($50/50$ events, $\Delta\text{p95} = 0.0\,\text{ms}$)"*.
  - *Xong khi:* Tuyên bố ở Abstract, `§1`, `§7` và `§10` khớp đúng với phép đo thực tế.

- [ ] **5.4. Nâng cỡ mẫu ablation `No Observation Redactor` (`§7`, tr. 11):**
  - Tăng lượt thử kiểm chứng cho `No Observation Redactor` từ `1/1` lên ít nhất $n = 10$ (hoặc $n = 30$) để kết luận $L = 1.00$ có ý nghĩa thống kê.
  - Ghi rõ các dòng ablation khác (`No Source Minting`, `No Destination Binding`, `No Atomic CAS`) là lượt chạy tách biệt hay đối chiếu từ kết quả B0/B1/RQ3.
  - *Xong khi:* Không còn kết luận ablation dựa trên mẫu $n = 1$.

- [ ] **5.5. Củng cố phương pháp đo năng lượng trên Galaxy A52s (`§7` RQ6, tr. 10):**
  - Ghi rõ $< 0.12\,\text{mJ}$ mỗi sự kiện trung gian là ước lượng từ mô hình phần mềm `dumpsys batterystats` (không phải thiết bị đo công suất phần cứng).
  - *(Nên làm nếu đủ thời gian)* Chạy thêm phiên đo 15–30 phút trên Galaxy A52s ở trạng thái **rút cáp USB** (dùng ADB qua Wi-Fi, khóa cố định độ sáng màn hình, ghi rõ **trạng thái sóng/chế độ máy bay** và **trạng thái nhiệt độ thiết bị**) đọc `/sys/class/power_supply/battery/current_now` & `voltage_now` để đối chứng công suất B0 vs. B3 và báo cáo **tổng năng lượng tiêu hao cho một tác vụ 15 bước**.
  - *Xong khi:* Phương pháp và điều kiện đo năng lượng được nêu trung thực, có ghi nhận điều kiện sóng/nhiệt độ và quy đổi ra mức tác vụ.

---

## Nhóm 6: Công trình liên quan, BibTeX, Artifact & Chế bản LaTeX/PDF (~1.5 ngày)

- [ ] **6.1. Bổ sung công trình liên quan 2026 & kinh điển (`§8`, tr. 11–12) và dọn `references_verified.bib`:**
  - Thêm 3–4 câu đối chiếu trong `§8` với:
    - **Aura** (`arXiv:2602.10915`, 02/2026 — hệ điều hành tác tử di động hướng ý định).
    - **SUPOR** (USENIX Security '15) & **UIPicker** (USENIX Security '15 — nhận diện trường giao diện nhạy cảm trên Android).
    - **TrustUI** (APSys '14) / **TruZ-Droid** (MobiSys '18 — đường dẫn UI tin cậy trên ARM TrustZone).
    - *(Tùy chọn, công trình đồng thời)* **MATE** (EMNLP Findings 10/2026 / `arXiv:2611.25526`).
  - Sửa mục `dennis1966semantics` (`[18]`, tr. 13) trong `references_verified.bib` từ `@inproceedings` sang `@article` (vì *Communications of the ACM* là tạp chí) và xóa 14 mục thừa chưa trích dẫn.
  - *Xong khi:* Biên dịch BibTeX không còn lỗi loại ấn phẩm và `§8` phủ đủ công trình 2026 gần nhất.

- [ ] **6.2. Hoàn thiện kho Artifact & Phụ lục A–B (tr. 14–15):**
  - Kiểm tra kho GitHub `https://github.com/SecretHandle/SecretHandle` truy cập công khai được và khớp chính xác từng tên tệp nêu trong Phụ lục A (`device/b3-secrethandle/b3.apk`, `configs/android14_eval.yaml`, `BenchmarkRunner`, `results/trials.jsonl`, `provenance.json`).
  - Bổ sung vào Phụ lục A các lệnh kích hoạt dịch vụ Android 14 còn thiếu sau bước `adb install`:
    - `adb shell cmd notification allow_listener ...`
    - `adb shell settings put secure enabled_accessibility_services ...`
    - lệnh kiểm tra `adb unroot` và `getenforce`.
  - Lưu system prompt đầy đủ và commit hash của Mobile-Agent v3.5 / AutoDroid trong repo (và tóm tắt cấu hình prompt chính trong Phụ lục B).
  - *Xong khi:* Một người ngoài có thể làm theo đúng các lệnh ở Phụ lục A từ đầu đến cuối mà không thiếu bước kích hoạt dịch vụ.

- [ ] **6.3. Sửa chế bản LaTeX, hình ảnh và ngân sách 12 trang:**
  - Xóa các dòng ép khoảng cách float trong phần preamble của `manuscript_full_source.tex` (dòng 83–88: `\textfloatsep`, `\floatsep`, `\intextsep`, `\dbltextfloatsep`, `\abovecaptionskip`, `\belowcaptionskip`) để tuân thủ $100\%$ khoảng cách mặc định của `acmart`.
  - Tăng chiều cao Hình 2 (tr. 9) từ `2.6cm` lên `3.2cm` để chữ trong ảnh chụp màn hình đọc rõ ở mức zoom $100\%$; bọc Hình 1 (tr. 4) trong `\resizebox{\textwidth}{!}{...}` nếu cần để đảm bảo đỉnh hình thoi `Injected content` không sát/chạm lề trên.
  - Kiểm tra trực quan bằng Adobe Acrobat ở mức zoom $100\%$: (a) Hình 1 không cắt mép trên hay chú thích; (b) tiêu đề `Mobile agents act through the UI.` (`§2`, tr. 2) không bị đúp dấu chấm `UI..`; (c) `Remark 5.16` (tr. 8) không tràn cột; (d) `pdfinfo` báo đúng `612 x 792 pts (letter)` và `pdffonts` báo $100\%$ `emb=yes`.
  - **Cân đối giới hạn $\le 12$ trang thân bài:** Nếu việc thêm bảng ở Nhóm 3–5 làm nội dung tràn sang trang 13, thu hồi chỗ trống bằng cách (i) gộp phần mô tả lặp lại giữa `§4` (*Building blocks*, tr. 6) và `§6` (*Integration points*, tr. 8), và (ii) viết gọn chứng minh 1 dòng của Corollary 5.10, Proposition 5.12, Proposition 5.13 thành câu nội dòng.
  - *Xong khi:* `paper/main.pdf` kết thúc phần `§10 Conclusion` ở đúng **trang 12**, References bắt đầu từ trang 13, không có cảnh báo LaTeX/BibTeX và sạch hoàn toàn các lỗi hiển thị.