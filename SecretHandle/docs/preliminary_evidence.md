# Bằng chứng sơ bộ từ mô hình tham chiếu (mô phỏng)

> **Nhãn bắt buộc:** Toàn bộ số trong tài liệu này đến từ **mô hình tham chiếu Python** chạy ở chế độ **synthetic** (canary tổng hợp, độ trễ là đại lượng thay thế tất định). Đây **không phải** kết quả trên thiết bị/AOSP và **không** phải số cho bài báo. Không con số nào ở đây được dùng làm kết quả đánh giá thật.

## 1. Mục đích

Cho thấy mô hình tham chiếu tái lập được các xu hướng định tính mà thiết kế \SH dự đoán (B0 → B3), làm nền cho khung bản thảo và cho kế hoạch đánh giá đầy đủ (`docs/evaluation_plan.md`).

## 2. Cách tái lập

```bash
python scripts/run_synthetic_demo.py --config configs/preliminary_evidence.yaml
python scripts/run_experiment.py  --config configs/preliminary_evidence.yaml --stage killer
```

- Cấu hình: `configs/preliminary_evidence.yaml` (seed `20261017`, `trials_per_attack: 200`, **8 họ tấn công** gồm cả `read_exfil` (họ 1) và `ambiguous_identity` (họ 7), tổng **6400 trials**).
- Đầu ra: `outputs/preliminary_evidence/{trials.jsonl,summary.json,metrics.csv,provenance.json}` (thư mục `outputs/` được gitignore; chạy lại để tái tạo).
- `provenance.json` ghi phiên bản Python/nền tảng, seed, hash cấu hình, và cờ `real_experiment=false`.

## 3. Kết quả (synthetic, n = 200/attack; khoảng tin cậy Wilson 95%)

| Điều kiện | E (exposure) | R (redirection) | U (utility) | L (post-entry leak) | F (forgery) | Y (replay) | identity_available |
|-----------|--------------|-----------------|-------------|---------------------|-------------|------------|--------------------|
| B0 (không bảo vệ) | 1.000 [0.998, 1.000] | 1.000 [0.990, 1.000] | 1.000 [0.981, 1.000] | — (n/a) | — (n/a) | — (n/a) | 0.875 [0.858, 0.890] |
| B1 (placeholder bị phát hiện) | 0.000 [0.000, 0.002] | 1.000 [0.990, 1.000] | 1.000 [0.981, 1.000] | **1.000** [0.981, 1.000] | — (n/a) | — (n/a) | 0.875 [0.858, 0.890] |
| B2 (platform flow) | — (không áp dụng) | — | — | — | — | — | — |
| B3 (\SH) | 0.000 [0.000, 0.002] | 0.000 [0.000, 0.010] | 1.000 [0.994, 1.000] | 0.000 [0.000, 0.010] | 0.000 [0.000, 0.019] | 0.000 [0.000, 0.019] | 0.875 [0.858, 0.890] |

- B3 thêm: `policy_rejection = 0.625` (1000/1600; các họ tấn công bị từ chối) và `false_rejection = 0.000` (0/200 tác vụ hợp lệ không bị chặn nhầm).
- `identity_available = 0.875` ở mọi điều kiện vì họ 7 (`ambiguous_identity`) cố ý tạo đích không xác định được danh tính (200/1600 trial); đây là dữ liệu, không phải lỗi.
- **B2 để trống có chủ đích**: baseline luồng nền tảng cần hạ tầng ngoài chưa cấp phát → mọi trial có `not_applicable` (đúng nguyên tắc `not_applicable`, không phải thất bại giả).

### 3.1. Chi tiết theo họ tấn công (B3)

| Họ | Attack | exposure | redirect | identity_unavail | rejected | utility |
|----|--------|----------|----------|------------------|----------|---------|
| 1 | `read_exfil` | 0/200 | — | 0/200 | 0/200 | — |
| 2 | `redirect` | 0/200 | 0/200 | 0/200 | 200/200 | — |
| 3 | `forgery` | 0/200 | — | 0/200 | 200/200 | — |
| 4 | `replay` | 0/200 | — | 0/200 | 200/200 | 200/200 (lần đầu hợp lệ) |
| — | `expired` | 0/200 | — | 0/200 | 200/200 | — |
| 5 | `reread` | 0/200 | — | 0/200 | 0/200 | 200/200 |
| 7 | `ambiguous_identity` | 0/200 | 0/200 | 200/200 | 200/200 | — |
| — | `benign` | 0/200 | — | 0/200 | 0/200 | 200/200 |

Các họ 1, 3, 4, 7 mà cổng G1 yêu cầu đều được mô hình hóa tường minh; trên baseline B0/B1 chúng rò (E hoặc R = 200/200), còn B3 chặn hết (E=R=0) và **thất bại đóng** (fail-closed) với danh tính mơ hồ (họ 7).

## 4. Killer experiment (synthetic, n = 1 cấu hình tất định)

Ba điều kiện (a)(b)(c) đều đạt:

| Điều kiện | Kết quả |
|-----------|---------|
| (a) RAW vắng trong artifact được thiết bị | ✅ `raw_absent_from_instrumented_artifacts = true` |
| (b) Đích của kẻ tấn công bị từ chối | ✅ `attacker_destination_rejected = true` |
| (c) Đăng nhập hợp lệ vẫn thành công | ✅ `legitimate_login_succeeds = true` |
| Tổng | `passed = true`, `synthetic_only = true` |

## 5. Diễn giải (và cảnh báo)

- **Insight 1:** phát hiện ≠ bảo vệ. Ở B1, `E = 0` (canary bị lọc khỏi artifact thô) nhưng `L = 1.0` — bí mật vẫn rò ở bước sau khi vào. Đây là luận điểm ủng hộ hướng "đúc tại nguồn + ràng buộc đích" của \SH thay vì chỉ che/placeholder.
- **Insight 2:** B1 vẫn chuyển hướng được (`R = 1.0`) vì không ràng buộc đích; kể cả khi detector hoàn hảo, một chỉ dẫn injection vẫn định tuyến được giá trị. B3 chặn ở điểm giải (resolve) nên `R = 0`.
- **Insight 3:** với danh tính đích mơ hồ (họ 7), một hệ đúng phải **thất bại đóng**; B3 từ chối 200/200 trong khi B0/B1 vẫn gửi đi (200/200).
- B3 đạt E=R=L=F=Y=0 và U=1.0 với false-rejection = 0 trong mô hình tham chiếu.

**Điều tài liệu này KHÔNG nói:**
- Không phải số đo thiết bị thật; không đo độ trễ/năng lượng/keystore phần cứng.
- Không chứng minh tính đúng của cài đặt AOSP (mới là mô hình tham chiếu).
- Không dùng các số này trong phần Results của bản nộp; chúng chỉ là bằng chứng định hướng (evidence-of-concept) cho thiết kế.
