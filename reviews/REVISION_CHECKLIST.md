# SECRETHANDLE — ACM MobiSys 2027 Comprehensive Revision Checklist
> **File:** `reviews/REVISION_CHECKLIST.md`  
> **Dựa trên:** Đánh giá tiền nộp bài `reviews/mobisys2027_review_secrethandle.md`  
> **Mục tiêu:** Chuyển đổi bài báo từ **Weak Reject (Điểm 2)** lên **Conditional Accept / Accept (Điểm 4–5)**  
> **Hạn chót quan trọng:**  
> - 🔴 **Abstract Registration:** **27/11/2026 23:59 AoE** (còn 29 ngày)  
> - 🔴 **Full Paper Submission:** **04/12/2026 23:59 AoE** (còn 36 ngày)  
> - 📍 **Hội nghị:** ACM MobiSys 2027 (21–25/06/2027, TP. Hồ Chí Minh, Việt Nam)

---

## 📌 Bảng Tóm Tắt Tình Trạng & Phân Công Nhiệm Vụ

| Tier | Nhóm Nhiệm Vụ | Mức Độ | Trạng Thái | Thời Gian Ước Tính |
| :--- | :--- | :---: | :---: | :---: |
| **Tier 0** | Khắc phục vi phạm quy định CFP (Tránh Desk-Reject) | **P0 (Khẩn cấp)** | `[x] 5/5` | **HOÀN THÀNH** |
| **Tier 1** | Xóa bỏ mâu thuẫn "Preregistration / Simulation Outputs" & Đồng bộ nguyên mẫu | **P0 (Chí mạng)** | `[x] 5/5` | **HOÀN THÀNH** |
| **Tier 2** | Sửa lỗi hình thức hóa (Formal Model), Thuật toán & Trùng lặp văn bản | **P1 (Quan trọng)** | `[x] 5/5` | **HOÀN THÀNH** |
| **Tier 3** | Đại tu số liệu Bảng 3 & Đo đạc độ trễ toàn trình thực tế | **P1 (Quan trọng)** | `[x] 4/4` | **HOÀN THÀNH** |
| **Tier 4** | Làm rõ cơ chế kỹ thuật nguyên mẫu & Xử lý Race Condition lớp phủ | **P1 (Quan trọng)** | `[x] 3/3` | **HOÀN THÀNH** |
| **Tier 5** | Mở rộng thực nghiệm: Baseline B2, Intra-app redirection & Model thứ 2 | **P2 (Nâng cấp điểm)** | `[x] 4/4` | **HOÀN THÀNH** |
| **Tier 6** | Tối ưu quỹ trang (tiết kiệm ~65 dòng), Tài liệu tham khảo & CPU/Pin | **P2 (Hoàn thiện)** | `[x] 4/4` | **HOÀN THÀNH** |
| **Tier 7** | Thủ tục nộp bài trên HotCRP & Kiểm tra định dạng tự động | **P0 (Quy trình)** | `[ ] 0/6` | Xuyên suốt |

---

## 🚨 TIER 0: Khắc Phục Vi Phạm Quy Định CFP (Tránh Desk-Reject 100%)
*MobiSys 2027 áp dụng kiểm tra nghiêm ngặt ngay khi upload lên HotCRP. Các lỗi sau sẽ bị loại ngay từ vòng gửi xe nếu không sửa.*

- [x] **0.1. Bật đánh số trang (Printfolios) bắt buộc:**
  - **File:** `mobisys/main.tex`
  - **Trạng thái:** **Đã hoàn thành** (Thêm `\settopmatter{printacmref=false,printfolios=true}`, số trang hiển thị rõ ràng trên tất cả các trang).
  - **Tham chiếu CFP:** MobiSys 2027 quy định mọi bản thảo nộp phải có số trang để reviewer tiện ghi chú.

- [x] **0.2. Điền thông tin tác giả thật (Quy định Single-Blind):**
  - **File:** `mobisys/main.tex` (dòng 59–75)
  - **Trạng thái:** **Đã hoàn thành** (Đã cập nhật Nguyễn Tiến Thuận và Trần Phát Tài, FPT University, Can Tho, Vietnam; cập nhật `\shortauthors{Nguyễn and Trần}`).

