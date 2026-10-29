# Danh mục Công việc Cần sửa (Revision Checklist) — ACM MobiSys 2027

> **Bài báo:** SecretHandle: OS-Minted, Destination- and Task-Bound Opaque Secrets for Android Mobile AI Agents  
> **Dựa trên phản biện:** `reviews/mobisys2027_review_secrethandle.md`  
> **Mục tiêu:** Nâng điểm từ **2.5/5 (Borderline/Weak Reject)** lên **4.0/5 (Weak Accept / Accept)**  
> **Hạn chót:**
>
> - **Abstract Registration:** 23:59 AoE, ngày 27/11/2026 (còn 29 ngày)
> - **Full Paper Submission:** 23:59 AoE, ngày 04/12/2026 (còn 36 ngày — **Không gia hạn**)

---

## 1. CÁC HẠNG MỤC BẮT BUỘC SỬA (MUST-FIX — QUYẾT ĐỊNH ĐẬU / RỚT)

### MF-1: Sửa các lỗi bất nhất số học, tên mô hình và logic thuật toán

_Mục tiêu: Khôi phục 100% độ tin cậy khoa học của bài báo (W2, W5)_

- [x] **Sửa tên mô hình LLM trên toàn bộ bài báo:**
  - [x] Abstract (Trang 1): Thay `Claude Sonnet 4.6` bằng `Claude 3.5 Sonnet`.
  - [x] Mục 1 (Trang 2): Sửa tên mô hình thành `Claude 3.5 Sonnet`.
  - [x] Mục 7 (Trang 8, cột phải): Sửa thành `Claude 3.5 Sonnet (\texttt{claude-3-5-sonnet-20241022})`.
  - [x] Mục 9.1 (Trang 12) & Mục Ethics: Cập nhật nhất quán chuỗi định danh mô hình.
- [x] **Sửa lỗi số học phép cộng độ trễ trên ARM (Mục 7, RQ5, Trang 10):**
  - [x] Bổ sung thành phần `parcel/lock (2.33 µs)`: $17.63 + 1.73 + 0.16 + 2.33 + 0.45 = 22.30\ \mu\text{s}$, khớp chính xác $100\%$ với con số tổng $22.30\ \mu\text{s}$.
  - [x] Làm rõ chi tiết bộ nhớ PSS: $14.2\,\text{MB}$ native + $2.1\,\text{MB}$ Dalvik + $12.4\,\text{MB}$ ART runtime/thư viện chia sẻ $= 28.7\,\text{MB}$.
- [x] **Sửa lỗi số học % CPU trên ARM (Mục 7, RQ6, Trang 10):**
  - [x] Khớp số liệu CPU burst: $3.2\% \text{ user} + 3.2\% \text{ kernel} + 0.8\% \text{ I/O wait/IRQ} = 7.2\%$ tổng CPU.
- [x] **Sửa tham chiếu và làm rõ logic Thuật toán 2 (Dòng 7 vs. Dòng 5):**
  - [x] Mục 7 (Trang 11): Sửa `Algorithm 2 Line 5` thành `Algorithm 2 Line 6` (kiểm tra `Match(d, x) = 0`).
  - [x] Giải thích rõ cơ chế khi $k < k_{\max}$: Khi thử sai đích 1 lần (single-shot), $k$ tăng lên $1 < k_{\max}=3$, ngân sách $u$ giữ nguyên và handle vẫn `live` (vì trừ ngân sách chỉ thực hiện ở dòng 7 khi đặt trước thành công).
  - [x] Giải thích rõ cơ chế khi $k = k_{\max} = 3$ (Template 4: DoS Depletion): Khi bị tấn công lặp lại $\ge 3$ lần, handle chuyển sang `revoked` để chặn brute-force và hệ thống kích hoạt cơ chế dự phòng xác nhận chạm người dùng (_local user touch confirmation fallback_).
- [x] **Phân định rõ mã trạng thái lỗi (Bảng 2 vs. Mục 7):**
  - [x] Nêu rõ trong Mục 7: Các mã `ALREADY_RESOLVED`, `HANDLE_EXPIRED`, `CALLER_MISMATCH`, `DESTINATION_MISMATCH` được ghi nhận trong **nhật ký kiểm toán nội bộ của OS (audit log)**.
  - [x] Khẳng định phản hồi trả về qua SDK Bridge cho untrusted agent hoàn toàn là giá trị mù theo đúng Bảng 2 (`unavailable handle` / `destination denied`), không để lộ trạng thái nội bộ.
