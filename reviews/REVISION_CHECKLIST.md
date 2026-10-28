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
| **Tier 0** | Khắc phục vi phạm quy định CFP (Tránh Desk-Reject) | **P0 (Khẩn cấp)** | `[ ] 0/5` | 2 giờ |
| **Tier 1** | Xóa bỏ mâu thuẫn "Preregistration / Simulation Outputs" & Đồng bộ nguyên mẫu | **P0 (Chí mạng)** | `[ ] 0/5` | 2 ngày |
| **Tier 2** | Sửa lỗi hình thức hóa (Formal Model), Thuật toán & Trùng lặp văn bản | **P1 (Quan trọng)** | `[ ] 0/5` | 1.5 ngày |
| **Tier 3** | Đại tu số liệu Bảng 3 & Đo đạc độ trễ toàn trình thực tế | **P1 (Quan trọng)** | `[ ] 0/4` | 3–4 ngày |
| **Tier 4** | Làm rõ cơ chế kỹ thuật nguyên mẫu & Xử lý Race Condition lớp phủ | **P1 (Quan trọng)** | `[ ] 0/3` | 2–3 ngày |
| **Tier 5** | Mở rộng thực nghiệm: Baseline B2, Intra-app redirection & Model thứ 2 | **P2 (Nâng cấp điểm)** | `[ ] 0/4` | 7–10 ngày |
| **Tier 6** | Tối ưu quỹ trang (tiết kiệm ~65 dòng), Tài liệu tham khảo & CPU/Pin | **P2 (Hoàn thiện)** | `[ ] 0/4` | 2 ngày |
| **Tier 7** | Thủ tục nộp bài trên HotCRP & Kiểm tra định dạng tự động | **P0 (Quy trình)** | `[ ] 0/6` | Xuyên suốt |

---

## 🚨 TIER 0: Khắc Phục Vi Phạm Quy Định CFP (Tránh Desk-Reject 100%)
*MobiSys 2027 áp dụng kiểm tra nghiêm ngặt ngay khi upload lên HotCRP. Các lỗi sau sẽ bị loại ngay từ vòng gửi xe nếu không sửa.*

- [ ] **0.1. Bật đánh số trang (Printfolios) bắt buộc:**
  - **File:** `mobisys/main.tex`
  - **Hành động:** Thêm `\settopmatter{printfolios=true}` vào phần preamble (trước `\begin{document}`). Đảm bảo các trang 1–12 và phần References/Appendix đều có số trang rõ ràng ở header/footer.
  - **Tham chiếu CFP:** MobiSys 2027 quy định mọi bản thảo nộp phải có số trang để reviewer tiện ghi chú.

- [ ] **0.2. Điền thông tin tác giả thật (Quy định Single-Blind):**
  - **File:** `mobisys/main.tex` (dòng 60–67)
  - **Hành động:** Thay thế toàn bộ placeholder:
    ```latex
    % Thay thế:
    \author{Author Name(s) TBD}
    \affiliation{\institution{Affiliation TBD}...}
    \email{email@example.com}
    \renewcommand{\shortauthors}{Author(s) TBD}
    ```
    bằng danh sách tác giả đầy đủ, đơn vị công tác chính thức và email.
  - **Cảnh báo:** MobiSys từ năm 2026 chuyển sang Single-Blind. Nộp bài với tên "TBD" sẽ bị hủy bài ngay lập tức và danh sách tác giả không được thay đổi sau hạn đăng ký Abstract.

- [ ] **0.3. Cập nhật Metadata Hội nghị trong Header:**
  - **File:** `mobisys/main.tex`
  - **Hành động:** Đổi tên hội nghị từ placeholder `Conference'17, July 2017, Washington, DC, USA` thành thông tin chính thức:
    `MobiSys '27, June 21–25, 2027, Ho Chi Minh City, Vietnam`.

- [ ] **0.4. Vector hóa Bảng 3 & Làm nét Hình 2:**
  - **File:** `mobisys/sections/evidence.tex`
  - **Hành động:** 
    - Đảm bảo Table 3 được biên dịch hoàn toàn bằng text/tabular chuẩn LaTeX (không dùng hình chụp chèn vào).
    - Tăng DPI hoặc xuất lại vector PDF/PNG độ phân giải cao cho `figures/b3_redacted_shade.png` và `figures/b3_masked_sms.png`. Font chữ trong nhãn hình phải đọc rõ ràng ở mức phóng to 100%.

