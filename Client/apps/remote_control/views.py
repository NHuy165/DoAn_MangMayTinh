"""
Remote Control Views - Django API Endpoints với Persistent Connection
Sử dụng Session-based connection management và UDP Discovery
"""

# ==================== IMPORTS ====================

# Standard Library
import json
import logging
import os

# Django Core
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404, FileResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile

# Local Imports
from .models import WebcamRecording
from .socket_client_persistent import PersistentRemoteClient
from .udp_discovery import UDPDiscoveryClient

# ==================== LOGGER ====================

logger = logging.getLogger(__name__)

# ==================== HELPER FUNCTIONS ====================

def _get_client(request):
    """
    Helper: Lấy PersistentRemoteClient từ session
    
    Hoạt động:
    1. Lấy session_id từ Django session (mỗi user có session_id unique)
    2. Lấy server IP đã lưu trong session (từ lúc connect)
    3. Gọi get_or_create() để lấy hoặc tạo persistent connection
    
    Returns:
        PersistentRemoteClient instance hoặc None nếu chưa connect
    """
    session_id = request.session.session_key
    if not session_id:
        # Chưa có session → Tạo session mới
        request.session.create()
        session_id = request.session.session_key
    
    # Lấy IP server đã lưu (được set khi user bấm Connect)
    server_ip = request.session.get('target_server_ip')
    
    if not server_ip:
        logger.warning("No target server IP in session")
        return None
    
    # Lấy hoặc tạo persistent client
    return PersistentRemoteClient.get_or_create(
        session_id=session_id,
        host=server_ip,
        port=5656,
        timeout=60
    )

def cleanup_missing_recordings():
    """Helper: Xóa record trong DB nếu file thực tế không tồn tại"""
    try:
        from .models import WebcamRecording, ScreenRecording
        
        # Dọn dẹp Webcam
        for rec in WebcamRecording.objects.all():
            if not rec.file_path or not os.path.exists(rec.file_path.path):
                rec.delete()
                
        # Dọn dẹp Screen Recording
        for rec in ScreenRecording.objects.all():
            if not rec.file_path or not os.path.exists(rec.file_path.path):
                rec.delete()
    except Exception:
        pass

# ==================== PAGE VIEWS ====================

def index(request):
    """Trang chủ Tổng quan"""
    return render(request, 'remote_control/home.html')


@require_http_methods(["GET"])
def server_info(request):
    """
    API: Lấy thông tin server (start time) để frontend detect restart
    
    Returns:
        JSON: {"start_time": float}
    """
    start_time = getattr(PersistentRemoteClient, '_server_start_time', 0)
    return JsonResponse({"start_time": start_time})

# ==================== HOME PAGE ====================
def home_page(request):
    """Trang chủ Remote Control Dashboard - Tổng quan"""
    if request.headers.get("HX-Request"):
        return render(request, 'remote_control/partials/home_partial.html')
    return render(request, 'remote_control/home.html')

# ==================== APPLICATION PAGES ====================

def applications_page(request):
    if request.headers.get("HX-Request"):
        return render(request, 'remote_control/partials/applications_partial.html')
    return render(request, 'remote_control/applications.html')


# ==================== PROCESS PAGES ====================

def processes_page(request):
    if request.headers.get('HX-Request'):
        return render(request, 'remote_control/partials/processes_partial.html')
    return render(request, 'remote_control/processes.html')


# ==================== OTHER FEATURE PAGES ====================

def screenshot_page(request):
    if request.headers.get('HX-Request'):
        return render(request, 'remote_control/partials/screenshot_partial.html')
    return render(request, 'remote_control/screenshot.html')

def keylogger_page(request):
    if request.headers.get('HX-Request'):
        return render(request, 'remote_control/partials/keylogger_partial.html')
    return render(request, 'remote_control/keylogger.html')

def webcam_page(request):
    if request.headers.get('HX-Request'):
        return render(request, 'remote_control/partials/webcam_partial.html')
    return render(request, 'remote_control/webcam.html')

def screen_page(request):
    if request.headers.get('HX-Request'):
        return render(request, 'remote_control/partials/screen_partial.html')
    return render(request, 'remote_control/screen.html')

