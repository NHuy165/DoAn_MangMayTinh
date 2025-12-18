# Remote Control App

Django app for remote computer control via socket connection to C# Target Server.

## Quick Start

1. Start C# Server (port 5656)
2. Run Django: `python manage.py runserver`
3. Access: http://127.0.0.1:8000/remote/

## Features

- 🚀 Start/Kill Processes & Applications
- ⌨️ Keylogger (Hook/Unhook/View)
- 📸 Screenshot capture
- ⚠️ Shutdown/Restart remote machine

## API Endpoints

All APIs under `/remote/api/`:
- Keylog: `/keylog/status/`, `/keylog/get/`, `/keylog/hook/`, `/keylog/clear/`
- Process: `/process/list/`, `/process/kill/`, `/process/start/`
- App: `/app/list/`, `/app/kill/`
- Screenshot: `/screenshot/`
- Power: `/power/`

## Configuration

Edit `socket_client.py` to change target server:
```python
RemoteControlClient(host='127.0.0.1', port=5656, timeout=10)
```

For full documentation, see `/docs/remote-control.md`
