"""
URL Configuration for Remote Control App
"""
from django.urls import path
from . import views

app_name = 'remote_control'

urlpatterns = [
    # Trang chủ Remote Control Dashboard
    path('', views.index, name='index'),
    
    # ==================== APPLICATION PAGES ====================
    path('applications/', views.applications_page, name='applications'),
    
    # ==================== PROCESS PAGES ====================
    path('processes/', views.processes_page, name='processes'),
    
    # ==================== OTHER FEATURE PAGES ====================
    path('screenshot/', views.screenshot_page, name='screenshot'),
    path('keylogger/', views.keylogger_page, name='keylogger'),
    
    path('webcam/', views.webcam_page, name='webcam'),

    path('shell/', views.shell_page, name='shell'),
    
    path('power/', views.power_page, name='power'),
    
    # ==================== API ENDPOINTS ====================
    # API Endpoints - Server Info
    path('api/server-info/', views.server_info, name='api_server_info'),
    
    # API Endpoints - UDP Discovery (NEW!)
    path('api/discover-servers/', views.discover_servers, name='api_discover_servers'),
    
    # API Endpoints - Connection Management
    path('api/connect-server/', views.connect_server, name='api_connect_server'),
    path('api/disconnect-server/', views.disconnect_server, name='api_disconnect_server'),
    
    # API Endpoints - Keylogger
    path('api/keylog/status/', views.get_keylog_status, name='api_keylog_status'),
    path('api/keylog/get/', views.get_keylog, name='api_keylog_get'),
    path('api/keylog/hook/', views.hook_keylog, name='api_keylog_hook'),
    path('api/keylog/clear/', views.clear_keylog, name='api_keylog_clear'),
    
    # API Endpoints - Process Management
    path('api/process/list/', views.get_processes, name='api_process_list'),
    path('api/process/kill/', views.kill_process, name='api_process_kill'),
    path('api/process/start/', views.start_process, name='api_process_start'),
    
    # API Endpoints - Application Management
    path('api/app/list/', views.get_apps, name='api_app_list'),
    path('api/app/kill/', views.kill_app, name='api_app_kill'),
    
    # API Endpoints - Screenshot
    path('api/screenshot/', views.take_screenshot, name='api_screenshot'),
    
    # API Endpoints - Webcam
    path('api/webcam/on/', views.webcam_on, name='api_webcam_on'),
    path('api/webcam/off/', views.webcam_off, name='api_webcam_off'),
    path('api/webcam/stream/', views.webcam_stream, name='api_webcam_stream'),
    path('api/webcam/start-recording/', views.webcam_start_recording, name='api_webcam_start_recording'),
    path('api/webcam/stop-recording/', views.webcam_stop_recording, name='api_webcam_stop_recording'),
    path('api/webcam/status/', views.webcam_status, name='api_webcam_status'),
    path('api/webcam/list/', views.webcam_list, name='api_webcam_list'),
    path('api/webcam/delete/<int:recording_id>/', views.webcam_delete, name='api_webcam_delete'),
    
    # API Endpoints - Power Control
    path('api/power/', views.power_action, name='api_power_action'),

    # API Endpoints - CMD
    path('shell/', views.shell_page, name='shell'),
    path('api/shell/execute/', views.execute_shell_command, name='api_shell_execute'),
]