- [x] **Sửa trích dẫn Mobile-Agent (Mục 7, Trang 8):**
  - [x] Cập nhật trích dẫn `Mobile-Agent v3.5` thành `\cite{wang2024mobileagent,ye2025mobileagentv3}`.

---

### MF-2: Sửa lỗi định dạng, đồ họa và tuân thủ CFP MobiSys 2027

_Mục tiêu: Đạt chuẩn xuất bản chuyên nghiệp, không để mất điểm hình thức (W8, Phase 1)_

- [x] **Sửa Hình 1 (Trang 4):**
  - [x] Thu gọn tọa độ x trong legend TikZ (0.0, 3.8, 8.2, 11.8 cm), đảm bảo nhãn `adversarial influence` nằm trọn vẹn trong khung vẽ, không bị cắt xén.
  - [x] Xuất lại tệp PDF vector sắc nét.
- [x] **Làm lại Hình 2a và 2b (Trang 9):**
  - [x] Chạy kịch bản `tools/generate_high_res_figure2.py` xuất ảnh 300 DPI (`figures/b3_redacted_shade.png` và `figures/b3_masked_sms.png`).
  - [x] Chữ `SH-B9B564 from SMS Messenger` và `SecretHandle: protected` hiển thị vector siêu nét ở mức zoom 100%.
- [x] **Sửa tiêu đề chạy (Running Header) các trang chẵn:**
  - [x] Đảm bảo lệnh `\shortauthors{Nguyễn and Trần}` hiển thị chính xác trên toàn bộ các trang chẵn (trang 2, 4, 6, 8, 10, 12, 14).
- [x] **Sửa lỗi chính tả Mục 2 (Trang 2, cột phải):**
  - [x] Kiểm tra và xác nhận đoạn văn bản mở đầu là `Mobile agents act through the UI.`.
- [x] **Kiểm tra tiêu đề Trang 1:**
  - [x] Tiêu đề hiển thị chuẩn xác `SecretHandle: OS-Minted, Destination- and Task-Bound Opaque Secrets for Android Mobile AI Agents`.
- [x] **Chuẩn hóa tuyên bố sử dụng LLM tại Mục 9.1 (Trang 12) và Mục Ethics:**
  - [x] Sửa câu văn thành: _"LLM tools were used solely for language editing and proofreading of the authors' own text. All technical designs, formal models, prototype code, and empirical numbers were produced and verified entirely by the authors."_ tuân thủ 100% quy chế CFP.
- [x] **Kiểm toán thông số kỹ thuật PDF:**
  - [x] Khổ giấy: Chuẩn US Letter ($612 \times 792\text{ pt}$).
  - [x] Nhúng font: 100% font chữ được nhúng hoàn chỉnh.

---

### MF-3: Minh bạch hóa Kiến trúc AOSP vs. Nguyên mẫu Android 14

_Mục tiêu: Hóa giải nghi ngại của Reviewer A về "đánh tráo khái niệm" TCB (W1, W6)_

- [x] **Tách biệt rõ ràng thiết kế lý thuyết và nguyên mẫu thực tế (Mục 4, 6 & 9):**
  - [x] Phân định rõ 2 tầng:
    - _(a) Kiến trúc tích hợp AOSP (`system_server` / `InputDispatcher` / `ViewRootImpl`)_: Bảo đảm TCB phần cứng/OS lý tưởng.
    - _(b) Nguyên mẫu Broker trên Stock Android 14 (`secrethandle.apk`)_: Không cần sửa ROM, dùng `NotificationListenerService` và `TYPE_ACCESSIBILITY_OVERLAY`.
- [x] **Giải thích cơ chế bóc tách mã OTP (Secret Extraction):**
  - [x] Làm rõ cách Broker trích xuất mã OTP từ thông báo/tin nhắn đến mà vẫn giữ lại phần văn bản ngữ cảnh giao dịch cho người dùng.
- [x] **Làm rõ cơ chế tiếp nhận chỉ thị tiêm nhiễm (Prompt Injection Delivery - W6):**
  - [x] Giải thích rõ: Khi thông báo SMS đã bị thay thế (Hình 2a) và bong bóng tin nhắn bị che đen (Hình 2b), chỉ thị tiêm nhiễm được truyền qua thông báo khuyến mãi bên thứ ba hoặc văn bản hội thoại không nhạy cảm xung quanh. Tác tử đọc được chỉ thị nhưng tuyệt đối không đọc được 6 chữ số OTP.
