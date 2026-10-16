# Nhật ký quyết định thiết kế (D0–D5)

Tài liệu này ghi lại các quyết định làm thay đổi phạm vi, chứng minh và mã nguồn, theo yêu cầu của Giai đoạn 0 trong `instructions/SecretHandle_HuongDan.tex`. Mỗi quyết định phải được chốt **trước cổng G0 (25/10/2026)**.

## Cách dùng

- Mỗi mục Dx có một **bản ghi quyết định** gồm: trạng thái, ngày/người chốt, câu hỏi, phương án, khuyến nghị, quyết định, lý do, hệ quả và điều kiện xem lại.
- Không xóa phương án đã loại; ghi lại để audit.
- Khi đổi quyết định, thêm một dòng vào **Lịch sử thay đổi** ở cuối tài liệu và giữ nguyên bản ghi cũ.
- Mọi hệ quả lên mã phải được phản ánh trong `audits/paper_to_code_traceability.csv` và các test tương ứng.

## Tổng quan trạng thái

| Mã | Quyết định | Khuyến nghị | Trạng thái | Ngày chốt | Người chốt |
|----|------------|-------------|------------|-----------|------------|
| D0 | Venue và lịch nộp | USENIX Security '27 Cycle 2 (MVP T1), giữ Plan B | **đã chốt — A** | 2026-10-17 | Nhóm đề tài |
| D1 | Authenticator `a` (MAC hay tra bảng) | Giữ MAC (HMAC-SHA-256) | **đã chốt — B** | 2026-10-17 | Nhóm đề tài |
| D2 | Kho lưu trữ | Chỉ trong bộ nhớ `system_server`; khởi động lại = thu hồi | **đã chốt — A** | 2026-10-17 | Nhóm đề tài |
| D3 | Principal tác nhân | Hỗ trợ 3 kiểu: UID app, UID shell/UiAutomation, quan sát serialize | **đã chốt — 3 kiểu** | 2026-10-17 | Nhóm đề tài |
| D4 | Thời điểm giảm ngân sách dùng `u` | Giảm tại bước giữ chỗ; hoàn trả chỉ khi chứng minh chưa giao | **đã chốt — bảo thủ** | 2026-10-17 | Nhóm đề tài |
| D5 | WebView | T1 chỉ view gốc (native/Compose); WebView fail-closed | **đã chốt — A** | 2026-10-17 | Nhóm đề tài |

---

## D0 — Venue và lịch nộp

- **Trạng thái:** đã chốt
- **Ngày/người chốt:** 2026-10-17, nhóm đề tài
- **Câu hỏi:** Nhắm venue/hạn nào, với phạm vi nào (MVP T1 hay đầy đủ)?
- **Phương án:**
  - A. USENIX Security '27 Cycle 2, phạm vi MVP (T1). Đăng ký 19/01/2027, nộp 26/01/2027, artifact 29/01/2027 (theo CFP sơ bộ, cần xác minh).
  - B. MobiSys 2027, phạm vi đầy đủ. Hạn ước tính 04–05/12/2026 (chưa công bố chính thức) — không đủ thời gian cho số đo thật.
  - C. Plan B: kỳ nộp kế tiếp của MobiSys / NDSS / IEEE S&P / USENIX Security.
- **Khuyến nghị:** Phương án A (MVP T1), giữ C làm dự phòng.
- **Quyết định:** **Phương án A.** Nhắm USENIX Security '27 Cycle 2 với phạm vi MVP (Tier T1); giữ C làm Plan B.
- **Lý do:** Chỉ hạn 26/01/2027 cho một bài có số đo thật (killer experiment + ma trận T1). Hạn MobiSys 2027 ước tính đầu 12/2026 chỉ còn ~8 tuần — không đủ để xây prototype AOSP và đo. Plan B dự phòng nếu G2 không qua. Đây cũng là quyết định trong Phụ lục D của tài liệu hướng dẫn (v2).
- **Hệ quả:**
  - Chốt ma trận T1 (~8.000 trial) và cỡ mẫu trong `docs/ec2_experiment_guide.md`.
  - Kiểm chính sách ẩn danh / đạo đức / AI-LLM / artifact của venue ở G0.
  - Chuyển `main.tex` khỏi class `elsarticle` chung nếu venue yêu cầu.
