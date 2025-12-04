# Remote Control System via LAN
> Đồ án Mạng máy tính - Ứng dụng điều khiển máy tính từ xa qua giao diện Web.

## Giới thiệu
Dự án xây dựng một hệ thống Client-Server cho phép người dùng điều khiển và giám sát một máy tính mục tiêu (Target Machine) thông qua giao diện Web. Hệ thống hoạt động trong mạng LAN, cho phép thao tác từ bất kỳ thiết bị nào có trình duyệt web.

### Kiến trúc hệ thống
Hệ thống bao gồm 2 thành phần chính:
1.  **Target Server (C#):** Chạy trên máy tính bị điều khiển. Chịu trách nhiệm thực thi các lệnh hệ thống.
2.  **Web Controller (Python):** Đóng vai trò là Client trung gian. Nhận tín hiệu từ người dùng qua Web và gửi lệnh đến Target Server.

---

## Tính năng chính

### Quản lý Hệ thống
- [x] **Applications:** Xem danh sách ứng dụng đang chạy, Stop ứng dụng.
- [x] **Processes:** Xem danh sách tiến trình, Kill tiến trình.
- [x] **Start App:** Khởi động một ứng dụng hoặc tiến trình mới.
- [x] **Power:** Shutdown hoặc Restart máy tính từ xa.

### Giám sát
- [x] **Screenshot:** Chụp ảnh màn hình máy tính mục tiêu.
- [x] **Webcam:** Bật/Tắt Webcam và ghi hình trong khoảng thời gian định trước.
- [x] **Keylogger:** Bắt và lưu lại các phím đã nhấn.

---

## Cấu trúc thư mục

```text
DoAn_MangMayTinh/
├── Target_Server_CSharp/     # Source code phần điều khiển máy tính (viết bằng C#)
├── Web_Controller_Python/    # Source code phần giao diện Web (viết bằng Python)
├── AI_Chatlog/               # Nhật ký phát triển và trao đổi với AI
└── README.md
