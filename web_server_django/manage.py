#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# --- In LAN address khi server start ---
def print_lan_address(port=8000):
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"\nDjango server LAN address: http://{local_ip}:{port}/\n")
    except Exception as e:
        print(f"Could not detect LAN IP: {e}")


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # --- In LAN address khi server thực sự chạy (không phải autoreload) ---
    if os.environ.get('RUN_MAIN') == 'true':
        # Lấy port từ sys.argv nếu có
        port = 8000
        for arg in sys.argv:
            if ':' in arg:
                try:
                    port = int(arg.split(':')[-1])
                except: pass
        print_lan_address(port)
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
