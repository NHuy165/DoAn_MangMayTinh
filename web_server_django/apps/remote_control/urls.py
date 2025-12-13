"""
URL Configuration for Remote Control App
"""
from django.urls import path
from . import views

app_name = 'remote_control'

urlpatterns = [
    # ==================== WEB PAGES (GIAO DIỆN) ====================
    # Trang chủ
    path('', views.index, name='index'),

    # Các trang tính năng chính
    path('applications/', views.applications_page, name='applications'),
    path('processes/', views.processes_page, name='processes'),
    path('file-manager/', views.file_manager_page, name='file_manager'), # Đưa lên cùng nhóm Pages

    # Các trang tính năng phụ (Tools)
    path('screenshot/', views.screenshot_page, name='screenshot'),
    path('keylogger/', views.keylogger_page, name='keylogger'),
    path('webcam/', views.webcam_page, name='webcam'),
    path('power/', views.power_page, name='power'),

    # ==================== API ENDPOINTS (XỬ LÝ NGẦM) ====================
    
    # --- Server & Connection ---
    path('api/server-info/', views.server_info, name='api_server_info'),
    path('api/discover-servers/', views.discover_servers, name='api_discover_servers'),
    path('api/connect-server/', views.connect_server, name='api_connect_server'),
    path('api/disconnect-server/', views.disconnect_server, name='api_disconnect_server'),
    path('api/power/', views.power_action, name='api_power_action'), # Gom nhóm Power về đây

    # --- Keylogger API ---
    path('api/keylog/status/', views.get_keylog_status, name='api_keylog_status'),
    path('api/keylog/get/', views.get_keylog, name='api_keylog_get'),
    path('api/keylog/hook/', views.hook_keylog, name='api_keylog_hook'),
    path('api/keylog/clear/', views.clear_keylog, name='api_keylog_clear'),

    # --- Process & App API ---
    path('api/process/list/', views.get_processes, name='api_process_list'),
    path('api/process/kill/', views.kill_process, name='api_process_kill'),
    path('api/process/start/', views.start_process, name='api_process_start'),
    path('api/app/list/', views.get_apps, name='api_app_list'),
    path('api/app/kill/', views.kill_app, name='api_app_kill'),

    # --- Screenshot API ---
    path('api/screenshot/', views.take_screenshot, name='api_screenshot'),

    # --- Webcam API ---
    path('api/webcam/on/', views.webcam_on, name='api_webcam_on'),
    path('api/webcam/off/', views.webcam_off, name='api_webcam_off'),
    path('api/webcam/stream/', views.webcam_stream, name='api_webcam_stream'),
    path('api/webcam/start-recording/', views.webcam_start_recording, name='api_webcam_start_recording'),
    path('api/webcam/stop-recording/', views.webcam_stop_recording, name='api_webcam_stop_recording'),
    path('api/webcam/status/', views.webcam_status, name='api_webcam_status'),
    path('api/webcam/list/', views.webcam_list, name='api_webcam_list'),
    path('api/webcam/delete/<int:recording_id>/', views.webcam_delete, name='api_webcam_delete'),

    # --- File Manager API ---
    path('api/file/drives/', views.file_get_drives, name='api_file_drives'),
    path('api/file/list/', views.file_get_dir, name='api_file_list'),
    path('api/file/delete/', views.file_delete, name='api_file_delete'),
    path('api/file/download/', views.file_download, name='api_file_download'),
]