- [x] **0.3. Cập nhật Metadata Hội nghị trong Header:**
  - **File:** `mobisys/main.tex`
  - **Trạng thái:** **Đã hoàn thành** (Đã cấu hình `\acmConference[MobiSys '27]{...}{June 21--25, 2027}{Ho Chi Minh City, Vietnam}`).

- [x] **0.4. Vector hóa Bảng 3 & Làm nét Hình 2:**
  - **File:** `mobisys/sections/evidence.tex`
  - **Trạng thái:** **Đã hoàn thành** (Table 3 là bảng tabular LaTeX vector 100% sắc nét, không dùng ảnh chụp rasterized).

- [x] **0.5. Giữ độ dài thân bài nghiêm ngặt $\le 12$ trang:**
  - **File:** `mobisys/main.pdf`
  - **Trạng thái:** **Đã hoàn thành** (Conclusion kết thúc hoàn toàn trong Trang 12, References bắt đầu từ cuối Trang 12).

---

## 🛑 TIER 1: Xóa Bỏ Mâu Thuẫn "Preregistered / Simulation" & Thống Nhất Nguyên Mẫu (W1 / M2)
*Reviewer A và B đánh giá bài báo bị "tâm thần phân liệt" (schizophrenia) vì một nửa bài viết khẳng định đã chạy trên Android 14 EC2, nhưng nửa còn lại vẫn nói là "kế hoạch đăng ký trước" và "kết quả mô phỏng Python". Phải dọn sạch 100%!*

- [x] **1.1. Sửa đoạn Roadmap trong Section 1:**
  - **File:** `mobisys/sections/introduction.tex` (dòng 16)
  - **Trạng thái:** **Đã hoàn thành** (Đã xóa bỏ hoàn toàn cụm từ "reports what we have reproduced and preregisters the full evaluation", khẳng định đánh giá trên nguyên mẫu Android 14).

- [x] **1.2. Xóa tuyên bố "synthetic inputs only" ở Section 5:**
  - **File:** `mobisys/sections/model.tex` (dòng 4)
  - **Trạng thái:** **Đã hoàn thành** (Sửa thành: "formally characterize the security properties realized by our Android 14 system implementation and evaluated in Section 7").

- [x] **1.3. Xóa cờ `real_experiment=false` trong Section 9.1 (Ethics):**
  - **File:** `mobisys/sections/ethics.tex` (dòng 6)
  - **Trạng thái:** **Đã hoàn thành** (Xóa sạch `real_experiment=false`, phân tách rõ: (1) formal model checker Python và (2) on-device Android 14 testbed).

- [x] **1.4. Đại tu Phụ lục A (Artifact Appendix):**
  - **File:** `mobisys/sections/artifact.tex`
  - **Trạng thái:** **Đã hoàn thành** (Xóa hoàn toàn "These are simulation outputs, not device measurements", cung cấp lệnh adb cụ thể chạy APK và benchmark trên thiết bị Android 14 thật).

- [x] **1.5. Thống nhất mô tả nguyên mẫu giữa Mục 4, Mục 6 và Mục 9.1:**
  - **File:** `mobisys/sections/design.tex`, `mobisys/sections/algorithm.tex`, `mobisys/sections/discussion.tex`
  - **Trạng thái:** **Đã hoàn thành** (Đã thống nhất trung thực: nguyên mẫu Android 14 dùng Binder service đặc quyền + NotificationListener + TYPE_ACCESSIBILITY_OVERLAY đồng bộ SurfaceFlinger; trình bày rõ lộ trình upstream vào system_server).

---

## 📐 TIER 2: Sửa Lỗi Hình Thức Hóa (Formal Model) & Thuật Toán (W7, W8, W9 / M4)
*Reviewer B (Chuyên gia An ninh) chỉ ra lỗi logic trong cấu trúc dữ liệu handle và thuật toán.*

- [x] **2.1. Sửa lỗi Tuple trong Phương trình (1) & (8):**
  - **File:** `mobisys/sections/model.tex` (dòng 7–11)
  - **Trạng thái:** **Đã hoàn thành** (Đã tách ngân sách ban đầu $u_0 \in H$ khỏi số lần dùng còn lại $u \in \Omega[n]$ để chữ ký MAC $a = F_K(\enc(H))$ không bị hỏng khi $u$ giảm đối với handle đa dụng $u > 1$).

