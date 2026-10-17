# Bằng chứng sơ bộ từ mô hình tham chiếu (mô phỏng)

> **Nhãn bắt buộc:** Toàn bộ số trong tài liệu này đến từ **mô hình tham chiếu Python** chạy ở chế độ **synthetic** (canary tổng hợp, độ trễ là đại lượng thay thế tất định). Đây **không phải** kết quả trên thiết bị/AOSP và **không** phải số cho bài báo. Không con số nào ở đây được dùng làm kết quả đánh giá thật.

## 1. Mục đích

Cho thấy mô hình tham chiếu tái lập được các xu hướng định tính mà thiết kế \SH dự đoán (B0 → B3), làm nền cho khung bản thảo và cho kế hoạch đánh giá đầy đủ (`docs/evaluation_plan.md`).

## 2. Cách tái lập

```bash
python scripts/run_synthetic_demo.py --config configs/preliminary_evidence.yaml
python scripts/run_experiment.py  --config configs/preliminary_evidence.yaml --stage killer
```

- Cấu hình: `configs/preliminary_evidence.yaml` (seed `20261017`, `trials_per_attack: 200`, tổng **4800 trials**).
- Đầu ra: `outputs/preliminary_evidence/{trials.jsonl,summary.json,metrics.csv,provenance.json}` (thư mục `outputs/` được gitignore; chạy lại để tái tạo).
- `provenance.json` ghi phiên bản Python/nền tảng, seed, hash cấu hình, và cờ `real_experiment=false`.

## 3. Kết quả (synthetic, n = 200/attack; khoảng tin cậy Wilson 95%)

| Điều kiện | E (exposure) | R (redirection) | U (utility) | L (post-entry leak) | F (forgery) | Y (replay) |
|-----------|--------------|-----------------|-------------|---------------------|-------------|------------|
| B0 (không bảo vệ) | 1.000 [0.997, 1.000] | 1.000 [0.981, 1.000] | 1.000 [0.981, 1.000] | — (n/a) | — (n/a) | — (n/a) |
| B1 (placeholder bị phát hiện) | 0.000 [0.000, 0.003] | 1.000 [0.981, 1.000] | 1.000 [0.981, 1.000] | **1.000** [0.981, 1.000] | — (n/a) | — (n/a) |
| B2 (platform flow) | — (không áp dụng) | — | — | — | — | — |
| B3 (\SH) | 0.000 [0.000, 0.003] | 0.000 [0.000, 0.019] | 1.000 [0.994, 1.000] | 0.000 [0.000, 0.010] | 0.000 [0.000, 0.019] | 0.000 [0.000, 0.019] |

- B3 thêm: `policy_rejection = 0.667` (800/1200; 4 họ tấn công bị từ chối) và `false_rejection = 0.000` (200/200 tác vụ hợp lệ không bị chặn nhầm).
- **B2 để trống có chủ đích**: baseline luồng nền tảng cần hạ tầng ngoài chưa cấp phát → mọi trial có `not_applicable` (đúng nguyên tắc `not_applicable`, không phải thất bại giả).

## 4. Killer experiment (synthetic, n = 1 cấu hình tất định)

Ba điều kiện (a)(b)(c) đều đạt:

| Điều kiện | Kết quả |
|-----------|---------|
| (a) RAW vắng trong artifact được thiết bị | ✅ `raw_absent_from_instrumented_artifacts = true` |
| (b) Đích của kẻ tấn công bị từ chối | ✅ `attacker_destination_rejected = true` |
| (c) Đăng nhập hợp lệ vẫn thành công | ✅ `legitimate_login_succeeds = true` |
| Tổng | `passed = true`, `synthetic_only = true` |

## 5. Diễn giải (và cảnh báo)

- **Insight chính:** phát hiện ≠ bảo vệ. Ở B1, `E = 0` (canary bị lọc khỏi artifact thô) nhưng `L = 1.0` — bí mật vẫn rò ở bước sau khi vào. Đây là luận điểm ủng hộ hướng "đúc tại nguồn + ràng buộc đích" của \SH thay vì chỉ che/placeholder.
- B3 đạt E=R=L=F=Y=0 và U=1.0 với false-rejection = 0 trong mô hình tham chiếu.

**Điều tài liệu này KHÔNG nói:**
- Không phải số đo thiết bị thật; không đo độ trễ/năng lượng/keystore phần cứng.
- Không chứng minh tính đúng của cài đặt AOSP (mới là mô hình tham chiếu).
- Không dùng các số này trong phần Results của bản nộp; chúng chỉ là bằng chứng định hướng (evidence-of-concept) cho thiết kế.