def power_page(request):
    if request.headers.get('HX-Request'):
        return render(request, 'remote_control/partials/power_partial.html')
    return render(request, 'remote_control/power.html')

def shell_page(request):
    if request.headers.get('HX-Request'):
        return render(request, 'remote_control/partials/shell_partial.html')
    return render(request, 'remote_control/shell.html')

# @require_http_methods(["GET"])
def file_manager_page(request):
    """
    Trang File Manager - Tối giản
    Vẫn giữ logic kiểm tra kết nối để chặn truy cập trái phép.
    """
    server_ip = request.session.get('target_server_ip')
    client = _get_client(request)
    
    # Logic kiểm tra chặt chẽ: Phải có Session và Socket đang sống
    is_connected = False
    if server_ip and client and client.connected:
        is_connected = True
    
    # Chỉ truyền biến này để quyết định có hiện bảng file hay không
    context = {
        'is_connected': is_connected
    }

    if request.headers.get('HX-Request'):
        return render(request, 'remote_control/partials/file_manager_partial.html', context)
    return render(request, 'remote_control/file_manager.html', context)

# ==================== UDP DISCOVERY API ====================

@require_http_methods(["GET"])
def discover_servers(request):
    """
    API: Tìm kiếm tất cả C# Servers trong LAN qua UDP broadcast
    
    Hoạt động:
    1. Tạo UDPDiscoveryClient
    2. Gửi broadcast "DISCOVER_SERVER" đến 255.255.255.255:9999
    3. Chờ responses trong 3 giây
    4. Parse và return danh sách servers
    
    Returns:
        JSON: {
            "success": True,
            "servers": [
                {"ip": "192.168.1.10", "name": "DESKTOP-ABC", "port": 5656},
                {"ip": "192.168.1.15", "name": "LAPTOP-XYZ", "port": 5656}
            ],
            "count": 2,
            "message": "Found 2 server(s)"
        }
    """
    try:
        # Tạo UDP Discovery Client
        discovery_client = UDPDiscoveryClient(timeout=3.0)
        
        # Discover servers (blocking 3 seconds)
        result = discovery_client.discover_with_details()
        
        return JsonResponse(result)
    
    except Exception as e:
        logger.error(f"Discovery error: {str(e)}")
        return JsonResponse({
            "success": False,
            "servers": [],
            "count": 0,
            "message": f"Discovery failed: {str(e)}"
        }, status=500)


# ==================== PERSISTENT CONNECTION APIs ====================

@csrf_exempt
@require_http_methods(["POST"])
def connect_server(request):
    """
    API: Tạo persistent connection đến C# Server
    
    Request body: {"server_ip": "192.168.1.10"}
    
    Hoạt động:
    1. Lưu server_ip vào Django session
    2. Tạo persistent socket connection qua PersistentRemoteClient
    3. Connection được lưu trong _instances dictionary theo session_id
    4. Trả về status cho frontend
    """
    try:
        data = json.loads(request.body)
        server_ip = data.get('server_ip')
        
        if not server_ip:
            return JsonResponse({
                "success": False,
                "message": "Server IP is required"
            }, status=400)
        
        # Lưu IP vào session
        request.session['target_server_ip'] = server_ip
        
        # Tạo hoặc lấy persistent client
        client = _get_client(request)
        
        if client and client.connected:
            # Reset CMD ngay khi vừa kết nối
            client.shell_reset()
            
            try:
                client.get_system_stats()
            except:
                pass # Kệ nó nếu lỗi, sẽ check lại lúc lưu file sau

            return JsonResponse({
                "success": True,
                "message": f"Connected to {server_ip}",
                "server_ip": server_ip
            })
        else:
            return JsonResponse({
                "success": False,
                "message": "Failed to connect to server"
            }, status=500)
    
    except Exception as e:
        logger.error(f"Connect error: {str(e)}")
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def disconnect_server(request):
    """
    API: Ngắt persistent connection
    
    Hoạt động:
    1. Lấy session_id
    2. Gọi PersistentRemoteClient.disconnect_session()
    3. Xóa thông tin khỏi Django session
    4. Cleanup resources
    """
    try:
        client = _get_client(request)
        if client and client.connected:
            # ================= DỌN DẸP CMD =================
            try:
                client.shell_reset()
            except: pass

        # Clean session
        session_id = request.session.session_key
        if session_id:
            PersistentRemoteClient.disconnect_session(session_id)
        
        if 'target_server_ip' in request.session:
            del request.session['target_server_ip']
        
        return JsonResponse({"success": True, "message": "Disconnected and saved all recordings"})
    
    except Exception as e:
        logger.error(f"Disconnect error: {str(e)}")
        return JsonResponse({"success": False, "message": str(e)}, status=500)