- **Điều kiện xem lại:** khi CFP chính thức của venue mục tiêu được công bố.

---

## D1 — Authenticator `a`

- **Trạng thái:** đã chốt
- **Ngày/người chốt:** 2026-10-17, nhóm đề tài
- **Câu hỏi:** Giữ MAC `a = F_K(enc(H))` hay thay bằng định danh ngẫu nhiên không đoán được + tra bảng `Ω[n]`?
- **Bối cảnh:** Nếu kho nằm trong TCB và `n` lấy đều từ `{0,1}^λ`, việc tra `Ω[n]` đã đủ bất khả giả mạo (cận `Q/2^λ`). MAC chỉ thêm giá trị khi bản ghi lưu ngoài TCB/bền vững hoặc khi cần xác thực metadata do handle mang theo. Reviewer sẽ hỏi "vì sao cần MAC".
- **Phương án:**
  - A. Bỏ MAC ở T1; bất khả giả mạo chỉ dựa vào định danh ngẫu nhiên + tra bảng. Đơn giản hóa định lý bất khả giả mạo.
  - B. Giữ MAC (HMAC-SHA-256, `enc(H)` chuẩn tắc, tách khóa). Cần nêu lý do cụ thể (ví dụ chuẩn bị cho kho bền vững T3).
- **Khuyến nghị:** Phương án A cho T1; ghi rõ MAC là hạng mục T3 nếu kho ra khỏi TCB.
- **Quyết định:** **Phương án B — giữ MAC (HMAC-SHA-256, canonical `enc(H)`, tách khóa).**
- **Lý do:**
  1. **Tương thích đặc tả đã khóa.** `topic_signature.json` yêu cầu hạng tử `authenticator` trong bản ghi và hướng định lý "handle unforgeability reduced to the authenticator"; `audits/topic_alignment_check.md` kiểm đúng đặc tả này. Bỏ MAC gây trôi chủ đề và phải viết lại Eq. (1), Eq. (6), Theorem 2, traceability — rủi ro cao ngay trước G0 mà không tăng an ninh ở T1.
  2. **Phòng thủ nhiều lớp ở ranh giới tin cậy.** Handle là bearer token đi qua vùng không tin cậy; authenticator làm bất khả giả mạo không phụ thuộc *duy nhất* vào tính bí mật của `n`, và giữ nguyên tính chất khi kho chuyển ra ngoài TCB/ bền vững ở T3.
  3. **Trung thực định lý.** Cận `Adv^forge ≤ Adv^EUF_F + Q/2^λ` vẫn ghi rõ số hạng entropy định danh, nên không thổi phồng; ta nêu rõ MAC thêm giá trị chủ yếu ở T3.
- **Hệ quả:**
  - Giữ `src/secrethandle/crypto.py`, `core.py`, `store.py` như hiện tại (không phải gỡ).
  - Trong `sections/theory.tex` / `appendix/proofs.tex`: bổ sung một câu nêu rõ MAC là "defense-in-depth chủ yếu cho kho ngoài TCB/T3"; số hạng `Q/2^λ` là trội ở T1.
  - Cập nhật `audits/math_to_code_audit.md` và traceability ghi rõ lý do giữ MAC.
- **Điều kiện xem lại:** nếu G0 chốt kho bền vững ngay ở T1, hoặc reviewer yêu cầu tối giản hóa primitive; khi đó chuyển sang A và cập nhật định lý.

---

## D2 — Kho lưu trữ