- [ ] **0.5. Giữ độ dài thân bài nghiêm ngặt $\le 12$ trang:**
  - **File:** `mobisys/main.pdf`
  - **Hành động:** Thân bài từ Trang 1 (Title) đến hết Mục 10 (Conclusion) phải kết thúc ở Trang 12. References bắt đầu từ Trang 13.
  - **Lưu ý:** Việc thêm khối tác giả đầy đủ ở Trang 1 sẽ đẩy nội dung xuống ~4–6 dòng. Cần áp dụng kế hoạch cắt giảm ở **Tier 6** để không bị tràn Conclusion sang Trang 13!

---

## 🛑 TIER 1: Xóa Bỏ Mâu Thuẫn "Preregistered / Simulation" & Thống Nhất Nguyên Mẫu (W1 / M2)
*Reviewer A và B đánh giá bài báo bị "tâm thần phân liệt" (schizophrenia) vì một nửa bài viết khẳng định đã chạy trên Android 14 EC2, nhưng nửa còn lại vẫn nói là "kế hoạch đăng ký trước" và "kết quả mô phỏng Python". Phải dọn sạch 100%!*

- [ ] **1.1. Sửa đoạn Roadmap trong Section 1:**
  - **File:** `mobisys/sections/introduction.tex` (dòng 16)
  - **Hiện tại:** `Section~\ref{sec:evidence} reports what we have reproduced and preregisters the full evaluation...`
  - **Sửa thành:** 
    ```latex
    Section~\ref{sec:evidence} evaluates \SH{} across RQ1--RQ6 on an Android~14 prototype, and Sections~\ref{sec:related}--\ref{sec:limitations} position the work, discuss deployment considerations, and state its limits.
    ```

- [ ] **1.2. Xóa tuyên bố "synthetic inputs only" ở Section 5:**
  - **File:** `mobisys/sections/model.tex` (dòng 4)
  - **Hiện tại:** `...characterize the model, not a deployed implementation, and are validated only on controlled synthetic inputs (Section~\ref{sec:evidence}).`
  - **Sửa thành:**
    ```latex
    ...characterize the model's security properties, which are realized by our Android~14 system implementation and empirically evaluated in Section~\ref{sec:evidence}.
    ```

- [ ] **1.3. Xóa cờ `real_experiment=false` trong Section 9.1 (Ethics):**
  - **File:** `mobisys/sections/ethics.tex` (dòng 6)
  - **Hiện tại:** Đề cập đến cờ `real_experiment=false` và "Regenerating every reported simulation number... The paper distinguishes simulated from measured results throughout."
  - **Sửa thành:** Khẳng định rõ ràng: "All experimental trials reported in Section~\ref{sec:evidence} were executed live on an Android 14 testbed with Mobile-Agent v3.5 and Claude Sonnet 4.6. Synthetic canaries refer strictly to generated test secret values, ensuring zero exposure of real personal data."

- [ ] **1.4. Đại tu Phụ lục A (Artifact Appendix):**
  - **File:** `mobisys/sections/artifact.tex` (dòng 4, 18, 24)
  - **Hiện tại:** Viết rằng "Every generated output is labeled synthetic smoke-test output, not a paper result" và "The preliminary-evidence numbers in Section 7 are regenerated by make evidence... These are simulation outputs, not device measurements."
  - **Sửa thành:** Phân tách rõ ràng 2 thành phần độc lập của bộ mã nguồn:
    1. **Offline Formal Model Checker (`src/secrethandle/`):** Bộ kiểm thử tính chất máy trạng thái bằng Python (`make smoke`, 6,400 synthetic trials) dùng để kiểm tra tính đúng đắn toán học của các bất biến.
    2. **On-Device Prototype (`device/b3-secrethandle/`):** Hệ thống Android 14 hoàn chỉnh chạy trên môi trường thử nghiệm với AOSP Binder service, Notification Broker và Accessibility Redactor. Cung cấp lệnh khởi chạy máy ảo/thiết bị và script chạy `run_experiment.py` thực tế để tái hiện Bảng 3.

