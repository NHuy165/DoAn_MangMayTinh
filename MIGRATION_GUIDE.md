# 📚 Hướng Dẫn Migration (Migration Guide)

> Tài liệu mô tả quá trình migration từ Flask sang Django

---

## 📖 Tổng Quan

Dự án ban đầu được xây dựng trên **Flask**, sau đó được **migrate sang Django** để tận dụng các tính năng mạnh mẽ hơn như ORM, Admin Panel, và cấu trúc project chuẩn hóa.

---

## 🔄 So Sánh Kiến Trúc

### Trước (Flask)
```
Web_Controller_Python/
├── app.py              # Single file application
├── templates/
└── static/
```

### Sau (Django)
```
Client/
├── apps/
│   ├── remote_control/     # App chính
│   └── pages/
├── config/
├── templates/
└── manage.py
```

---

## 🚀 Các Thay Đổi Chính

### 1. Socket Connection

**Flask (Non-Persistent)**
```python
@app.route('/api/screenshot')
def screenshot():
    sock = socket.socket()
    sock.connect((SERVER_IP, 5656))
    sock.send(b"TAKEPIC")
    data = sock.recv(1024)
    sock.close()  # Đóng sau mỗi request
    return data
```

**Django (Persistent)**
```python
class PersistentRemoteClient:
    _instances = {}  # Cache connections
    
    @classmethod
    def get_or_create(cls, session_id, host, port, timeout):
        key = f"{session_id}_{host}_{port}"
        if key not in cls._instances:
            cls._instances[key] = cls(host, port, timeout)
        return cls._instances[key]
```

### 2. Server Discovery

**Flask**: Không có - phải nhập IP thủ công

**Django**: UDP Broadcast tự động
```python
class UDPDiscoveryClient:
    def discover(self, timeout=3):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(b"DISCOVER_SERVER", ('<broadcast>', 5657))
        # ...
```

### 3. Session Management

**Flask**: Hardcoded IP
```python
SERVER_IP = "127.0.0.1"
```

**Django**: Session-based
```python
def connect_server(request):
    server_ip = request.POST.get('ip')
    request.session['target_server_ip'] = server_ip
    client = PersistentRemoteClient.get_or_create(
        session_id=request.session.session_key,
        host=server_ip, port=5656
    )
```

---

## 📊 So Sánh Tính Năng

| Tính năng | Flask | Django |
|-----------|-------|--------|
| **Connection** | Non-persistent | Persistent |
| **Discovery** | ❌ Manual | ✅ UDP Broadcast |
| **Session** | ❌ Basic | ✅ Full-featured |
| **Database** | ❌ None | ✅ ORM |
| **Admin Panel** | ❌ None | ✅ Built-in |
| **Multi-user** | ❌ Single | ✅ Session-based |

---

## 🆕 Tính Năng Mới Sau Migration

1. **Persistent Connection** - Giảm latency, auto recovery
2. **UDP Server Discovery** - Tự động tìm server trong LAN
3. **Recording Management** - Lưu trữ có tổ chức (theo năm/tháng)
4. **Screen Recording** - Tính năng mới
5. **Remote Shell** - CMD từ xa
6. **File Manager** - Duyệt/download/delete file
7. **System Dashboard** - CPU, RAM, Disk realtime

---

## ⚠️ Breaking Changes

### API Endpoints

| Flask | Django |
|-------|--------|
| `/api/process` | `/remote/api/process/list/` |
| `/api/screenshot` | `/remote/api/screenshot/` |
| `/api/keylog` | `/remote/api/keylog/get/` |

### Response Format

**Flask**: `{ "data": "..." }`

**Django**: `{ "success": true, "data": "...", "message": "..." }`

---

**🎓 Đồ án Môn Mạng Máy Tính - 2025**