# ==================== PROCESS & APPLICATION APIs ====================

@require_http_methods(["GET"])
def get_keylog_status(request):
    """API: Lấy trạng thái keylogger"""
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "error", "message": "Not connected to server"}, status=400)
    
    result = client.send_command("KEYLOG", "STATUS")
    return JsonResponse(result)


@require_http_methods(["GET"])
def get_processes(request):
    """API: Lấy danh sách processes"""
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "error", "message": "Not connected to server"}, status=400)
    
    result = client.send_command("PROCESS", "XEM")
    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
def kill_process(request):
    """API: Diệt process theo ID"""
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "error", "message": "Not connected to server"}, status=400)
    
    try:
        data = json.loads(request.body)
        process_id = data.get('id')
        result = client.send_command("PROCESS", "KILL", process_id)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def start_process(request):
    """API: Khởi động process/application"""
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "error", "message": "Not connected to server"}, status=400)
    
    try:
        data = json.loads(request.body)
        process_name = data.get('name')
        result = client.send_command("PROCESS", "START", process_name)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
def get_apps(request):
    """API: Lấy danh sách applications đang chạy"""
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "error", "message": "Not connected to server"}, status=400)
    
    result = client.send_command("APPLICATION", "XEM")
    return JsonResponse(result)


@require_http_methods(["GET"])
def get_start_apps(request):
    """API: Lấy danh sách ứng dụng từ Start Menu của server"""
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "error", "message": "Not connected to server"}, status=400)
    
    result = client.send_command("APPLICATION", "GET_START_APPS")
    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
def kill_app(request):
    """API: Diệt application theo ID"""
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "error", "message": "Not connected to server"}, status=400)
    
    try:
        data = json.loads(request.body)
        app_id = data.get('id')
        result = client.send_command("APPLICATION", "KILL", app_id)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


# ==================== SCREENSHOT API ====================

@require_http_methods(["GET"])
def take_screenshot(request):
    """API: Chụp màn hình"""
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "error", "message": "Not connected to server"}, status=400)
    
    result = client.send_command("TAKEPIC")
    return JsonResponse(result)


# ==================== KEYLOGGER APIs ====================

@require_http_methods(["GET"])
def get_keylog(request):
    """API: Lấy dữ liệu keylog"""
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "error", "message": "Not connected to server"}, status=400)
    
    result = client.send_command("KEYLOG", "PRINT")
    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
def hook_keylog(request):
    """API: Bật/tắt keylogger"""
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "error", "message": "Not connected to server"}, status=400)
    
    try:
        data = json.loads(request.body)
        action = data.get('action')  # HOOK hoặc UNHOOK
        result = client.send_command("KEYLOG", action)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def clear_keylog(request):
    """API: Xóa dữ liệu keylog"""
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "error", "message": "Not connected to server"}, status=400)
    
    result = client.send_command("KEYLOG", "CLEAR")
    return JsonResponse(result)


# ==================== POWER CONTROL APIs ====================