- [ ] **1.5. Thống nhất mô tả nguyên mẫu giữa Mục 4, Mục 6 và Mục 9.1:**
  - **File:** `mobisys/sections/design.tex`, `mobisys/sections/algorithm.tex` (dòng 50), `mobisys/sections/discussion.tex` (Sec 9.1)
  - **Vấn đề:** Mục 6 tuyên bố sửa mã nguồn AOSP `system_server` và che khuất màn hình trước khi render frame, nhưng Mục 9.1 lại thừa nhận dùng user-space `AccessibilityService` và `TYPE_ACCESSIBILITY_OVERLAY`.
  - **Hành động:** 
    - Trình bày kiến trúc hai tầng nhất quán: Nguyên mẫu đánh giá trên Android 14 gồm một dịch vụ Binder đặc quyền (`SecretHandleVaultService`) kết hợp với `NotificationListenerService` và bộ che phủ `TYPE_ACCESSIBILITY_OVERLAY`.
    - Giải thích rõ tại sao `TYPE_ACCESSIBILITY_OVERLAY` vẫn đảm bảo an toàn: Được bộ tổng hợp `SurfaceFlinger` của hệ điều hành hòa trộn vào framebuffer màn hình *trước khi* hàm API `takeScreenshot()` trả ảnh chụp về cho tiến trình agent.

---

## 📐 TIER 2: Sửa Lỗi Hình Thức Hóa (Formal Model) & Thuật Toán (W7, W8, W9 / M4)
*Reviewer B (Chuyên gia An ninh) chỉ ra lỗi logic trong cấu trúc dữ liệu handle và thuật toán.*

- [ ] **2.1. Sửa lỗi Tuple trong Phương trình (1) & (8):**
  - **File:** `mobisys/sections/model.tex` (dòng 7–11)
  - **Vấn đề:** Nếu đưa số lần dùng $u$ vào bên trong $H$, khi $u$ giảm sau mỗi lần dùng, giá trị băm $\enc(H)$ sẽ thay đổi làm cho thẻ xác thực $a = F_K(\enc(H))$ bị sai (invalid MAC) trong các lần dùng sau của handle dùng nhiều lần ($u > 1$).
  - **Hành động:** Sửa định nghĩa bản ghi và handle:
    ```latex
    \Omega[n] = (s, H, a, z, r, u), \qquad H = (n, q, \sigma, d, \tau, t_i, t_e, u_0, c)
    ```
    Trong đó $u_0$ là hạn mức ban đầu nằm trong metadata bất biến $H$, còn $u$ là số lần dùng còn lại được lưu như trạng thái khả biến trong bản ghi của Vault $\Omega[n]$.

- [ ] **2.2. Sửa Thuật toán 1 (\Mint) và Thuật toán 2 (\Resolve):**
  - **File:** `mobisys/sections/algorithm.tex`
  - **Hành động:**
    - **Thuật toán 1 (Mint):** Dòng 17 khởi tạo $H \gets (n, q, \sigma, d, \tau, t_i, t_e, u_0, c)$ và dòng 18 lưu $\Omega[n] \gets (s, H, a, \mathsf{live}, \bot, u_0)$.
    - **Thuật toán 2 (Resolve):**
      - Dòng 31 nạp $\Omega[n] = (s, H, a_H, z, r, u)$.
      - Dòng 37 trừ dần $u$: `$(z, r, u) \gets (\mathsf{reserved}, \mathsf{nonce}, u - 1)$`.
      - Dòng 43: Làm rõ bước finalize. Nếu $u > 0$ thì trả trạng thái về $z \gets \mathsf{live}$; chỉ khi $u = 0$ mới chuyển sang $z \gets \mathsf{consumed}$ và xóa bí mật $s$ khỏi Vault (`explicit_bzero`).

- [ ] **2.3. Xóa đoạn văn trùng lặp nguyên văn (Duplicate Paragraph W8):**
  - **File:** `mobisys/sections/algorithm.tex` (dòng 48)
  - **Hành động:** Xóa 6 dòng lặp lại nguyên văn giải thích về mutable $u$ giữa Mục 5 (`model.tex:L11`) và Mục 6 (`algorithm.tex:L48`). Thay bằng một câu tham chiếu ngắn: "As formalized in Section~\ref{sec:model}, the store tracks the remaining budget $u$ as mutable record state outside $H$ to preserve authenticator invariance."
  - **Lợi ích:** Tiết kiệm ngay 5–6 dòng văn bản quý giá cho trang 7–8!

