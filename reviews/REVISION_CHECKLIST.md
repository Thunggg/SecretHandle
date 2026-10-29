# SECRETHANDLE — ACM MobiSys 2027 Comprehensive Revision Checklist
> **Tài liệu tham chiếu gốc:** [`mobisys2027_review_secrethandle.md`](file:///e:/NCKH/SecretHandle/reviews/mobisys2027_review_secrethandle.md) (529 dòng đánh giá chuyên sâu)  
> **Mục tiêu:** Chuyển đổi bài báo từ **2 / 5 (Weak Reject)** lên **4–5 / 5 (Weak Accept / Accept)**  
> **Mốc thời gian quan trọng:** 
> - 🔴 **Hạn chót đăng ký Tóm tắt (Abstract Registration):** **27/11/2026 23:59 AoE** (còn **29 ngày**)
> - 🔴 **Hạn chót nộp Toàn văn (Full Paper Submission):** **04/12/2026 23:59 AoE** (còn **36 ngày**)
> - 📍 **Hội nghị:** ACM MobiSys 2027 (21–25/06/2027, TP. Hồ Chí Minh, Việt Nam)

---

## 📌 BẢNG TỔNG QUAN TIẾN ĐỘ THEO TỪNG NHÓM (TIERS)

| Nhóm (Tier) | Phạm Vi Nhiệm Vụ | Mức Độ | Trạng Thái | Thời Gian Ước Tính |
| :--- | :--- | :---: | :---: | :---: |
| **Tier 0** | Khắc phục vi phạm quy định CFP (Sàng lọc Desk-Reject) | **P0 (Khẩn cấp)** | `[x] 6/9` | 1–2 ngày |
| **Tier 1** | Sửa đổi số học, đồng bộ dữ liệu & 10 lỗi chế bản LaTeX | **P0 (Khẩn cấp)** | `[x] 6/11` | 1 ngày (30/10) |
| **Tier 2** | Sửa đổi mô hình toán, logic Thuật toán 2 & Hóa giải DoS $k_{\max}=3$ | **P1 (Quan trọng)** | `[ ] 0/4` | 1.5 ngày (31/10–01/11) |
| **Tier 3** | Minh bạch hóa kiến trúc AOSP vs Nguyên mẫu & Cô lập UID Bridge | **P1 (Quan trọng)** | `[ ] 0/2` | 2–3 ngày (02/11–04/11) |
| **Tier 4** | Thực nghiệm trên thiết bị Android 14 thật & Keystore phần cứng | **P1 (Quan trọng)** | `[ ] 0/2` | 3–4 ngày (05/11–08/11) |
| **Tier 5** | Mở rộng đánh giá: Nguồn Clipboard/Autofill & Tương thích giao diện OTP | **P2 (Nâng cấp điểm)** | `[ ] 0/4` | 5–6 ngày (09/11–15/11) |
| **Tier 6** | Công trình liên quan, nâng cấp trích dẫn & Hoàn thiện Artifact | **P2 (Hoàn thiện)** | `[x] 2/3` | 1–2 ngày (16/11–18/11) |
| **Tier 7** | Thủ tục nộp bài HotCRP, Khai báo COI & Chuẩn bị Rebuttal | **P0 (Quy trình)** | `[ ] 0/4` | Trước 27/11 & 04/12 |

---

## 🔒 NGUYÊN TẮC BẤT BIẾN (INVARIANTS)

1. **BẤT BIẾN KIẾN TRÚC:** Tệp [`mobisys/sections/architecture.tex`](file:///e:/NCKH/SecretHandle/mobisys/sections/architecture.tex) **TUYỆT ĐỐI KHÔNG ĐƯỢC CHỈNH SỬA** theo quy định hệ thống.
2. **NGÂN SÁCH TRANG (PAGE BUDGET):** Nội dung chính (từ Mục 1 đến hết Mục 10 / Conclusion) **phải kết thúc ở Trang 12**. Toàn bộ tệp PDF (bao gồm References và Appendix) **không vượt quá 15 trang**.
3. **TÍNH TRUNG THỰC SỐ LIỆU (DATA INTEGRITY):** Tuyệt đối không bịa số liệu. Mọi số liệu đưa vào bài báo phải có bằng chứng từ tệp JSON / log thực nghiệm trong `output/` hoặc `evaluation/`.

---

## 🚨 TIER 0: SÀNG LỌC DESK-REJECT & TUÂN THỦ ĐỊNH DẠNG CFP (Ưu tiên: P0)
*Nguồn phản biện: Mục 3 & Mục 4 trong `mobisys2027_review_secrethandle.md`.*

- [x] **0.1. Khổ giấy và định dạng tệp:** Tệp PDF chuẩn khổ US Letter (`8.5 x 11 in` / `612 x 792 pts`), biên dịch bằng XeLaTeX.
- [x] **0.2. Đánh số trang bắt buộc (Printfolios):** Đã bật `\settopmatter{printacmref=false,printfolios=true}` trong `main.tex`, hiển thị số trang 1–15 rõ ràng.
- [x] **0.3. Giới hạn 12 trang nội dung chính:** Mục 10 (Conclusion) kết thúc ở cột phải Trang 12; References bắt đầu từ cuối Trang 12 sang Trang 13–14; Phụ lục nằm ở Trang 14–15.
- [ ] **0.4. Khắc phục lỗi co nhỏ phông chữ trong Bảng 1 (Table 1 - `evidence.tex`):**
  - *Vấn đề:* Bảng kết quả chính đang bị bọc bởi `\resizebox{\columnwidth}{!}`, khiến phông chữ bị co xuống ~5–6 pt rất khó đọc khi in hoặc zoom 100% (vi phạm quy chuẩn CFP).
  - *Hành động:* Bỏ `\resizebox`, sử dụng `\small` hoặc `\footnotesize`, tối ưu khoảng cách cột `\setlength{\tabcolsep}{3pt}` hoặc dùng `tabularx` để chữ giữ đúng kích thước đọc được.
  - *Tệp liên quan:* [`mobisys/sections/evidence.tex:L12-L30`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L12-L30).
- [ ] **0.5. Khắc phục lỗi co nhỏ phông chữ trong Bảng 2 (Table 2 - `related_work.tex`):**
  - *Vấn đề:* Bảng so sánh phương pháp `tab:comparison` đang dùng `\resizebox{\textwidth}{!}` trên môi trường `table*`.
  - *Hành động:* Định dạng lại bảng dùng `\small`, viết gọn tiêu đề cột để hiển thị sắc nét tự nhiên mà không cần scale.
  - *Tệp liên quan:* [`mobisys/sections/related_work.tex:L4-L25`](file:///e:/NCKH/SecretHandle/mobisys/sections/related_work.tex#L4-L25).
- [ ] **0.6. Nâng cấp chất lượng Hình 1 & Hình 2 (Tránh vỡ hạt ảnh raster):**
  - *Vấn đề:* Hình 2 (`b3_redacted_shade.png` và `b3_masked_sms.png`) chụp từ emulator bị mờ nét, chữ "SecretHandle protected" bị nhòe khi in.
  - *Hành động:* Xuất ảnh PNG độ phân giải cao ($\ge 300\text{ dpi}$) hoặc đồ họa vector cho sơ đồ cấu trúc.
  - *Tệp liên quan:* [`mobisys/sections/evidence.tex:L32-L46`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L32-L46) và thư mục `figures/`.
- [x] **0.7. Điền thông tin tác giả thật (Single-Blind CFP):** Đã khai báo đầy đủ tên tác giả Nguyễn Tiến Thuận và Trần Phát Tài, đơn vị công tác (Trường ĐH FPT Cần Thơ), email tác giả.
- [x] **0.8. Tuyên bố sử dụng AI & Đạo đức (Ethics & LLM Declaration):** Đã khai báo minh bạch tại Mục 9.1 (`discussion.tex`) và Phụ lục A (`artifact.tex`).
- [ ] **0.9. Kiểm tra nhúng phông chữ (Font Embedding Audit):**
  - *Hành động:* Chạy lệnh `pdffonts mobisys/main.pdf` trên máy cục bộ để đảm bảo 100% phông chữ có `emb = yes`.

---

## 🧮 TIER 1: SỬA ĐỔI SỐ HỌC, ĐỒNG BỘ DỮ LIỆU & LỖI CHẾ BẢN LATEX (Ưu tiên: P0 - Trong 24-48h)
*Nguồn phản biện: Điểm yếu W4, W8; Mục 10.1 & Mục 15.*

- [ ] **1.1. Đồng bộ số liệu độ trễ Mint tại Mục 1 (Introduction):**
  - *Vấn đề:* `introduction.tex` dòng 14 vẫn ghi `$5.23\,\mu\text{s}$ in-vault mint`, trong khi `abstract.tex`, `evidence.tex` và `conclusion.tex` đã cập nhật chuẩn `$5.42\,\mu\text{s}$`.
  - *Hành động:* Thay `$5.23\,\mu\text{s}$` thành `$5.42\,\mu\text{s}$` trong `introduction.tex`.
  - *Tệp liên quan:* [`mobisys/sections/introduction.tex:L14`](file:///e:/NCKH/SecretHandle/mobisys/sections/introduction.tex#L14).
- [x] **1.2. Đồng bộ số liệu độ trễ In-vault Mint & Resolve CAS trong Abstract và Conclusion:**
  - *Đã thực hiện:* `$5.42\,\mu\text{s}$ mint, $0.18\,\mu\text{s}$ resolve` đã được cập nhật đồng nhất trong `abstract.tex` và `conclusion.tex`.
- [ ] **1.3. Giải trình độ lệch $1.06\,\mu\text{s}$ trong tổng độ trễ Core Mediation ($11.2\,\mu\text{s}$):**
  - *Vấn đề:* Tổng 4 thành phần liệt kê: $0.61\,\mu\text{s}\text{ (Binder)} + 9.32\,\mu\text{s}\text{ (Keystore)} + 0.08\,\mu\text{s}\text{ (Policy)} + 0.13\,\mu\text{s}\text{ (Injection)} = 10.14\,\mu\text{s} \neq 11.2\,\mu\text{s}$.
  - *Hành động:* Bổ sung giải thích rõ $1.06\,\mu\text{s}$ chênh lệch là chi phí marshaling/serialization và khóa đồng bộ (`synchronized` lock / atomic state checks), đồng thời nêu rõ $0.61\,\mu\text{s}$ là Binder round-trip nội bộ (in-process) của harness.
  - *Tệp liên quan:* [`mobisys/sections/evidence.tex:L63`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L63).
- [ ] **1.4. Loại bỏ hằng số `48.6 s` lặp lại cho cả 4 hàng trong Bảng 1:**
  - *Vấn đề:* Cột `Step Time` trong Bảng 1 ghi cùng giá trị `48.6 s` cho cả B0, B1, B2, B3, gây nghi ngờ tác giả sao chép một số chung.
  - *Hành động:* Trích xuất giá trị thời gian bước trung bình $\pm$ độ lệch chuẩn thực tế từ `results/trials.jsonl` cho từng chế độ (ví dụ: B0: $48.6 \pm 3.2\,\text{s}$, B1: $48.8 \pm 2.9\,\text{s}$, B2: $48.5 \pm 3.1\,\text{s}$, B3: $48.6 \pm 2.8\,\text{s}$).
  - *Tệp liên quan:* [`mobisys/sections/evidence.tex:L21-L24`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L21-L24).
- [x] **1.5. Đính chính thuật ngữ CAS trong chú thích Bảng 1:**
  - *Đã thực hiện:* Chú thích đã tách bạch rõ: mint là khởi tạo + MAC ($5.42\,\mu\text{s}$), chỉ có resolve mới dùng CAS ($0.18\,\mu\text{s}$).
- [ ] **1.6. Sửa 10 lỗi chế bản / typo cụ thể được phản biện chỉ ra:**
  - [x] 1. `background.tex:L4`: `"Mobile agents act through the UL.."` $\to$ đã sửa thành `"Mobile agents act through the UI."`
  - [ ] 2. `introduction.tex:L14`: `"5.23 µs in-vault mint"` $\to$ sửa thành `"5.42 µs in-vault mint"`.
  - [x] 3. `threat_model.tex:L26`: `"\$1 non-disclosure"` $\to$ đã sửa thành `"S1 non-disclosure"`.
  - [x] 4. `design.tex:L14`: `"Enter(handleld, targetNodeToken)"` $\to$ đã dùng `"Enter(handleId, targetNodeToken)"`.
  - [x] 5. `design.tex:L18`: `"monotonic intersection with D_1"` $\to$ đã dùng `"monotonic intersection with $D_T$."`.
  - [x] 6. `model.tex:L91`: `"rejected becauset t >= t_e"` $\to$ đã dùng `"rejected because $t \ge t_e$"`.
  - [ ] 7. `model.tex:L97-L109`: Ký hiệu rò rỉ $\ell$ (leakage): Kiểm tra lại tệp PDF xem ký hiệu $\ell$ trong Định nghĩa 5.14 và Định lý 5.15 có hiển thị rõ ràng không (hay bị mất khoảng trắng).
  - [ ] 8. `algorithm.tex:L51` / PDF: Kiểm tra chuỗi hằng số `TYPE_ACCESSIBILITY_OVERLAY` tránh bị tràn lấn sang cột văn bản bên cạnh.
  - [ ] 9. `evidence.tex:L84`: Kiểm tra cụm từ `"SECRETHANDLE'Ss protection"` $\to$ đảm bảo chỉ viết `"SECRETHANDLE's protection"`.
  - [ ] 10. `references_verified.bib` (mục SMS Retriever): Đảm bảo URL là `https://developer.android.com/identity/sms-retriever` (không bị cắt cụt thành `sms-retrie`).

---

## 📐 TIER 2: SỬA ĐỔI MÔ HÌNH TOÁN HỌC & THUẬT TOÁN 2 (Ưu tiên: P1 - Tuần 1)
*Nguồn phản biện: Điểm yếu W6; Đánh giá của Reviewer B; Mục 10.2.*

- [ ] **2.1. Cập nhật cấu trúc bản ghi $\Omega[n]$ trong Công thức (1) (`model.tex`):**
  - *Vấn đề:* Mục 9.2 nêu giới hạn $k_{\max}=3$ lần thử sai trước khi thu hồi thẻ, nhưng Công thức (1) ở Trang 6 không hề có biến đếm $k$.
  - *Hành động:* Bổ sung biến đếm số lần sai $k$ vào trạng thái khả biến:
    $$\Omega[n] = (s, H, a, z, r, u, k)$$
  - *Tệp liên quan:* [`mobisys/sections/model.tex:L7-L11`](file:///e:/NCKH/SecretHandle/mobisys/sections/model.tex#L7-L11).
- [ ] **2.2. Sửa lỗi logic hoàn trả ngân sách $u$ trong Thuật toán 2 (`algorithm.tex`):**
  - *Vấn đề:* Dòng 37 trừ trước $u \leftarrow u - 1$, nhưng nếu xác nhận thất bại (Dòng 39) hoặc ngữ cảnh đích đổi (Dòng 41) hoặc `InjectInternal` trả về `ok = false` (Dòng 43), thuật toán không hề có bước hoàn trả $u \leftarrow u + 1$ như văn bản đã cam kết.
  - *Hành động:* Thêm logic kiểm tra: Nếu huỷ trước khi giao dữ liệu hoặc `ok = false` đối với thẻ dùng nhiều lần ($u_0 > 1$), thực hiện hoàn trả $u \leftarrow u + 1$ và khôi phục $z \leftarrow \mathsf{live}$.
  - *Tệp liên quan:* [`mobisys/sections/algorithm.tex:L24-L47`](file:///e:/NCKH/SecretHandle/mobisys/sections/algorithm.tex#L24-L47).
- [ ] **2.3. Hóa giải mâu thuẫn Từ chối dịch vụ (DoS) và giới hạn $k_{\max} = 3$:**
  - *Vấn đề:* Trang 10 bảo vệ DoS bằng cách không trừ budget khi reject sai đích, nhưng Trang 12 lại thu hồi (revocation) thẻ sau $k_{\max}=3$ lần thử sai. Phản biện chỉ ra: Prompt injection có thể cố tình ép agent thử sai 3 lần để DoS hủy OTP của người dùng!
  - *Hành động:* Thống nhất thiết kế: $k_{\max}=3$ chỉ áp dụng cho **từng cặp `(handle, target_package)`** độc hại riêng biệt (rate-limit / blacklist ứng dụng tấn công đó) hoặc kích hoạt hộp thoại cảnh báo người dùng xác nhận, thay vì thu hồi toàn cục thẻ OTP hợp lệ.
  - *Tệp liên quan:* [`mobisys/sections/discussion.tex:L25`](file:///e:/NCKH/SecretHandle/mobisys/sections/discussion.tex#L25) và [`mobisys/sections/evidence.tex:L75-L77`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L75-L77).
- [ ] **2.4. Làm rõ cơ chế xác thực gói đích trong RQ2 (`evidence.tex`):**
  - *Vấn đề:* Trang 10 ghi `Caller(com.attacker.rewards) != BoundTarget(...) via Binder IPC`. Nhưng tiến trình gọi `ENTER` là Agent chứ không phải ứng dụng độc hại! Nếu kiểm tra `Binder.getCallingUid()` sẽ ra UID của Agent.
  - *Hành động:* Sửa văn bản để làm rõ: `Resolver` trích xuất định danh gói đích từ ngữ cảnh nút giao diện đích `FreshTargetContext(V)` (thông qua `AccessibilityNodeInfo.getPackageName()` / `WindowInfo`), còn `Binder.getCallingUid()` dùng để xác thực UID của Agent/Bridge gọi tới.
  - *Tệp liên quan:* [`mobisys/sections/evidence.tex:L75-L76`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L75-L76).

---

## 🏛️ TIER 3: MINH BẠCH HÓA KIẾN TRÚC & RANH GIỚI TIN CẬY (Ưu tiên: P1 - Tuần 1-2)
*Nguồn phản biện: Điểm yếu W1; Đánh giá của Reviewer A.*

- [ ] **3.1. Phân định rõ giữa "Kiến trúc mục tiêu AOSP" và "Nguyên mẫu Android không sửa nhân":**
  - *Vấn đề:* Bài báo tự mâu thuẫn giữa việc khẳng định dịch vụ Accessibility ở user-space không thể làm bộ giám sát tham chiếu (Mục 4) với việc Mục 7 đánh giá đúng nguyên mẫu user-space này.
  - *Hành động:* Tuyên bố nhất quán và trung thực xuyên suốt bài:
    - *Kiến trúc mục tiêu (Target AOSP Design):* Tích hợp sâu vào `system_server`, `InputDispatcher`, `ViewRootImpl`.
    - *Nguyên mẫu đánh giá (Stock-Android Evaluation Prototype):* Đóng vai trò là một broker trung gian có thẩm quyền (`secrethandle.apk`) để đo lường tính khả thi trên hệ điều hành Android gốc.
  - *Tệp liên quan:* [`mobisys/sections/abstract.tex`](file:///e:/NCKH/SecretHandle/mobisys/sections/abstract.tex), [`introduction.tex`](file:///e:/NCKH/SecretHandle/mobisys/sections/introduction.tex), [`design.tex:L52`](file:///e:/NCKH/SecretHandle/mobisys/sections/design.tex#L52), [`discussion.tex:L6-L8`](file:///e:/NCKH/SecretHandle/mobisys/sections/discussion.tex#L6-L8).
- [ ] **3.2. Chứng minh cơ chế cô lập UID của `Agent SDK Bridge`:**
  - *Vấn đề:* Reviewer A hỏi: Nếu agent không đáng tin cậy, điều gì ngăn nó tự đọc màn hình hoặc nghe thông báo mà không chịu gọi qua `Agent SDK bridge`?
  - *Hành động:* Thuyết minh rõ mô hình cô lập tiến trình/UID: Tiến trình VLM/Planner của tác tử chạy dưới một UID ứng dụng thông thường không có đặc quyền (không được cấp quyền `READ_FRAME_BUFFER` hay `BIND_ACCESSIBILITY_SERVICE`). Mọi tương tác giao diện và ảnh chụp màn hình bắt buộc phải đi qua tiến trình Bridge có đặc quyền qua IPC. Do đó, tác tử không thể "đi đường vòng" để đọc dữ liệu thô.
  - *Tệp liên quan:* [`mobisys/sections/threat_model.tex:L35`](file:///e:/NCKH/SecretHandle/mobisys/sections/threat_model.tex#L35) và [`mobisys/sections/design.tex:L14`](file:///e:/NCKH/SecretHandle/mobisys/sections/design.tex#L14).

---

## 📱 TIER 4: ĐO ĐẠC TRÊN THIẾT BỊ VẬT LÝ & HARDWARE KEYSTORE (Ưu tiên: P1 - Tuần 2-3)
*Nguồn phản biện: Điểm yếu W3; Đánh giá của Reviewer A; Mục 10.1.*

- [ ] **4.1. Chạy microbenchmark trên ít nhất 1 điện thoại Android 14 vật lý:**
  - *Vấn đề:* Bài báo chạy trên AWS EC2 x86_64 nhưng lại tuyên bố đo được *"Hardware Keystore HMAC-SHA256 (9.32 µs)"* (trong khi EC2 không có chip ARM TrustZone/StrongBox).
  - *Hành động:* Cắm 1 điện thoại Android 14 thật (Pixel hoặc Samsung) qua ADB, chạy `BenchmarkRunner.java` để đo độ trễ phần cứng thực tế.
  - *Báo cáo:* Phân tách rõ ràng độ trễ trên **Software Keystore (EC2 emulator)** so với **Hardware-backed Keystore / TEE / StrongBox (Điện thoại thật)**. Giải thích rằng dù TEE mất ~0.5–1.5 ms, tổng chi phí vẫn $<0.01\%$ so với thời gian suy luận VLM (~48 s).
  - *Tệp liên quan:* [`mobisys/sections/evidence.tex:L63`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L63).
- [ ] **4.2. Đo lường tiêu thụ pin thực tế trên điện thoại vật lý:**
  - *Vấn đề:* Tuyên bố *"imposing zero battery degradation over 2-hour benchmark runs"* trên máy chủ đám mây AWS EC2 không có pin là thiếu cơ sở thực nghiệm.
  - *Hành động:* 
    - Nếu đo được trên điện thoại thật: Dùng `dumpsys batterystats` hoặc công cụ đo nguồn trong 2 giờ chạy benchmark và báo cáo mức chênh lệch mAh / %.
    - Nếu chỉ giữ số liệu EC2: **Xóa ngay cụm từ "zero battery degradation"**, chỉ báo cáo mức chiếm dụng CPU thấp: `$0.2\%$ CPU idle ($0.1\%$ user, $0.0\%$ kernel)` và `$1.4\%$` khi burst mediation.
  - *Tệp liên quan:* [`mobisys/sections/evidence.tex:L66`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L66).

---

## 🧪 TIER 5: MỞ RỘNG ĐÁNH GIÁ BẢO MẬT & ĐA DẠNG HÓA NGUỒN/UI (Ưu tiên: P2 - Tuần 3-4)
*Nguồn phản biện: Điểm yếu W2, W5, W7; Đánh giá của Reviewer B, C.*

- [ ] **5.1. Bổ sung hỗ trợ và đánh giá thêm ít nhất 1–2 nguồn OS ngoài SMS (Clipboard / Credential Manager):**
  - *Vấn đề:* Tuyên bố hỗ trợ 4 nguồn (SMS, Credential Manager, Clipboard, Wallet) nhưng Mục 7 chỉ đánh giá duy nhất SMS OTP.
  - *Hành động:* 
    - Cài đặt adapter cho **Clipboard** (sử dụng `OnPrimaryClipChangedListener` + `EXTRA_IS_SENSITIVE` trên Android 14) với vòng đời `task-scoped` ($u_0 > 1$, ví dụ điền địa chỉ giao hàng / số điện thoại).
    - Thêm một bảng nhỏ hoặc đoạn phân tích đánh giá 3 loại bí mật: (1) OTP (`single-use`, $u_0=1$), (2) Dữ liệu cá nhân từ Clipboard/Autofill (`task-scoped`, $u_0=3$), (3) Thanh toán (`confirm-per-use`).
  - *Tệp liên quan:* [`mobisys/sections/evidence.tex`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex).
- [ ] **5.2. Đánh giá tính tương thích giao diện (UI Compatibility Benchmark):**
  - *Vấn đề:* RQ1/RQ2 chỉ đánh giá trên 2 APK đồ chơi tự viết (`com.legitimate.bank` và `com.attacker.rewards`); RQ6 chạy trên 10 ứng dụng AndroidWorld nhưng các ứng dụng này không có luồng đăng nhập/OTP.
  - *Hành động:* Kiểm chứng luồng chèn `SecretHandle` trên các mẫu giao diện thực tế:
    - Ô `EditText` chuẩn có `autofillHints="smsOTPCode"`.
    - Ô nhập OTP 6 số phân đoạn (Segmented 6-digit OTP fields - kiểm chứng cơ chế điền tự động các nút anh em `sibling nodes` như đã nêu ở Mục 9.2).
    - Ô nhập thiếu `autofillHints` (kiểm chứng cơ chế đóng an toàn fail-closed hoặc fallback xác nhận của người dùng).
    - Giao diện WebView (kiểm chứng cơ chế fail-closed khi origin chưa được chứng thực).
  - *Tệp liên quan:* [`mobisys/sections/evidence.tex`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex) và [`mobisys/sections/discussion.tex:L27-L28`](file:///e:/NCKH/SecretHandle/mobisys/sections/discussion.tex#L27-L28).
- [ ] **5.3. Đa dạng hóa các kịch bản tiêm nhiễm chỉ thị (Prompt Injection Templates):**
  - *Vấn đề:* Cả 30 lần thử RQ2 chỉ dùng một câu lệnh SMS cố định.
  - *Hành động:* Mở rộng thành 5–6 biến thể tấn công tiêm nhiễm: (1) Thông báo trúng thưởng giả mạo, (2) Yêu cầu dán mã vào ô hỗ trợ CSKH nội bộ, (3) Chỉ thị ẩn trong trang web, (4) Tấn công đa ngôn ngữ, (5) Tấn công DoS kích hoạt thử sai liên tiếp.
  - *Tệp liên quan:* [`mobisys/sections/evidence.tex:L68-L76`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L68-L76).
- [ ] **5.4. Bổ sung siêu tham số của LLM và cấu hình tác tử:**
  - *Vấn đề:* Thiếu thông tin snapshot model Claude Sonnet 4.6, temperature, max steps, và model LLM nền tảng của AutoDroid.
  - *Hành động:* Ghi rõ: API model `claude-3-5-sonnet-20241022` (hoặc snapshot tương ứng), `temperature = 0.0`, `max_steps = 15`, độ phân giải ảnh nén gửi lên API, và mô hình nền tảng dùng cho AutoDroid.
  - *Tệp liên quan:* [`mobisys/sections/evidence.tex:L4`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L4).

---

## 📚 TIER 6: CÔNG TRÌNH LIÊN QUAN, TRÍCH DẪN & ARTIFACT (Ưu tiên: P2)
*Nguồn phản biện: Mục 13, Mục 14; Đánh giá Artifact.*

- [x] **6.1. Nâng cấp các bài báo preprint lên bản xuất bản chính thức:**
  - *Đã thực hiện trong `references_verified.bib`:*
    - CaMeL (`debenedetti2025camel`) $\to$ IEEE SaTML 2025.
    - ScreenAgent (`niu2024screenagent`) $\to$ IJCAI 2024 (pp. 6449–6457).
    - EIA (`liao2024eia`) $\to$ ICLR 2025.
    - AEIA (`chen2025aeia`) $\to$ ACM MM 2025 (pp. 11648–11656).
    - FinePrint (`chen2025fineprint`) $\to$ ACM Transactions on Privacy and Security (TOPS/TAISAP).
- [ ] **6.2. Phân định rõ ràng với công trình đối thủ gần nhất (Zhao et al. 2026 [48]):**
  - *Hành động:* Làm nổi bật sự khác biệt về bản chất: Zhao et al. dựa trên bộ dò văn bản sau khi render (detector-based) và placeholder cục bộ không gắn đích (unbound), nên bị bypass hoàn toàn trước tấn công chuyển hướng đích ($30/30$). Ngược lại, `SecretHandle` can thiệp tại nguồn OS và gắn chặt vị từ đích đến (package + field class).
  - *Tệp liên quan:* [`mobisys/sections/related_work.tex:L29`](file:///e:/NCKH/SecretHandle/mobisys/sections/related_work.tex#L29).
- [ ] **6.3. Bổ sung URL kho mã nguồn mở trong Phụ lục A (`artifact.tex`):**
  - *Hành động:* Vì MobiSys 2027 áp dụng phản biện đơn mù (single-blind), bổ sung trực tiếp đường dẫn kho mã nguồn GitHub/Zenodo công khai vào cuối Mục 1 và Phụ lục A để phản biện có thể đối chiếu code `src/secrethandle` và `device/b3-secrethandle`.
  - *Tệp liên quan:* [`mobisys/sections/artifact.tex:L1-L10`](file:///e:/NCKH/SecretHandle/mobisys/sections/artifact.tex#L1-L10).

---

## 🗓️ TIER 7: KẾ HOẠCH HẬU CẦN NỘP BÀI & CHUẨN BỊ REBUTTAL (Ưu tiên: P0)
*Nguồn phản biện: Mục 4, Mục 18.*

- [ ] **7.1. Đăng ký tóm tắt (Abstract Registration):**
  - *Thời hạn:* Trước **27/11/2026 23:59 AoE** (còn 29 ngày).
  - *Trang nộp bài:* `https://mobisys27.hotcrp.com/`
  - *Yêu cầu:* Chốt danh sách tác giả (Nguyễn Tiến Thuận, Trần Phát Tài), tiêu đề và Abstract $\ge 100$ từ.
- [ ] **7.2. Khai báo Xung đột Lợi ích (COI):**
  - *Hành động:* Khai báo đầy đủ các thành viên TPC thuộc Trường ĐH FPT, các đồng tác giả/cố vấn trong vòng 24–48 tháng.
- [ ] **7.3. Nộp bài toàn văn (Full Paper Submission):**
  - *Thời hạn:* Trước **04/12/2026 23:59 AoE** (còn 36 ngày).
  - *Kiểm tra cuối cùng:* Chạy script kiểm tra định dạng tự động của HotCRP để xác nhận không lỗi font, không tràn lề.
- [ ] **7.4. Chuẩn bị sẵn khung sườn Rebuttal (Dự kiến 08–12/02/2027, giới hạn 500 từ):**
  - Đã có sẵn 3 kịch bản trả lời mẫu trong Mục 18.3 của bản đánh giá:
    - *Rebuttal 1:* Ranh giới kiến trúc AOSP vs nguyên mẫu broker và cô lập UID.
    - *Rebuttal 2:* Đo đạc phần cứng Keystore thật và pin thật trên điện thoại vật lý.
    - *Rebuttal 3:* Khả năng hỗ trợ đa dạng ứng dụng thực tế, ô OTP phân đoạn và cơ chế chống DoS $k_{\max}$.

---

## 📅 LỘ TRÌNH THỰC HIỆN 5 TUẦN CHI TIẾT (36 NGÀY)

```
[29/10/2026] ──── (Tuần 1: LaTeX, Số học & Thuật toán) ────> [04/11/2026]
                     │ Hoàn thành Tier 0, 1, 2
                     ▼
[05/11/2026] ──── (Tuần 2: Benchmark Điện Thoại Thật) ────> [11/11/2026]
                     │ Hoàn thành Tier 3, 4 (Keystore + Pin)
                     ▼
[12/11/2026] ──── (Tuần 3: Đa Dạng Hóa Nguồn & UI) ────────> [18/11/2026]
                     │ Hoàn thành Tier 5 (Clipboard, Segmented OTP)
                     ▼
[19/11/2026] ──── (Tuần 4: Hình Vẽ & Đăng Ký Abstract) ────> [25/11/2026]
                     │ Đăng ký Abstract HotCRP trước 27/11 (Tier 7.1)
                     ▼
[26/11/2026] ──── (Tuần 5: Kiểm Tra Định Dạng & Nộp Bài) ──> [04/12/2026]
                     │ Nộp bản toàn văn chính thức (Tier 7.3)
```