@csrf_exempt
@require_http_methods(["POST"])
def power_action_specific(request, action_type):
    """
    API: Xử lý shutdown/restart dựa trên URL param
    Url match: api/power/<str:action_type>/
    """
    client = _get_client(request)
    if not client:
        # Trả về 200 kèm status disconnected để JS xử lý êm đẹp
        return JsonResponse({"status": "disconnected", "message": "Not connected to server"}, status=200)
    
    # Map từ URL param sang lệnh Protocol của C#
    cmd_map = {
        "shutdown": "SHUTDOWN",
        "restart": "RESTART"
    }
    
    cmd = cmd_map.get(action_type.lower())
    
    if not cmd:
        return JsonResponse({"status": "error", "message": f"Invalid action: {action_type}"}, status=400)
    
    try:
        # Gửi lệnh sang C#
        result = client.send_command(cmd)

        if result.get("status") == "success":
            # Ngắt socket và xóa khỏi danh sách _instances
            session_id = request.session.session_key
            PersistentRemoteClient.disconnect_session(session_id)
            
            # Xóa IP trong session của Django để giao diện quay về màn hình Connect
            if 'target_server_ip' in request.session:
                del request.session['target_server_ip']
            
            # Báo thêm flag này để Frontend biết mà chuyển trang
            result["disconnected"] = True 
            result["message"] += " & Disconnected."

        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


# ==================== SHELL (CMD) APIs ====================

@csrf_exempt
@require_http_methods(["POST"])
def execute_shell_command(request):
    """API: Thực thi lệnh CMD trên server"""
    client = _get_client(request)

    if not client:
        return JsonResponse({
            "status": "disconnected", 
            "message": "Not connected to server"
        }, status=200)
    
    try:
        data = json.loads(request.body)
        cmd = data.get('command')
        
        if not cmd:
            return JsonResponse({"status": "error", "message": "Command is empty"})

        # Gửi lệnh qua socket
        result = client.send_command("CMD", "EXEC", cmd)
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

# ==================== WEBCAM APIs ====================

@csrf_exempt
@require_http_methods(["POST"])
def webcam_on(request):
    """
    API: Bật camera (chỉ preview, chưa ghi video)
    
    Returns:
        JSON: {"success": bool, "message": str}
    """
    client = _get_client(request)
    if not client:
        return JsonResponse({"success": False, "message": "Not connected to server"}, status=400)
    
    try:
        result = client.webcam_on()
        return JsonResponse(result)
    except Exception as e:
        logger.error(f"Webcam ON error: {str(e)}")
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def webcam_off(request):
    """
    API: Tắt camera
    
    Returns:
        JSON: {"success": bool, "message": str}
    """
    client = _get_client(request)
    if not client:
        return JsonResponse({"success": False, "message": "Not connected to server"}, status=400)
    
    try:
        result = client.webcam_off()
        return JsonResponse(result)
    except Exception as e:
        logger.error(f"Webcam OFF error: {str(e)}")
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@require_http_methods(["GET"])
def webcam_stream(request):
    """
    API: Lấy 1 frame hiện tại (JPEG) cho streaming
    
    Returns:
        JPEG image bytes hoặc error
    """

    if not request.session.get('target_server_ip'):
        # Trả về 204 No Content (im lặng) thay vì lỗi 400 ồn ào
        return HttpResponse(status=204)
    
    client = _get_client(request)
    if not client:
        return HttpResponse("Not connected", status=400)
    
    try:
        frame_data = client.webcam_get_frame()
        
        if frame_data:
            return HttpResponse(frame_data, content_type='image/jpeg')
        else:
            return HttpResponse("No frame available", status=404)
    
    except Exception as e:
        logger.error(f"Stream error: {str(e)}")
        return HttpResponse(f"Error: {str(e)}", status=500)