- **Trạng thái:** đã chốt
- **Ngày/người chốt:** 2026-10-17, nhóm đề tài
- **Câu hỏi:** Kho handle chỉ trong bộ nhớ hay bền vững qua khởi động lại?
- **Phương án:**
  - A. Chỉ trong bộ nhớ `system_server`; khởi động lại dịch vụ thu hồi mọi handle. Không có trạng thái `reserved` sống sót qua crash.
  - B. Bền vững: cần nhật ký fsync, chống rollback, tách đa người dùng. Nếu làm, áp dụng quy tắc bảo thủ: `reserved` sau sự cố không chắc chắn bị `consumed` với bí mật dùng một lần.
- **Khuyến nghị:** Phương án A cho T1; B là T3.
- **Quyết định:** **Phương án A** cho T1; kho bền vững là hạng mục T3.
- **Lý do:** Đơn giản hóa phục hồi sự cố (không có `reserved` sống qua crash), giảm phạm vi Track A trong 16 tuần, và nhất quán với quy tắc bảo thủ của D4.
- **Hệ quả:**
  - Xác định phạm vi test crash/recovery trong `tests/` (chỉ mô phỏng lịch trình, không chứng minh bền vững thiết bị).
  - Ghi rõ trong `docs/implementation_notes.md` và `audits/implementation_gaps.md`.
- **Điều kiện xem lại:** khi chuyển sang T3 hoặc khi có yêu cầu đa người dùng/sao lưu.

---

## D3 — Principal tác nhân

- **Trạng thái:** đã chốt
- **Ngày/người chốt:** 2026-10-17, nhóm đề tài
- **Câu hỏi:** "Principal tác nhân" `A` gồm những kiểu caller nào, và xác định ở điểm chặn nào?
- **Bối cảnh:** Nhiều tác nhân mã nguồn mở điều khiển qua ADB (`screencap`, `uiautomator`/UiAutomation, `input`), chủ thể là UID `shell`, không phải ứng dụng trợ năng.
- **Các kiểu:**
  - (i) Dịch vụ trợ năng / MediaProjection của một ứng dụng (UID ứng dụng).
  - (ii) Tiến trình ADB / UiAutomation (UID shell).
  - (iii) Tác nhân từ xa chỉ nhận quan sát đã serialize.
- **Khuyến nghị:** Hỗ trợ cả ba kiểu; redactor và resolver chặn theo principal tại điểm giao ảnh chụp / cây trợ năng. Đánh giá với `adb unroot` + SELinux enforcing.
- **Quyết định:** **Hỗ trợ cả ba kiểu principal** (i)(ii)(iii). Resolver và redactor chặn theo principal tại điểm giao ảnh chụp và cây trợ năng; đánh giá ở `adb unroot` + SELinux enforcing.
- **Lý do:** Nhiều runner (AppAgent, AndroidWorld-compatible) điều khiển qua ADB dưới UID `shell`; nếu chỉ định nghĩa principal theo UID ứng dụng thì redactor không biết chặn ai và kết quả vô nghĩa (rủi ro lớn đã nêu trong tài liệu hướng dẫn).
- **Bảng "điểm chặn → cách xác định caller":**

  | Điểm chặn | Cách xác định caller | Kiểu principal |
  |---|---|---|
  | Resolver `enter` qua service | UID/`PID` của caller binder + kiểm `app id`/allowlist | (i) UID app, (ii) UID shell |
  | Ảnh chụp (`screencap`, MediaProjection, `takeScreenshot`) | UID của tiến trình nhận buffer trước khi map | (i)(ii)(iii) |
  | Cây trợ năng / sự kiện (AccessibilityManagerService) | UID/`accessibilityWindowId` của client đăng ký | (i)(ii) |
  | Quan sát serialize gửi ra ngoài | cấu hình kênh/model endpoint đã đăng ký | (iii) |

- **Hệ quả:**
  - Định nghĩa API xác định caller trong adapter AOSP.
  - Cập nhật `sections/system_model.tex` (Mục principal) và `src/secrethandle/redaction.py`.
  - Nếu tác nhân có root, kết quả vô nghĩa — ghi rõ trong quy trình chạy.
