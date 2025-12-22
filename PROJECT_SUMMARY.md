# 📊 Tổng Quan Dự Án (Project Summary)

> **Remote Control System via LAN** - Hệ thống điều khiển máy tính từ xa qua mạng LAN

---

## 🎯 Mục Tiêu Dự Án

Xây dựng một hệ thống **Client-Server** cho phép người dùng:
- **Điều khiển** một máy tính mục tiêu (Target Machine) từ xa
- **Giám sát** hoạt động của máy mục tiêu thông qua giao diện Web
- Hoạt động hoàn toàn trong **mạng LAN**, không cần Internet

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

### Các Thành Phần Chính

| Thành phần | Ngôn ngữ | Vai trò | Vị trí |
|------------|----------|---------|--------|
| **Target Server** | C# (.NET 4.7.2) | Máy bị điều khiển, thực thi lệnh | `Server/TargetServer/` |
| **Web Controller** | Python (Django 4.2) | Giao diện điều khiển trung gian | `Client/` |
| **Web UI** | HTML/CSS/JS (Tailwind) | Giao diện người dùng | `Client/templates/` |

---

## 🔌 Giao Thức Truyền Thông

### 1. UDP Discovery (Port 5657)
- **Mục đích**: Tìm kiếm các server trong mạng LAN
- **Cơ chế**: Client broadcast → Server response với IP và thông tin

### 2. TCP Persistent Connection (Port 5656)
- **Mục đích**: Truyền lệnh và dữ liệu giữa Client-Server
- **Cơ chế**: Kết nối một lần, duy trì xuyên suốt phiên làm việc
- **Format**: `COMMAND|SUB_COMMAND|DATA`

---

## ✨ Tính Năng Chi Tiết

### 🖥️ Quản Lý Hệ Thống

| Tính năng | Mô tả | Trạng thái |
|-----------|-------|------------|
| **Applications** | Xem/Dừng các ứng dụng đang chạy (có cửa sổ) | ✅ Hoàn thành |
| **Processes** | Xem/Kill tất cả tiến trình hệ thống | ✅ Hoàn thành |
| **Start App** | Khởi động ứng dụng từ Start Menu hoặc đường dẫn | ✅ Hoàn thành |
| **Power** | Shutdown / Restart máy tính từ xa | ✅ Hoàn thành |

### 📷 Giám Sát

| Tính năng | Mô tả | Trạng thái |
|-----------|-------|------------|
| **Screenshot** | Chụp ảnh màn hình tức thời | ✅ Hoàn thành |
| **Screen Recording** | Quay video màn hình, lưu file .avi | ✅ Hoàn thành |
| **Webcam** | Bật/Ghi hình webcam của máy mục tiêu | ✅ Hoàn thành |
| **Keylogger** | Ghi lại các phím đã nhấn | ✅ Hoàn thành |

### 🛠️ Quản Lý Nâng Cao

| Tính năng | Mô tả | Trạng thái |
|-----------|-------|------------|
| **Remote Shell** | Chạy lệnh CMD trực tiếp trên server | ✅ Hoàn thành |
| **File Manager** | Duyệt, Download, Xóa file trên server | ✅ Hoàn thành |
| **System Info** | Xem thông tin CPU, RAM, Disk, GPU | ✅ Hoàn thành |

---

## 🛠️ Công Nghệ Sử Dụng

### Backend

| Công nghệ | Phiên bản | Mục đích |
|-----------|-----------|----------|
| **Django** | 4.2.9 | Web Framework chính |
| **Python** | 3.10 - 3.13 | Ngôn ngữ backend |
| **C# .NET** | 4.7.2 | Server-side (Windows) |
| **SQLite** | - | Database mặc định |

### Frontend

| Công nghệ | Mục đích |
|-----------|----------|
| **Tailwind CSS** | Styling framework |
| **JavaScript (Vanilla)** | Client-side logic |
| **Alpine.js** | Reactive UI components |

### Networking

| Công nghệ | Mục đích |
|-----------|----------|
| **TCP Socket** | Persistent connection |
| **UDP Broadcast** | Server discovery |
| **HTTP/REST** | Web API |