- [ ] **2.4. Xác định cơ chế suy diễn $D_T$ và $D_S$ trong `VerifyTask(T)`:**
  - **File:** `mobisys/sections/design.tex` và `mobisys/sections/algorithm.tex`
  - **Hành động:** Làm rõ câu hỏi phản biện: "Hệ điều hành lấy $D_T$ (tập package hợp lệ) từ đâu mà không cần tin tưởng LLM?"
    - Nêu rõ: $D_T$ được gán cứng từ định danh package của ứng dụng mà người dùng trực tiếp mở hoặc giao tác vụ ban đầu từ Launcher của HĐH.
    - $D_S$ được xác định dựa trên chữ ký nguồn (ví dụ mã băm 11 ký tự của SMS Retriever API, hoặc Digital Asset Links trong Credential Manager). Với SMS thường không có mã băm, $D_S$ để mở (wildcard) và chính sách bị chặn chặt bởi $D_T$.

- [ ] **2.5. Làm rõ cơ chế chống Denial-of-Service / Handle Exhaustion (W9):**
  - **File:** `mobisys/sections/algorithm.tex`, `evidence.tex`, `discussion.tex` (Sec 9.2)
  - **Hành động:** Đồng bộ nhất quán: khi xảy ra lỗi `CALLER_MISMATCH` (gọi sai app đích), Thuật toán 2 từ chối ở Dòng 5–6 *trước khi* trừ hạn mức $u$ ở Dòng 8. Nhờ đó, kẻ tấn công prompt injection không thể cố tình gọi sai app để đốt mất mã OTP của người dùng (bảo vệ tính sẵn sàng / Availability). Có thể bổ sung bộ đếm giới hạn thử lại $k_{\max}=3$ để chống brute-force.

---

## 📊 TIER 3: Đại Tu Số Liệu & Phương Pháp Luận Bảng 3 (W2 / M3)
*Reviewer A chỉ trích nặng nề việc so sánh 48.6 giây (suy luận LLM) với 9.30 micro-giây (tra bảng in-memory Java) trong cùng một cột Latency, và con số 0.13 µs là "bất khả thi về mặt vật lý" nếu tính cả Binder IPC và UI injection.*

- [ ] **3.1. Thiết kế lại Bảng 3 (Tách bạch các chiều đo lường):**
  - **File:** `mobisys/sections/evidence.tex` (Table 3, dòng 12–28)
  - **Hành động:** Thay đổi cấu trúc bảng để phản ánh trung thực:
    - **Cột 1:** Điều kiện kiểm thử (B0, B1, B2, B3).
    - **Cột 2–3:** Exposure Rate $E$ và Redirection Rate $R$ (kèm 95% Wilson CI).
    - **Cột 4–5: Tách Utility $U$ thành:**
      - $U_{\text{benign}}$: Tỷ lệ hoàn thành tác vụ khi không có tấn công ($1.00$ cho cả B0, B1, B3).
      - $U_{\text{attack}}$: Tỷ lệ hoàn thành tác vụ khi có tấn công chuyển hướng đích ($0.00$ cho B1 vì bị cướp mất token; với B3, báo cáo tỷ lệ agent phục hồi quay lại app ngân hàng hoặc fail-closed an toàn).
    - **Cột 6: End-to-End Action Time (s):** Báo cáo thời gian trôi qua mỗi bước của Agent (~45–50 s/step cho tất cả các điều kiện, vì thời gian suy luận VLM áp đảo).
    - **Cột 7: Security Overhead (ms):** Báo cáo chi phí trung gian (Mediation overhead) do cơ chế bảo vệ tạo ra (B0: 0 ms, B1: ~150 ms regex/OCR, B3: chi phí đo thực tế).