- **Điều kiện xem lại:** nếu runner tác nhân chính thay đổi cách điều khiển thiết bị.

---

## D4 — Thời điểm giảm ngân sách dùng `u`

- **Trạng thái:** đã chốt
- **Ngày/người chốt:** 2026-10-17, nhóm đề tài
- **Câu hỏi:** Giảm `u` ngay tại bước giữ chỗ hay ở bước cuối của Algorithm 2?
- **Bối cảnh:** v1 mâu thuẫn giữa Algorithm 2 (giảm ở bước cuối) và mục Vòng đời (giảm ngay khi giữ chỗ).
- **Khuyến nghị:** Bảo thủ — giảm tại bước giữ chỗ; hoàn trả `u` chỉ khi có bằng chứng bền vững là chưa giao. Khớp với quy tắc phục hồi "reserved sau sự cố không chắc chắn ⇒ consumed".
- **Quyết định:** **Bảo thủ — giảm `u` tại bước giữ chỗ; hoàn trả `u` chỉ khi có bằng chứng bền vững là chưa giao.**
- **Lý do:** An toàn với handle dùng một lần dưới tranh chấp/TOCTOU: kẻ tấn công không thể lợi dụng khoảng giữa reserve và inject để dùng lại. Tránh giao hai lần khi không chắc chắn; thống nhất Algorithm 2 với mục Vòng đời.
- **Hệ quả:**
  - Cập nhật `src/secrethandle/core.py`, `tests/test_core.py`, `tests/test_concurrency.py`.
  - Cập nhật mệnh đề single-use trong `sections/theory.tex` / `appendix/proofs.tex`.
  - Đồng bộ Algorithm 2 trong `sections/algorithm.tex`.
- **Điều kiện xem lại:** nếu adapter chứng minh được trạng thái non-delivery một cách bền vững theo cách khác.

---

## D5 — WebView

- **Trạng thái:** đã chốt
- **Ngày/người chốt:** 2026-10-17, nhóm đề tài
- **Câu hỏi:** T1 có hỗ trợ trường nhập trong WebView không?
- **Phương án:**
  - A. T1 chỉ view gốc (native View / Compose); trường trong WebView bị từ chối (fail-closed) và ghi `unsupported`.
  - B. Xác thực WebView origin (node→frame→origin) — hạng mục T3, cần sửa Chromium/WebView.
- **Khuyến nghị:** Phương án A cho T1; B ghi vào Giới hạn/Hướng phát triển, không nêu trong đóng góp nếu chưa làm.
- **Quyết định:** **Phương án A.** T1 chỉ view gốc (native View / Compose); trường trong WebView bị từ chối (fail-closed) và ghi `unsupported`. Hạng mục B là T3.
- **Lý do:** Xác thực WebView origin (node→frame→origin) là khoảng trống nghiên cứu chưa giải quyết (cần sửa Chromium/WebView); không thể bảo đảm ràng buộc đích cho web trong 16 tuần. Fail-closed trung thực hơn một binding thô.
- **Hệ quả:**
  - Ghi `unsupported` trong bảng tương thích của `sections/experiments.tex`.
  - Đo tỉ lệ từ chối sai khi WebView fail-closed (hạng mục T2).
  - Cập nhật `audits/implementation_gaps.md` (WebView origin attestation).
- **Điều kiện xem lại:** nếu làm hạng mục T3 xác thực WebView origin.

---

## Lịch sử thay đổi

| Ngày | Mã | Thay đổi | Lý do | Người thực hiện |
|------|----|----------|-------|-----------------|
| 2026-10-17 | D0–D5 | Chốt toàn bộ: D0=A, D1=B, D2=A, D3=3 kiểu, D4=bảo thủ, D5=A | Thiết lập baseline thiết kế trước cổng G0 | Nhóm đề tài |
