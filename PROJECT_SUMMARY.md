# 📊 Tổng Quan Dự Án (Project Summary)

> **Remote Control System via LAN** - Hệ thống điều khiển máy tính từ xa qua mạng LAN

---

## 🎯 Mục Tiêu Dự Án

Xây dựng một hệ thống **Client-Server** cho phép:
- **Điều khiển** máy tính mục tiêu (Target Machine) từ xa
- **Giám sát** hoạt động của máy mục tiêu thông qua giao diện Web

---

## 🏗️ Kiến Trúc Hệ Thống

- **Web Browser** (HTML/CSS/JS) - Giao diện người dùng, chỉ hiển thị
- **Django Server** (Python 4.2) - Xử lý logic, giao tiếp socket với Target → `Client/`
- **Target Server** (C# .NET 4.7.2) - Máy bị điều khiển, thực thi lệnh → `Server/TargetServer/`

### 🔌 Giao Thức Truyền Thông
- **UDP:5657** - Discovery (tìm server trong LAN)
- **TCP:5656** - Persistent connection (truyền lệnh và dữ liệu)

---

## ✨ Tính Năng

### 🖥️ Quản Lý Hệ Thống
- **Applications** - Xem/Dừng các ứng dụng đang chạy
- **Processes** - Xem/Kill tất cả tiến trình hệ thống
- **Start App** - Khởi động ứng dụng từ Start Menu hoặc đường dẫn
- **Power** - Shutdown / Restart máy tính từ xa

### 📷 Giám Sát
- **Screenshot** - Chụp ảnh màn hình tức thời
- **Screen Recording** - Quay video màn hình, lưu file .avi
- **Webcam** - Bật/Ghi hình webcam
- **Keylogger** - Ghi lại các phím đã nhấn

### 🛠️ Quản Lý Nâng Cao
- **Remote Shell** - Chạy lệnh CMD trực tiếp
- **File Manager** - Duyệt, Download, Xóa file
- **System Info** - Xem thông tin CPU, RAM, Disk

---

## 🛠️ Công Nghệ Sử Dụng

### Backend
- **Django 4.2** - Web Framework
- **Python 3.10+** - Ngôn ngữ backend
- **C# .NET 4.7.2** - Server-side

### Frontend
- **Tailwind CSS** - Styling
- **JavaScript** - Client-side logic

### Libraries (C#)
- **AForge.Video** - Webcam capture
- **System.Drawing** - Screenshot

---

## 📂 Cấu Trúc Thư Mục

```
DoAn_MangMayTinh/
│
├── Client/                                     # 🌐 Web Controller (Django)
│   │
│   ├── apps/                                   # Django applications
│   │   └── remote_control/                     # ⭐ App điều khiển chính
│   │       ├── views.py                        # API endpoints xử lý request
│   │       ├── urls.py                         # Định tuyến URL
│   │       ├── socket_client_persistent.py     # 🔌 Quản lý kết nối TCP với Target
│   │       └── udp_discovery.py                # 📡 Broadcast tìm server trong LAN
│   │
│   ├── config/                                 # ⚙️ Cấu hình Django
│   │   ├── settings.py                         # Settings chính
│   │   └── urls.py                             # Root URL configuration
│   │
│   ├── templates/                              # 🎨 Giao diện HTML
│   │   ├── remote_control/                     # Templates cho từng tính năng
│   │   │   ├── *.html                          # Wrapper templates
│   │   │   └── partials/                       # ⭐ Code JS/HTML thực tế
│   │   │       ├── applications_partial.html   # Logic quản lý applications
│   │   │       ├── processes_partial.html      # Logic quản lý processes
│   │   │       ├── screenshot_partial.html     # Logic chụp màn hình
│   │   │       ├── screen_partial.html         # Logic quay màn hình
│   │   │       ├── webcam_partial.html         # Logic webcam
│   │   │       ├── keylogger_partial.html      # Logic keylogger
│   │   │       ├── shell_partial.html          # Logic remote shell
│   │   │       ├── file_manager_partial.html   # Logic file manager
│   │   │       ├── power_partial.html          # Logic power control
│   │   │       └── home_partial.html           # Logic home/system info
│   │   │
│   │   ├── layouts/                            # Base templates
│   │   └── includes/                           # Reusable components (sidebar)
│   │
│   ├── static/assets/                          # 📁 CSS, JS tĩnh
│   │
│   ├── media/                                  # 📂 Lưu trữ file từ Target
│   │   ├── screen_recordings/                  # Video quay màn hình (.avi)
│   │   └── webcam/                             # Video webcam (.avi)
│   │
│   ├── manage.py                               # Django CLI
│   ├── requirements.txt                        # Python dependencies
│   │
│   └── ...
│
├── Server/                                     # 🖥️ Target Server (C#)
│   └── TargetServer/
│       ├── server.cs                           # ⭐ Logic server chính
│       ├── server.Designer.cs                  # WinForms UI designer
│       ├── Program.cs                          # Entry point
│       ├── Keylog.cs                           # 🔑 Module ghi phím
│       ├── WebcamRecorder.cs                   # 📷 Module quay webcam
│       ├── ScreenRecorder.cs                   # 🖼️ Module quay màn hình
│       ├── FileManager.cs                      # 📁 Module quản lý file
│       ├── TargetServer.csproj                 # Project file
│       ├── TargetServer.slnx                   # Solution file
│       └── packages/                           # NuGet packages (AForge, Accord)
│
├── AI_Chatlog/                                 # 📝 Nhật ký phát triển với AI
│
├── README.md                                   # 📚 Giới thiệu tổng quan
├── QUICK_START.md                              # 📚 Hướng dẫn chạy nhanh
└── PROJECT_SUMMARY.md                          # 📚 Chi tiết kiến trúc
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
