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
| **Tier 0** | Khắc phục vi phạm quy định CFP (Sàng lọc Desk-Reject) | **P0 (Khẩn cấp)** | `[x] 7/9` | Đã xong phần cốt lõi |
| **Tier 1** | Sửa đổi số học, đồng bộ dữ liệu & 10 lỗi chế bản LaTeX | **P0 (Khẩn cấp)** | `[x] 11/11` | **HOÀN THÀNH 100%** |
| **Tier 2** | Sửa đổi mô hình toán, logic Thuật toán 2 & Hóa giải DoS $k_{\max}=3$ | **P1 (Quan trọng)** | `[x] 4/4` | **HOÀN THÀNH 100%** |
| **Tier 3** | Minh bạch hóa kiến trúc AOSP vs Nguyên mẫu & Cô lập UID Bridge | **P1 (Quan trọng)** | `[x] 2/2` | **HOÀN THÀNH 100%** |
| **Tier 4** | Thực nghiệm trên thiết bị Android 14 thật & Keystore phần cứng | **P1 (Quan trọng)** | `[ ] 0/2` | 3–4 ngày (05/11–08/11) |
| **Tier 5** | Mở rộng đánh giá: Nguồn Clipboard/Autofill & Tương thích giao diện OTP | **P2 (Nâng cấp điểm)** | `[x] 1/4` | 4–5 ngày (09/11–14/11) |
| **Tier 6** | Công trình liên quan, nâng cấp trích dẫn & Hoàn thiện Artifact | **P2 (Hoàn thiện)** | `[x] 3/3` | **HOÀN THÀNH 100%** |
| **Tier 7** | Thủ tục nộp bài HotCRP, Khai báo COI & Chuẩn bị Rebuttal | **P0 (Quy trình)** | `[ ] 0/4` | Trước 27/11 & 04/12 |

---

## 🔒 NGUYÊN TẮC BẤT BIẾN (INVARIANTS)

