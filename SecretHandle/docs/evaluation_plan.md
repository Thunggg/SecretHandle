# Kế hoạch đánh giá đầy đủ (bản full / Plan B)

Tài liệu này cố định thiết kế đánh giá cho **bản full** (Plan B: MobiSys 2028 / USENIX / NDSS / IEEE S&P). Bản nộp **04/12/2026** (MobiSys Emerging Ideas) chỉ dùng tập con có ghi chú rõ ràng — xem mục 12. Mọi số liệu bản full phải đến từ **cài đặt AOSP thật + thiết bị thật**; bằng chứng sơ bộ hiện có là **mô phỏng** (`docs/preliminary_evidence.md`).

## 1. Câu hỏi nghiên cứu

- **RQ1:** Đúc tại nguồn OS có giữ giá trị thô ra khỏi mọi quan sát/vết của tác nhân được thiết bị không?
- **RQ2:** Ràng buộc đích + tác vụ có chặn chuyển hướng do injection mà không chặn nhầm tác vụ hợp lệ?
- **RQ3:** Vòng đời + giữ chỗ nguyên tử có chặn replay, vượt hạn và tranh chấp đồng thời?
- **RQ4:** Che quan sát có chặn đọc lại sau khi nhập trong ảnh và cây trợ năng?

RQ1--RQ4 là **kết cục chính**; các so sánh khác là thăm dò.

## 2. Điều kiện

| Mã | Điều kiện | Mô tả |
|----|-----------|-------|
| B0 | không bảo vệ | Tác nhân nhận giá trị thô trong quan sát và nhập bình thường |
| B1 | placeholder bị phát hiện | OCR/NER thay chữ nhạy cảm bằng placeholder cục bộ, giải cho đích yêu cầu **không ràng buộc** |
| B2 | luồng nền tảng | Autofill / OTP Autofill / Credential Manager khi app gọi được; workflow không hỗ trợ ghi `not_applicable` |
| B3 | \SH | Đúc nguồn + ràng buộc đích/tác vụ + vòng đời + che |

**Ablation** (chỉ với canary tổng hợp + endpoint cô lập): tắt lần lượt từng thành phần (đúc nguồn, ràng buộc đích, ràng buộc tác vụ, vòng đời nguyên tử, che sau nhập, kiểm origin, xác nhận từng lần).

## 3. Họ tấn công

Đủ 7 họ (bản full): (1) đọc và rò rỉ; (2) chuyển hướng đích; (3) handle giả; (4) replay/tranh chấp; (5) đọc lại sau nhập; (6) lạm dụng ngữ nghĩa cùng đích; (7) nhập nhằng danh tính (WebView, frame lồng, overlay, bàn phím OEM, tái sử dụng view, xoay màn hình, kết nối lại trợ năng).

**G1 (sơ bộ)** chỉ cần tái hiện họ **1, 3, 4, 7**.

## 4. Chỉ số

- **E** (exposure): tỉ lệ tác vụ có canary xuất hiện trong artifact tác nhân (khớp chính xác + chuẩn hóa/encoded/OCR/substring).
- **R** (redirection): tỉ lệ trial tấn công mà giá trị thô tới đích ngoài `d`.
- **U** (utility): tỉ lệ trial hợp lệ thỏa oracle ứng dụng.
- **L** (post-entry leakage): tỉ lệ trial mà giá trị xuất hiện trong quan sát sau đó.
- **F/Y** (forgery/replay acceptance): tỉ lệ injection trái phép thành công.
- Bổ sung: `policy_rejection`, `false_rejection`, latency (mint/auth/lookup/confirm/inject/redact; trung vị + p95 + phân phối), bộ nhớ/CPU/năng lượng (khi hỗ trợ), số lần xác nhận người dùng, kết quả crash-recovery, sẵn có danh tính đích, và **hồi quy tác vụ thường** (chênh lệch thành công trên benchmark không dùng handle, ví dụ AndroidWorld).

## 5. Killer experiment

Trên app đăng nhập + OTP mở: dưới B0, tác nhân đọc canary và bị điều khiển forward; dưới B3, adapter SMS chỉ lộ handle buộc vào app/trường OTP. **Chỉ đạt khi cả ba điều kiện:**
(a) giá trị thô vắng khỏi mọi artifact được thiết bị;
(b) giải vào đích của kẻ tấn công bị từ chối;
(c) đăng nhập hợp lệ thành công.

Bất kỳ điều kiện nào fail ⇒ chặn claim tương ứng và phân tích gốc rễ trước khi mở rộng sang credential/checkout.

## 6. Ma trận T1

Ma trận T1 = {app hợp tác × nguồn bí mật} cho lát cắt T1: nguồn {SMS/notification} × đích {app gốc, app khác, WebView origin khác, trường không-OTP, node cũ} × chế độ xác nhận {NONE, PER_USE} × trạng thái vòng đời {live, reserved, consumed, expired}. Mỗi ô: kỳ vọng chấp nhận/từ chối + oracle cô lập.

## 7. Thiết kế & cỡ mẫu

- Seed cố định; ghép cặp benign/adversarial. Khối hóa theo thiết bị, tác nhân, model, ứng dụng, loại bí mật.
- **Killer (bản full):** B3 `n ≥ 300`; B0 so sánh cặp.
- Cỡ mẫu chọn bằng phân tích độ chính xác tiên lượng **trước khi nhìn kết quả** (prospective precision).

## 8. Thống kê

- Kết cục nhị phân: **Wilson CI**; so sánh cặp: **paired permutation** hoặc **McNemar chính xác** khi phù hợp.
- Latency: trung vị, percentile đuôi, bootstrap CI, phân phối đầy đủ.
- Zero quan sát ghi là **"0/n" kèm CI**, không phải "bất khả".
- Giới hạn đa giả thuyết bằng cách chỉ định RQ1--RQ4 là chính.

## 9. Loại trừ

Ghi theo nhóm: tác nhân crash, nền tảng crash, mất mạng, người dùng hủy, danh tính không hỗ trợ. Báo cáo đủ; không loại im lặng.

## 10. Mối đe dọa tới hiệu lực

- **Không Pixel/thiết bị thật:** keystore phần cứng + độ trễ/năng lượng là future work (D6).
- **E không chứng minh vắng mặt** ở kênh không được thiết bị.
- **Rò rỉ ngữ nghĩa cùng đích** (họ 6) là rủi ro còn lại mà ràng buộc đích không tuyên bố loại bỏ.
- **Số liệu mô hình tham chiếu** không thay cho AOSP.

## 11. Tái lập / provenance

Ghim: commit AOSP, build/kernel thiết bị, hash app, phiên bản provider, commit tác nhân, định danh model, prompt, seed, endpoint mạng, tệp policy. Kèm lệnh một-phát chạy canary cô lập, script dựng lại mọi bảng/hình từ dữ liệu thô, schema che vết, và kiểm tra không thu bí mật thật.

## 12. Ranh giới bản nộp 04/12/2026 vs bản full

| Hạng mục | 04/12 (Emerging Ideas) | Bản full (Plan B) |
|----------|------------------------|-------------------|
| Killer experiment | Mô hình tham chiếu + tái hiện B0 trên emulator | B0 vs B3 trên app A, thiết bị thật |
| Họ tấn công | B0 (họ 1) + kế hoạch 1--7 | 1--7 đầy đủ |
| Số đo thiết bị | Không (ghi Limitations) | Có (latency/energy/keystore) |
| Thống kê | Wilson CI trên mô hình tham chiếu (mô phỏng) | McNemar/permutation trên dữ liệu thật |
| T1 matrix | Mô tả | Chạy đầy đủ |
