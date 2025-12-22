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
├── Client/                         # Web Controller (Django)
│   ├── apps/
│   │   └── remote_control/         # App điều khiển chính
│   │       ├── views.py
│   │       ├── urls.py
│   │       ├── socket_client_persistent.py
│   │       ├── udp_discovery.py
│   │       └── ...
│   ├── config/                     # Cấu hình Django
│   ├── templates/
│   │   ├── remote_control/         # Giao diện các tính năng
│   │   ├── layouts/
│   │   └── includes/
│   ├── manage.py
│   └── requirements.txt
│
├── Server/                         # Target Server (C#)
│   └── TargetServer/
│       ├── server.cs               # Logic server chính
│       ├── Keylog.cs
│       ├── WebcamRecorder.cs
│       ├── ScreenRecorder.cs
│       ├── FileManager.cs
│       └── TargetServer.slnx
│
├── AI_Chatlog/                     # Nhật ký phát triển
└── *.md                            # Tài liệu
```

---

## 📝 Nhật Ký Phát Triển

| # | Giai đoạn | Nội dung | AI |
|---|-----------|----------|-----|
| 1 | Xây dựng nền tảng | Khởi tạo project, chức năng cơ bản | Gemini |
| 2 | Webcam | Bật/tắt và ghi hình webcam | Gemini |
| 3 | Nâng cấp UI | Django, persistent socket, UDP discovery | GitHub Copilot |
| 4 | Sửa lỗi webcam | Stream và recording | Gemini |
| 5 | Remote Shell | CMD từ xa qua web | Gemini |
| 6 | Screen Recording | Quay màn hình | Gemini |
| 7 | Sửa lỗi | Screen recording và webcam | Gemini |
| 8 | File Manager | Duyệt, download, xóa file | Gemini |
| 9 | Home tab | System info dashboard | Gemini |
| 10 | App scanner | Start Menu scan, tối ưu code | GitHub Copilot |

---

## 📚 Tài Liệu

- [QUICK_START.md](QUICK_START.md) - Hướng dẫn chạy nhanh
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Tổng quan kiến trúc
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - Migration Flask → Django
- [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md) - Checklist test

---

**🎓 Đồ án Môn Mạng Máy Tính - 2025**
