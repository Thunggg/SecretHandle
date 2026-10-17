# Khung đạo đức và an toàn nghiên cứu

Tài liệu này là khung đạo đức cho giai đoạn hiện tại (tái hiện B0 trên emulator). Nó thỏa mục "Khung đạo đức" trong PHẦN B của `checkLists/MASTER_CHECKLIST.tex` và mục ethics của CFP MobiSys.

## 1. Phạm vi và tuyên bố

- Nghiên cứu **phòng thủ**: chứng minh rò rỉ OTP/bí mật qua quan sát của tác nhân AI di động trên Android, rồi thiết kế cơ chế chống lại.
- Giai đoạn này chỉ dùng **emulator** và **canary tổng hợp**. Không có người tham gia, không dữ liệu cá nhân thật.

## 2. Nguyên tắc

1. **Không dữ liệu thật.** Chỉ canary tổng hợp (OTP giả sinh ngẫu nhiên); không số điện thoại, email, tài khoản hay bí mật thật. Không đăng nhập tài khoản Google thật trên emulator.
2. **Endpoint cô lập.** Monitor disclosure chỉ nghe trên mạng nội bộ của máy chủ; payload không rời khỏi máy. Không gửi ra Internet.
3. **Không ảnh hưởng bên thứ ba.** Mọi thử nghiệm chạy trong emulator do nhóm kiểm soát; không nhắm vào thiết bị/dịch vụ của người khác.
4. **Minh bạch.** Ghi rõ môi trường (emulator, ảnh stock) và nguồn số liệu (mô phỏng/tái hiện); **không** trình bày placeholder như kết quả thật.
5. **Không human subjects.** Chỉ dùng canary tổng hợp ⇒ không cần IRB ở giai đoạn này.

## 3. Quy trình canary

- Sinh canary ngẫu nhiên mỗi lần chạy; dùng một lần cho một kịch bản.
- Log chỉ chứa canary và bối cảnh tổng hợp; không chứa PII.
- Sau mỗi phiên: dừng monitor; xóa log/đầu ra harness nếu không cần giữ lại.

## 4. Endpoint và đồng thuận

- `device/b0-otp-forwarding/monitor/monitor.py` bind cổng nội bộ (mặc định `8787`); emulator trỏ tới `10.0.2.2`. Không TLS, không Internet.
- Không thu thập dữ liệu người; không cần consent form.

## 5. Kiểm yêu cầu IRB / ethics CFP

- MobiSys yêu cầu tuyên bố ethics: nêu rõ dùng canary tổng hợp, không human subjects, không dữ liệu thật.
- Kết luận: **không cần IRB** cho giai đoạn emulator + canary.
- Điều kiện xem lại: nếu mở rộng sang **thiết bị thật có người dùng** hoặc dữ liệu thật ⇒ phải xin phê duyệt IRB và có đồng thuận.

## 6. Khóa/công cụ giả

- `device/b0-otp-forwarding/debug.keystore`: keystore debug Android dùng một lần để ký APK thử nghiệm (mật khẩu mặc định `android`), **không** phải khóa thật.
- Không commit artifact build (`build/`, `*.apk`) và không commit keystore trừ khi thật cần — xem `device/b0-otp-forwarding/.gitignore`.

## 7. Chia sẻ kết quả

- Không phát hành mã khai thác nhắm vào hệ thống thật; harness chỉ dùng nội bộ/emulator.
- Công bố kèm giới hạn rõ ràng để tránh phóng đại kết luận.