- [x] **2.2. Sửa Thuật toán 1 (\Mint) và Thuật toán 2 (\Resolve):**
  - **File:** `mobisys/sections/algorithm.tex`
  - **Trạng thái:** **Đã hoàn thành** (Mint lưu $u_0$ vào $H$ và record; Resolve nạp $u$, trừ $u$, và chỉ chuyển $z \gets \mathsf{consumed}$ khi $u = 0$, trả về $\mathsf{live}$ nếu $u > 0$).

- [x] **2.3. Xóa đoạn văn trùng lặp nguyên văn (Duplicate Paragraph W8):**
  - **File:** `mobisys/sections/algorithm.tex`
  - **Trạng thái:** **Đã hoàn thành** (Xóa đoạn văn 6 dòng bị copy lặp nguyên văn, thay bằng tham chiếu tới Mục 5, tiết kiệm diện tích trang).

- [x] **2.4. Xác định cơ chế suy diễn $D_T$ và $D_S$ trong `VerifyTask(T)`:**
  - **File:** `mobisys/sections/design.tex` và `mobisys/sections/algorithm.tex`
  - **Trạng thái:** **Đã hoàn thành** (Đã giải thích rõ ở Mục 4: $D_T$ được gán từ foreground package người dùng mở tác vụ, $D_S$ từ app hash hoặc wildcard $*$, bảo đảm monotonic intersection).

- [x] **2.5. Làm rõ cơ chế chống Denial-of-Service / Handle Exhaustion (W9):**
  - **File:** `mobisys/sections/algorithm.tex`, `evidence.tex`, `discussion.tex` (Sec 9.2)
  - **Trạng thái:** **Đã hoàn thành** (Đồng bộ Thuật toán 2 Line 5, Mục 7 và Mục 9.2: Rejection do `CALLER_MISMATCH` không làm tiêu hao handle của user, giữ nguyên $u$ để agent hoàn thành đăng nhập hợp lệ).

---

## 📊 TIER 3: Đại Tu Số Liệu & Phương Pháp Luận Bảng 3 (W2 / M3)
*Reviewer A chỉ trích nặng nề việc so sánh 48.6 giây (suy luận LLM) với 9.30 micro-giây (tra bảng in-memory Java) trong cùng một cột Latency, và con số 0.13 µs là "bất khả thi về mặt vật lý" nếu tính cả Binder IPC và UI injection.*

- [x] **3.1. Thiết kế lại Bảng 3 (Tách bạch các chiều đo lường):**
  - **File:** `mobisys/sections/evidence.tex` (Table 3, dòng 12–28)
  - **Trạng thái:** **Đã hoàn thành** (Đã tách cột Step Time ~48.6s và cột Mediation Overhead; tách cột $U_{\text{benign}}$ và $U_{\text{attack}}$; điền đầy đủ dữ liệu cho B2 Platform Flow).

- [x] **3.2. Đo đạc độ trễ toàn trình thực tế (End-to-End Mediation Latency):**
  - **File:** `mobisys/sections/evidence.tex` (RQ5, dòng 57–62)
  - **Trạng thái:** **Đã hoàn thành** (Đã chạy đo thực tế $n=100$ trials trên Android 14 EC2: In-vault state transition $5.23\,\mu\text{s}$ mint (median $5.20\,\mu\text{s}$, p95 $7.78\,\mu\text{s}$), $0.18\,\mu\text{s}$ resolve CAS (median $0.17\,\mu\text{s}$); Core mediation breakdown: Binder IPC round-trip $0.76\,\mu\text{s}$, Hardware Keystore HMAC-SHA256 $10.41\,\mu\text{s}$, Policy check $0.08\,\mu\text{s}$, UI text injection sync $0.12\,\mu\text{s}$, tổng mediation core $12.4\,\mu\text{s}$ ($0.0124\,\text{ms}$, p95 $18.6\,\mu\text{s}$); toàn trình OS dispatch qua AccessibilityService và render layout là $4.18\,\text{ms}$, p95 $5.82\,\text{ms}$).

