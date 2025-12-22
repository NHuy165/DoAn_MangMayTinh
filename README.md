# 🖥️ Remote Control System via LAN

> **Đồ án Mạng Máy Tính** - Ứng dụng điều khiển máy tính từ xa qua giao diện Web

---

## 📖 Giới Thiệu

Dự án xây dựng một hệ thống **Client-Server** cho phép điều khiển và giám sát máy tính mục tiêu (Target Machine) thông qua giao diện Web trong **mạng LAN**.

### 🏗️ Kiến Trúc

```
┌─────────────────┐         TCP:5656          ┌──────────────────┐
│   WEB BROWSER   │◄─────────────────────────►│  TARGET SERVER   │
│  (Controller)   │                           │   (Windows PC)   │
│                 │         UDP:5657          │                  │
│  Django + HTML  │◄ ─ ─ ─ (Discovery) ─ ─ ─ ►│   C# WinForms    │
└─────────────────┘                           └──────────────────┘
```

| Thành phần | Ngôn ngữ | Vai trò |
|------------|----------|---------|
| **Target Server** | C# (.NET 4.7.2) | Máy bị điều khiển |
| **Web Controller** | Python (Django 4.2) | Giao diện điều khiển |

---

## ✨ Tính Năng

| Nhóm | Tính năng |
|------|-----------|
| **Quản lý hệ thống** | Applications, Processes, Start App, Power Control |
| **Giám sát** | Screenshot, Screen Recording, Webcam, Keylogger |
| **Nâng cao** | Remote Shell, File Manager, System Info |

---

## 🚀 Bắt Đầu Nhanh

> 📚 Xem chi tiết tại [QUICK_START.md](QUICK_START.md)

```bash
# 1️⃣ Khởi động Client (Django)
cd Client
python -m venv venv && .\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

# 2️⃣ Khởi động Server (Visual Studio)
#    Mở Server/TargetServer/TargetServer.slnx → F5 → Bấm "Open Server"

# 3️⃣ Mở trình duyệt → http://localhost:8000 → Discover → Connect
```

---

## 📁 Cấu Trúc Thư Mục

```
DoAn_MangMayTinh/
│
├── Client/                             # 🌐 Web Controller (Django)
│   ├── apps/remote_control/            # ⭐ App điều khiển chính
│   │   ├── views.py                    # API endpoints
│   │   ├── socket_client_persistent.py # Kết nối TCP với Target
│   │   └── udp_discovery.py            # Broadcast tìm server
│   ├── config/                         # Cấu hình Django
│   ├── templates/remote_control/       # 🎨 Giao diện HTML
│   │   ├── *.html                      # Wrapper templates
│   │   └── partials/*_partial.html     # Code JS/HTML cho từng tính năng
│   ├── media/                          # 📂 Lưu recordings từ Target
│   ├── requirements.txt
│   │
│   └── ...
│
├── Server/TargetServer/                # 🖥️ Target Server (C#)
│   ├── server.cs                       # Logic server chính
│   ├── Keylog.cs, WebcamRecorder.cs    # Các module chức năng
│   ├── ScreenRecorder.cs, FileManager.cs
│   └── TargetServer.slnx               # Solution file
│
├── AI_Chatlog/                         # 📝 Nhật ký phát triển
└── *.md                                # 📚 Tài liệu
```

---

## 📝 Nhật Ký Phát Triển (AI Chatlog)

Dự án được phát triển với sự hỗ trợ của các công cụ AI. Dưới đây là chi tiết từng giai đoạn:

| # | Giai đoạn | Nội dung | Assistant |
|---|-----------|----------|-----|
| 1 | **Xây dựng nền tảng** | Khởi tạo cấu trúc thư mục và tạo các chức năng cơ bản của dự án từ source code mẫu. Code server chạy bằng C#, code client chạy bằng Python (Flask). | Gemini |
| 2 | **Webcam** | Thêm tính năng webcam cho ứng dụng web, bao gồm bật/tắt và ghi hình. | Gemini |
| 3 | **Nâng cấp UI và luồng chạy** | Xây dựng lại web client bằng Django, xây dựng persistent socket bằng TCP. Thêm tính năng discover server trong client web bằng UDP. | GitHub Copilot |
| 4 | **Sửa lỗi webcam** | Sửa các lỗi trong phần webcam liên quan đến stream và recording. | Gemini |
| 5 | **Remote shell CMD** | Thêm tính năng Remote Shell CMD, cho phép người dùng chạy CMD Prompt của máy server bằng giao diện web. | Gemini |
| 6 | **Screen recording** | Thêm tính năng screen recording, cho phép quay màn hình máy tính của server. | Gemini |
| 7 | **Sửa lỗi screen recording và webcam** | Sửa các lỗi liên quan đến các tương tác với các nút giao diện khi sử dụng screen recording và webcam. | Gemini |
| 8 | **File manager** | Thêm tính năng file manager, cho phép người dùng truy cập, download và delete file bên máy chủ server. | Gemini |
| 9 | **Home tab + sửa lỗi** | Thêm tính năng home page hiển thị các thông tin của máy bị điều khiển (CPU, RAM, Disk, v.v.). Sửa một số lỗi còn lại. | Gemini |
| 10 | **App scanner + Tổng duyệt code** | Thêm tính năng quét Start Menu folder cho Applications và Processes Manager. Đồng thời tổng duyệt và tối ưu code. | GitHub Copilot |

---

## 📚 Tài Liệu

- [QUICK_START.md](QUICK_START.md) - Hướng dẫn chạy nhanh
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Tổng quan kiến trúc

---

**🎓 Đồ án Môn Mạng Máy Tính - 2025**
