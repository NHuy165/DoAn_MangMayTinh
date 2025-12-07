"""
Remote Control Views - Django API Endpoints
Chuyển đổi từ Flask routes sang Django views
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .socket_client import RemoteControlClient


# Khởi tạo client (có thể config từ settings sau)
remote_client = RemoteControlClient(host='127.0.0.1', port=5656, timeout=10)


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


def webcam_off(request):
    return render(request, 'remote_control/webcam_off.html')


def webcam_record(request):
    return render(request, 'remote_control/webcam_record.html')


def power_page(request):
    return render(request, 'remote_control/power.html')


@require_http_methods(["GET"])
def get_keylog_status(request):
    """API: Lấy trạng thái keylogger"""
    result = remote_client.send_command_to_server("KEYLOG", "STATUS")
    return JsonResponse(result)


@require_http_methods(["GET"])
def get_processes(request):
    """API: Lấy danh sách processes"""
    result = remote_client.send_command_to_server("PROCESS", "XEM")
    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
def kill_process(request):
    """API: Diệt process theo ID"""
    try:
        data = json.loads(request.body)
        process_id = data.get('id')
        result = remote_client.send_command_to_server("PROCESS", "KILL", process_id)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def start_process(request):
    """API: Khởi động process/application"""
    try:
        data = json.loads(request.body)
        process_name = data.get('name')
        result = remote_client.send_command_to_server("PROCESS", "START", process_name)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
def get_apps(request):
    """API: Lấy danh sách applications"""
    result = remote_client.send_command_to_server("APPLICATION", "XEM")
    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
def kill_app(request):
    """API: Diệt application theo ID"""
    try:
        data = json.loads(request.body)
        app_id = data.get('id')
        result = remote_client.send_command_to_server("APPLICATION", "KILL", app_id)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
def take_screenshot(request):
    """API: Chụp màn hình"""
    result = remote_client.send_command_to_server("TAKEPIC")
    return JsonResponse(result)


@require_http_methods(["GET"])
def get_keylog(request):
    """API: Lấy dữ liệu keylog"""
    result = remote_client.send_command_to_server("KEYLOG", "PRINT")
    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
def hook_keylog(request):
    """API: Bật/tắt keylogger"""
    try:
        data = json.loads(request.body)
        action = data.get('action')  # HOOK hoặc UNHOOK
        result = remote_client.send_command_to_server("KEYLOG", action)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def clear_keylog(request):
    """API: Xóa dữ liệu keylog"""
    result = remote_client.send_command_to_server("KEYLOG", "CLEAR")
    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
def power_action(request):
    """API: Shutdown/Restart remote server"""
    try:
        data = json.loads(request.body)
        action = data.get('action')  # SHUTDOWN hoặc RESTART
        result = remote_client.send_command_to_server(action)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