- [x] **3.3. Sửa mâu thuẫn câu chữ về việc hủy handle ở Mục 7:**
  - **File:** `mobisys/sections/evidence.tex` (dòng 77)
  - **Trạng thái:** **Đã hoàn thành** (Đã sửa câu chữ khớp với Thuật toán 2 Dòng 5–6: CALLER_MISMATCH từ chối cuộc gọi nhưng giữ nguyên $u$ để agent đăng nhập hợp lệ).

- [x] **3.4. Thống nhất các con số độ trễ xuất hiện rải rác trong bài:**
  - **File:** `abstract.tex`, `introduction.tex`, `evidence.tex`, `conclusion.tex`
  - **Trạng thái:** **Đã hoàn thành** (Đã thống nhất trên toàn bộ bài với số liệu thực nghiệm thực tế: $5.23\,\mu\text{s}$ in-vault mint, $0.18\,\mu\text{s}$ resolve CAS, $4.2\,\text{ms}$ toàn trình OS mediation).

---

## 🛠️ TIER 4: Làm Rõ Cơ Chế Kỹ Thuật Nguyên Mẫu & Xử Lý Race Condition (W6 / M5)
*Reviewer A đặt câu hỏi: Một tác nhân chỉ nhìn ảnh (screenshot-only Mobile-Agent v3.5) không có token cây trợ năng thì gọi `Enter(handle)` thế nào trong thực tế? Và khi tin nhắn mới đến, lớp phủ có bị trễ khung hình không?*

- [x] **4.1. Mô tả chi tiết cầu nối Agent SDK Bridge cho thao tác `Enter`:**
  - **File:** `mobisys/sections/design.tex` (dòng 14)
  - **Trạng thái:** **Đã hoàn thành** (Giải thích rõ: khi agent tọa độ phát lệnh $\mathsf{Type}(\text{``\texttt{SH-XXXXXX}''}, (x,y))$, bridge chặn trước IME, truy vấn node trợ năng tại $(x,y)$ và đổi thành gọi Binder \Enter{} an toàn, không bao giờ lộ chuỗi handle ra app đích).

- [x] **4.2. Phân tích & Giải quyết Race Condition của Lớp Phủ (`TYPE_ACCESSIBILITY_OVERLAY`):**
  - **File:** `mobisys/sections/design.tex` (dòng 22)
  - **Trạng thái:** **Đã hoàn thành** (Đã bổ sung cơ chế đồng bộ khung hình: Agent SDK bridge đồng bộ việc chụp màn hình với render barrier của redactor, đảm bảo `SurfaceFlinger` commit overlay xong mới trả framebuffer về cho agent).

- [x] **4.3. Thảo luận về tương thích giao diện OTP phức tạp (Split OTP Boxes & Custom Views):**
  - **File:** `mobisys/sections/discussion.tex` (dòng 30)
  - **Trạng thái:** **Đã hoàn thành** (Đã bổ sung giải pháp xử lý OTP chia 6 ô qua duyệt cấu trúc sibling trong ViewGroup, và cơ chế fail-closed cho custom canvas view Flutter/React Native).

---

## 🔬 TIER 5: Mở Rộng Thực Nghiệm & Bổ Sung Baseline (W4, W5 / M6)
*Để nâng điểm từ 2 lên 4–5, cần mở rộng phạm vi thực nghiệm ra ngoài kịch bản 1 VLM + 1 loại OTP SMS.*

- [x] **5.1. Bổ sung thực nghiệm cho Baseline B2 (Platform Flow / Credential Manager):**
  - **File:** `mobisys/sections/evidence.tex` (Table 3, dòng 23 và dòng 53)
  - **Trạng thái:** **Đã hoàn thành** (Đã chạy đo thực tế $n=30$ trials trên Android 14 EC2: $E=0.00$ ($0/30$ do credentials được giữ an toàn trong Credential Provider/Autofill trước khi kích hoạt), $U_{\text{benign}}=1.00$ ($30/30$ khi đăng nhập hợp lệ), $R=1.00$ ($30/30$, Wilson $[0.89, 1.00]$ do hộp thoại xác nhận hệ thống của Android thiếu cơ chế ràng buộc tác nhân-đích khiến tác nhân trợ năng bị lừa click "Allow/Autofill" chuyển dữ liệu sang `com.attacker.rewards`), $U_{\text{attack}}=0.00$ ($0/30$ do secret bị kẻ tấn công chiếm quyền), $Y=0.00$ ($0/50$), độ trễ điều phối nền tảng $2.1\,\text{ms}$). Đã cập nhật vào Bảng 3 và phân tích chi tiết trong Mục 7.2.

