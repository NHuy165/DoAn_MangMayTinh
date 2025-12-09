"""
Script để test Persistent Connection
Chạy script này để kiểm tra xem persistent connection có hoạt động đúng không

Usage:
    python test_persistent.py
"""
import time

def test_connection_lifecycle():
    """
    Test: Tạo → Reuse → Disconnect
    """
    print("=" * 60)
    print("TEST PERSISTENT CONNECTION LIFECYCLE")
    print("=" * 60)
    
    print("\n📝 Manual Testing Steps:")
    print("-" * 60)
    
    print("\n1. Start C# Server:")
    print("   - Mở TargetServer.exe")
    print("   - Click 'Open Server'")
    print("   - Chờ message 'Server Running on Port 5656'")
    
    print("\n2. Start Django Server:")
    print("   - cd web_server_django")
    print("   - python manage.py runserver")
    
    print("\n3. Test trong Browser:")
    print("   - Mở http://localhost:8000/remote/")
    print("   - F12 → Console để xem logs")
    
    print("\n4. Test Connect:")
    print("   - Nhập IP: 127.0.0.1")
    print("   - Click 'Connect'")
    print("   - ✅ Button chuyển xanh 'Connected'")
    print("   - ✅ Alert 'Connected to 127.0.0.1'")
    
    print("\n5. Test Reuse Socket (Processes):")
    print("   - Click sidebar 'Processes'")
    print("   - ✅ Danh sách hiện ra KHÔNG TẠO SOCKET MỚI!")
    print("   - Check Django logs: KHÔNG có log 'Created new persistent connection'")
    print("   - Check Django logs: CÓ log 'Reusing existing connection'")
    
    print("\n6. Test Reuse Socket (Keylogger):")
    print("   - Click sidebar 'Keylogger'")
    print("   - Click 'Start Keylogger'")
    print("   - ✅ Keylogger bật KHÔNG TẠO SOCKET MỚI!")
    
    print("\n7. Test Reuse Socket (Screenshot):")
    print("   - Click sidebar 'Screenshot'")
    print("   - Click 'Take Screenshot'")
    print("   - ✅ Ảnh hiện ra KHÔNG TẠO SOCKET MỚI!")
    
    print("\n8. Test Disconnect:")
    print("   - Click 'Disconnect' (nếu có button)")
    print("   - Hoặc đóng browser tab")
    print("   - ✅ Socket bị đóng")
    print("   - Check Django logs: 'Disconnected session ...'")
    
    print("\n9. Verify Socket Closed:")
    print("   - Mở lại browser tab")
    print("   - Try click 'Processes' KHÔNG connect trước")
    print("   - ✅ Error: 'Not connected to server'")
    
    print("\n" + "=" * 60)
    print("EXPECTED BEHAVIOR:")
    print("=" * 60)
    print("✅ 1 lần connect → Nhiều API calls → 1 socket duy nhất")
    print("✅ Disconnect → Socket đóng → Phải connect lại")
    print("✅ Session-based → Mỗi user riêng biệt")
    print("=" * 60)
    
    print("\n💡 TIP: Xem Django logs để verify:")
    print("   - 'Created new persistent connection' = Tạo socket mới")
    print("   - 'Reusing existing connection' = Reuse socket cũ")
    print("   - 'Disconnected session' = Socket đã đóng")
    
    print("\n" + "=" * 60)

def explain_architecture():
    """
    Giải thích kiến trúc Persistent Connection
    """
    print("\n\n" + "=" * 60)
    print("KIẾN TRÚC PERSISTENT CONNECTION")
    print("=" * 60)
    
    print("\n📊 LUỒNG DỮ LIỆU:")
    print("""
    Browser                 Django                    C# Server
       │                      │                          │
       │  POST /connect       │                          │
       ├─────────────────────→│                          │
       │                      │  Socket.connect()        │
       │                      ├─────────────────────────→│
       │                      │←─────────────────────────│
       │                      │  Lưu socket vào          │
       │                      │  _instances[session_id]  │
       │  ← "Connected"       │                          │
       │←─────────────────────│                          │
       │                      │                          │
       │  GET /api/process    │                          │
       ├─────────────────────→│                          │
       │                      │  REUSE socket cũ!        │
       │                      │  send("PROCESS")         │
       │                      ├─────────────────────────→│
       │                      │←─────────────────────────│
       │  ← Process list      │                          │
       │←─────────────────────│                          │
       │                      │                          │
       │  GET /api/keylog     │                          │
       ├─────────────────────→│                          │
       │                      │  REUSE socket cũ!        │
       │                      │  send("KEYLOG")          │
       │                      ├─────────────────────────→│
       │                      │←─────────────────────────│
       │  ← Keylog data       │                          │
       │←─────────────────────│                          │
       │                      │                          │
       │  POST /disconnect    │                          │
       ├─────────────────────→│                          │
       │                      │  send("QUIT")            │
       │                      ├─────────────────────────→│
       │                      │  socket.close()          │
       │                      │  Remove from _instances  │
       │  ← "Disconnected"    │                          │
       │←─────────────────────│                          │
    """)
    
    print("\n🔑 KEY COMPONENTS:")
    print("-" * 60)
    print("1. PersistentRemoteClient._instances = {}")
    print("   - Dictionary lưu tất cả active connections")
    print("   - Key: session_id (unique cho mỗi user)")
    print("   - Value: PersistentRemoteClient object")
    
    print("\n2. PersistentRemoteClient.get_or_create()")
    print("   - Kiểm tra session_id đã có trong _instances chưa")
    print("   - Nếu có → Return connection cũ (REUSE!)")
    print("   - Nếu chưa → Tạo mới và lưu vào _instances")
    
    print("\n3. _get_client(request)")
    print("   - Helper function trong views.py")
    print("   - Lấy session_id từ Django request")
    print("   - Gọi get_or_create() để lấy persistent client")
    
    print("\n4. Django Session")
    print("   - Lưu 'target_server_ip' khi user connect")
    print("   - Mỗi browser tab có session riêng")
    print("   - Session expire → Auto cleanup")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_connection_lifecycle()
    explain_architecture()
    
    print("\n\n🚀 Ready to test! Follow the steps above.")
    print("📝 Remember: Check Django terminal logs for 'Created' vs 'Reusing' messages")