### Libraries (C#)

| Library | Mục đích |
|---------|----------|
| **AForge.Video** | Webcam capture |
| **System.Drawing** | Screenshot, Image processing |
| **System.Diagnostics** | Process management |

---

## 📂 Cấu Trúc Thư Mục Chi Tiết

```
DoAn_MangMayTinh/
│
├── 📁 Client/                          # Web Controller (Django)
│   ├── 📁 apps/
│   │   ├── 📁 remote_control/          # ⭐ App chính
│   │   │   ├── views.py                # API endpoints
│   │   │   ├── urls.py                 # URL routing
│   │   │   ├── models.py               # Database models
│   │   │   ├── socket_client_persistent.py  # TCP client
│   │   │   └── udp_discovery.py        # UDP discovery
│   │   └── 📁 pages/                   # Dashboard & Pages
│   ├── 📁 config/
│   │   ├── settings.py                 # Django config
│   │   └── urls.py                     # Root URL config
│   ├── 📁 templates/
│   │   ├── 📁 remote_control/          # Feature templates
│   │   └── 📁 layouts/                 # Base templates
│   ├── 📁 static/                      # CSS, JS, Images
│   ├── manage.py                       # Django CLI
│   └── requirements.txt                # Python dependencies
│
├── 📁 Server/                          # Target Server (C#)
│   └── 📁 TargetServer/
│       ├── server.cs                   # ⭐ Main server logic
│       ├── Program.cs                  # Entry point
│       ├── Keylog.cs                   # Keylogger module
│       ├── WebcamRecorder.cs           # Webcam module
│       ├── ScreenRecorder.cs           # Screen recording module
│       ├── FileManager.cs              # File manager module
│       └── TargetServer.csproj         # Project file
│
├── 📁 AI_Chatlog/                      # Nhật ký phát triển
│   ├── 1 - Xây dựng nền tảng.md
│   ├── 2 - Webcam.md
│   └── ...
│
├── README.md                           # Giới thiệu dự án
├── QUICK_START.md                      # Hướng dẫn chạy nhanh
├── PROJECT_SUMMARY.md                  # Tổng quan dự án (file này)
├── MIGRATION_GUIDE.md                  # Hướng dẫn migration
└── TESTING_CHECKLIST.md                # Checklist test
```

---

## 🔄 Luồng Hoạt Động (Flow)

### 1. Khám Phá Server (Discovery)

```
[Web Browser] ──HTTP──► [Django] ──UDP Broadcast──► [All Servers in LAN]
                              ◄──UDP Response────── [Target Server]
```

### 2. Kết Nối (Connect)

```
[Web Browser] ──HTTP──► [Django] ──TCP Connect──► [Target Server:5656]
                              ◄──TCP ACK──────────
```

### 3. Gửi Lệnh (Command)

```
[User Click] → [JavaScript] → [HTTP POST] → [Django View]
                                              ↓
                                    [socket.send("SCREENSHOT")]
                                              ↓
                                    [Target Server executes]
                                              ↓
                                    [socket.recv(image_data)]
                                              ↓
                                    [JSON Response] → [Display on Web]
```

---

## 📈 Thống Kê Dự Án

| Metric | Giá trị |
|--------|---------|
| **Số file Python** | ~30 files |
| **Số file C#** | ~10 files |
| **Số tính năng** | 12 tính năng chính |
| **Thời gian phát triển** | ~3 tuần (12/2025) |
| **Lines of Code (ước tính)** | ~5000 LOC |

---

## 👥 Đóng Góp

Dự án được phát triển với sự hỗ trợ của các công cụ AI:
- **Gemini** - Xây dựng nền tảng và các tính năng core
- **GitHub Copilot (Claude Opus 4.5)** - Nâng cấp UI, tối ưu hóa code

---

## 📜 License

Dự án được phát triển cho mục đích học tập tại môn **Mạng Máy Tính** - 2025.

---

**🎓 Đồ án Môn Mạng Máy Tính - 2025**