- [ ] **3.2. Đo đạc độ trễ toàn trình thực tế (End-to-End Mediation Latency):**
  - **File:** `mobisys/sections/evidence.tex` (RQ5, dòng 57–59)
  - **Vấn đề:** Con số `0.13 µs` (130 ns) chỉ là tra cứu biến bộ nhớ in-process trong Java, chưa tính Binder IPC, Keystore MAC và bơm text vào UI.
  - **Hành động:** Viết lại đoạn văn RQ5 và báo cáo bảng phân rã chi tiết (Breakdown latency):
    - *In-Vault State Transition:* $\sim 0.13\,\mu\text{s}$ – $5.61\,\mu\text{s}$.
    - *Cross-Process Binder IPC:* $\sim 30\,\mu\text{s}$ – $80\,\mu\text{s}$.
    - *Hardware Keystore / HMAC Verification:* $\sim 0.8\,\text{ms}$ – $2.5\,\text{ms}$.
    - *Target Window Inspection (`FreshTargetContext`):* $\sim 1.0\,\text{ms}$ – $2.0\,\text{ms}$.
    - *Private Injection (`ACTION_SET_TEXT`) & Overlay Update:* $\sim 1.5\,\text{ms}$ – $3.5\,\text{ms}$.
    - **Tổng cộng (Total Mediation Latency):** $\sim 3.5\,\text{ms}$ – $8.0\,\text{ms}$ (vẫn cực kỳ nhỏ, $< 0.02\%$ thời gian một bước suy luận của LLM là 48 s).
    - *Đo trên thiết bị:* Chạy benchmark đo đạc trên cả máy ảo EC2 và ít nhất 1 thiết bị Android thật (có chip StrongBox/TrustZone).

- [ ] **3.3. Sửa mâu thuẫn câu chữ về việc hủy handle ở Mục 7:**
  - **File:** `mobisys/sections/evidence.tex` (dòng 77)
  - **Hiện tại:** `The resolver immediately halts resolution, emits a CALLER_MISMATCH audit violation, and safely consumes the handle.`
  - **Sửa thành:** Khớp với Thuật toán 2 (Dòng 5–6):
    ```latex
    The resolver halts resolution, emits a \texttt{CALLER\_MISMATCH} audit violation, and rejects the call without consuming the single-use budget ($u$ remains intact). This prevents the injected adversary from mounting a denial-of-service attack, leaving the handle available for the agent to complete the legitimate banking login.
    ```

- [ ] **3.4. Thống nhất các con số độ trễ xuất hiện rải rác trong bài:**
  - **File:** `abstract.tex`, `introduction.tex`, `evidence.tex`, `conclusion.tex`
  - **Hành động:** 
    - Abstract hiện ghi `0.13 µs`, Intro ghi `5.61 µs`, Table 3 ghi `9.30 µs`.
    - Thống nhất cách gọi: Nêu rõ `5.61 µs` là in-vault mint latency, `0.13 µs` là in-vault resolve transition, và đưa thêm con số toàn trình $\approx X\,\text{ms}$ end-to-end mediation overhead.

---

## 🛠️ TIER 4: Làm Rõ Cơ Chế Kỹ Thuật Nguyên Mẫu & Xử Lý Race Condition (W6 / M5)
*Reviewer A đặt câu hỏi: Một tác nhân chỉ nhìn ảnh (screenshot-only Mobile-Agent v3.5) không có token cây trợ năng thì gọi `Enter(handle)` thế nào trong thực tế? Và khi tin nhắn mới đến, lớp phủ có bị trễ khung hình không?*

- [ ] **4.1. Mô tả chi tiết cầu nối Agent SDK Bridge cho thao tác `Enter`:**
  - **File:** `mobisys/sections/algorithm.tex` hoặc bổ sung một mục con trong `mobisys/sections/evidence.tex`
  - **Hành động:** Giải thích rõ luồng thực thi trong nguyên mẫu:
    1. Agent quan sát thấy nhãn `SH-A8F29C` trên thanh thông báo hoặc overlay và sinh hành động dạng `Type("SH-A8F29C")` tại tọa độ `(x, y)` hoặc gọi hàm SDK `Enter("SH-A8F29C", (x, y))`.
    2. Cầu nối Agent Bridge (chạy song song với Accessibility Service) bắt lấy chuỗi ký tự định dạng `SH-XXXXXX`.
    3. Bridge gọi `findAccessibilityNodeInfosByViewId` hoặc lấy node tại tọa độ `(x, y)` để trích xuất ngữ cảnh đích (package name, view class).
    4. Bridge chuyển ngữ cảnh qua Binder AIDL đến `SecretHandleVaultService` để kiểm tra chính sách và thực hiện `ACTION_SET_TEXT` trực tiếp vào trường dữ liệu, hoàn toàn không để lộ chuỗi OTP ra bàn phím IME.

