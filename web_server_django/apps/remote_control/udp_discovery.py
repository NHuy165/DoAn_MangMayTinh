"""
UDP Discovery Client - Tìm kiếm C# Servers trong LAN
Sử dụng UDP Broadcast để discover servers đang chạy

Giao thức:
1. Python gửi broadcast "DISCOVER_SERVER" đến 255.255.255.255:9999
2. C# Server nhận message và trả lời với hostname + IP
3. Python collect tất cả responses trong timeout period (3 giây)
4. Return danh sách servers tìm được
"""
import socket
import json
import logging

logger = logging.getLogger(__name__)


class UDPDiscoveryClient:
    """
    Client để discover C# Remote Control Servers trong LAN qua UDP broadcast
    
    Hoạt động:
    - Gửi broadcast message đến tất cả devices trong LAN
    - Chờ responses từ các servers (timeout 3s)
    - Parse và return danh sách servers
    """
    
    # Cấu hình UDP Discovery
    DISCOVERY_PORT = 9999  # Port C# Server lắng nghe UDP
    BROADCAST_IP = '255.255.255.255'  # Broadcast địa chỉ (gửi đến tất cả devices)
    DISCOVERY_MESSAGE = 'DISCOVER_SERVER'  # Message định danh
    TIMEOUT = 3.0  # Thời gian chờ responses (3 giây)
    BUFFER_SIZE = 1024  # Kích thước buffer nhận data
    
    def __init__(self, timeout=None):
        """
        Khởi tạo UDP Discovery Client
        
        Args:
            timeout: Thời gian chờ responses (mặc định 3s)
        """
        self.timeout = timeout or self.TIMEOUT
    
    def discover_servers(self):
        """
        Tìm kiếm tất cả C# Servers trong LAN
        
        Quy trình:
        1. Tạo UDP socket với broadcast enabled
        2. Gửi broadcast message "DISCOVER_SERVER"
        3. Lắng nghe responses trong TIMEOUT seconds
        4. Parse responses và deduplicate theo IP
        5. Return danh sách servers
        
        Returns:
            list: [{"ip": "192.168.1.10", "name": "DESKTOP-ABC", "port": 5656}, ...]
        """
        servers = []
        seen_ips = set()  # Để deduplicate nếu có duplicate responses
        sock = None
        
        try:
            # === TẠO UDP SOCKET ===
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # QUAN TRỌNG: Enable broadcast
            # SO_BROADCAST cho phép gửi đến địa chỉ broadcast (255.255.255.255)
            # Mặc định socket không cho phép broadcast để tránh spam network
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
            # Set timeout để không block mãi mãi khi chờ responses
            sock.settimeout(self.timeout)
            
            logger.info(f"Broadcasting discovery message to {self.BROADCAST_IP}:{self.DISCOVERY_PORT}")
            
            # === GỬI BROADCAST MESSAGE ===
            # Gửi "DISCOVER_SERVER" đến tất cả devices trong LAN
            # Mọi device trên port 9999 sẽ nhận được message này
            message = self.DISCOVERY_MESSAGE.encode('utf-8')
            sock.sendto(message, (self.BROADCAST_IP, self.DISCOVERY_PORT))
            
            logger.info(f"Waiting for responses (timeout: {self.timeout}s)...")
            
            # === NHẬN RESPONSES ===
            # Vòng lặp nhận responses cho đến khi timeout
            while True:
                try:
                    # Nhận data từ bất kỳ server nào response
                    # recvfrom() trả về (data, (ip, port))
                    data, addr = sock.recvfrom(self.BUFFER_SIZE)
                    
                    # Parse response
                    server_info = self._parse_response(data, addr)
                    
                    if server_info and server_info['ip'] not in seen_ips:
                        servers.append(server_info)
                        seen_ips.add(server_info['ip'])
                        logger.info(f"Discovered server: {server_info['name']} ({server_info['ip']})")
                
                except socket.timeout:
                    # Timeout đạt → Không còn responses nữa
                    logger.info(f"Discovery timeout reached. Found {len(servers)} server(s)")
                    break
                
                except Exception as e:
                    logger.error(f"Error receiving response: {str(e)}")
                    continue
        
        except Exception as e:
            logger.error(f"UDP Discovery error: {str(e)}")
        
        finally:
            # Đóng socket
            if sock:
                sock.close()
        
        return servers
    
    def _parse_response(self, data, addr):
        """
        Parse response từ C# Server
        
        Format response từ C# (có thể là 1 trong 2 dạng):
        1. Plain text: "HOSTNAME|IP_ADDRESS"
           Ví dụ: "DESKTOP-ABC|192.168.1.10"
        
        2. JSON: {"hostname": "DESKTOP-ABC", "ip": "192.168.1.10", "port": 5656}
        
        Args:
            data: Bytes data nhận được
            addr: Tuple (ip, port) của sender
            
        Returns:
            dict: {"ip": "...", "name": "...", "port": 5656} hoặc None nếu parse fail
        """
        try:
            # Decode bytes → string
            response = data.decode('utf-8').strip()
            
            logger.debug(f"Received from {addr[0]}: {response}")
            
            # TRY PARSE JSON FIRST (nếu C# gửi JSON)
            try:
                json_data = json.loads(response)
                return {
                    'ip': json_data.get('ip', addr[0]),  # Fallback to sender IP
                    'name': json_data.get('hostname', 'Unknown'),
                    'port': json_data.get('port', 5656)
                }
            except json.JSONDecodeError:
                pass
            
            # FALLBACK: PARSE PLAIN TEXT FORMAT "HOSTNAME|IP"
            if '|' in response:
                parts = response.split('|')
                if len(parts) >= 2:
                    return {
                        'ip': parts[1].strip(),
                        'name': parts[0].strip(),
                        'port': 5656  # Default port
                    }
            
            # FALLBACK: Chỉ có hostname hoặc message khác
            # Sử dụng IP từ sender address
            return {
                'ip': addr[0],
                'name': response if response else 'Unknown Server',
                'port': 5656
            }
        
        except Exception as e:
            logger.error(f"Error parsing response from {addr[0]}: {str(e)}")
            return None
    
    def discover_with_details(self):
        """
        Tìm kiếm servers và bao gồm thêm thông tin chi tiết
        Có thể mở rộng để test connection TCP sau khi discover
        
        Returns:
            dict: {
                "success": True,
                "servers": [...],
                "count": 3,
                "message": "Found 3 server(s)"
            }
        """
        servers = self.discover_servers()
        
        return {
            'success': True,
            'servers': servers,
            'count': len(servers),
            'message': f'Found {len(servers)} server(s)' if servers else 'No servers found'
        }


def quick_discover(timeout=3.0):
    """
    Helper function: Quick discover servers
    
    Usage:
        from .udp_discovery import quick_discover
        servers = quick_discover()
    
    Args:
        timeout: Thời gian chờ responses
        
    Returns:
        list: Danh sách servers
    """
    client = UDPDiscoveryClient(timeout=timeout)
    return client.discover_servers()