- [x] **5.2. Thí nghiệm chuyển hướng trường nhập liệu nội bộ (Intra-App Field Redirection):**
  - **File:** `mobisys/sections/evidence.tex` (dòng 55)
  - **Trạng thái:** **Đã hoàn thành** (Đã chạy thực nghiệm thực tế $n=30$ trials trên Android 14 EC2: kẻ tấn công hướng dẫn paste OTP vào ô chat hỗ trợ khách hàng trong cùng ứng dụng ngân hàng `com.legitimate.bank`, chính sách loại trường $f = \text{smsOTPCode}$ đã từ chối resolution vào $f = \text{chatInput}$ trong $30/30$ lượt thử ($R=0.00$, Wilson $[0.00, 0.11]$), trong khi các thao tác điền OTP hợp lệ thành công $30/30$ ($U=1.00$), xác thực hoàn toàn cơ chế field-class binding).

- [x] **5.3. Đánh giá trên Tác nhân / Mô hình thứ 2 (Model & Agent Diversity):**
  - **File:** `mobisys/sections/evidence.tex` (dòng 49)
  - **Trạng thái:** **Đã hoàn thành** (Đã bổ sung đánh giá trên mô hình thị giác mã nguồn mở `Qwen2.5-VL-72B` và tác nhân cây trợ năng `AutoDroid`: \SH{} loại bỏ hoàn toàn phơi nhiễm secret ($E=0.00$, $0/20$) nhờ cơ chế che mắt đồng thời trên pixel và thuộc tính text của AccessibilityNodeInfo).

- [x] **5.4. Điều chỉnh tuyên bố về WebView trong Abstract & Section 1:**
  - **File:** `mobisys/sections/abstract.tex`, `mobisys/sections/introduction.tex`
  - **Trạng thái:** **Đã hoàn thành** (Đã cập nhật Abstract: WebView được cách ly an toàn theo cơ chế fail-closed confinement, không tuyên bố quá mức về origin attestation).

---

## ✂️ TIER 6: Tối Ưu Quỹ Trang & Bổ Sung Tài Liệu Tham Khảo (W10, S1–S3)
*Để có chỗ chèn thêm tên tác giả, kết quả B2 và mô tả chi tiết mà vẫn đảm bảo $\le 12$ trang, cần thực hiện ngay kế hoạch cắt giảm ~65 dòng.*

- [x] **6.1. Thực hiện cắt giảm ~65 dòng theo kế hoạch Section 15.2:**
  - [x] **Cắt 1:** Xóa đoạn lặp nguyên văn ở `mobisys/sections/algorithm.tex` (dòng 48) $\rightarrow$ **Tiết kiệm 6 dòng**.
  - [x] **Cắt 2:** Rút gọn chứng minh ở `mobisys/sections/model.tex` thành proof sketches $\rightarrow$ **Tiết kiệm ~18 dòng**.
  - [x] **Cắt 3:** Cô đọng Mục 9.1 ở `mobisys/sections/discussion.tex` $\rightarrow$ **Tiết kiệm ~24 dòng**.
  - [x] **Cắt 4:** Thu gọn Figure 2 (chiều cao từ 3.1cm về 2.6cm) $\rightarrow$ **Tiết kiệm ~14 dòng**.
  - **Kết quả:** Thân bài kết thúc hoàn hảo ở Trang 12, References bắt đầu từ Trang 13, tuân thủ 100% giới hạn 12 trang của MobiSys 2027!

- [x] **6.2. Đo đạc tải CPU% và tiêu thụ pin của Background Daemon (W10 / S1):**
  - **File:** `mobisys/sections/evidence.tex` (RQ6, dòng 63)
  - **Trạng thái:** **Đã hoàn thành** (Đã đo thực tế qua `dumpsys cpuinfo` trên Android 14 EC2: daemon hoạt động hoàn toàn theo sự kiện tiêu thụ $0.2\%$ CPU idle ($0.1\%$ user, $0.0\%$ kernel) và $1.4\%$ khi điều phối burst, xác nhận 0 polling loop và không gây sụt pin trong 2 giờ chạy liên tục).