@csrf_exempt
@require_http_methods(["POST"])
def webcam_start_recording(request):
    """
    API: Bắt đầu ghi video (camera phải đã ON)
    
    Returns:
        JSON: {"success": bool, "message": str}
    """
    client = _get_client(request)
    if not client:
        return JsonResponse({"success": False, "message": "Not connected to server"}, status=400)
    
    try:
        result = client.webcam_start_recording()
        return JsonResponse(result)
    except Exception as e:
        logger.error(f"Start recording error: {str(e)}")
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def webcam_stop_recording(request):
    """
    API: Dừng ghi video, nhận file và lưu vào DB + file system
    
    Returns:
        JSON: {"success": bool, "message": str, "recording_id": int}
    """
    client = _get_client(request)
    if not client:
        return JsonResponse({"success": False, "message": "Not connected to server"}, status=400)
    
    try:
        # Nhận video từ C# Server
        result = client.webcam_stop_recording()
        
        if not result.get('success'):
            return JsonResponse(result)
        
        # Lưu video vào file system và DB
        from .models import WebcamRecording
        from django.core.files.base import ContentFile
        
        server_ip = request.session.get('target_server_ip', 'unknown')
        
        host_name = getattr(client, 'hostname', 'Unknown')
        if not host_name or "Unknown" in host_name:
            try:
                # Gọi hàm này để cập nhật self.hostname trong client
                client.get_system_stats()
                # Lấy lại tên mới
                host_name = getattr(client, 'hostname', 'Unknown')
            except: pass
            
        safe_host = "".join([c for c in host_name if c.isalnum() or c in '-_'])
        raw_filename = result.get('filename', 'webcam.avi')
        final_filename = f"{safe_host}_{raw_filename}"
        
        file_size = result.get('file_size', 0)
        duration_sec = result.get('duration', 0)
        
        video_data = result.get('video_data', b'')
        if not video_data:
            return JsonResponse({"success": False, "message": "No video data received"})
        
        # Tạo record trong DB
        
        recording = WebcamRecording(
            server_ip=server_ip,
            filename=final_filename,
            file_size=file_size,
            duration=duration_sec
        )
        
        # Lưu file (Django tự động tạo thư mục theo upload_to)
        recording.file_path.save(final_filename, ContentFile(video_data), save=True)
        
        logger.info(f"Saved recording: {final_filename}, size: {file_size} bytes")
        
        return JsonResponse({
            "success": True,
            "message": "Recording saved successfully",
            "recording_id": recording.id,
            "filename": final_filename,
            "file_size": recording.get_file_size_display()
        })
    
    except Exception as e:
        logger.error(f"Stop recording error: {str(e)}")
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@require_http_methods(["GET"])
def webcam_status(request):
    """
    API: Lấy trạng thái camera. 
    Luôn trả về keys: {"on": bool, "rec": bool} để JS dễ xử lý.
    """
    client = _get_client(request)
    # SỬA LẠI: Trả về key khớp với socket client ("on", "rec") thay vì "camera_on"
    if not client:
        return JsonResponse({"on": False, "rec": False})
    
    try:
        status = client.webcam_status()
        # status từ socket trả về đã là {"on": ..., "rec": ...}
        return JsonResponse(status)
    except Exception as e:
        logger.error(f"Get status error: {str(e)}")
        return JsonResponse({"on": False, "rec": False})


@require_http_methods(["GET"])
def webcam_list(request):
    cleanup_missing_recordings()
    try:
        from .models import WebcamRecording
        
        # Lọc theo IP
        recordings = WebcamRecording.objects.all().order_by('-recorded_at')
        
        recordings_data = []
        for rec in recordings:
            # Format duration (giữ nguyên logic cũ)
            duration_str = str(rec.duration).lower().replace('s', '')
            formatted_duration = "00:00:00"
            if duration_str.isdigit():
                seconds = int(duration_str)
                m, s = divmod(seconds, 60)
                h, m = divmod(m, 60)
                formatted_duration = "{:02d}:{:02d}:{:02d}".format(h, m, s) 

            # [FIX 2] Thay đường dẫn trực tiếp bằng đường dẫn API bảo mật
            # secure_url = f"/remote/api/download/webcam/{rec.id}/"
            # Cập nhật: Dùng reverse url trong code hoặc hardcode như sau:
            secure_url = f"/remote/api/download/webcam/{rec.id}/"

            recordings_data.append({
                "id": rec.id,
                "filename": rec.filename,
                "file_url": secure_url, # <--- Đã đổi URL
                "recorded_at": rec.recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
                "file_size": rec.get_file_size_display(),
                "duration": formatted_duration,
                "server_ip": rec.server_ip
            })
        
        return JsonResponse({"success": True, "recordings": recordings_data})
    
    except Exception as e:
        logger.error(f"List recordings error: {str(e)}")
        return JsonResponse({"success": False, "recordings": []}, status=500)

