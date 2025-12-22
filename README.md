# 🖥️ Remote Control System via LAN

> **Đồ án Mạng Máy Tính** - Ứng dụng điều khiển máy tính từ xa qua giao diện Web

[![Python](https://img.shields.io/badge/Python-3.10--3.13-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![C#](https://img.shields.io/badge/C%23-.NET%204.7.2-purple.svg)](https://dotnet.microsoft.com/)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)](#)

---

## 📖 Giới Thiệu

Dự án xây dựng một hệ thống **Client-Server** cho phép người dùng điều khiển và giám sát một máy tính mục tiêu (Target Machine) thông qua giao diện Web. Hệ thống hoạt động trong **mạng LAN**, cho phép thao tác từ bất kỳ thiết bị nào có trình duyệt web.

### 🏗️ Kiến Trúc Hệ Thống

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
| **Target Server** | C# (.NET 4.7.2) | Máy bị điều khiển, thực thi lệnh hệ thống |
| **Web Controller** | Python (Django 4.2) | Client trung gian, nhận tín hiệu từ Web và gửi đến Server |

---

## ✨ Tính Năng Chính

### 🖥️ Quản Lý Hệ Thống
| Tính năng | Mô tả | Trạng thái |
|-----------|-------|:----------:|
| **Applications** | Xem/Dừng các ứng dụng đang chạy | ✅ |
| **Processes** | Xem/Kill tất cả tiến trình hệ thống | ✅ |
| **Start App** | Khởi động ứng dụng từ Start Menu hoặc đường dẫn | ✅ |
| **Power** | Shutdown / Restart máy tính từ xa | ✅ |

### 📷 Giám Sát
| Tính năng | Mô tả | Trạng thái |
|-----------|-------|:----------:|
| **Screenshot** | Chụp ảnh màn hình tức thời | ✅ |
| **Screen Recording** | Quay video màn hình, lưu file .avi | ✅ |
| **Webcam** | Bật/Ghi hình webcam của máy mục tiêu | ✅ |
| **Keylogger** | Ghi lại các phím đã nhấn | ✅ |

### 🛠️ Quản Lý Nâng Cao
| Tính năng | Mô tả | Trạng thái |
|-----------|-------|:----------:|
| **Remote Shell** | Chạy lệnh CMD trực tiếp trên server | ✅ |
| **File Manager** | Duyệt, Download, Xóa file trên server | ✅ |
| **System Info** | Xem thông tin CPU, RAM, Disk, GPU realtime | ✅ |

---

## 🚀 Bắt Đầu Nhanh

> 📚 Xem hướng dẫn chi tiết tại [QUICK_START.md](QUICK_START.md)

### Yêu Cầu
- **Python** 3.10 - 3.13 (Client)
- **Visual Studio** 2019/2022 với .NET Framework 4.7.2 (Server)
- Cả hai máy cùng **mạng LAN**

### 3 Bước Chạy Nhanh

```bash
# 1️⃣ Khởi động Server (Visual Studio)
#    Mở Server/TargetServer/TargetServer.slnx → F5 → Bấm "Open Server"

# 2️⃣ Khởi động Client
cd Client
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

# 3️⃣ Mở trình duyệt → http://localhost:8000 → Discover → Connect
```

---

## 📁 Cấu Trúc Thư Mục

```
DoAn_MangMayTinh/
│
├── 📁 Client/                      # 🌐 Web Controller (Django)
│   ├── 📁 apps/
│   │   └── 📁 remote_control/      # ⭐ App điều khiển chính
│   ├── 📁 config/                  # Cấu hình Django
│   ├── 📁 templates/               # Giao diện HTML
│   ├── manage.py
│   └── requirements.txt
│
├── 📁 Server/                      # 🖥️ Target Server (C#)
│   └── 📁 TargetServer/
│       ├── server.cs               # ⭐ Logic server chính
│       ├── Keylog.cs               # Module Keylogger
│       ├── WebcamRecorder.cs       # Module Webcam
│       ├── ScreenRecorder.cs       # Module Screen Recording
│       ├── FileManager.cs          # Module File Manager
│       └── TargetServer.slnx       # Solution file
│
├── 📁 AI_Chatlog/                  # 📝 Nhật ký phát triển với AI
│   ├── 1 - Xây dựng nền tảng.md
│   ├── 2 - Webcam.md
│   ├── 3 - Nâng cấp UI và luồng chạy.md
│   ├── 4 - Sửa lỗi webcam.md
│   ├── 5 - Remote shell CMD.md
│   ├── 6 - Screen recording.md
│   ├── 7 - Sửa lỗi screen recording và webcam.md
│   ├── 8 - File manager.md
│   ├── 9 - Home tab + sửa lỗi.md
│   └── 10 - App scanner + Tổng duyệt code.md
│
├── 📄 README.md                    # Giới thiệu dự án (file này)
├── 📄 QUICK_START.md               # 🚀 Hướng dẫn chạy nhanh
├── 📄 PROJECT_SUMMARY.md           # 📊 Tổng quan kiến trúc
├── 📄 MIGRATION_GUIDE.md           # 📚 Chi tiết migration Flask → Django
└── 📄 TESTING_CHECKLIST.md         # ✅ Checklist test đầy đủ
```

---

## 📝 Nhật Ký Phát Triển (AI Chatlog)

Dự án được phát triển với sự hỗ trợ của các công cụ AI. Dưới đây là chi tiết từng giai đoạn:

| # | Giai đoạn | Nội dung | Assistant |
|---|-----------|----------|-----------|
| 1 | **Xây dựng nền tảng** | Khởi tạo cấu trúc thư mục và tạo các chức năng cơ bản của dự án từ source code mẫu. Code server chạy bằng C#, code client chạy bằng Python (Flask). | Gemini |
| 2 | **Webcam** | Thêm tính năng webcam cho ứng dụng web, bao gồm bật/tắt và ghi hình. | Gemini |
| 3 | **Nâng cấp UI và luồng chạy** | Xây dựng lại web client bằng Django, xây dựng persistent socket bằng TCP. Thêm tính năng discover server trong client web bằng UDP. | GitHub Copilot |
| 4 | **Sửa lỗi webcam** | Sửa các lỗi trong phần webcam liên quan đến stream và recording. | Gemini |
| 5 | **Remote Shell CMD** | Thêm tính năng Remote Shell CMD, cho phép người dùng chạy CMD Prompt của máy server bằng giao diện web. | Gemini |
| 6 | **Screen Recording** | Thêm tính năng screen recording, cho phép quay màn hình máy tính của server. | Gemini |
| 7 | **Sửa lỗi screen recording và webcam** | Sửa các lỗi liên quan đến các tương tác với các nút giao diện khi sử dụng screen recording và webcam. | Gemini |
| 8 | **File Manager** | Thêm tính năng file manager, cho phép người dùng truy cập, download và delete file bên máy chủ server. | Gemini |
| 9 | **Home tab + sửa lỗi** | Thêm tính năng home page hiển thị các thông tin của máy bị điều khiển (CPU, RAM, Disk, v.v.). Sửa một số lỗi còn lại. | Gemini |
| 10 | **App scanner + Tổng duyệt code** | Thêm tính năng quét Start Menu folder cho Applications và Processes Manager. Đồng thời tổng duyệt và tối ưu code. | GitHub Copilot |

---

## 📚 Tài Liệu Bổ Sung

| Tài liệu | Mô tả |
|----------|-------|
| [QUICK_START.md](QUICK_START.md) | 🚀 Hướng dẫn chạy nhanh trong 3 bước |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | 📊 Tổng quan kiến trúc và công nghệ |
| [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) | 📚 Chi tiết quá trình migration Flask → Django |
| [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md) | ✅ Checklist test đầy đủ các tính năng |

---

## 🛠️ Công Nghệ Sử Dụng

### Backend
- **Django 4.2** - Web Framework
- **Python 3.10 - 3.13** - Ngôn ngữ backend
- **C# .NET 4.7.2** - Server-side (Windows)
- **SQLite** - Database

### Frontend
- **Tailwind CSS** - Styling
- **JavaScript (Vanilla)** - Client-side logic
- **Alpine.js** - Reactive UI

### Networking
- **TCP Socket** - Persistent connection (Port 5656)
- **UDP Broadcast** - Server discovery (Port 5657)

### Libraries (C#)
- **AForge.Video** - Webcam capture
- **System.Drawing** - Screenshot, Image processing

---

## ⚠️ Lưu Ý Quan Trọng

1. **Thứ tự khởi động**: Luôn khởi động **Server trước**, sau đó mới **Client**
2. **Firewall**: Cho phép cổng 5656 (TCP) và 5657 (UDP)
3. **Antivirus**: Một số tính năng có thể bị cảnh báo - đây là hành vi bình thường
4. **Quyền Admin**: Chạy Visual Studio với quyền Administrator

---

## 📜 License

Dự án được phát triển cho mục đích **học tập** tại môn Mạng Máy Tính.

---

<p align="center">
  <b>🎓 Đồ án Môn Mạng Máy Tính - 2025</b>
</p>
