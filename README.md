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
│                 │         UDP:9999          │                  │
│  Django + HTML  │◄ ─ ─ ─ (Discovery) ─ ─ ─ ►│   C# WinForms    │
└─────────────────┘                           └──────────────────┘
```

| Thành phần | Ngôn ngữ | Vai trò |
|------------|----------|---------|
| **Target Server** | C# (.NET 4.7.2) | Máy bị điều khiển |
| **Web Controller** | Python (Django 4.2) | Giao diện điều khiển |

---
### 📡 Giao thức Giao tiếp (Communication Protocol)

Hệ thống sử dụng giao thức dựa trên văn bản (Text-based) qua TCP Socket để gửi lệnh điều khiển.

**Định dạng lệnh (Request):**
`COMMAND_TYPE` | `SUB_COMMAND` | `DATA (Optional)`

**Ví dụ:**
- **Lấy thông tin hệ thống:** `SYSTEM_INFO`
- **Mở Notepad:** `PROCESS | START | notepad`
- **Tắt Process:** `PROCESS | KILL | 1234`
- **Keylogger:** `KEYLOG | HOOK`

**Dữ liệu nhị phân (Binary Data):**
Riêng với hình ảnh (Screen/Webcam) và File, dữ liệu được gửi dưới dạng byte array kèm header độ dài để đảm bảo toàn vẹn dữ liệu.
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

# 3️⃣ Mở trình duyệt → http://x.x.x.x:8000 → Discover → Connect
```
# ⚠️ LƯU Ý QUAN TRỌNG (TROUBLESHOOTING)

### 🔥 1. Tường lửa (Firewall)
* **Cấu hình:** Cần cho phép (**Allow**) hoặc mở các cổng sau:
    * **TCP Port:** `5656`
    * **UDP Port:** `9999`
* **Mẹo nhanh:** Để demo không bị gián đoạn, bạn có thể **tắt tạm thời Windows Firewall**.

### 🌐 2. Mạng LAN
* **Kết nối:** Máy Client và Server phải kết nối chung một mạng Wifi hoặc Router.
* **Kiểm tra:** Sử dụng lệnh sau trong Terminal/CMD để kiểm tra thông mạng:
    ```bash
    ping <IP_SERVER>
    ```
### 📦 3. Lỗi thiếu thư viện (Dependencies)
* **Vấn đề:** Visual Studio báo lỗi thiếu các thư viện như `AForge` hoặc `Accord`.
* **Cách xử lý:** 1. Chuột phải vào **Solution** trong Solution Explorer.
    2. Chọn **Restore NuGet Packages**.
---
## 🛠️ Công nghệ & Thư viện

### Backend (C# Server)
- **Networking:** `System.Net.Sockets` (TCP/UDP Async)
- **Video Processing:** `AForge.NET`, `Accord.Video.FFMPEG` (Xử lý Stream & Recording)
- **System Internals:**
  - `User32.dll` (Windows API Hooking cho Keylogger)
  - `GDI+` (Chụp màn hình hiệu năng cao)
  - `WMI` (Lấy thông tin phần cứng chi tiết)

### Frontend (Python Client)
- **Framework:** Django 4.2 (MVT Pattern)
- **UI Library:** TailwindCSS (Responsive Design)
- **Communication:** Python `socket` & `threading` (Quản lý kết nối song song)
---
## 📁 Cấu Trúc Thư Mục

> 📚 Xem chi tiết tại [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

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
│   │
│   └── ...
│
├── Server/TargetServer/                # 🖥️ Target Server (C#)
│   ├── server.cs                       # Logic server chính
│   ├── Keylog.cs                       # 🔑 Module ghi phím
│   ├── WebcamRecorder.cs               # 📷 Module quay webcam
│   ├── ScreenRecorder.cs               # 🖼️ Module quay màn hình
│   ├── FileManager.cs                  # 📁 Module quản lý file
│   ├── TargetServer.slnx               # Solution file
│   │
│   └── ...
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