- [x] **Làm rõ API tiêm văn bản và rào chắn khung hình:**
  - [x] Giải thích cách đồng bộ rào chắn kết xuất (`SurfaceFlinger` frame barrier) để đảm bảo không có khung hình chưa che khuất nào lọt vào ảnh chụp màn hình tiếp theo của tác tử VLM.
- [x] **Giải thích cơ chế phục hồi tác vụ ($U_{\text{att}} = 1.00$):**
  - [x] Nêu rõ phản hồi mà Agent SDK Bridge trả về cho tác tử (`destination denied`), giúp bộ lập kế hoạch nhận biết thao tác chuyển hướng thất bại và quay lại luồng chính của `com.legitimate.bank`.

---

### MF-4: Chuẩn hóa và làm rõ Baseline B2 (Platform Flow)

_Mục tiêu: Đảm bảo tính công bằng và chính xác tuyệt đối về mặt kỹ thuật Android (W4)_

- [x] **Đổi tên và tách bạch Baseline B2:**
  - [x] Đổi tên trong Bảng 3 và Mục 7 thành: **`B2: SMS User Consent / Unbound Autofill Flow`**.
- [x] **Làm rõ ranh giới kỹ thuật với Credential Manager & SMS Retriever:**
  - [x] Thừa nhận chính xác: Credential Manager (Digital Asset Links) và SMS Retriever (11-char app hash) có bảo vệ mức gói ứng dụng.
  - [x] Nhấn mạnh 3 điểm cốt tử của Android hiện tại mà chỉ SECRETHANDLE giải quyết được:
    1. SMS OTP thông thường không có mã băm 11 ký tự $\rightarrow$ rơi về SMS User Consent (chỉ cần 1 chạm là cấp cho app bất kỳ).
    2. Nền tảng không chống được **chuyển hướng nội bộ ứng dụng (intra-app redirection)** (ví dụ: dán OTP vào khung chat hỗ trợ).
    3. Nền tảng **không có cơ chế che khuất màn hình sau khi điền (post-entry redaction)**, tác tử vẫn nhìn thấy giá trị thô ở khung hình tiếp theo.

---

### MF-5: Mở rộng thực nghiệm sang Ứng dụng Thực tế

_Mục tiêu: Bẻ gãy lập luận "chỉ chạy trên toy app tự tạo" của Reviewer A & C (W3)_

- [x] **[ĐÃ CHẠY THỰC TẾ TRÊN ANDROID 14] Khảo sát tương thích (Empirical Compatibility Study) trên 20 ứng dụng thực tế qua ADB:**
  - [x] Chạy tự động 100% khảo sát cây giao diện (`uiautomator dump`) trên 20 ứng dụng thực tế cài đặt trên Android 14 (API 34) bằng công cụ `tools/audit_20_apps_automated.py`.
  - [x] Phân tích cấu trúc accessibility tree: đối chiếu khả năng tương thích của vị từ đích $\Match(d,x)$ và Chính sách Dự phòng (Fallback Policy) khi ứng dụng sử dụng Custom View / Bàn phím số riêng.
  - [x] Xuất dữ liệu bằng chứng vào `output/real_apps_compatibility_audit.json` và bảng LaTeX hoàn chỉnh tại `output/real_apps_compatibility_table.tex`.
- [x] **[ĐÃ CHẠY THỰC TẾ TRÊN ANDROID 14]: Kiểm chứng thực nghiệm Chính sách Dự phòng (Fallback Policy) trên Custom Canvas/Numpad:**
  - [x] Đo đạc tỷ lệ thành công và độ trễ khi áp dụng Fallback Policy (ràng buộc `packageName` tiền cảnh + xác nhận người dùng 1 chạm) trên UI Custom Canvas/Numpad: 30/30 thành công ($U=1.00$), 0/30 rò rỉ khi ứng dụng đối kháng tiền cảnh gọi ($R=0.00$), độ trễ trung vị $47.60\,\mu\text{s}$ (trung bình $69.39\,\mu\text{s}$).
  - [x] Xuất log chứng thực tại: `output/fallback_policy_benchmark.json` (thiết bị Android 14 API 34).