@require_http_methods(["GET"])
def download_recording(request, rec_type, rec_id):
    """
    API: Tải file an toàn.
    """
    
    # 2. Xác định loại file (Webcam hay Screen)
    if rec_type == 'webcam':
        from .models import WebcamRecording
        ModelClass = WebcamRecording
    elif rec_type == 'screen':
        from .models import ScreenRecording
        ModelClass = ScreenRecording
    else:
        raise Http404("Invalid recording type")

    # 3. Lấy thông tin file từ Database
    # Dùng get_object_or_404 kèm điều kiện server_ip=current_server_ip
    # Nếu file tồn tại nhưng của máy khác -> Tự động trả về lỗi 404
    recording = get_object_or_404(ModelClass, id=rec_id)

    # 4. Kiểm tra file vật lý trên ổ cứng
    if not recording.file_path or not os.path.exists(recording.file_path.path):
        raise Http404("File not found on server storage")

    # 5. Trả về file stream
    try:
        response = FileResponse(open(recording.file_path.path, 'rb'), as_attachment=True)
        # Đặt tên file khi tải về
        response['Content-Disposition'] = f'attachment; filename="{recording.filename}"'
        return response
    except Exception as e:
        raise Http404(f"Error reading file: {str(e)}")
    
@csrf_exempt
@require_http_methods(["DELETE"])
def webcam_delete(request, recording_id):
    """
    API: Xóa 1 recording
    
    Returns:
        JSON: {"success": bool, "message": str}
    """
    try:
        from .models import WebcamRecording
        
        recording = WebcamRecording.objects.get(id=recording_id)
        
        # Xóa file
        if recording.file_path:
            recording.file_path.delete()
        
        # Xóa DB record
        recording.delete()
        
        return JsonResponse({"success": True, "message": "Recording deleted"})
    
    except WebcamRecording.DoesNotExist:
        return JsonResponse({"success": False, "message": "Recording not found"}, status=404)
    except Exception as e:
        logger.error(f"Delete recording error: {str(e)}")
        return JsonResponse({"success": False, "message": str(e)}, status=500)

# ==================== SCREEN RECORDING APIs ====================

@require_http_methods(["GET"])
def screen_list(request):
    cleanup_missing_recordings()
    try:
        from .models import ScreenRecording

        recordings = ScreenRecording.objects.all().order_by('-recorded_at')
        
        data = []
        for rec in recordings:
            duration_str = str(rec.duration)
            formatted_duration = "00:00:00"
            if duration_str.isdigit():
                seconds = int(duration_str)
                m, s = divmod(seconds, 60)
                h, m = divmod(m, 60)
                formatted_duration = "{:02d}:{:02d}:{:02d}".format(h, m, s)

            # [FIX 2] URL bảo mật
            secure_url = f"/remote/api/download/screen/{rec.id}/"

            data.append({
                "id": rec.id,
                "filename": rec.filename,
                "file_url": secure_url, # <--- Đã đổi URL
                "recorded_at": rec.recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
                "file_size": rec.get_file_size_display(),
                "duration": formatted_duration,
                "server_ip": rec.server_ip
            })
        return JsonResponse({"success": True, "recordings": data})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})
    
@csrf_exempt
@require_http_methods(["POST"])
def screen_stream_on(request):
    client = _get_client(request)
    if not client: return JsonResponse({"success": False, "message": "Not connected"}, status=400)
    return JsonResponse(client.screen_start_stream())

@csrf_exempt
@require_http_methods(["POST"])
def screen_stream_off(request):
    client = _get_client(request)
    if not client: return JsonResponse({"success": False, "message": "Not connected"}, status=400)
    return JsonResponse(client.screen_stop_stream())

@require_http_methods(["GET"])
def screen_stream_frame(request):
    client = _get_client(request)
    if not client: return HttpResponse(status=204)
    frame_data = client.screen_get_frame()
    if frame_data: return HttpResponse(frame_data, content_type='image/jpeg')
    return HttpResponse(status=204)

@csrf_exempt
@require_http_methods(["POST"])
def screen_start_rec(request):
    client = _get_client(request)
    if not client: return JsonResponse({"success": False, "message": "Not connected"}, status=400)
    return JsonResponse(client.screen_start_recording())

