# 📚 Hướng Dẫn Migration (Migration Guide)

> Tài liệu mô tả quá trình phát triển và nâng cấp dự án từ Flask sang Django

---

## 📖 Tổng Quan

Dự án ban đầu được xây dựng trên **Flask** (framework Python nhẹ), sau đó được **migrate sang Django** để tận dụng các tính năng mạnh mẽ hơn như ORM, Admin Panel, và cấu trúc project chuẩn hóa.

---

## 🔄 So Sánh Kiến Trúc

### Trước (Flask)

```
Web_Controller_Python/
├── app.py              # Single file application
├── templates/
│   └── index.html      # Giao diện đơn giản
└── static/
    └── style.css
```

### Sau (Django)

```
Client/
├── apps/
│   ├── remote_control/     # App chính với nhiều modules
│   │   ├── views.py        # API endpoints tách biệt
│   │   ├── models.py       # Database models
│   │   ├── urls.py         # URL routing
│   │   └── ...
│   └── pages/              # Dashboard & static pages
├── config/
│   ├── settings.py         # Centralized configuration
│   └── urls.py             # Root URL routing
├── templates/              # Organized template structure
└── manage.py               # Django CLI
```

---

## 🚀 Các Thay Đổi Chính

### 1. Socket Connection

#### Flask (Non-Persistent)
```python
# Mỗi request tạo connection mới
@app.route('/api/screenshot')
def screenshot():
    sock = socket.socket()
    sock.connect((SERVER_IP, 5656))
    sock.send(b"TAKEPIC")
    data = sock.recv(1024)
    sock.close()  # Đóng ngay sau mỗi request
    return data
```

#### Django (Persistent Connection)
```python
# Connection được giữ xuyên suốt session
class PersistentRemoteClient:
    _instances = {}  # Cache connections
    
    @classmethod
    def get_or_create(cls, session_id, host, port, timeout):
        key = f"{session_id}_{host}_{port}"
        if key not in cls._instances:
            cls._instances[key] = cls(host, port, timeout)
        return cls._instances[key]
    
    def send_command(self, command):
        # Sử dụng connection đã có
        self.sock.send(command.encode())
        return self.sock.recv(4096)
```

### 2. Server Discovery

#### Flask
- Không có tính năng discovery
- Phải nhập IP thủ công

#### Django
```python
# UDP Broadcast để tìm server tự động
class UDPDiscoveryClient:
    def discover(self, timeout=3):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(b"DISCOVER_SERVER", ('<broadcast>', 5657))
        
        servers = []
        while True:
            data, addr = sock.recvfrom(1024)
            servers.append({'ip': addr[0], 'info': data.decode()})
        return servers
```

### 3. Session Management

#### Flask
```python
# Không quản lý session phức tạp
SERVER_IP = "127.0.0.1"  # Hardcoded
```

#### Django
```python
# Session-based connection management
def connect_server(request):
    server_ip = request.POST.get('ip')
    request.session['target_server_ip'] = server_ip
    
    client = PersistentRemoteClient.get_or_create(
        session_id=request.session.session_key,
        host=server_ip,
        port=5656
    )
    return JsonResponse({'success': client.connected})
```

### 4. Database Integration

#### Flask
- Không sử dụng database
- Dữ liệu không được lưu trữ

#### Django
```python
# ORM Models cho recordings
class WebcamRecording(models.Model):
    file_path = models.FileField(upload_to='webcam/%Y/%m/')
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class ScreenRecording(models.Model):
    file_path = models.FileField(upload_to='screen_recordings/%Y/%m/')
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 🔧 Các Bước Migration

### Bước 1: Tạo Project Django

```bash
# Tạo project mới
django-admin startproject config .

