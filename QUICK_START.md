# 🚀 Hướng Dẫn Chạy Nhanh (Quick Start Guide)

> **Đồ án Mạng Máy Tính** - Hệ thống điều khiển máy tính từ xa qua LAN

---

## 📋 Yêu Cầu Hệ Thống

### Phía Client (Web Controller - Django)
| Thành phần | Yêu cầu |
|------------|---------|
| **Hệ điều hành** | Windows 10/11, macOS, hoặc Linux |
| **Python** | 3.10 - 3.13 |
| **Trình duyệt** | Chrome, Edge, Firefox |

### Phía Server (Target Machine - C#)
| Thành phần | Yêu cầu |
|------------|---------|
| **Hệ điều hành** | Windows 10/11 |
| **Visual Studio** | 2019/2022 với .NET Framework 4.7.2 |

---

## ⚡ Chạy Nhanh Trong 3 Bước

### Bước 1️⃣: Khởi động Client (Web Controller)

```powershell
cd Client

# Tạo môi trường ảo (chỉ cần làm lần đầu)
python -m venv venv

# Kích hoạt môi trường ảo
.\venv\Scripts\activate        # Windows PowerShell
# hoặc: source venv/bin/activate (macOS/Linux)

# Cài đặt dependencies (chỉ cần làm lần đầu)
pip install -r requirements.txt

# Chạy migrations (chỉ cần làm lần đầu)
python manage.py migrate

# Khởi động Web Server
python manage.py runserver 0.0.0.0:8000
```

### Bước 2️⃣: Khởi động Server (Máy bị điều khiển)

```
1. Mở Visual Studio
2. Mở file: Server/TargetServer/TargetServer.slnx
3. Nhấn F5 hoặc Ctrl+F5 để chạy
4. Khi Form hiện ra → Bấm nút "Open Server" để bắt đầu lắng nghe
```

### Bước 3️⃣: Kết nối và Điều khiển

1. **Mở trình duyệt** và truy cập: `http://localhost:8000`
2. **Tìm Server**: Bấm nút **"Discover"** để quét các server trong LAN
3. **Kết nối**: Chọn server từ danh sách và bấm **"Connect"**
4. **Điều khiển**: Sử dụng các tính năng từ menu bên trái

---

## 🌐 Truy Cập Từ Thiết Bị Khác Trong LAN

```powershell
# Xác định IP của máy chạy Client
ipconfig    # Windows
ifconfig    # macOS/Linux
```

Truy cập từ thiết bị khác: `http://<IP_máy_client>:8000`

---

## 🛠️ Xử Lý Sự Cố Thường Gặp

### Server không hiện trong danh sách Discover
- Kiểm tra nút "Open Server" đã được bấm chưa
- Đảm bảo 2 máy cùng mạng WiFi/Ethernet

### Không kết nối được đến Server
```powershell
ping <IP_Server>
Test-NetConnection -ComputerName <IP_Server> -Port 5656
```

### ModuleNotFoundError
```bash
.\venv\Scripts\activate  # Đảm bảo đã kích hoạt venv
pip list                 # Kiểm tra đã cài đủ chưa
```

---

**🎓 Đồ án Môn Mạng Máy Tính - 2025**
