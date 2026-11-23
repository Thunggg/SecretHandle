# Checklist Hoàn thiện Cuối cùng — *SecretHandle* (ACM MobiSys 2027)

> **Nguồn đối chiếu:** `mobisys2027_review_secrethandle_v3.md` (Mode B Re-Review Vòng 3 ngày 23/11/2026).
>
> **Trạng thái hiện tại:** **4.0 / 5 (*Weak Accept — Đạt chuẩn sẵn sàng nộp*)**. Toàn bộ lỗi **Critical** và **Major** về số liệu, log JSON và định dạng CFP 12 trang đã được xử lý triệt để $100\%$.
>
> **Thời gian thực hiện ước tính:** $\sim 20$ phút (chỉ còn các mục đánh bóng nhỏ và hậu cần nộp bài).

---

## 1. Sửa bố cục trang 16 trống ở Phụ lục C (~2 phút)

**File cần sửa:** `mobisys/sections/artifact.tex`

- [x] Đưa `\clearpage` + khối `\begin{table*}[t]` (`\renewcommand{\arraystretch}{0.84}`) và tiêu đề `\section{Real-App UI Compatibility Audit}\label{sec:appendix_compat}` + đoạn giới thiệu 3 dòng nằm chung gọn gàng trên **Trang 16** (tổng số trang PDF rút từ 17 xuống còn **16 trang** gọn đẹp, không còn trang lẻ 3 dòng).
- *Xong khi:* Tiêu đề Phụ lục C, đoạn giới thiệu và Bảng 8 nằm chung gọn gàng trên **Trang 16** (tổng số trang PDF rút từ 17 xuống còn **16 trang** gọn đẹp, không còn trang lẻ 3 dòng).

---

## 2. Chuẩn hóa từ ngữ độ trễ khung hình ở Abstract, Intro và Conclusion (~3 phút)

**File cần sửa:** `mobisys/sections/abstract.tex`, `mobisys/sections/introduction.tex` (mục *Contribution (v)*), `mobisys/sections/conclusion.tex`

- [x] Đổi cụm *"zero touch-passthrough or measured frame-latency regression"* thành *"zero touch-passthrough or measured median/p95 frame-latency regression"* ở cả 3 vị trí (Abstract tr. 1, Intro tr. 2, Conclusion tr. 12).
- *Xong khi:* Câu chữ ở phần mở đầu và kết luận khớp tuyệt đối $100\%$ với phần báo cáo trung thực đuôi `p99` của `Settings` ($38.0 \rightarrow 101.0\,\text{ms}$) trong `§7 RQ6`.

---

## 3. Làm sạch 1 chuỗi chú thích nhỏ trong JSON & checklist (~2 phút)

**File cần sửa:** `output/real_apps_compatibility_audit.json`, `evidence_logs_all.json`, `tools/audit_real_apps_compatibility.py` *(và `revision_checklist.md` nếu lưu trữ nội bộ)*

- [x] Trong mục `OKX` $\rightarrow$ node `vg_country_code` (`android.widget.LinearLayout`), đã đổi trường `"reason"` từ `"WebView / custom / opaque view container (package boundary + touch confirmation)"` thành `"Custom / opaque view container (package boundary + touch confirmation)"` để không gây hiểu nhầm node này là `WebView`.
- [x] Sửa nhầm lẫn nhỏ `7/20, 10/20, 3/20` $\rightarrow$ `6/20, 9/20, 5/20` tại mục 4.3 của `ai_review_bundle/revision_checklist.md` cho đồng nhất với bài báo.

---

## 4. Biên dịch lại & kiểm tra chất lượng PDF cuối (~5 phút)

- [x] Chạy biên dịch sạch 5 lượt (XeLaTeX + BibTeX) và kiểm tra `manuscript_check.py` đạt `PASS`.
- [x] Xác nhận nhanh bằng công cụ:
  - `pdfinfo`: kích thước US Letter ($612 \times 792\,\text{pts}$), tổng **16 trang**, nội dung chính (`§1–§10`) kết thúc gọn trên **Trang 12** ($\le 12$ trang), Appendix C + Bảng 8 nằm chung trên **Trang 16**.
  - `pdffonts`: $100\%$ (`10/10`) font nhúng (`emb=yes, sub=yes, uni=yes`).
- [ ] Mở PDF trong Adobe Acrobat ở mức zoom $100\%$, rà nhanh Trang 1, Trang 4 (Hình 1), Trang 9 (Hình 2), Trang 11 (Bảng 6), Trang 12 (Kết luận) và Trang 16 (Phụ lục C + Bảng 8).

---

## 5. Kiểm tra Artifact công khai & Nộp bài trên HotCRP (~10 phút)

- [ ] **GitHub Artifact:** Đẩy toàn bộ mã nguồn, `output/*.json` và `evidence_logs_all.json` bản cuối lên `https://github.com/SecretHandle/SecretHandle`, sau đó mở bằng **trình duyệt ẩn danh (*incognito*)** để xác nhận kho truy cập công khai bình thường.
- [ ] **Mốc 1 — Đăng ký Abstract (trước `27/11/2026 23:59 AoE` — còn 4 ngày):**
  - Truy cập `https://mobisys27.hotcrp.com/`, điền tiêu đề, bản Abstract cuối ($\ge 100$ từ), chọn Regular Full Paper track (không tick Emerging Ideas).
  - Kiểm tra kỹ danh sách tác giả cố định (`Nguyễn Tiến Thuận`, `Trần Phát Tài`, FPT University Can Tho — không thể đổi sau khi nộp).
  - Rà soát và khai báo đầy đủ, chính xác mọi xung đột lợi ích (**COI**) với danh sách TPC và PC Co-Chairs (Jun Han, Falko Dressler).
- [ ] **Mốc 2 — Nộp bản PDF chính thức (trước `04/12/2026 23:59 AoE` — còn 11 ngày):**
  - Upload bản PDF cuối, chạy trình kiểm tra định dạng tự động (*format checker*) của HotCRP và xác nhận không còn cảnh báo.
  - Kiểm tra tính nhất quán khai báo Ethics (chỉ dùng synthetic canaries & static UI dumps, không human subjects) và khai báo LLM (khớp `§9`: proofreading only).
  - Hoàn tất nộp sớm trước hạn ít nhất 6–12 giờ.