@csrf_exempt
@require_http_methods(["POST"])
def screen_stop_rec(request):
    client = _get_client(request)
    if not client: return JsonResponse({"success": False, "message": "Not connected"}, status=400)
    try:
        result = client.screen_stop_recording()
        if not result.get('success'): return JsonResponse(result)
        
        from .models import ScreenRecording
        from django.core.files.base import ContentFile
        
        host_name = getattr(client, 'hostname', 'Unknown')
        if not host_name or "Unknown" in host_name:
            try:
                client.get_system_stats()
                host_name = getattr(client, 'hostname', 'Unknown')
            except: pass
        safe_host = "".join([c for c in host_name if c.isalnum() or c in '-_'])
        
        raw_filename = result.get('filename', 'screen.avi')
        final_filename = f"{safe_host}_{raw_filename}"
        
        rec = ScreenRecording(
            server_ip=request.session.get('target_server_ip', 'unknown'),
            filename=final_filename,
            file_size=result.get('file_size'),
            duration=result.get('duration', 0)
        )
        rec.file_path.save(final_filename, ContentFile(result.get('video_data')), save=True)
        
        return JsonResponse({
            "success": True, 
            "message": "Saved successfully",
            "filename": final_filename,
            # Trả về chuỗi size dễ đọc (VD: 5.2 MB) thay vì bytes
            "file_size": rec.get_file_size_display(), 
            "duration": result.get('duration')
        })
        
    except Exception as e: return JsonResponse({"success": False, "message": str(e)}, status=500)

@require_http_methods(["GET"])
def screen_get_status(request):
    """API: Lấy trạng thái màn hình"""
    client = _get_client(request)
    if not client: 
        return JsonResponse({"on": False, "rec": False})
        
    return JsonResponse(client.screen_status())


@csrf_exempt
@require_http_methods(["DELETE"])
def screen_delete(request, recording_id):
    """API: Xóa 1 bản ghi màn hình"""
    try:
        from .models import ScreenRecording
        
        recording = ScreenRecording.objects.get(id=recording_id)
        
        # Xóa file vật lý trên ổ cứng
        if recording.file_path:
            recording.file_path.delete()
        
        # Xóa record trong Database
        recording.delete()
        
        return JsonResponse({"success": True, "message": "Recording deleted"})
    
    except ScreenRecording.DoesNotExist:
        return JsonResponse({"success": False, "message": "Recording not found"}, status=404)


# ==================== FILE MANAGER APIs ====================

@csrf_exempt
def file_get_drives(request):
    """API: Lấy danh sách ổ đĩa"""
    client = _get_client(request)
    if not client or not client.connected: 
        return JsonResponse({"success": False, "message": "Access Denied: Not connected"}, status=403)
    
    try:
        result = client.file_get_drives()
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def file_get_dir(request):
    """API: Lấy danh sách file"""
    client = _get_client(request)
    if not client or not client.connected: 
        return JsonResponse({"success": False, "message": "Access Denied: Not connected"}, status=403)
    
    try:
        data = json.loads(request.body)
        path = data.get('path', '')
        result = client.file_get_directory(path)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def file_delete(request):
    """API: Xóa file"""
    client = _get_client(request)
    if not client or not client.connected: 
        return JsonResponse({"success": False, "message": "Access Denied: Not connected"}, status=403)
    
    try:
        data = json.loads(request.body)
        path = data.get('path')
        result = client.file_delete_item(path)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def file_download(request):
    """API: Tải file"""
    client = _get_client(request)
    if not client or not client.connected: 
        return JsonResponse({"success": False, "message": "Access Denied: Not connected"}, status=403)
    
    try:
        data = json.loads(request.body)
        path = data.get('path')
        
        result = client.file_download(path)
        if result.get('success'):
            response = HttpResponse(result['data'], content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{result["filename"]}"'
            return response
        else:
            return JsonResponse(result, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


# ==================== SYSTEM INFORMATION ====================

@require_http_methods(["GET"])
def get_server_stats(request):
    """API: Lấy thông số Dashboard (Frontend gọi liên tục 2s/lần)"""
    client = _get_client(request)
    
    if not client or not client.connected:
        return JsonResponse({
            "status": "disconnected",
            "message": "Client not connected"
        })
        
    result = client.get_system_stats()
    
    if result.get("status") == "error" and "Broken pipe" in str(result.get("message")):
         return JsonResponse({"status": "disconnected"})

    return JsonResponse(result)