# Tạo app chính
python manage.py startapp remote_control
mv remote_control apps/
```

### Bước 2: Chuyển Logic Socket

1. Tạo file `socket_client_persistent.py`
2. Implement class `PersistentRemoteClient`
3. Thêm connection pooling và error handling

### Bước 3: Tạo Views & URLs

```python
# urls.py
urlpatterns = [
    path('remote/applications/', views.applications_page),
    path('remote/api/app/list/', views.get_apps),
    # ... các routes khác
]

# views.py
def get_apps(request):
    client = _get_client(request)
    if not client:
        return JsonResponse({'error': 'Not connected'}, status=400)
    
    result = client.get_applications()
    return JsonResponse(result)
```

### Bước 4: Migrate Templates

- Tách template thành components
- Sử dụng Django template inheritance
- Thêm Tailwind CSS cho styling

### Bước 5: Thêm UDP Discovery

1. Tạo file `udp_discovery.py`
2. Implement broadcast mechanism
3. Thêm UI cho server selection

---

## 📊 So Sánh Tính Năng

| Tính năng | Flask | Django |
|-----------|-------|--------|
| **Connection Type** | Non-persistent | Persistent |
| **Server Discovery** | ❌ Manual IP | ✅ UDP Broadcast |
| **Session Management** | ❌ Basic | ✅ Full-featured |
| **Database** | ❌ None | ✅ SQLite/ORM |
| **Admin Panel** | ❌ None | ✅ Built-in |
| **Recording Storage** | ❌ Temp files | ✅ Organized media |
| **Multi-user Support** | ❌ Single | ✅ Session-based |
| **URL Routing** | Basic | Advanced |
| **Template Engine** | Jinja2 | Django Templates |
| **Static Files** | Manual | Whitenoise |

---

## 🆕 Tính Năng Mới Sau Migration

### 1. Persistent Connection
- Kết nối một lần, sử dụng nhiều lần
- Giảm latency cho mỗi command
- Connection recovery tự động

### 2. UDP Server Discovery
- Tự động tìm server trong LAN
- Không cần nhập IP thủ công
- Support nhiều server

### 3. Recording Management
- Lưu trữ có tổ chức (theo năm/tháng)
- Danh sách recordings với metadata
- Download và delete từ web

### 4. Screen Recording
- Tính năng mới hoàn toàn
- Stream realtime preview
- Lưu file .avi

### 5. Remote Shell
- Chạy CMD commands từ xa
- Output realtime
- Working directory tracking

### 6. File Manager
- Duyệt file system
- Download files
- Delete files

### 7. System Info Dashboard
- CPU, RAM usage realtime
- Disk space
- Hardware info

---

## ⚠️ Breaking Changes

### API Endpoints

| Flask | Django |
|-------|--------|
| `/api/process` | `/remote/api/process/list/` |
| `/api/screenshot` | `/remote/api/screenshot/` |
| `/api/keylog` | `/remote/api/keylog/get/` |

### Response Format

#### Flask
```json
{
  "data": "..."
}
```

#### Django
```json
{
  "success": true,
  "data": "...",
  "message": "Operation completed"
}
```

---

## 🔍 Troubleshooting Migration

### Lỗi: "No target server IP in session"
```python
# Đảm bảo đã connect trước khi gọi API
request.session['target_server_ip'] = server_ip
```

### Lỗi: Connection refused
```python
# Kiểm tra server đã chạy và firewall đã mở
# Port TCP: 5656, UDP: 5657
```

### Lỗi: Template not found
```python
# Kiểm tra TEMPLATES setting trong settings.py
TEMPLATES = [{
    'DIRS': [BASE_DIR / 'templates'],
}]
```

---

## 📝 Lessons Learned

1. **Persistent connections** cần quản lý lifecycle cẩn thận
2. **Session-based** approach phù hợp hơn global state
3. **UDP discovery** cần handle timeout properly
4. **Django ORM** giúp quản lý data dễ dàng hơn
5. **Template inheritance** giúp DRY code

---

**🎓 Đồ án Môn Mạng Máy Tính - 2025**