- [ ] **4.2. Phân tích & Giải quyết Race Condition của Lớp Phủ (`TYPE_ACCESSIBILITY_OVERLAY`):**
  - **File:** `mobisys/sections/design.tex` và `mobisys/sections/discussion.tex`
  - **Vấn đề:** Khi SMS đến hoặc khi cuộn màn hình, có khoảng trễ 16–50 ms trước khi Accessibility Event kích hoạt vẽ lại ô che đen.
  - **Hành động:** Trình bày 2 cơ chế bảo vệ đồng bộ:
    1. **Tại thanh thông báo:** `NotificationListenerService` can thiệp ở mức hệ thống để hủy (cancel) và thay thế notification chứa mã OTP gốc trước khi hệ thống kịp vẽ lên thanh trạng thái. Agent không cần mở app SMS Messenger.
    2. **Đồng bộ hóa chụp màn hình:** Cầu nối Agent SDK chặn hàm `takeScreenshot()`, chờ cờ xác nhận từ `AccessibilityRedactor` xác nhận rằng lớp phủ đã được cập nhật hoàn tất trên `SurfaceFlinger` rồi mới trả ảnh chụp về cho VLM. Nhờ đó triệt tiêu hoàn toàn khoảng hở rò rỉ frame (zero-frame leakage).

- [ ] **4.3. Thảo luận về tương thích giao diện OTP phức tạp (Split OTP Boxes & Custom Views):**
  - **File:** `mobisys/sections/discussion.tex` (Mục 9.2)
  - **Hành động:** Bổ sung thảo luận cách xử lý các ứng dụng fintech (như ví điện tử, ngân hàng) chia OTP thành 6 ô `EditText` riêng biệt hoặc vẽ trên Canvas tùy biến (Flutter / React Native). Đề xuất cơ chế Resolver tự động duyệt qua các node con trong cùng ViewGroup để phân phối từng ký tự của mã OTP, hoặc hỗ trợ API khai báo trợ năng chuẩn.

---

## 🔬 TIER 5: Mở Rộng Thực Nghiệm & Bổ Sung Baseline (W4, W5 / M6)
*Để nâng điểm từ 2 lên 4–5, cần mở rộng phạm vi thực nghiệm ra ngoài kịch bản 1 VLM + 1 loại OTP SMS.*

- [ ] **5.1. Bổ sung thực nghiệm cho Baseline B2 (Platform Flow / Credential Manager):**
  - **File:** `mobisys/sections/evidence.tex`
  - **Vấn đề:** Hiện tại hàng B2 trong Bảng 3 bị để trống `N/A` toàn bộ các cột, tạo cảm giác thiếu sót lớn.
  - **Hành động:** 
    - Bổ sung kịch bản đăng nhập bằng tài khoản/mật khẩu qua Android Credential Manager / Autofill.
    - Đo đạc thực tế tỷ lệ rò rỉ: Chỉ ra rằng khi kẻ tấn công chèn prompt injection yêu cầu agent copy mật khẩu từ trình quản lý hoặc điền vào form lừa đảo, các giải pháp Autofill truyền thống không ngăn được vì agent vẫn có thể bị điều khiển ấn nút chia sẻ hoặc paste sang app khác.
    - Điền số liệu thực tế vào hàng B2 trong Bảng 3.

- [ ] **5.2. Thí nghiệm chuyển hướng trường nhập liệu nội bộ (Intra-App Field Redirection):**
  - **File:** `mobisys/sections/evidence.tex`
  - **Hành động:** Thiết kế kịch bản tấn công tinh vi hơn: Kẻ tấn công không bảo agent mở app khác (`com.attacker.app`), mà lừa agent paste mã OTP vào ô chat hỗ trợ khách hàng (Customer Support Chat) hoặc ô tìm kiếm *bên trong cùng ứng dụng ngân hàng* `com.legitimate.bank`.
  - **Kết quả:** Chứng minh cơ chế kiểm tra loại trường nhập liệu ($f = \text{smsOTPCode}$) trong `SECRETHANDLE` từ chối điền vào ô chat (`f = chatInput`), xác thực giá trị thực tiễn của thuộc tính Field-Class Binding!

- [ ] **5.3. Đánh giá trên Tác nhân / Mô hình thứ 2 (Model & Agent Diversity):**
  - **File:** `mobisys/sections/evidence.tex`
  - **Hành động:** Chạy thêm thực nghiệm bảo mật với:
    - Một mô hình VLM khác (ví dụ: `GPT-4o` hoặc mô hình mã nguồn mở `Qwen2.5-VL-72B`).
    - Hoặc một agent có sử dụng Cây trợ năng (Accessibility Tree) như `AutoDroid` hoặc `AppAgent`.
    - **Mục tiêu:** Chứng minh `SECRETHANDLE` bảo vệ hiệu quả cả ở kênh hình ảnh (screenshot banner) lẫn kênh cây trợ năng (`AccessibilityNodeInfo` role `secret_handle`).

