from django.apps import AppConfig
import signal
import sys


class RemoteControlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.remote_control'

    def ready(self):
        """Đăng ký signal handlers khi Django khởi động"""
        # Import ở đây để tránh circular import
        from .socket_client_persistent import PersistentRemoteClient
        import time
        
        # ===== FORCE RESET KHI DJANGO RESTART =====
        # 1. Xóa tất cả socket references
        PersistentRemoteClient._instances.clear()
        
        # 2. Lưu server startup timestamp để frontend detect restart
        PersistentRemoteClient._server_start_time = time.time()
        
        print(f"[Startup] Socket reset complete (timestamp: {PersistentRemoteClient._server_start_time:.0f})")
        
        def cleanup_connections(signum, frame):
            """Cleanup tất cả connections khi shutdown"""
            print("\n[Shutdown] Closing persistent connections...")
            try:
                session_ids = list(PersistentRemoteClient._instances.keys())
                closed_count = 0
                
                for session_id in session_ids:
                    try:
                        client = PersistentRemoteClient._instances.get(session_id)
                        if client and client.socket:
                            try:
                                client.socket.shutdown(2)
                            except:
                                pass
                            client.socket.close()
                            closed_count += 1
                    except:
                        pass
                
                PersistentRemoteClient._instances.clear()
                print(f"[Shutdown] Closed {closed_count} socket(s)")
            except Exception as e:
                print(f"[Shutdown] Error during cleanup: {str(e)}")
            sys.exit(0)
        
        # Đăng ký signal handlers
        signal.signal(signal.SIGINT, cleanup_connections)   # Ctrl+C
        signal.signal(signal.SIGTERM, cleanup_connections)  # Kill command
