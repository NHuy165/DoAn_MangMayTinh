"""
Script để test UDP Discovery
Test xem UDP broadcast có hoạt động đúng không

Usage:
    python test_udp_discovery.py
"""
from apps.remote_control.udp_discovery import UDPDiscoveryClient, quick_discover


def test_udp_discovery():
    """
    Test UDP Discovery manually
    """
    print("=" * 70)
    print("TEST UDP DISCOVERY - TÌM KIẾM SERVERS TRONG LAN")
    print("=" * 70)
    
    print("\n📝 CÁC BƯỚC TEST:")
    print("-" * 70)
    
    print("\n1. Start C# Server:")
    print("   - Mở TargetServer.exe")
    print("   - Click 'Open Server'")
    print("   - Chờ message: 'Server Running on Port 5656'")
    print("   - Chờ message: '[UDP Discovery] Listening on Port 9999...'")
    
    print("\n2. Test từ Python (có 2 cách):")
    
    print("\n   CÁCH 1: Test trực tiếp (không cần Django):")
    print("   ```bash")
    print("   cd web_server_django")
    print("   python test_udp_discovery.py")
    print("   ```")
    
    print("\n   CÁCH 2: Test qua Django API:")
    print("   ```bash")
    print("   # Terminal 1: Start Django")
    print("   python manage.py runserver")
    print("   ")
    print("   # Terminal 2: Test với curl hoặc browser")
    print("   curl http://localhost:8000/remote/api/discover-servers/")
    print("   ```")
    
    print("\n3. Test từ Browser:")
    print("   - Mở http://localhost:8000/remote/")
    print("   - Click button 'Discover'")
    print("   - ✅ Alert hiện: 'Found X server(s)'")
    print("   - ✅ Dropdown hiển thị danh sách servers")
    print("   - ✅ Format: 'DESKTOP-ABC (192.168.1.10)'")
    
    print("\n4. Verify kết quả:")
    print("   - Check C# Server console: '[UDP Discovery] Received from ...'")
    print("   - Check C# Server console: '[UDP Discovery] Sent response: ...'")
    print("   - Check Django logs: 'Discovered server: ...'")
    
    print("\n" + "=" * 70)
    print("CHẠY TEST NGAY BÂY GIỜ")
    print("=" * 70)
    
    try:
        print("\n🔍 Starting UDP Discovery...")
        print("📡 Broadcasting to 255.255.255.255:9999...")
        print("⏱️  Waiting 3 seconds for responses...\n")
        
        # Gọi discovery
        client = UDPDiscoveryClient(timeout=3.0)
        result = client.discover_with_details()
        
        # Hiển thị kết quả
        print("\n" + "=" * 70)
        print("KẾT QUẢ DISCOVERY")
        print("=" * 70)
        
        if result['success'] and result['count'] > 0:
            print(f"\n✅ {result['message']}")
            print("\nDANH SÁCH SERVERS:")
            print("-" * 70)
            for i, server in enumerate(result['servers'], 1):
                print(f"{i}. {server['name']}")
                print(f"   IP: {server['ip']}")
                print(f"   Port: {server['port']}")
                print()
        else:
            print(f"\n❌ {result['message']}")
            print("\nKHÔNG TÌM THẤY SERVER NÀO!")
            print("\nKiểm tra lại:")
            print("- C# Server đã chạy chưa?")
            print("- UDP Port 9999 có bị block bởi firewall không?")
            print("- C# Server và Python có trong cùng LAN không?")
        
        print("\n" + "=" * 70)
        
        return result
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nPossible causes:")
        print("- Network issues")
        print("- Firewall blocking UDP port 9999")
        print("- No servers running")
        return None