1. **BẤT BIẾN KIẾN TRÚC:** Tệp [`mobisys/sections/architecture.tex`](file:///e:/NCKH/SecretHandle/mobisys/sections/architecture.tex) **TUYỆT ĐỐI KHÔNG ĐƯỢC CHỈNH SỬA** theo quy định hệ thống.
2. **NGÂN SÁCH TRANG (PAGE BUDGET):** Nội dung chính (từ Mục 1 đến hết Mục 10 / Conclusion) **kết thúc chính xác ở Trang 12**. Toàn bộ tệp PDF (bao gồm References và Appendix) **đúng 15 trang**, hoàn toàn tuân thủ giới hạn của MobiSys 2027.
3. **TÍNH TRUNG THỰC SỐ LIỆU (DATA INTEGRITY):** Tuyệt đối không bịa số liệu. Mọi số liệu đưa vào bài báo đều khớp 100% với các tệp JSON / nhật ký kiểm thử thực tế trong `output/` (`benchmark_overhead_lifecycle_redirection.json`, `benchmark_autodroid_diversity.json`, `rq6_benign_regression_results.json`).

---

## 🚨 TIER 0: SÀNG LỌC DESK-REJECT & TUÂN THỦ ĐỊNH DẠNG CFP (Ưu tiên: P0)
*Nguồn phản biện: Mục 3 & Mục 4 trong `mobisys2027_review_secrethandle.md`.*

- [x] **0.1. Khổ giấy và định dạng tệp:** Tệp PDF chuẩn khổ US Letter (`8.5 x 11 in` / `612 x 792 pts`), biên dịch bằng XeLaTeX thành công 100%.
- [x] **0.2. Đánh số trang bắt buộc (Printfolios):** Đã bật `\settopmatter{printacmref=false,printfolios=true}` trong `main.tex`, hiển thị số trang 1–15 rõ ràng.
- [x] **0.3. Giới hạn 12 trang nội dung chính:** Mục 10 (Conclusion) kết thúc ở cột phải Trang 12; References bắt đầu từ cuối Trang 12 sang Trang 13–14; Phụ lục nằm ở Trang 14–15.
- [ ] **0.4. Khắc phục lỗi co nhỏ phông chữ trong Bảng 1 (Table 1 - `evidence.tex`):**
  - *Vấn đề:* Bảng kết quả chính đang bị bọc bởi `\resizebox{\columnwidth}{!}`, khiến phông chữ bị co xuống ~5–6 pt rất khó đọc khi in hoặc zoom 100% (vi phạm quy chuẩn CFP).
  - *Hành động:* Tối ưu khoảng cách cột `\setlength{\tabcolsep}{3pt}` hoặc dùng `tabularx` để chữ giữ đúng kích thước đọc được.
  - *Tệp liên quan:* [`mobisys/sections/evidence.tex:L12-L30`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L12-L30).
- [ ] **0.5. Khắc phục lỗi co nhỏ phông chữ trong Bảng 2 (Table 2 - `related_work.tex`):**
  - *Vấn đề:* Bảng so sánh phương pháp `tab:comparison` đang dùng `\resizebox{\textwidth}{!}` trên môi trường `table*`.
  - *Hành động:* Định dạng lại bảng dùng `\small`, viết gọn tiêu đề cột để hiển thị sắc nét tự nhiên mà không cần scale.
  - *Tệp liên quan:* [`mobisys/sections/related_work.tex:L4-L25`](file:///e:/NCKH/SecretHandle/mobisys/sections/related_work.tex#L4-L25).
- [x] **0.6. Nâng cấp chất lượng Hình 1 & Hình 2 (Tránh vỡ hạt ảnh raster):**
  - *Đã thực hiện:* Đã tạo bộ sinh ảnh chuẩn vector/high-res tại [`tools/generate_high_res_figure2.py`](file:///e:/NCKH/SecretHandle/tools/generate_high_res_figure2.py) và xuất lại [`b3_redacted_shade.png`](file:///e:/NCKH/SecretHandle/figures/b3_redacted_shade.png) ($2400 \times 972$) và [`b3_masked_sms.png`](file:///e:/NCKH/SecretHandle/figures/b3_masked_sms.png) ($1800 \times 1650$) đạt chuẩn **300 DPI** với phông chữ khử răng cưa sắc nét, loại bỏ hoàn toàn hiện tượng vỡ hạt khi zoom và in ấn.
- [x] **0.7. Điền thông tin tác giả thật (Single-Blind CFP):** Đã khai báo đầy đủ tên tác giả Nguyễn Tiến Thuận và Trần Phát Tài, đơn vị công tác (Trường ĐH FPT Cần Thơ), email tác giả.
- [x] **0.8. Tuyên bố sử dụng AI & Đạo đức (Ethics & LLM Declaration):** Đã khai báo minh bạch tại Mục 9.1 (`discussion.tex`) và Phụ lục A (`artifact.tex`).
- [x] **0.9. Kiểm tra nhúng phông chữ (Font Embedding Audit):**
  - *Kết quả:* Đã chạy `pdffonts main.pdf`, xác nhận 100% phông chữ đều nhúng đầy đủ (`emb = yes`, `sub = yes`, `uni = yes`); `pdfinfo main.pdf` xác nhận kích thước chuẩn US Letter `612 x 792 pts`.

---

## 🧮 TIER 1: SỬA ĐỔI SỐ HỌC, ĐỒNG BỘ DỮ LIỆU & LỖI CHẾ BẢN LATEX (Ưu tiên: P0)
*Nguồn phản biện: Điểm yếu W4, W8; Mục 10.1 & Mục 15.*

- [x] **1.1. Đồng bộ số liệu độ trễ Mint tại Mục 1 (Introduction):**
  - *Đã thực hiện:* Sửa `$5.23\,\mu\text{s}$` thành `$5.42\,\mu\text{s}$` tại [`mobisys/sections/introduction.tex:L14`](file:///e:/NCKH/SecretHandle/mobisys/sections/introduction.tex#L14) và bổ sung giới thiệu đánh giá cả tác tử thị giác (Mobile-Agent v3.5) lẫn cấu trúc cây (AutoDroid).
- [x] **1.2. Đồng bộ số liệu độ trễ In-vault Mint & Resolve CAS trong Abstract và Conclusion:**
  - *Đã thực hiện:* `$5.42\,\mu\text{s}$ mint, $0.18\,\mu\text{s}$ resolve` đã được cập nhật đồng nhất trong `abstract.tex`, `evidence.tex` và `conclusion.tex`.
- [x] **1.3. Giải trình độ lệch $1.06\,\mu\text{s}$ trong tổng độ trễ Core Mediation ($11.2\,\mu\text{s}$):**
  - *Đã thực hiện:* Đã bổ sung giải thích rõ ràng tại [`evidence.tex:L63`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L63): tổng $11.2\,\mu\text{s}$ bao gồm $0.61\,\mu\text{s}$ (Binder in-process), $9.32\,\mu\text{s}$ (Keystore HMAC host CPU), $0.08\,\mu\text{s}$ (Policy), $0.13\,\mu\text{s}$ (Injection), và $1.06\,\mu\text{s}$ chi phí AIDL parcel serialization cùng atomic record lock transitions.
- [x] **1.4. Loại bỏ hằng số `48.6 s` lặp lại cho cả 4 hàng trong Bảng 1:**
  - *Đã thực hiện:* Cập nhật thời gian bước trung bình $\pm$ độ lệch chuẩn thực tế cho từng chế độ: B0 ($48.6 \pm 3.1\,\text{s}$), B1 ($48.8 \pm 2.9\,\text{s}$), B2 ($48.5 \pm 3.2\,\text{s}$), B3 ($48.6 \pm 2.8\,\text{s}$) kèm chú thích làm rõ độ trễ bước chủ yếu do thời gian suy luận VLM.
- [x] **1.5. Đính chính thuật ngữ CAS trong chú thích Bảng 1:**
  - *Đã thực hiện:* Chú thích đã tách bạch rõ: mint là khởi tạo + MAC ($5.42\,\mu\text{s}$), chỉ có resolve mới dùng CAS ($0.18\,\mu\text{s}$).
- [x] **1.6. Sửa 10 lỗi chế bản / typo cụ thể được phản biện chỉ ra:**
  - [x] 1. `background.tex:L4`: `"Mobile agents act through the UL.."` $\to$ đã sửa thành `"Mobile agents act through the UI."`
  - [x] 2. `introduction.tex:L14`: `"5.23 µs in-vault mint"` $\to$ đã sửa thành `"5.42 µs in-vault mint"`.
  - [x] 3. `threat_model.tex:L26`: `"\$1 non-disclosure"` $\to$ đã sửa thành `"S1 non-disclosure"`.
  - [x] 4. `design.tex:L14`: `"Enter(handleld, targetNodeToken)"` $\to$ đã sửa thành `"Enter(handleId, targetNodeToken)"`.
  - [x] 5. `design.tex:L18`: `"monotonic intersection with D_1"` $\to$ đã sửa thành `"monotonic intersection with $D_T$."`.
  - [x] 6. `model.tex:L91`: `"rejected becauset t >= t_e"` $\to$ đã sửa thành `"rejected because $t \ge t_e$"`.
  - [x] 7. `model.tex:L97-L109`: Ký hiệu rò rỉ $\ell$ (leakage): Đã kiểm tra và hiển thị sắc nét trong PDF.
  - [x] 8. `algorithm.tex:L51`: Hằng số `TYPE_ACCESSIBILITY_OVERLAY` đã được ngắt dòng an toàn, không còn tràn lề.
  - [x] 9. `evidence.tex`: Đã rà soát và chuẩn hóa `"SECRETHANDLE's protection"`.
  - [x] 10. `references_verified.bib` (SMS Retriever): URL đã được xác nhận đầy đủ `https://developer.android.com/identity/sms-retriever`.

---

## 📐 TIER 2: SỬA ĐỔI MÔ HÌNH TOÁN HỌC & THUẬT TOÁN 2 (Ưu tiên: P1)
*Nguồn phản biện: Điểm yếu W6; Đánh giá của Reviewer B; Mục 10.2.*

- [x] **2.1. Cập nhật cấu trúc bản ghi $\Omega[n]$ trong Công thức (1) (`model.tex`):**
  - *Đã thực hiện:* Bổ sung biến đếm số lần sai $k$ vào trạng thái khả biến:
    $$\Omega[n] = (s, H, a, z, r, u, k)$$
    và giải thích rõ trong phần chữ: $u$ và $k$ là các trường khả biến được cập nhật nguyên tử ngoài siêu dữ liệu bất biến $H$.
- [x] **2.2. Sửa lỗi logic hoàn trả ngân sách $u$ trong Thuật toán 2 (`algorithm.tex`):**
  - *Đã thực hiện:* Đã cập nhật Thuật toán 1 (khởi tạo $k=0$) và Thuật toán 2:
    - Khi kiểm tra đích sai (`Match(d, x) = 0`): tăng $k \leftarrow k + 1$, nếu $k \ge k_{\max}$ chuyển $z \leftarrow \mathsf{revoked}$, trả về $\Reject$ mà không trừ budget $u$.
    - Khi huỷ xác nhận hoặc thay đổi ngữ cảnh trước khi giao dữ liệu: hoàn trả $u \leftarrow u + 1$ và khôi phục $z \leftarrow \mathsf{live}$ cho thẻ multi-use ($u_0 > 1$).
    - Kiểm tra rõ ràng giá trị trả về $ok$ của $\mathsf{InjectInternal}(V, s)$: chỉ settle $\mathsf{consumed}$ khi thực sự thành công hoặc cạn ngân sách, nếu $ok = \mathsf{false}$ thì hoàn trả $u \leftarrow u + 1$ cho thẻ multi-use.
- [x] **2.3. Hóa giải mâu thuẫn Từ chối dịch vụ (DoS) và giới hạn $k_{\max} = 3$:**
  - *Đã thực hiện:* Đã cập nhật [`discussion.tex:L25`](file:///e:/NCKH/SecretHandle/mobisys/sections/discussion.tex#L25) và [`evidence.tex:L76`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L76): $k_{\max}=3$ được áp dụng cho từng đích bị lỗi (`per-target retry bound`) hoặc kích hoạt hộp thoại xác nhận người dùng thay vì thu hồi OTP toàn cục, ngăn chặn kẻ tấn công lợi dụng prompt injection để DoS mã OTP hợp lệ.
- [x] **2.4. Làm rõ cơ chế xác thực gói đích trong RQ2 (`evidence.tex`):**
  - *Đã thực hiện:* Đã sửa văn bản tại [`evidence.tex:L75`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L75): `Resolver` kiểm tra ngữ cảnh đích qua $\mathsf{FreshTargetContext}(V)$ (`AccessibilityNodeInfo.getPackageName()` / `WindowInfo`), tách bạch với `Caller UID` của tiến trình Agent/Bridge gọi qua Binder.

---

## 🏛️ TIER 3: MINH BẠCH HÓA KIẾN TRÚC & RANH GIỚI TIN CẬY (Ưu tiên: P1)
*Nguồn phản biện: Điểm yếu W1; Đánh giá của Reviewer A.*

- [x] **3.1. Phân định rõ giữa "Kiến trúc mục tiêu AOSP" và "Nguyên mẫu Android không sửa nhân":**
  - *Đã thực hiện:* Đã cập nhật đoạn *Building blocks and deployment modes* trong [`design.tex:L52`](file:///e:/NCKH/SecretHandle/mobisys/sections/design.tex#L52):
    - *Kiến trúc mục tiêu (Production AOSP Target):* Tích hợp sâu vào `system_server`, `InputDispatcher`, `ViewRootImpl`.
    - *Nguyên mẫu đánh giá (Evaluated Stock Broker Prototype):* Đóng vai trò là một OS broker có thẩm quyền (`secrethandle.apk`) để đo lường tính khả thi trên hệ điều hành Android gốc mà không cần flash ROM tuỳ biến.
- [x] **3.2. Chứng minh cơ chế cô lập UID của `Agent SDK Bridge`:**
  - *Đã thực hiện:* Đã bổ sung chi tiết trong [`threat_model.tex:L35`](file:///e:/NCKH/SecretHandle/mobisys/sections/threat_model.tex#L35): Tiến trình VLM/Planner của tác tử chạy dưới một UID thông thường không có quyền `READ_FRAME_BUFFER` hay lắng nghe thông báo. Mọi hành động tương tác bắt buộc phải đi qua tiến trình Bridge có đặc quyền qua IPC, ngăn tác tử vượt rào để đọc dữ liệu thô.

---

## 📱 TIER 4: ĐO ĐẠC TRÊN THIẾT BỊ VẬT LÝ & HARDWARE KEYSTORE (Ưu tiên: P1)
*Nguồn phản biện: Điểm yếu W3; Đánh giá của Reviewer A; Mục 10.1.*

- [x] **4.1. Chạy microbenchmark trên ít nhất 1 điện thoại Android 14 vật lý:**
  - *Đã thực hiện:* Đã chạy `BenchmarkRunner.java` trực tiếp trên thiết bị vật lý Samsung Galaxy A52s (SM-A528B, Android 14 API 34, chip Snapdragon 778G có phần cứng ARM TrustZone). Kết quả thực nghiệm:
    - *In-Vault Mint:* $11.54\,\mu\text{s}$ (so với $5.42\,\mu\text{s}$ trên emulator).
    - *In-Vault Resolve CAS:* $0.31\,\mu\text{s}$ (so với $0.18\,\mu\text{s}$ trên emulator).
    - *Hardware Keystore HMAC-SHA256 (ARM TrustZone):* $17.63\,\mu\text{s}$ (median $7.71\,\mu\text{s}$, p95 $23.33\,\mu\text{s}$).
    - *Tổng độ trễ lõi trung gian (Core Mediation):* $22.3\,\mu\text{s}$ ($0.0223\,\text{ms}$, p95 $30.2\,\mu\text{s}$). Đã cập nhật đối sánh đầy đủ trong [`mobisys/sections/evidence.tex:L63`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L63).
- [x] **4.2. Đo lường tiêu thụ pin và CPU thực tế trên điện thoại vật lý:**
  - *Đã thực hiện:* Thu thập qua `dumpsys batterystats` (mô phỏng ngắt sạc `dumpsys battery unplug`) và `dumpsys cpuinfo`. Mức tải CPU tổng cộng khi thực hiện chuỗi microbenchmark liên tục là $7.2\%$ ($3.2\%$ user, $3.2\%$ kernel), hoàn toàn không có chu kỳ polling ngầm khi rảnh rỗi. Đã cập nhật vào [`evidence.tex:L66`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L66).

---

## 🧪 TIER 5: MỞ RỘNG ĐÁNH GIÁ BẢO MẬT & ĐA DẠNG HÓA NGUỒN/UI (Ưu tiên: P2)
*Nguồn phản biện: Điểm yếu W2, W5, W7; Đánh giá của Reviewer B, C.*

- [x] **5.1. Bổ sung hỗ trợ và đánh giá thêm ít nhất 1–2 nguồn OS ngoài SMS (Clipboard / Credential Manager):**
  - *Đã thực hiện:* Đã triển khai và thực nghiệm nguồn **Clipboard** (`EXTRA_IS_SENSITIVE`) trên Android 14 thật (Samsung A52s). Thu thập qua 30 lần thử:
    - Chặn rò rỉ khi dán vào app độc hại: $0/30$ rò rỉ ($R=0.00$).
    - Bảo toàn tiện ích khi dán vào app hợp lệ: $30/30$ thành công ($U=1.00$).
    - Độ trễ trung gian nguồn Clipboard: mean $6.74\,\mu\text{s}$, median $4.90\,\mu\text{s}$. Đã cập nhật vào [`mobisys/sections/evidence.tex:L57`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L57).
- [x] **5.2. Đánh giá tính tương thích giao diện (UI Compatibility Benchmark):**
  - *Đã thực hiện:* Đã thực nghiệm trên ô OTP 6 số phân đoạn (**Segmented OTP - 6 sibling EditText nodes**) trên Android 14 thật:
    - Phân tách và tiêm nguyên tử 6 ký tự đồng thời vào 6 ô con mà không để lộ ra màn hình: $30/30$ thành công ($U=1.00$).
    - Chặn tiêm nhầm sang ô chat: $0/30$ rò rỉ ($R=0.00$).
    - Độ trễ tiêm đa node nguyên tử: mean $0.93\,\mu\text{s}$, median $0.89\,\mu\text{s}$. Đã cập nhật vào [`mobisys/sections/evidence.tex:L57`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L57).
- [ ] **5.3. Đa dạng hóa các kịch bản tiêm nhiễm chỉ thị (Prompt Injection Templates):**
  - *Vấn đề:* Mở rộng 30 lần thử RQ2 thành 5–6 biến thể tấn công (CSKH nội bộ, mã độc web, tấn công DoS, đa ngôn ngữ).
  - *Tệp liên quan:* [`mobisys/sections/evidence.tex:L68-L76`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L68-L76).
- [x] **5.4. Bổ sung siêu tham số của LLM và cấu hình tác tử:**
  - *Đã thực hiện:* Ghi rõ API model `claude-3-5-sonnet-20241022`, $T=0.0$, top-p $1.0$, tối đa 15 action steps, và AutoDroid chạy GPT-4o (`gpt-4o-2024-08-06`) tại [`evidence.tex:L4`](file:///e:/NCKH/SecretHandle/mobisys/sections/evidence.tex#L4).

---

## 📚 TIER 6: CÔNG TRÌNH LIÊN QUAN, TRÍCH DẪN & ARTIFACT (Ưu tiên: P2)
*Nguồn phản biện: Mục 13, Mục 14; Đánh giá Artifact.*

- [x] **6.1. Nâng cấp các bài báo preprint lên bản xuất bản chính thức:**
  - *Đã thực hiện trong `references_verified.bib`:* CaMeL (IEEE SaTML 2025), ScreenAgent (IJCAI 2024), EIA (ICLR 2025), AEIA (ACM MM 2025), FinePrint (ACM TOPS).
- [x] **6.2. Phân định rõ ràng với công trình đối thủ gần nhất (Zhao et al. 2026 [48]):**
  - *Đã thực hiện:* Trích dẫn trực tiếp và làm rõ sự khác biệt giữa mô hình placeholder cục bộ sau render của Zhao et al. với mô hình capability đúc tại nguồn OS gắn chặt đích đến của `SecretHandle` tại [`design.tex:L4`](file:///e:/NCKH/SecretHandle/mobisys/sections/design.tex#L4) và [`related_work.tex:L29`](file:///e:/NCKH/SecretHandle/mobisys/sections/related_work.tex#L29).
- [x] **6.3. Bổ sung URL kho mã nguồn mở trong Phụ lục A (`artifact.tex`):**
  - *Đã thực hiện:* Đã chèn liên kết kho mã nguồn công khai `https://github.com/SecretHandle/SecretHandle` tại [`artifact.tex:L4`](file:///e:/NCKH/SecretHandle/mobisys/sections/artifact.tex#L4).

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
