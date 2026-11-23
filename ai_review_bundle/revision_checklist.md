# Danh sách Công việc Cần sửa Vòng 2 — *SecretHandle* (ACM MobiSys 2027)

> **Nguồn đối chiếu:** [`reviews/acm_mobisys_2027.md`](file:///e:/NCKH/SecretHandle/reviews/acm_mobisys_2027.md) (Mode B Re-Review ngày 23/11/2026).
>
> **Trạng thái hiện tại:** Đã hoàn tất sửa toàn bộ **RMF-1, RMF-2, RMF-3, RMF-4 (4.1–4.3)** trên mã nguồn, JSON và LaTeX (chỉ còn kiểm tra link GitHub công khai và nộp HotCRP).

---

## Nhóm 1 (RMF-1 — Major, ưu tiên số 1, ~2–3 giờ): Sửa phân loại & tính nhất quán WebView trong Khảo sát 20 Ứng dụng Thực tế

**File cần tác động:** `tools/audit_real_apps_compatibility.py`, `output/real_apps_compatibility_audit.json` (và `evidence_logs_all.json`), `§7` (tr. 10–11), Phụ lục C Bảng 8 (tr. 16).

- [x] **1.1. Tách 3 ứng dụng dùng WebView sang nhóm thứ 3 (`WebView Fail-Closed`):**
  - Đã cập nhật [`tools/audit_real_apps_compatibility.py`](file:///e:/NCKH/SecretHandle/tools/audit_real_apps_compatibility.py) và [`output/real_apps_compatibility_audit.json`](file:///e:/NCKH/SecretHandle/output/real_apps_compatibility_audit.json): xếp cả 3 ứng dụng có `android.webkit.WebView` (`SoundCloud`, `CocCoc Browser`, `Binance`) vào `WEBVIEW_FAIL_CLOSED` ($3/20 = 15.0\%$, *Fail-Closed Rejection*).

- [x] **1.2. Sửa lỗi gán nhãn nhầm của `Grab` (và lọc nút `TextView` của `Lazada`):**
  - Sửa lỗi khớp chuỗi con (`"passenger"` $\rightarrow$ `"pass"`) bằng ranh giới token + tách `:id/` trong `_extract_semantic_hints`, đồng thời bỏ qua các node nút bấm `TextView`/`Button` không nhập liệu (`btn_email_otp_login` ở `Lazada`). `Grab` (`verify_number_edit_number`, `is_password: false`) chuyển chuẩn xác sang `STANDARD_INPUT_FALLBACK` (`phone`, *Pkg+Class / Touch Gate*).

- [x] **1.3. Chú thích minh bạch 2 ứng dụng bắt màn hình khóa / server URL trên Galaxy A52s:**
  - `Gmail (Lock Gate)` (`com.google.android.gms`, `lockPassword`) và `GitHub (Server URL)` (`enterprise_server_url_edit_text`) đã được chú thích rõ trong `§7`, Bảng 8 (Phụ lục C) và trường `screen_note` của `real_apps_compatibility_audit.json`.

- [x] **1.4. Cập nhật thống kê 3 hạng mục và phạm vi khảo sát trong `§7` & Bảng 8:**
  - Khớp $100\%$ giữa JSON, `§7`, Bảng 6 (`tab:compat_summary`) và Bảng 8 (`tab:app_compatibility`): **`7/20 (35.0%)` Direct Match**, **`10/20 (50.0%)` Pkg+Class + Touch Gate**, **`3/20 (15.0%)` WebView Fail-Closed** (tổng $20/20$, và ghi rõ $0/20$ trường `EditText` mang `smsOTPCode` động sau đăng nhập).

---

## Nhóm 2 (RMF-2 — Major, rất quan trọng cho Artifact, ~2 giờ): Đồng bộ hóa `rq6_benign_regression_results.json` với `§7 RQ6`

**File cần tác động:** `output/rq6_benign_regression_results.json` (và `evidence_logs_all.json`), `§7 RQ6`.

- [x] **2.1. Xử lý minh bạch 2 cờ `FALSE_POSITIVE` trong `false_positive_audit` (`SMS_Benign`, `Contacts`):**
  - Áp dụng **Cách B (trung thực tuyệt đối với log EC2 gốc):** giữ nguyên số đo gốc, bổ sung các trường tóm tắt minh bạch vào `summary` của `rq6_benign_regression_results.json` (`visible_overlay_false_positive_rate: 0.0`, `internal_heuristic_trigger_count: 2`, `internal_heuristic_trigger_apps: ["SMS_Benign", "Contacts"]`) và nêu rõ trong `§7 RQ6` (*`0/10` visible false-positive overlays; `SMS_Benign` and `Contacts` logged one suppressed heuristic check with `overlay_detected=false`*).

- [x] **2.2 & 2.3. Xử lý trung thực `Clock` (0 frame) và báo cáo đầy đủ `p95`, `p99`, `jank` trong `§7 RQ6`:**
  - Vì emulator EC2 gốc đã xóa (không tự sửa tay số liệu `Clock`), đã ghi rõ `excluded_zero_frame_app` trong `summary` của JSON và báo cáo đầy đủ cả **`p95`**, **`p99`** và **`jank`** trong `§7 RQ6` (`Markor`: `p95=18.0 ms`, `p99: 27.0 -> 31.0 ms`, `jank 3.70%`; `Settings`: `p95=36.0 ms`, `p99: 38.0 -> 101.0 ms`, `jank 2.30% -> 3.66%`; `Clock`: `0` B3 frames / sentinel `4950 ms` bị loại khỏi phép so sánh khung hình động).

---

## Nhóm 3 (RMF-3 — Major về Minh bạch hóa, ~45 phút): Làm rõ T4 DoS & Phạm vi Log Lưu trữ

- [x] **3.1. Chú thích minh bạch cho $U_{\text{att}} = 1.00$ trên Template 4 (`DoS Depletion`):**
  - Đã thêm chú thích `$^\S$` ngay dưới **Bảng 4** và nêu rõ trong `§7` (*Qualitative Analysis*) rằng $U_{\text{att}} = 1.00$ ($30/30$) bao gồm xác nhận chạm người dùng (*single-tap user touch confirmation*) ở các lượt Template 4 ($n=6$) sau khi vượt $k_{\max}=3$.

- [x] **3.2. Phân định rõ log JSON lưu trữ vs. số liệu tổng hợp từ phiên EC2 cũ trong Phụ lục A:**
  - Đã ghi rõ trong Phụ lục A danh mục đầy đủ các log JSON chi tiết lưu trong `output/*.json` (`evidence_logs_all.json`) và tách bạch phần số liệu tổng hợp từ phiên EC2 KVM đã đóng (`Mobile-Agent v3.5` $29/30$ / $48.6\,\text{s}$, B1 $150\,\text{ms}$, OS dispatch $4.18\,\text{ms}$, PSS $28.7\,\text{MB}$, `batterystats` $< 0.12\,\text{mJ}$).

---

## Nhóm 4 (RMF-4 — Minor & Hậu cần trước hạn nộp, ~1 giờ): Đồng bộ hóa Chi tiết & Kiểm tra Cuối

- [x] **4.1. Thống nhất tên tệp APK xuyên suốt bài báo:**
  - Đã thay toàn bộ 3 chỗ `b3.apk` (`discussion.tex` $\times 2$, `model.tex` $\times 1$) thành `b3secrethandle.apk` (còn `0` kết quả `b3.apk`).

- [x] **4.2. Thêm mệnh đề giới hạn đo pin rút cáp 15 phút (`§7 RQ6`):**
  - Đã bổ sung đầy đủ điều kiện đo thực tế (`screen-on ~950 mW baseline`, `4.5 mAh` coulomb quantization, `36.8 -> 34.8 C` cooling).

- [x] **4.3. Tận dụng khoảng trống Trang 11–12 để thêm bảng tóm tắt 20 app:**
  - Đã thêm bảng tóm tắt **Bảng 6 (`tab:compat_summary`)** ngay trong `§7` (3 dòng: Direct Match `7/20`, Pkg+Class `10/20`, WebView `3/20`) trong khi thân bài (`§1–§10`) vẫn kết thúc gọn trên **Trang 12**.

- [ ] **4.4. Kiểm tra biên dịch, Artifact công khai & Mốc thời gian HotCRP:**
  - [x] Biên dịch sạch 4 lượt (XeLaTeX + BibTeX), `manuscript_check.py` `PASS`, `pdfinfo` (`612 x 792 pts`), đồng bộ `ai_review_bundle/`.
  - [ ] *(Tác giả kiểm tra trước khi nộp)* Kiểm tra lại PDF ở zoom $100\%$, đẩy `output/*.json` và `evidence_logs_all.json` lên `https://github.com/SecretHandle/SecretHandle` công khai (incognito).
  - [ ] **Đăng ký Abstract trên HotCRP trước `27/11/2026 23:59 AoE` (còn 4 ngày).**
  - [ ] **Nộp bản PDF chính thức & chạy trình kiểm tra định dạng của HotCRP trước `04/12/2026 23:59 AoE` (còn 11 ngày).**