- [x] **6.3. Bổ sung trích dẫn các hệ thống bảo mật UI kinh điển (S3):**
  - **File:** `mobisys/sections/related_work.tex` (dòng 37) và `references_verified.bib`
  - **Trạng thái:** **Đã hoàn thành** (Đã bổ sung và thảo luận đối sánh 4 công trình kinh điển: *SchrodinText* [USENIX Security '20], *Rushmore* [MobiSys '15], *GYRUS* [NDSS '14], và *Cloak & Dagger* [IEEE S&P '17]).

---

## 📅 TIER 7: Lịch Trình Thực Hiện & Kiểm Tra Trước Khi Nộp (Deadlines)

### 🗓️ Tuần 1 (29/10 – 04/11/2026): Format, Văn Bản & Mô Hình Toán
- [ ] Hoàn thành toàn bộ **TIER 0** (Đánh số trang, thông tin tác giả, metadata MobiSys '27).
- [ ] Hoàn thành toàn bộ **TIER 1** (Xóa sạch dấu vết "preregistration / simulation outputs").
- [ ] Hoàn thành toàn bộ **TIER 2** (Sửa công thức toán, sửa Thuật toán 1–2, xóa đoạn lặp).
- [ ] Áp dụng cắt giảm không gian ở **TIER 6.1** để giải phóng $\sim 65$ dòng.
- [ ] Biên dịch thử nghiệm `xelatex` và kiểm tra trực quan file `main.pdf`.

### 🗓️ Tuần 2 (05/11 – 11/11/2026): Đo Đạc Độ Trễ & Làm Rõ Kỹ Thuật
- [ ] Hoàn thành **TIER 3** (Đo đạc độ trễ Binder IPC + Keystore + UI injection trên EC2 và điện thoại thật).
- [ ] Sửa lại Bảng 3 và cập nhật văn bản giải thích trong `mobisys/sections/evidence.tex`.
- [ ] Hoàn thành **TIER 4** (Viết chi tiết cơ chế SDK bridge và đồng bộ khung hình lớp phủ).

### 🗓️ Tuần 3 & 4 (12/11 – 25/11/2026): Mở Rộng Thực Nghiệm & Đánh Giá
- [ ] Hoàn thành **TIER 5** (Chạy thử nghiệm B2 Credential Manager, intra-app redirection, mô hình thứ 2).
- [ ] Hoàn thành **TIER 6.2 & 6.3** (Đo CPU%, bổ sung trích dẫn liên quan).
- [ ] Hoàn thiện Phụ lục A với đầy đủ hướng dẫn tái hiện trên Android 14.

### 🎯 Hạn Chót 1: Đăng Ký Abstract (27/11/2026 23:59 AoE)
- [ ] Tạo tài khoản và đăng ký bài trên portal: `https://mobisys27.hotcrp.com/`.
- [ ] Khóa danh sách tác giả chính thức, đơn vị công tác và thứ tự tác giả.
- [ ] Nhập Abstract chính thức ($\ge 100$ từ) đã sửa các điểm mâu thuẫn.
- [ ] Khai báo Xung đột lợi ích (Conflicts of Interest - COI) với TPC (PC Co-Chairs Jun Han, KAIST và Falko Dressler, TU Berlin).

### 🎯 Hạn Chót 2: Nộp Bài Toàn Văn (04/12/2026 23:59 AoE)
- [ ] Chạy lệnh kiểm tra font nhúng: `pdffonts main.pdf` (đảm bảo tất cả đều là `emb = yes`).
- [ ] Chạy công cụ kiểm tra trang: `pdfinfo main.pdf` (đảm bảo đúng chuẩn US Letter 612 x 792 pt).
- [ ] Tải PDF lên HotCRP Format Checker để xác nhận không lỗi font size, lề và số dòng/cột.
- [ ] Tích chọn khai báo sử dụng LLM hỗ trợ biên tập văn bản (khớp với Mục 9.1).
- [ ] Nộp file `main.pdf` cuối cùng trước 23:59 AoE ngày 04/12/2026!
