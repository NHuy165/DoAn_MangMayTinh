# 🚀 Hướng Dẫn Chạy Nhanh (Quick Start Guide)

> **Đồ án Mạng Máy Tính** - Hệ thống điều khiển máy tính từ xa qua LAN

---

## 📋 Yêu Cầu Hệ Thống

### Phía Client (Web Controller - Django)
| Thành phần | Yêu cầu |
|------------|---------|
| **Hệ điều hành** | Windows 10/11, macOS, hoặc Linux |
| **Python** | 3.10 - 3.13 |
| **pip** | Phiên bản mới nhất |
| **Trình duyệt** | Chrome, Edge, Firefox (phiên bản mới) |

### Phía Server (Target Machine - C#)
| Thành phần | Yêu cầu |
|------------|---------|
| **Hệ điều hành** | Windows 10/11 |
| **Visual Studio** | 2019/2022 với .NET Framework 4.7.2 |
| **Kết nối mạng** | Cùng mạng LAN với Client |

---

## ⚡ Chạy Nhanh Trong 3 Bước

### Bước 1️⃣: Khởi động Server (Máy bị điều khiển)

```bash
# 1. Mở Visual Studio
# 2. Mở file: Server/TargetServer/TargetServer.slnx
# 3. Nhấn F5 hoặc Ctrl+F5 để chạy
# 4. Khi Form hiện ra → Bấm nút "Open Server" để bắt đầu lắng nghe
```

> ⚠️ **Lưu ý:** Nếu Windows Firewall hỏi, chọn **"Allow Access"** cho cả Private và Public networks.

### Bước 2️⃣: Khởi động Client (Web Controller)

```powershell
# Di chuyển vào thư mục Client
cd Client

# Tạo môi trường ảo (chỉ cần làm lần đầu)
python -m venv venv

# Kích hoạt môi trường ảo
.\venv\Scripts\activate        # Windows PowerShell
# hoặc
source venv/bin/activate       # macOS/Linux

# Cài đặt dependencies (chỉ cần làm lần đầu)
pip install -r requirements.txt

# Chạy migrations (chỉ cần làm lần đầu)
python manage.py migrate

# Khởi động Web Server
python manage.py runserver 0.0.0.0:8000
```

### Bước 3️⃣: Kết nối và Điều khiển

1. **Mở trình duyệt** và truy cập: `http://localhost:8000` hoặc `http://<IP_máy_client>:8000`
2. **Tìm Server**: Tại thanh Navigation, bấm nút **"Discover"** để quét các server trong LAN
3. **Kết nối**: Chọn server từ danh sách và bấm **"Connect"**
4. **Điều khiển**: Sử dụng các tính năng từ menu bên trái (Applications, Processes, Screenshot, v.v.)

---

## 📁 Cấu Trúc Cần Thiết

```
DoAn_MangMayTinh/
├── Client/                 # 🌐 Web Controller (Django)
│   ├── apps/
│   │   └── remote_control/ # Logic điều khiển chính
│   ├── config/
│   │   └── settings.py     # Cấu hình Django
│   ├── templates/          # Giao diện HTML
│   ├── manage.py           # Django CLI
│   └── requirements.txt    # Dependencies
│
└── Server/                 # 🖥️ Target Server (C#)
    └── TargetServer/
        ├── server.cs       # Logic server chính
        ├── TargetServer.slnx  # Solution file
        └── bin/Debug/
            └── TargetServer.exe  # File thực thi
```

---

## 🔧 Cấu Hình (Optional)

### File `.env` (Client)

Tạo file `.env` trong thư mục `Client/` với nội dung:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
```

### Đổi cổng Server (C#)

Mở file `Server/TargetServer/server.cs`, tìm và sửa:

```csharp
// TCP Port (mặc định: 5656)
int TCP_PORT = 5656;

// UDP Discovery Port (mặc định: 5657)
int UDP_PORT = 5657;
```

### Đổi cổng Client (Django)

```bash
# Chạy trên cổng khác (ví dụ: 3000)
python manage.py runserver 0.0.0.0:3000
```

---

## 🌐 Truy Cập Từ Thiết Bị Khác Trong LAN

### 1. Xác định IP của máy chạy Client

```powershell
# Windows
ipconfig

# macOS/Linux
ifconfig
```

Tìm địa chỉ IPv4, ví dụ: `192.168.1.100`

### 2. Truy cập từ thiết bị khác

Mở trình duyệt trên điện thoại/máy tính khác và truy cập:
```
http://192.168.1.100:8000
```

---

## 🛠️ Xử Lý Sự Cố Thường Gặp

### ❌ Server không hiện trong danh sách Discover

| Nguyên nhân | Giải pháp |
|-------------|-----------|
| Firewall chặn | Tắt tạm Windows Firewall hoặc cho phép cổng 5656, 5657 |
| Khác mạng LAN | Đảm bảo 2 máy cùng mạng WiFi/Ethernet |
| Server chưa chạy | Kiểm tra nút "Open Server" đã được bấm chưa |

### ❌ Không kết nối được đến Server

```powershell
# Test kết nối từ Client đến Server
ping <IP_Server>

# Kiểm tra cổng (Windows)
Test-NetConnection -ComputerName <IP_Server> -Port 5656
```

### ❌ Lỗi khi cài dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Cài từng package nếu lỗi
pip install django==4.2.9
pip install Pillow==11.1.0
```

### ❌ ModuleNotFoundError

```bash
# Đảm bảo đã kích hoạt venv
.\venv\Scripts\activate  # Windows

# Kiểm tra đã cài đủ chưa
pip list
```

---

## 📌 Lưu Ý Quan Trọng

1. **Thứ tự khởi động**: Luôn khởi động **Server (C#) trước**, sau đó mới **Client (Django)**
2. **Cùng mạng LAN**: Cả hai máy phải kết nối cùng một mạng WiFi hoặc qua cùng một Router
3. **Antivirus**: Một số tính năng (Keylogger, Screen Capture) có thể bị antivirus cảnh báo - đây là hành vi bình thường cho ứng dụng Remote Control
4. **Quyền Admin**: Chạy Visual Studio với quyền **Administrator** để tránh lỗi với một số tính năng

---

## 📞 Liên Hệ Hỗ Trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra lại các bước trong hướng dẫn
2. Xem mục [Xử Lý Sự Cố](#️-xử-lý-sự-cố-thường-gặp)
3. Tham khảo file `PROJECT_SUMMARY.md` để hiểu rõ hơn về kiến trúc hệ thống

---

**🎓 Đồ án Môn Mạng Máy Tính - 2025**