- [ ] **5.4. Điều chỉnh tuyên bố về WebView trong Abstract & Section 1:**
  - **File:** `mobisys/sections/abstract.tex`, `mobisys/sections/introduction.tex`
  - **Hành động:** Tinh chỉnh câu chữ ở Tóm tắt để khớp hoàn toàn với Mục 3 ("Out of scope"): Nêu rõ `SECRETHANDLE` hỗ trợ chính sách gắn kết nguồn gốc mở rộng, trong đó các trường dữ liệu bên trong WebView chưa được chứng thực nguồn gốc sẽ mặc định được xử lý từ chối an toàn (fail-closed rejection), tránh việc người đọc hiểu lầm là đã tích hợp sâu vào mã nguồn Chromium.

---

## ✂️ TIER 6: Tối Ưu Quỹ Trang & Bổ Sung Tài Liệu Tham Khảo (W10, S1–S3)
*Để có chỗ chèn thêm tên tác giả, kết quả B2 và mô tả chi tiết mà vẫn đảm bảo $\le 12$ trang, cần thực hiện ngay kế hoạch cắt giảm ~65 dòng.*

- [ ] **6.1. Thực hiện cắt giảm ~65 dòng theo kế hoạch Section 15.2:**
  - [ ] **Cắt 1:** Xóa đoạn lặp nguyên văn ở `mobisys/sections/algorithm.tex` (dòng 48) $\rightarrow$ **Tiết kiệm 6 dòng**.
  - [ ] **Cắt 2:** Rút gọn chứng minh ở `mobisys/sections/model.tex` (chỉ để phát biểu Theorem/Proposition và Proof Sketch 2 câu, chuyển chứng minh chi tiết sang Appendix B) $\rightarrow$ **Tiết kiệm ~25 dòng**.
  - [ ] **Cắt 3:** Cô đọng Mục 9.1 ở `mobisys/sections/discussion.tex` (các đoạn về `mlock()`, `explicit_bzero` và `AttestedResolutionReceipt` gộp thành 1 đoạn súc tích) $\rightarrow$ **Tiết kiệm ~24 dòng**.
  - [ ] **Cắt 4:** Thu gọn Figure 2 (dàn ngang Figure 2a và 2b, giảm chiều cao) $\rightarrow$ **Tiết kiệm ~10 dòng**.
  - **Tổng cộng không gian thu hồi:** **~65 dòng (> 1.2 cột)** $\rightarrow$ Dư chỗ cho danh sách tác giả và bảng kết quả mở rộng!

- [ ] **6.2. Đo đạc tải CPU% và tiêu thụ pin của Background Daemon (W10 / S1):**
  - **File:** `mobisys/sections/evidence.tex` (RQ5/RQ6)
  - **Hành động:** Chạy `dumpsys cpuinfo` và đo lường mức độ sử dụng CPU của `SecretHandleVaultService` và Redactor trong suốt quá trình chạy 10 tác vụ AndroidWorld. Nêu rõ hệ thống hoạt động hoàn toàn theo hướng sự kiện (event-driven callbacks), tiêu thụ $< 0.5\%$ CPU ở trạng thái chờ và không ảnh hưởng đến pin.

- [ ] **6.3. Bổ sung trích dẫn các hệ thống bảo mật UI kinh điển (S3):**
  - **File:** `mobisys/sections/related_work.tex`
  - **Hành động:** Bổ sung và so sánh với các công trình kinh điển trên Android về UI overlay và bảo vệ màn hình:
    - *SchrodinText* (USENIX Security '20): Cách ly hiển thị văn bản nhạy cảm.
    - *Rushmore / TruZ-Droid* (MobiSys '15 / CCS): Vùng tin cậy hiển thị trên thiết bị di động.
    - *GYRUS* (NDSS '14): Xác thực ý định người dùng qua UI.
    - *Cloak & Dagger* (IEEE S&P '17): Phân tích bề mặt tấn công của Android Accessibility Service.

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