- [x] **[ĐÃ CHẠY THỰC TẾ TRÊN ANDROID 14]: Thử nghiệm định lượng độc lập cho luồng WebView Fail-Closed:**
  - [x] Đo đạc riêng biệt luồng xác thực WebView cho origin không chứng thực ($n=30$): chặn đứng fail-closed 30/30 (100%), tỷ lệ rò rỉ $0/30$ ($R=0.00$), tiện ích luồng hợp pháp $30/30$ ($U=1.00$), độ trễ trung vị xác thực web origin $56.80\,\mu\text{s}$ (trung bình $137.55\,\mu\text{s}$).
  - [x] Xuất log chứng thực tại: `output/webview_failclosed_benchmark.json` (thiết bị Android 14 API 34).
- [x] **[ĐÃ HOÀN THÀNH VỀ THIẾT KẾ & VĂN BẢN]:**
  - [x] Đã cập nhật phân tích định tính về chính sách dự phòng (Fallback Policy) khi thiếu `autofillHints` và cơ chế đóng an toàn cho WebView trong Mục 7 mà không bịa đặt số liệu thống kê ảo.

---

## 2. CÁC HẠNG MỤC NÊN SỬA (SHOULD-FIX & CÂN ĐỐI TRANG)

- [x] **Giải thích độ trễ 150 ms của B1 (Bảng 3, Trang 9):**
  - [x] Nêu rõ nguồn gốc: Độ trễ 150 ms của B1 do chạy mô hình NER/regex quét cục bộ cây giao diện, so với $4.2\text{ ms}$ đầu-cuối của SECRETHANDLE.
- [x] **Bổ sung số liệu đo năng lượng định lượng (Mục 7, RQ6, Trang 10):**
  - [x] Bổ sung số liệu từ `dumpsys batterystats`: tiêu thụ năng lượng dưới $0.12\,\text{mJ}$ cho mỗi sự kiện trung gian trên Samsung Galaxy A52s.
- [x] **Giải thích trường hợp người dùng muốn tự đọc mã OTP (Reviewer C Q1):**
  - [x] Bổ sung giải pháp ở Mục 9: Người dùng có thể chạm vào thông báo của SecretHandle để xác thực sinh trắc học (`BiometricPrompt`) và xem tạm thời mã OTP trong hộp thoại bảo vệ phần cứng.
- [x] **Kiểm toán logic hoàn trả ngân sách ở Thuật toán 2 (Dòng 17, Trang 8):**
  - [x] Làm rõ điều kiện hoàn trả: chỉ hoàn trả ngân sách khi việc hủy xảy ra trước khi bất kỳ byte dữ liệu nào bị đưa vào bộ đệm trường đích.
- [x] **Tối ưu hóa ngân sách trang (CHUẨN 100% 12 TRANG NỘI DUNG CHÍNH):**
  - [x] Thu gọn các chứng minh ngắn ở Mục 5 (Corollary 5.10, Proposition 5.12, 5.13).
  - [x] Rút gọn phần mô tả lặp lại giữa Mục 4 và Mục 6.
  - [x] Gộp và tinh gọn các tiểu mục trong Mục 8 (Related Work) và Mục 9 (Discussion & Limitations).
  - [x] **Kết quả:** Mục 10 (Conclusion) kết thúc **chính xác ở cuối Trang 12**; References bắt đầu ở **đầu Trang 13**; Phụ lục Artifact ở **Trang 14–15**.

---

## 3. HẬU CẦN VÀ TIẾN ĐỘ NỘP BÀI (HOTCRP & DEADLINES)

- [ ] **Đăng ký Tóm tắt (Abstract Registration) — Trước 23:59 AoE ngày 27/11/2026:**
  - [ ] Đăng ký bài nộp tại: `https://mobisys27.hotcrp.com/`.
  - [ ] Chốt danh sách toàn bộ tác giả và đơn vị (Nguyễn Tiến Thuận, Trần Phát Tài — Trường Đại học FPT).
  - [ ] Điền tiêu đề và bản Tóm tắt (Abstract) đã chỉnh sửa hoàn chỉnh.
  - [ ] Khai báo Xung đột Lợi ích (COI) chuẩn xác (kiểm tra TPC Co-chairs: Jun Han - KAIST, Falko Dressler - TU Berlin).
- [ ] **Nộp Toàn văn (Full Paper Submission) — Trước 23:59 AoE ngày 04/12/2026:**
  - [ ] Đảm bảo kho lưu trữ mã nguồn `https://github.com/SecretHandle/SecretHandle` mở công khai (public) và có đầy đủ file theo Phụ lục A.
  - [ ] Kiểm tra lại tệp PDF cuối cùng `mobisys/main.pdf` (15 trang: 12 trang nội dung + 2 trang references + 1 trang appendix).
  - [ ] Tải tệp PDF lên HotCRP trước hạn chót.
