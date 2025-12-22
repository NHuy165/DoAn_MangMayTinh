# 📊 Tổng Quan Dự Án (Project Summary)

> **Remote Control System via LAN** - Hệ thống điều khiển máy tính từ xa qua mạng LAN

---

## 🎯 Mục Tiêu Dự Án

Xây dựng một hệ thống **Client-Server** cho phép:
- **Điều khiển** máy tính mục tiêu (Target Machine) từ xa
- **Giám sát** hoạt động của máy mục tiêu thông qua giao diện Web

---

## 🏗️ Kiến Trúc Hệ Thống

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           MẠNG LAN (Local Area Network)                 │
│                                                                         │
│  ┌─────────────────┐           TCP/UDP          ┌──────────────────┐    │
│  │   WEB BROWSER   │◄──────────────────────────►│  TARGET SERVER   │    │
│  │  (Any Device)   │                            │   (Windows PC)   │    │
│  │                 │                            │                  │    │
│  │  ┌───────────┐  │    HTTP Request/Response   │  ┌────────────┐  │    │
│  │  │  Web UI   │  │◄────────────────────────►  │  │   C# App   │  │    │
│  │  │  (HTML/   │  │                            │  │  (WinForms)│  │    │
│  │  │   CSS/JS) │  │         TCP:5656           │  │            │  │    │
│  │  └───────────┘  │     (Persistent Socket)    │  │  - Keylog  │  │    │
│  └────────┬────────┘◄ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ► │  │  - Webcam  │  │    │
│           │                                     │  │  - Screen  │  │    │
│           │ HTTP:8000                           │  │  - Shell   │  │    │
│           ▼                                     │  │  - Files   │  │    │
│  ┌─────────────────┐         UDP:5657           │  └────────────┘  │    │
│  │  DJANGO SERVER  │◄ ─ ─ ─ ─(Discovery) ─ ─ ─ ►│                  │    │
│  │  (Web Client)   │                            └──────────────────┘    │
│  │                 │                                                    │
│  │  ┌───────────┐  │                                                    │
│  │  │  Python   │  │                                                    │
│  │  │  Backend  │  │                                                    │
│  │  └───────────┘  │                                                    │
│  └─────────────────┘                                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Các Thành Phần

| Thành phần | Ngôn ngữ | Vai trò | Vị trí |
|------------|----------|---------|--------|
| **Target Server** | C# (.NET 4.7.2) | Máy bị điều khiển | `Server/TargetServer/` |
| **Web Controller** | Python (Django 4.2) | Giao diện điều khiển | `Client/` |

---

## 🔌 Giao Thức Truyền Thông

| Giao thức | Port | Mục đích |
|-----------|------|----------|
| **UDP Discovery** | 5657 | Tìm kiếm server trong mạng LAN |
| **TCP Persistent** | 5656 | Truyền lệnh và dữ liệu |

---

## ✨ Tính Năng

### 🖥️ Quản Lý Hệ Thống
| Tính năng | Mô tả |
|-----------|-------|
| **Applications** | Xem/Dừng các ứng dụng đang chạy |
| **Processes** | Xem/Kill tất cả tiến trình hệ thống |
| **Start App** | Khởi động ứng dụng từ Start Menu hoặc đường dẫn |
| **Power** | Shutdown / Restart máy tính từ xa |

### 📷 Giám Sát
| Tính năng | Mô tả |
|-----------|-------|
| **Screenshot** | Chụp ảnh màn hình tức thời |
| **Screen Recording** | Quay video màn hình, lưu file .avi |
| **Webcam** | Bật/Ghi hình webcam |
| **Keylogger** | Ghi lại các phím đã nhấn |

### 🛠️ Quản Lý Nâng Cao
| Tính năng | Mô tả |
|-----------|-------|
| **Remote Shell** | Chạy lệnh CMD trực tiếp |
| **File Manager** | Duyệt, Download, Xóa file |
| **System Info** | Xem thông tin CPU, RAM, Disk |

---

## 🛠️ Công Nghệ Sử Dụng

### Backend
| Công nghệ | Mục đích |
|-----------|----------|
| **Django 4.2** | Web Framework |
| **Python 3.10+** | Ngôn ngữ backend |
| **C# .NET 4.7.2** | Server-side |

### Frontend
| Công nghệ | Mục đích |
|-----------|----------|
| **Tailwind CSS** | Styling |
| **JavaScript** | Client-side logic |

### Libraries (C#)
| Library | Mục đích |
|---------|----------|
| **AForge.Video** | Webcam capture |
| **System.Drawing** | Screenshot |

---

## 📂 Cấu Trúc Thư Mục

```
DoAn_MangMayTinh/
├── Client/                             # Web Controller (Django)
│   ├── apps/
│   │   ├── remote_control/             # App chính
│   │   │   ├── views.py                # API endpoints
│   │   │   ├── urls.py
│   │   │   ├── socket_client_persistent.py
│   │   │   ├── udp_discovery.py
│   │   │   └── ...
│   │   └── pages/                      # Dashboard pages
│   ├── config/
│   │   ├── settings.py
│   │   └── urls.py
│   ├── templates/
│   │   ├── remote_control/             # Feature templates
│   │   │   ├── home.html
│   │   │   ├── applications.html
│   │   │   ├── processes.html
│   │   │   ├── screenshot.html
│   │   │   ├── screen.html
│   │   │   ├── webcam.html
│   │   │   ├── keylogger.html
│   │   │   ├── shell.html
│   │   │   ├── file_manager.html
│   │   │   ├── power.html
│   │   │   └── partials/
│   │   ├── layouts/
│   │   └── includes/
│   ├── static/
│   ├── media/
│   ├── manage.py
│   └── requirements.txt
│
├── Server/                             # Target Server (C#)
│   └── TargetServer/
│       ├── server.cs                   # Main server logic
│       ├── Program.cs
│       ├── Keylog.cs
│       ├── WebcamRecorder.cs
│       ├── ScreenRecorder.cs
│       ├── FileManager.cs
│       ├── TargetServer.csproj
│       └── TargetServer.slnx
│
├── AI_Chatlog/                         # Nhật ký phát triển
│   └── *.md
│
└── *.md                                # Tài liệu
```

---

## 🔄 Luồng Hoạt Động

### 1. Discovery
```
[Django] ──UDP Broadcast──► [All Servers in LAN]
       ◄──UDP Response────── [Target Server]
```

### 2. Connect
```
[Django] ──TCP Connect──► [Target Server:5656]
       ◄──TCP ACK─────────
```

### 3. Command
```
[User Click] → [HTTP POST] → [Django] → [socket.send()] → [Server executes]
                                      ← [socket.recv()] ← [Response]
```

---

**🎓 Đồ án Môn Mạng Máy Tính - 2025**