def explain_udp_discovery():
    """
    Giải thích cách UDP Discovery hoạt động
    """
    print("\n\n" + "=" * 70)
    print("CÁCH HOẠT ĐỘNG CỦA UDP DISCOVERY")
    print("=" * 70)
    
    print("\n📊 UDP vs TCP:")
    print("-" * 70)
    print("TCP (Port 5656 - Remote Control):")
    print("  ✓ Connection-oriented (3-way handshake)")
    print("  ✓ Reliable (đảm bảo data đến nơi)")
    print("  ✓ Phải biết chính xác IP đích")
    print("  ✓ Dùng cho: Gửi lệnh, nhận response")
    
    print("\nUDP (Port 9999 - Discovery):")
    print("  ✓ Connectionless (không cần handshake)")
    print("  ✓ Unreliable (có thể mất packet)")
    print("  ✓ Hỗ trợ BROADCAST (gửi đến tất cả)")
    print("  ✓ Dùng cho: Tìm kiếm servers trong LAN")
    
    print("\n📡 BROADCAST là gì?")
    print("-" * 70)
    print("IP Address: 255.255.255.255 = 'Gửi đến TẤT CẢ devices'")
    print()
    print("VD: LAN có 4 máy:")
    print("  - 192.168.1.10 (C# Server 1)")
    print("  - 192.168.1.15 (C# Server 2)")
    print("  - 192.168.1.20 (Laptop khác)")
    print("  - 192.168.1.25 (Python Web Server)")
    print()
    print("Khi Python gửi broadcast đến 255.255.255.255:9999:")
    print("  → TẤT CẢ 4 máy đều nhận được message!")
    print("  → Chỉ C# Servers (đang listen port 9999) mới response")
    print("  → Laptop khác bỏ qua (không listen port 9999)")
    
    print("\n🔄 LUỒNG HOẠT ĐỘNG:")
    print("-" * 70)
    print("""
    Step 1: C# Server khởi động
        ├─ Thread TCP (Port 5656) - Lắng nghe remote control
        └─ Thread UDP (Port 9999) - Lắng nghe discovery
    
    Step 2: Python Web Server gửi broadcast
        Python → UDP Socket
              → SO_BROADCAST enabled
              → sendto("DISCOVER_SERVER", 255.255.255.255:9999)
              → Packet gửi đến TẤT CẢ devices trong LAN
    
    Step 3: C# Server nhận broadcast
        C# UDP Listener (Port 9999)
            ├─ Receive() → "DISCOVER_SERVER"
            ├─ Kiểm tra message hợp lệ
            ├─ Lấy hostname: Dns.GetHostName()
            ├─ Lấy IP: Dns.GetHostAddresses()
            ├─ Tạo response: "HOSTNAME|IP"
            └─ Send(response) → Gửi lại Python
    
    Step 4: Python nhận responses
        Python UDP Socket (timeout 3s)
            ├─ Loop: recvfrom() nhận data
            ├─ Parse: "DESKTOP-ABC|192.168.1.10"
            ├─ Deduplicate: Loại bỏ duplicate IPs
            ├─ Timeout → Stop loop
            └─ Return: List[{ip, name, port}]
    
    Step 5: Frontend hiển thị
        Dropdown: [DESKTOP-ABC (192.168.1.10)] [LAPTOP-XYZ (192.168.1.15)]
        User chọn → Click Connect → Tạo TCP connection persistent
    """)
    
    print("\n⚠️ LƯU Ý QUAN TRỌNG:")
    print("-" * 70)
    print("1. FIREWALL:")
    print("   - Windows Firewall có thể block UDP port 9999")
    print("   - Cần add exception cho TargetServer.exe")
    print("   - Hoặc tắt firewall khi test trong LAN riêng")
    
    print("\n2. NETWORK:")
    print("   - Chỉ hoạt động trong cùng LAN (cùng subnet)")
    print("   - Không hoạt động qua Internet/VPN")
    print("   - Router có thể block broadcast packets")
    
    print("\n3. TIMEOUT:")
    print("   - Mặc định 3 giây chờ responses")
    print("   - Nếu LAN chậm, có thể tăng timeout lên 5s")
    
    print("\n4. MULTIPLE SERVERS:")
    print("   - Nếu có nhiều servers, tất cả đều response")
    print("   - Python deduplicate theo IP")
    print("   - Dropdown hiển thị tất cả servers tìm được")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    # Test discovery
    result = test_udp_discovery()
    
    # Giải thích
    explain_udp_discovery()
    
    print("\n\n🎯 READY TO USE!")
    print("Giờ có thể test từ browser: http://localhost:8000/remote/")
    print("Click 'Discover' → Chọn server → Click 'Connect' → Sử dụng!")
