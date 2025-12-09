# Hướng dẫn đồ án RAT Client-Server

**Exported:** 12/9/2025 14:19:05  
**Link:** [https://gemini.google.com/app/e0e207ecf507f709](https://gemini.google.com/app/e0e207ecf507f709)

## Prompt:
> Keylog - CS

> Program - CS

> server - CS

> TargetServer.csproj - XML

> app - PY

> file structure - TXT

thầy tôi đang cho làm 1 đồ án mạng máy tính như sau, và sau đây là code và file structure của tôi, để làm rõ, server là thiết bị bị điều khiển, client là thiết bị điều khiển, vscode sẽ chạy app.py và vs sẽ chạy file target

## Prompt:
không, bây giờ tôi muốn thêm chức năng web cam, hãy nói cho tôi biết các loại webcam tôi có thể chọn để bổ sung

## Prompt:
bây giờ chức năng là record, streaming luôn thì nên dùng gì

## Prompt:
> file structure - TXT

bây giờ, trước hết hãy đọc lại file structure.txt để xem bạn còn cần thông tin nào để thực hiện thêm mới chức năng này

## Prompt:
> index - HTML

> keylog_cache - TXT

> TargetServer.exe - Không xác định

> TargetServer.exe - CONFIG

> TargetServer.pdb - Không xác định

đây

## Prompt:
Cài NuGet Packages:

Mở Package Manager Console trong Visual Studio và chạy các lệnh sau: tôi chưa hiểu, mở package manager console là làm như thế nào

## Prompt:
PM\> Install-Package AForge.Video.DirectShow

Install-Package : Project 'Default' is not found.

At line:1 char:1

\+ Install-Package AForge.Video.DirectShow

\+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    + CategoryInfo          : ObjectNotFound: (Default:String) \[Install-Package\], ItemNotFoundException

    + FullyQualifiedErrorId : NuGetProjectNotFound,NuGet.PackageManagement.PowerShellCmdlets.InstallPackageCommand

PM\> Install-Package AForge.Video.DirectShow Install-Package AForge.Video.FFMPEG

Install-Package : Project 'Install-Package' is not found.

At line:1 char:1

\+ Install-Package AForge.Video.DirectShow Install-Package AForge.Video. ...

\+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    + CategoryInfo          : ObjectNotFound: (Install-Package:String) \[Install-Package\], ItemNotFoundException

    + FullyQualifiedErrorId : NuGetProjectNotFound,NuGet.PackageManagement.PowerShellCmdlets.InstallPackageCommand tôi làm ở cách 1 nhưng lại bị lỗi này

## Prompt:
Bấm chuột phải vào chữ TargetServer (tên dự án của bạn).

Chọn dòng Manage NuGet Packages... (Quản lý các gói NuGet...). sau khi bấm, tôi ko thấy chỗ chọn dòng đó

## Prompt:
> file structure - TXT

targetServer là tên folder của tôi hả, hay là tên đồ án của tôi, đây là file structure

## Prompt:
> ![Preview Image](https://lh3.googleusercontent.com/gg/AIJ2gl8WS5WbUdhyYVzb4d-dtrpOh0gnp0dHQJxNEqZXvoOqqPA8Reyt1gztfTXcQiAueHL5jtVnDNNn6J3NnTWGwKjllxmseRoR4IY_CA8TvxoGmpKpdB8hy6mQjPz7K6mq_jY_qLgIYjdo7hTj8kTUsfDQEDKyr_GYloVyiOWKZudBrAxIAUs7PkD6FcDpzchqHZTTooo4rdFaUkht9S12uvuPNF3l5wSZZ7qQo87EuzU3_BnzQF3zGWqAg0SHLEjCIvTLvTx9NK5sQ6alAZiiToQpXqywkEkrqg)

hãy coi thử ở trong bức ảnh này đi

## Prompt:
không, cái tôi gửi bạn là visual studio màu tím mà

## Prompt:
> ![Preview Image](https://lh3.googleusercontent.com/gg/AIJ2gl_8AhOJiaYW_eoZDn7PrXAFVeVNgMUKd-VNgTTJKEM62WsPIScrm66SXWFs-N267-Fy5A-8fAbfRI325XbdsNklThuxmY-CD26MeLsPkFPK8NC6sXFHHmvs-DoewD2yHlOoy0GVdRof7z5SUWL6vmRGkzK6fSgHbdffM9QRlKE-IZlKVlmRn2EY9CJlNSW0leG_lNVfzRljmd9ztvL9TviaUISjS8NXE_6yutLBi9DXhTAZXBTM41rdt5wPvLS_qMjzqZ2dsVbD_QmjMBkq35xv-O5zr7GTWw)

tôi phải chọn cái nào

## Prompt:
> ![Preview Image](https://lh3.googleusercontent.com/gg/AIJ2gl8wJdcN27Ic2yRmg8pYTT78-Tz20aNse6-7jiKLt61JUnuCfkBY5pwMjG--LB34ljrJsxLFfqSftOnr54cbpZgqgjtnvZvEl6SYq2hebarLBm3YNj5Or3H0B7ihiTtBefAS8-8xUhkRuYAl5OHfUEWXb8G-N5zXL-t_DKcnti9uvCC09gjSWAaU_IECvJpu7Mejn9UjNFLj6Nwl0AEfvzJUTtnNkSed1GFaN0dgo6Oi_O6AV2ArrMI7eE9Tf3i5LyXRry1mHS2VNPCck_GkG-mNPO-Kk5Wk1Q)

nếu tôi tải bản x64 thì ko cần chuyển chế độ này đúng không Chuyển sang chế độ x86 (Bắt buộc):

AForge.Video.FFMPEG chỉ chạy được trên nền tảng 32-bit.

Trong Visual Studio, trên thanh công cụ, đổi "Any CPU" thành "x86".

## Prompt:
bây giờ tôi đã tải xong, hãy chỉ tiếp bước này cực kì cẩn thận cho tôi trước đã, lưu ý rằng tôi chỉ tải được Accord.Video.FFMPEG.x64 và AForge.Video.DirectShow, chưa Copy các file DLL, cần hướng dẫn ở bước này

## Prompt:
khoan đã, bây giờ tôi muốn mở lại nguyên thư mục đồ án, thì tôi chọn open folder hay opder project vậy

## Prompt:
> ![Preview Image](https://lh3.googleusercontent.com/gg/AIJ2gl8cAGT6e9k-M9mjL0zp7e5IwYFofkPP0bhrHdgPr1SV1tARlceb4f-D5xfP2nVWjJrTRaZcM0rN_XVIZ0Ex0sL183ju8FlqNgZmPMLZaoJZDb25_Bhe75dR3kKzQaSk5AZwsagq-rVwhB7tZyCi2_HHhAx1hbQ30ZP8yQ3qcWMqXGbhOBgoNICX5LUpnxy7PJnYwEZEF2Ue1qNzbUmvss1Avo3yxPVNqViaOgPBqva16NFPL-uMjuFVzX2h7EORGO8AYA0A_N1G7h1oqbj3l7SP7rHlXKZMhDc)

> ![Preview Image](https://lh3.googleusercontent.com/gg/AIJ2gl87yESOlQg3jhnfQWxYSbEY3_Z1YOjF7r0t_CHrC7Er5xtlg3xAcqLaJZ454sJhxn8RkYdkmbn5WQGQckQgcvWD-ATl3KzmrKs43ohm7_0J9dv-vsJ5JF_cD96hnCjge9iQCdxlzQpERXLSFIleEN3OxxlWTlVfpKlUPhKfsJAcH_Pra96DneGoqjdTSuRFPg4kGHfHnKnTLWTHjjAbSVvZ9-Q5mf0qxRLb6ta3eLa0L64ueDlZ5RsCXi683YfHTwnA4-tQ7OMkWSMdSCcLSrm_QNhRoOceSA)

BƯỚC 3: Sửa Code C# (server.cs) ủa file này ở đâu, sao tôi mở server.cs thì chỉ ra server.cs\[design\] vậy

## Prompt:
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

            this.FormClosing += new FormClosingEventHandler(server\_FormClosing);

            // Xóa file log cũ khi khởi động lại server để tránh file bị phình to

            try

            {

                if (File.Exists(KeyLogger.appstart.path))

                    File.Delete(KeyLogger.appstart.path);

            }

            catch { }

        }

        // Đảm bảo ngắt toàn bộ tiến trình khi đóng Form

        private void server\_FormClosing(object sender, FormClosingEventArgs e)

        {

            System.Diagnostics.Process.GetCurrentProcess().Kill();

        }

        // Sự kiện nút "Open Server"

        private void button1\_Click(object sender, EventArgs e)

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

                    case "KEYLOG": keylog(); break;     // Chuyển sang xử lý Keylog

                    case "SHUTDOWN": System.Diagnostics.Process.Start("ShutDown", "-s"); break;

                    case "RESTART": System.Diagnostics.Process.Start("shutdown", "/r /t 0"); break;

                    case "TAKEPIC": takepic(); break;   // Chụp màn hình

                    case "PROCESS": process(); break;   // Quản lý tiến trình

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

            KeyLogger.appstart.path = Application.StartupPath + @"\\keylog\_cache.txt";

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

                        byte\[\] b = ms.ToArray();

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

                    Process\[\] pr = Process.GetProcesses();

                    List\<Process\> filteredList = new List\<Process\>();

                    foreach (Process p in pr)

                    {

                        // Nếu mode là App thì chỉ lấy cửa sổ có tiêu đề

                        if (mode == "All" || p.MainWindowTitle.Length \> 0) filteredList.Add(p);

                    }

                    // Sắp xếp danh sách

                    if (mode == "App") filteredList = filteredList.OrderBy(p =\> p.MainWindowTitle).ToList();

                    else filteredList = filteredList.OrderBy(p =\> p.ProcessName).ToList();

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

                            Program.nw.WriteLine(\$"Successfully killed: {pName} (ID: {id})");

                        }

                        catch (Exception ex) { Program.nw.WriteLine("Failed: " + ex.Message.Replace("\\n", " ")); }

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

                        catch (Exception ex) { Program.nw.WriteLine("Failed: " + ex.Message.Replace("\\n", " ")); }

                        Program.nw.Flush();

                    }

                }

            }

        }

    }

} sửa file này thành cái của bạn hả

## Prompt:
không, tôi không muốn phá vỡ cấu trúc của file này, hãy viết cho tôi những gì CẦN THÊM VÀO để tôi ghi

## Prompt:
ủa vậy chỗ luồng riêng ở đâu, tôi ko thấy ở đây bạn thêm vô nhỉ

## Prompt:
> server - CS

khoan, ở BƯỚC CUỐI: Cập nhật hàm đóng Form, tôi chưa hiểu vị trí cần thêm vào lắm, đây là file sau khi đã thêm các bước ở trên, hãy kiểm tra thật kĩ một lần nữa và nói rõ hơn vị trí cần thêm vào ở bước cuối nhé

## Prompt:
        private void server\_FormClosing(object sender, FormClosingEventArgs e)

        {

            System.Diagnostics.Process.GetCurrentProcess().Kill();

        } ủa hình như chưa có

## Prompt:
> index - HTML

> app - PY

khoan, vậy còn file app.py và file index.html cần phải thêm những gì, hãy viết cho tôi đầy đủ, cụ thể hơn, tôi sẽ gửi lại file nguyên mẫu của tôi

## Prompt:
Bước 1: Thêm giao diện Webcam

Tìm đoạn code hiển thị Process Control (khoảng dòng 30-40). Bạn hãy chèn đoạn code HTML này vào ngay bên dưới nó (hoặc bất kỳ vị trí nào bạn thấy đẹp trong div.container): tôi chưa biết nên thêm vào đâu là hợp lí nhất, tôi sẽ địa lại file cho bạn(đã thêm hàm trong script), bạn hãy gợi ý chỗ nào nên thêm mới và giải thích lí do sao cho trình bày một cách hợp lí

## Prompt:
tôi đã thêm vào, vậy bây giờ tôi sẽ test thôi đúng không

## Prompt:
hướng dẫn cách chạy cho tôi

## Prompt:
> app - PY

> index - HTML

> server - CS

> TargetServer.csproj - XML

> ![Preview Image](https://lh3.googleusercontent.com/gg/AIJ2gl_37KjgsCXVVAM03iWqS6_434ytxJq2RcZpiUedezQsiR-I7Np5p_avVr_yUezSJhYr5PgxwpyWWF4ll5Lsfj6mX5gOgSXAspevZW6UOKkJYa244BRAoEcMw6UVDyedtBfAcw0tXDa12dzJanJ2HTBFDy_sMhDfZytT9BZ1oaPnvJlMVKlWi3kd9tEny9FqqyOfufNNVeg0AIBr4QNJS8DWeF3PdFixg-F0pljIf4qQQAXGoTZ_VkQzwI28moA-sxMawisfFrazoa8aIdrWQ_-2DqedphqVEQ)

> ![Preview Image](https://lh3.googleusercontent.com/gg/AIJ2gl-NzUPHd96NFnk0RlRRFJ9mlu60D8vMc9S4P9fmz3i-4SdloxynneUgsbYVs89JqcCFeh8OTGXlL2Zo-rDR_EI8CIZ3SiHtJPMF-M4ve2cjYO5kMMocab6xhT5Doe8IhzbLOyZFczcdLkkWjblG4CWud0uVU4AmFDUYpNYJ84bX4cLuqmDm94zgDKHwZ2FtOwE5A_FC8GXMOrqvZGiNdQxuE6TABnl0_VFv4uaOZHR26GfYuc2oZ2sp-_8X8Zxu-vTO2RwsBKhX-y-GUlz5bfxwyGt4XX93F3E)

code đã bị lỗi vì tôi ko nhấn được start streaming, hãy chỉ tôi fix, suy nghĩ thật cẩn thận

## Prompt:
> server - CS

> app - PY

> index - HTML

vẫn chưa mở được Camera khi nhấn start stream, hãy kiểm tra thật kĩ các file này, trong khi đó ở thư mục này C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug tôi đã thấy đủ, nếu cần tôi có thể gửi tất cả files trong folder này

## Prompt:
> server - CS

> app - PY

> index - HTML

không, nếu sửa như bước 1 thì không thể thêm được tính năng, tôi cần thêm tính năng các sau này, yêu cầu sửa lại 3 files index, server.cs, app.py 1 cách rõ ràng, cụ thể từng bước để có tính triển khai mở rộng sau này, hướng dẫn kĩ càng cho tôi từng bước, chức năng này cần có câu lệnh cụ thể, không bị nhầm lẫn như các chức năng trước đó đã từng làm, lưu ý là trong thư mục TargetServer\\bin\\x64\\Debug đã đầy đủ, ko cần nhắc lại lỗi này là lỗi tiềm ẩn nữa

## Prompt:
tôi đã sửa nhưng vẫn không bật được máy quay, bạn nghĩ vấn đề không phải do code thì có thể nào do package không

## Prompt:
> avcodec-57.dll - Không xác định

> avdevice-57.dll - Không xác định

> avfilter-6.dll - Không xác định

> avformat-57.dll - Không xác định

> avutil-55.dll - Không xác định

> keylog_cache - TXT

> postproc-54.dll - Không xác định

> swresample-2.dll - Không xác định

> swscale-4.dll - Không xác định

chúng đây

## Prompt:
khi chạy tôi đã nhấn 1 xóa 1 tab chạy CPU gì đó của server.cs, làm thế nào để mở lại

## Prompt:
'TargetServer.exe' (CLR v4.0.30319: DefaultDomain): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_64\\mscorlib\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\mscorlib.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: DefaultDomain): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\TargetServer.exe'. Symbols loaded.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Windows.Forms\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\System.Windows.Forms.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\System.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Drawing\\v4.0\_4.0.0.0\_\_b03f5f7f11d50a3a\\System.Drawing.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\Program Files\\Microsoft Visual Studio\\18\\Community\\Common7\\IDE\\PrivateAssemblies\\Runtime\\Microsoft.VisualStudio.Debugger.Runtime.Desktop.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Configuration\\v4.0\_4.0.0.0\_\_b03f5f7f11d50a3a\\System.Configuration.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Core\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\System.Core.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Xml\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\System.Xml.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.FFMPEG.x64.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.DirectShow.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (11608) has exited with code 0 (0x0).

The program '\[33612\] TargetServer.exe' has exited with code 4294967295 (0xffffffff). đây là tất cả output, vẫn không chạy được camera ghi hình, tôi không biết tại sao

## Prompt:
'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\TargetServer.exe'. 

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ntdll.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\mscoree.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\kernel32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\KernelBase.dll'. Symbol loading disabled by Include/Exclude setting.

The thread 20160 has exited with code 0 (0x0).

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\advapi32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msvcrt.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\sechost.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\rpcrt4.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\mscoreei.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\shlwapi.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ucrtbase.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\kernel.appcore.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\version.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\clr.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\user32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\vcruntime140\_1\_clr0400.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\win32u.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ucrtbase\_clr0400.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\vcruntime140\_clr0400.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\gdi32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\gdi32full.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msvcp\_win.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\imm32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\combase.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\combase.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\psapi.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\psapi.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\mscorlib\\8967064a93c70884749ad00de74dd7a1\\mscorlib.ni.dll'. 

'TargetServer.exe' (CLR v4.0.30319: DefaultDomain): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_64\\mscorlib\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\mscorlib.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ole32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\combase.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\bcryptprimitives.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\uxtheme.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (CLR v4.0.30319: DefaultDomain): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\TargetServer.exe'. Symbols loaded.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\clrjit.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\System\\22f4d83e48c2201947e262d4bca638b9\\System.ni.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\System.Drawing\\5821108419fb5a77cec19ab38b18df8d\\System.Drawing.ni.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\System.Windows.Forms\\178af1a38c876ea1858e97cb2cacfd71\\System.Windows.Forms.ni.dll'. 

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Windows.Forms\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\System.Windows.Forms.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\System.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Drawing\\v4.0\_4.0.0.0\_\_b03f5f7f11d50a3a\\System.Drawing.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\System.Core\\f61ee525f58db9cd7a10cfcd4d09d809\\System.Core.ni.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\System.Configuration\\fa14af79c42b95ce77c01a830ef23378\\System.Configuration.ni.dll'. 

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Configuration\\v4.0\_4.0.0.0\_\_b03f5f7f11d50a3a\\System.Configuration.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Core\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\System.Core.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\System.Xml\\b0d622690434a583a34bc048e1549b69\\System.Xml.ni.dll'. 

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Xml\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\System.Xml.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\shell32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\WinTypes.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\windows.storage.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\SHCore.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\profapi.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\bcrypt.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\cryptsp.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\rsaenh.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\cryptbase.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\WinSxS\\amd64\_microsoft.windows.common-controls\_6595b64144ccf1df\_5.82.26100.5074\_none\_87eb64a37a300c6e\\comctl32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msctf.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\WinSxS\\amd64\_microsoft.windows.gdiplus\_6595b64144ccf1df\_1.1.26100.7019\_none\_6ef1f2863dc83276\\GdiPlus.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DWrite.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\WinSxS\\amd64\_microsoft.windows.common-controls\_6595b64144ccf1df\_6.0.26100.7019\_none\_3e06ffa0e335b8a8\\comctl32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\oleaut32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\TextInputFramework.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\CoreMessaging.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\CoreUIComponents.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\TextShaping.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ws2\_32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\mswsock.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.FFMPEG.x64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.FFMPEG.x64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Unloaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.FFMPEG.x64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.FFMPEG.x64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\vcruntime140.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\avformat-57.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\avutil-55.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\avcodec-57.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msvcp140.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\swscale-4.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\secur32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\winmm.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\swresample-2.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\vcruntime140\_1.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\sspicli.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.FFMPEG.x64.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.dll'. 

'TargetServer.exe' (Win32): Unloaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.dll'

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.DirectShow.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.DirectShow.dll'. 

'TargetServer.exe' (Win32): Unloaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.DirectShow.dll'

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.DirectShow.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.dll'. 

'TargetServer.exe' (Win32): Unloaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.dll'

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\sxs.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\clbcatq.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\devenum.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\cfgmgr32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\setupapi.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ntmarta.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\devobj.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\wintrust.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\crypt32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msasn1.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msdmo.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\qcap.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\quartz.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Program Files\\obs-studio\\data\\obs-plugins\\win-dshow\\obs-virtualcam-module64.dll'. Symbols loaded without source information.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\qedit.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\comdlg32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msvfw32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ddraw.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\dxgi.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\dciman32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DXCore.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\powrprof.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\umpdc.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\WindowsCodecs.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

The thread 31232 has exited with code 0 (0x0).

The thread 31572 has exited with code 4294967295 (0xffffffff).

The thread 12388 has exited with code 4294967295 (0xffffffff).

The thread 1056 has exited with code 4294967295 (0xffffffff).

The thread 30472 has exited with code 4294967295 (0xffffffff).

The thread 6600 has exited with code 4294967295 (0xffffffff).

The thread 13756 has exited with code 4294967295 (0xffffffff).

The thread 17180 has exited with code 4294967295 (0xffffffff).

The thread 17144 has exited with code 4294967295 (0xffffffff).

The thread 9040 has exited with code 4294967295 (0xffffffff).

The thread 22616 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (16156) has exited with code 4294967295 (0xffffffff).

The thread 13564 has exited with code 4294967295 (0xffffffff).

The thread 31720 has exited with code 4294967295 (0xffffffff).

The thread 9684 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (19436) has exited with code 4294967295 (0xffffffff).

The thread 21484 has exited with code 4294967295 (0xffffffff).

The thread 31084 has exited with code 4294967295 (0xffffffff).

The thread 6032 has exited with code 4294967295 (0xffffffff).

The thread 31180 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (20572) has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (32112) has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (32080) has exited with code 4294967295 (0xffffffff).

The thread 28628 has exited with code 4294967295 (0xffffffff).

The thread 16716 has exited with code 4294967295 (0xffffffff).

The thread 4204 has exited with code 4294967295 (0xffffffff).

The thread 33508 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (29976) has exited with code 4294967295 (0xffffffff).

The thread 23832 has exited with code 4294967295 (0xffffffff).

The thread 12636 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (8548) has exited with code 4294967295 (0xffffffff).

The thread 32764 has exited with code 4294967295 (0xffffffff).

The thread 20772 has exited with code 4294967295 (0xffffffff).

The thread 7192 has exited with code 4294967295 (0xffffffff).

The program '\[18104\] TargetServer.exe' has exited with code 4294967295 (0xffffffff).

đã sửa và không được

## Prompt:
Tìm dòng có chữ OBS Virtual Camera. ko có dòng chữ này

## Prompt:
'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\TargetServer.exe'. 

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ntdll.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\mscoree.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\kernel32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\KernelBase.dll'. Symbol loading disabled by Include/Exclude setting.

The thread 31552 has exited with code 0 (0x0).

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\advapi32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msvcrt.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\sechost.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\rpcrt4.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\mscoreei.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\shlwapi.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ucrtbase.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\kernel.appcore.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\version.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\clr.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\user32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\win32u.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\vcruntime140\_1\_clr0400.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\gdi32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\vcruntime140\_clr0400.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ucrtbase\_clr0400.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\gdi32full.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msvcp\_win.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\imm32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\combase.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\combase.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\psapi.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\psapi.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\mscorlib\\8967064a93c70884749ad00de74dd7a1\\mscorlib.ni.dll'. 

'TargetServer.exe' (CLR v4.0.30319: DefaultDomain): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_64\\mscorlib\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\mscorlib.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ole32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\combase.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\bcryptprimitives.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\uxtheme.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (CLR v4.0.30319: DefaultDomain): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\TargetServer.exe'. Symbols loaded.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\clrjit.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\System\\22f4d83e48c2201947e262d4bca638b9\\System.ni.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\System.Drawing\\5821108419fb5a77cec19ab38b18df8d\\System.Drawing.ni.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\System.Windows.Forms\\178af1a38c876ea1858e97cb2cacfd71\\System.Windows.Forms.ni.dll'. 

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Windows.Forms\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\System.Windows.Forms.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\System.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Drawing\\v4.0\_4.0.0.0\_\_b03f5f7f11d50a3a\\System.Drawing.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\System.Core\\f61ee525f58db9cd7a10cfcd4d09d809\\System.Core.ni.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\System.Configuration\\fa14af79c42b95ce77c01a830ef23378\\System.Configuration.ni.dll'. 

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Configuration\\v4.0\_4.0.0.0\_\_b03f5f7f11d50a3a\\System.Configuration.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Core\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\System.Core.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\System.Xml\\b0d622690434a583a34bc048e1549b69\\System.Xml.ni.dll'. 

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Xml\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\System.Xml.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\shell32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\WinTypes.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\windows.storage.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\SHCore.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\profapi.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\bcrypt.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\cryptsp.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\rsaenh.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\cryptbase.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\WinSxS\\amd64\_microsoft.windows.common-controls\_6595b64144ccf1df\_5.82.26100.5074\_none\_87eb64a37a300c6e\\comctl32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msctf.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\WinSxS\\amd64\_microsoft.windows.gdiplus\_6595b64144ccf1df\_1.1.26100.7019\_none\_6ef1f2863dc83276\\GdiPlus.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DWrite.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\WinSxS\\amd64\_microsoft.windows.common-controls\_6595b64144ccf1df\_6.0.26100.7019\_none\_3e06ffa0e335b8a8\\comctl32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\oleaut32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\TextInputFramework.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\CoreMessaging.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\CoreUIComponents.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\TextShaping.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ws2\_32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\mswsock.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.FFMPEG.x64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.FFMPEG.x64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Unloaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.FFMPEG.x64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.FFMPEG.x64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\vcruntime140.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\avutil-55.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\avformat-57.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\avcodec-57.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msvcp140.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\swscale-4.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\secur32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\swresample-2.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\winmm.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\vcruntime140\_1.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\sspicli.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.FFMPEG.x64.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.dll'. 

'TargetServer.exe' (Win32): Unloaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.dll'

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\WindowsCodecs.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.DirectShow.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.DirectShow.dll'. 

'TargetServer.exe' (Win32): Unloaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.DirectShow.dll'

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.DirectShow.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.dll'. 

'TargetServer.exe' (Win32): Unloaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.dll'

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\sxs.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\clbcatq.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\devenum.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\cfgmgr32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\setupapi.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ntmarta.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\devobj.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\wintrust.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\crypt32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msasn1.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msdmo.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\qcap.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\quartz.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Program Files\\obs-studio\\data\\obs-plugins\\win-dshow\\obs-virtualcam-module64.dll'. Symbols loaded without source information.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\qedit.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\comdlg32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msvfw32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ddraw.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\dxgi.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\dciman32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\powrprof.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DXCore.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\umpdc.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

The thread 26836 has exited with code 0 (0x0).

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

The thread 33616 has exited with code 0 (0x0).

The thread 9220 has exited with code 0 (0x0).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (31492) has exited with code 0 (0x0).

The thread 4628 has exited with code 4294967295 (0xffffffff).

The thread 30356 has exited with code 4294967295 (0xffffffff).

The thread 33136 has exited with code 4294967295 (0xffffffff).

The thread 12916 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (32940) has exited with code 4294967295 (0xffffffff).

The thread 28728 has exited with code 4294967295 (0xffffffff).

The thread 32008 has exited with code 4294967295 (0xffffffff).

The thread 15104 has exited with code 4294967295 (0xffffffff).

The thread 18476 has exited with code 4294967295 (0xffffffff).

The thread 26368 has exited with code 4294967295 (0xffffffff).

The thread 20912 has exited with code 4294967295 (0xffffffff).

The thread 26884 has exited with code 4294967295 (0xffffffff).

The thread 30340 has exited with code 4294967295 (0xffffffff).

The thread 14460 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (32408) has exited with code 4294967295 (0xffffffff).

The thread 31876 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (33280) has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (30920) has exited with code 4294967295 (0xffffffff).

The thread 10572 has exited with code 4294967295 (0xffffffff).

The thread 16304 has exited with code 4294967295 (0xffffffff).

The thread 32228 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (12152) has exited with code 4294967295 (0xffffffff).

The thread 21704 has exited with code 4294967295 (0xffffffff).

The thread 14668 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (19548) has exited with code 4294967295 (0xffffffff).

The thread 18648 has exited with code 4294967295 (0xffffffff).

The thread 20428 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (30892) has exited with code 4294967295 (0xffffffff).

The thread 20716 has exited with code 4294967295 (0xffffffff).

The thread 13796 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (29320) has exited with code 4294967295 (0xffffffff).

The thread 12276 has exited with code 4294967295 (0xffffffff).

The thread 11036 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (26816) has exited with code 4294967295 (0xffffffff).

The thread 17428 has exited with code 4294967295 (0xffffffff).

The thread 30036 has exited with code 4294967295 (0xffffffff).

The thread 23364 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (6604) has exited with code 4294967295 (0xffffffff).

The thread 10996 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (11244) has exited with code 4294967295 (0xffffffff).

The thread 18304 has exited with code 4294967295 (0xffffffff).

The thread 10792 has exited with code 4294967295 (0xffffffff).

The thread 25764 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (11296) has exited with code 4294967295 (0xffffffff).

The thread 31924 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (33524) has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (31348) has exited with code 4294967295 (0xffffffff).

The thread 33636 has exited with code 4294967295 (0xffffffff).

The thread 31292 has exited with code 4294967295 (0xffffffff).

The thread 14244 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (13388) has exited with code 4294967295 (0xffffffff).

The thread 29508 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (14292) has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (31308) has exited with code 4294967295 (0xffffffff).

The thread 26904 has exited with code 4294967295 (0xffffffff).

The thread 23180 has exited with code 4294967295 (0xffffffff).

The thread 18832 has exited with code 4294967295 (0xffffffff).

The thread 33092 has exited with code 4294967295 (0xffffffff).

The thread 4280 has exited with code 4294967295 (0xffffffff).

The thread 19780 has exited with code 4294967295 (0xffffffff).

The thread 6032 has exited with code 4294967295 (0xffffffff).

The thread 21356 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (33436) has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (18768) has exited with code 4294967295 (0xffffffff).

The thread 27672 has exited with code 4294967295 (0xffffffff).

The thread 24080 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (31568) has exited with code 4294967295 (0xffffffff).

The thread 11592 has exited with code 4294967295 (0xffffffff).

The thread 30768 has exited with code 4294967295 (0xffffffff).

The thread 32460 has exited with code 4294967295 (0xffffffff).

The thread 2688 has exited with code 4294967295 (0xffffffff).

The thread 25744 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (30108) has exited with code 4294967295 (0xffffffff).

The thread 23348 has exited with code 4294967295 (0xffffffff).

The thread 12112 has exited with code 4294967295 (0xffffffff).

The thread 12824 has exited with code 4294967295 (0xffffffff).

The thread 23328 has exited with code 4294967295 (0xffffffff).

The thread 4916 has exited with code 4294967295 (0xffffffff).

The thread 30368 has exited with code 4294967295 (0xffffffff).

The thread 12816 has exited with code 4294967295 (0xffffffff).

The thread 17708 has exited with code 4294967295 (0xffffffff).

The thread 5648 has exited with code 4294967295 (0xffffffff).

The thread 19220 has exited with code 4294967295 (0xffffffff).

The thread 7888 has exited with code 4294967295 (0xffffffff).

The thread 31004 has exited with code 4294967295 (0xffffffff).

The thread 4672 has exited with code 4294967295 (0xffffffff).

The thread 24072 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (33404) has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (27880) has exited with code 4294967295 (0xffffffff).

The thread 27040 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (20200) has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (2400) has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (30116) has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (17496) has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (27872) has exited with code 4294967295 (0xffffffff).

The thread 23912 has exited with code 4294967295 (0xffffffff).

The thread 16256 has exited with code 4294967295 (0xffffffff).

The thread 15320 has exited with code 4294967295 (0xffffffff).

The thread 31352 has exited with code 4294967295 (0xffffffff).

The thread 32356 has exited with code 4294967295 (0xffffffff).

The thread 10744 has exited with code 4294967295 (0xffffffff).

The thread 33336 has exited with code 4294967295 (0xffffffff).

The thread 22404 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (30848) has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (6420) has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (33760) has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (7232) has exited with code 4294967295 (0xffffffff).

The thread 30552 has exited with code 4294967295 (0xffffffff).

The thread 19580 has exited with code 4294967295 (0xffffffff).

The program '\[17304\] TargetServer.exe' has exited with code 4294967295 (0xffffffff).

vẫn bị lỗi

## Prompt:
'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\TargetServer.exe'. 

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ntdll.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\mscoree.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\kernel32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\KernelBase.dll'. Symbol loading disabled by Include/Exclude setting.

The thread 3620 has exited with code 0 (0x0).

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\advapi32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msvcrt.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\sechost.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\rpcrt4.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\mscoreei.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\shlwapi.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ucrtbase.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\kernel.appcore.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\version.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\clr.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\user32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\vcruntime140\_1\_clr0400.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\win32u.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\vcruntime140\_clr0400.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ucrtbase\_clr0400.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\gdi32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\gdi32full.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msvcp\_win.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\imm32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\combase.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\combase.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\psapi.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\psapi.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\mscorlib\\8967064a93c70884749ad00de74dd7a1\\mscorlib.ni.dll'. 

'TargetServer.exe' (CLR v4.0.30319: DefaultDomain): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_64\\mscorlib\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\mscorlib.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ole32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\combase.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\bcryptprimitives.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\uxtheme.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (CLR v4.0.30319: DefaultDomain): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\TargetServer.exe'. Symbols loaded.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\clrjit.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\System\\22f4d83e48c2201947e262d4bca638b9\\System.ni.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\System.Drawing\\5821108419fb5a77cec19ab38b18df8d\\System.Drawing.ni.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\System.Windows.Forms\\178af1a38c876ea1858e97cb2cacfd71\\System.Windows.Forms.ni.dll'. 

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Windows.Forms\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\System.Windows.Forms.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\System.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Drawing\\v4.0\_4.0.0.0\_\_b03f5f7f11d50a3a\\System.Drawing.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\System.Core\\f61ee525f58db9cd7a10cfcd4d09d809\\System.Core.ni.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\System.Configuration\\fa14af79c42b95ce77c01a830ef23378\\System.Configuration.ni.dll'. 

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Configuration\\v4.0\_4.0.0.0\_\_b03f5f7f11d50a3a\\System.Configuration.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Core\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\System.Core.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\assembly\\NativeImages\_v4.0.30319\_64\\System.Xml\\b0d622690434a583a34bc048e1549b69\\System.Xml.ni.dll'. 

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\WINDOWS\\Microsoft.Net\\assembly\\GAC\_MSIL\\System.Xml\\v4.0\_4.0.0.0\_\_b77a5c561934e089\\System.Xml.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\shell32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\WinTypes.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\windows.storage.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\SHCore.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\profapi.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\bcrypt.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\cryptsp.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\rsaenh.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\cryptbase.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\WinSxS\\amd64\_microsoft.windows.common-controls\_6595b64144ccf1df\_5.82.26100.5074\_none\_87eb64a37a300c6e\\comctl32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msctf.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\WinSxS\\amd64\_microsoft.windows.gdiplus\_6595b64144ccf1df\_1.1.26100.7019\_none\_6ef1f2863dc83276\\GdiPlus.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DWrite.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\WinSxS\\amd64\_microsoft.windows.common-controls\_6595b64144ccf1df\_6.0.26100.7019\_none\_3e06ffa0e335b8a8\\comctl32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\oleaut32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\TextInputFramework.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\CoreMessaging.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\CoreUIComponents.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\TextShaping.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ws2\_32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\mswsock.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.FFMPEG.x64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.FFMPEG.x64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Unloaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.FFMPEG.x64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.FFMPEG.x64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\vcruntime140.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\avutil-55.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msvcp140.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\avformat-57.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\swscale-4.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\avcodec-57.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\vcruntime140\_1.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\secur32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\winmm.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\sspicli.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\swresample-2.dll'. Module was built without symbols.

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.FFMPEG.x64.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.dll'. 

'TargetServer.exe' (Win32): Unloaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.dll'

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.DirectShow.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.DirectShow.dll'. 

'TargetServer.exe' (Win32): Unloaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.DirectShow.dll'

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.DirectShow.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.dll'. 

'TargetServer.exe' (Win32): Unloaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.dll'

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\AForge.Video.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\sxs.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\clbcatq.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\devenum.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\cfgmgr32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\setupapi.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ntmarta.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\devobj.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\wintrust.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\crypt32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msasn1.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msdmo.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\qcap.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\quartz.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Program Files\\obs-studio\\data\\obs-plugins\\win-dshow\\obs-virtualcam-module64.dll'. Symbols loaded without source information.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\qedit.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\comdlg32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\msvfw32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\ddraw.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\dxgi.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\dciman32.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\powrprof.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DXCore.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\umpdc.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\WindowsCodecs.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

The thread 31400 has exited with code 0 (0x0).

The thread 18816 has exited with code 0 (0x0).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (33156) has exited with code 0 (0x0).

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'. Symbol loading disabled by Include/Exclude setting.

'TargetServer.exe' (Win32): Loaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'. Module was built without symbols.

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdihk64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\amdxn64.dll'

'TargetServer.exe' (Win32): Unloaded 'C:\\Windows\\System32\\DriverStore\\FileRepository\\u0407959.inf\_amd64\_44b45732b02a83bf\\B406653\\atidx9loader64.dll'

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.dll'. 

'TargetServer.exe' (Win32): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.dll'. 

'TargetServer.exe' (Win32): Unloaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.dll'

'TargetServer.exe' (CLR v4.0.30319: TargetServer.exe): Loaded 'C:\\HK3\\Mạng máy tính\\DO\_AN\\Target\_Server\_CSharp\\TargetServer\\bin\\x64\\Debug\\Accord.Video.dll'. Skipped loading symbols. Module is optimized and the debugger option 'Just My Code' is enabled.

The thread 20288 has exited with code 0 (0x0).

The thread 15444 has exited with code 0 (0x0).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (27160) has exited with code 0 (0x0).

The thread 3808 has exited with code 0 (0x0).

The thread 3780 has exited with code 4294967295 (0xffffffff).

The thread 24360 has exited with code 4294967295 (0xffffffff).

The thread 17456 has exited with code 4294967295 (0xffffffff).

The thread 18660 has exited with code 4294967295 (0xffffffff).

The thread 33072 has exited with code 4294967295 (0xffffffff).

The thread 21964 has exited with code 4294967295 (0xffffffff).

The thread 33000 has exited with code 4294967295 (0xffffffff).

The thread 33008 has exited with code 4294967295 (0xffffffff).

The thread 20484 has exited with code 4294967295 (0xffffffff).

The thread 12308 has exited with code 4294967295 (0xffffffff).

The thread 18772 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (32020) has exited with code 4294967295 (0xffffffff).

The thread 13316 has exited with code 4294967295 (0xffffffff).

The thread 31220 has exited with code 4294967295 (0xffffffff).

The thread 31624 has exited with code 4294967295 (0xffffffff).

The thread 31092 has exited with code 4294967295 (0xffffffff).

The thread '@device:sw:{860BB310-5D01-11D0-BD3B-00A0C911CE86}\\{A3FCE0F5-3493-419F-958A-ABA1250EC20B}' (20520) has exited with code 4294967295 (0xffffffff).

The thread 32920 has exited with code 4294967295 (0xffffffff).

The thread 19448 has exited with code 4294967295 (0xffffffff).

The program '\[19888\] TargetServer.exe' has exited with code 4294967295 (0xffffffff).

vẫn bị lỗi

## Prompt:
để tôi gỡ cài đặt

## Prompt:
nếu vậy sau này tôi muốn quay màn hình lại thì dùng app nào thay thế, nếu bị lỗi nữa thì phải làm sao

## Prompt:
record video xong thì lưu video vô đâu vậy

## Prompt:
> server - CS

> app - PY

> index - HTML

chức năng record không có lấy toàn bộ màn hình quay được, chỉ lấy 1 phần nhỏ trong toàn bộ khung hình, tôi không biết tại sao, hãy giúp tôi sửa chữa lỗi này

## Prompt:
> server - CS

rất tốt là bạn đã tìm ra lỗi, bây giờ tôi sẽ gửi lại file server.cs, bạn hãy giúp tôi hướng dẫn cụ thể từng bước để sửa lỗi này, không chỉ 1 cách trừu tượng, tôi cần tường minh cụ thể

## Prompt:
BƯỚC 2: Thay thế hàm StartRecording

Bạn tìm đến hàm StartRecording (khoảng dòng 198 đến 212).

Hãy XÓA BỎ toàn bộ nội dung cũ của hàm đó và DÁN đoạn code mới này vào.

Mục đích: Hàm này bây giờ chỉ làm nhiệm vụ đặt tên file và bật công tắc "đang ghi", chứ chưa mở file ngay (vì chưa biết kích thước ảnh).

BƯỚC 3: Thay thế hàm video\_NewFrame (QUAN TRỌNG NHẤT)

Đây là nơi chúng ta sửa lỗi cắt hình. Bạn tìm hàm video\_NewFrame (khoảng dòng 215 đến 255).

Hãy XÓA BỎ toàn bộ hàm cũ và DÁN đoạn code mới này vào.

Mục đích: Khi nhận được tấm ảnh đầu tiên từ Camera, code sẽ đo chiều rộng/cao của nó (image.Width, image.Height) rồi mới tạo file video đúng kích thước đó. đoạn code đó ở đâu, tôi chưa có thấy

## Prompt:
bây giờ, tôi muốn lưu các ảnh chụp màn hình khi máy client nhấn screenshot và những video khi record ở một folder cụ thể, không ở trong bin/x64 nữa, và làm sao máy client có thể truy cập được folder này, bạn hãy gợi ý cho tôi cách làm

## Prompt:
khoan, ở bước này có xuất trực tiếp file video ở định dạng quen thuộc là mp4 được không string fileName = "Record\_" + DateTime.Now.ToString("yyyyMMdd\_HHmmss") + ".avi";

## Prompt:
khoan, tôi mới chỉ làm bước 1, chưa làm bước 2, hãy làm lại từ đầu từ bước 2 chứ không phải chỉ nói về đổi đuôi thành mp4, và hiện tại, chức năng download file bạn chưa viết đúng không, và những bức ảnh screenshot khi máy client chụp bạn cũng chưa sửa code để nó lưu vào dataFolder đúng không

## Prompt:
> app - PY

> index - HTML

ok, bây giờ hãy làm bước 4, và chỉnh sửa luôn file index.html và file app.py của tôi, để tôi gửi lại cho bạn các file này

## Prompt:
> ![Preview Image](https://lh3.googleusercontent.com/gg/AIJ2gl8EOj19g90KKFyNNZIgHN8HQvvyfs5fvRswBKytmuNVNQ4fuRk7MkOWFh29SQFgwLx0rBrfHY8ZQlb1IRHOt-qqx7LDt1ORg0qjCjqrkdoXBTwejql-_wefsOE0TaLbMNitkEH_FpZT4op6SOGt47k0-De-8P_g9xDewL8d4vPA38172U7DDipgidN0ez2GL-UxQIuymMfgxAC3OQRSx-ChIAQQ7HzeVHYmIPSvGMxGa0KGHSVILa9jHX1u3G3kdr7oS8xCuZoGa_tfXWgYRLfqyvyqRUlRReg)

> server - CS

> app - PY

khi nhấn start stream thì không bị lỗi, nhưng khi tôi nhấn record thì bị lỗi, hãy giúp tôi fix lại lỗi này, đây là file server.cs khi bị lỗi

## Prompt:
> ![Preview Image](https://lh3.googleusercontent.com/gg/AIJ2gl_SsXoWHK8vVioSuVsuMvutXpr84VN0A-rEcG8tOoAsA2UEa_ry60X4bvddSR2jD_kNL1vLbJxLsDgokfkARQYBKBWkN-5YzKhFMUu3YaOelS5cucf_dt1bpQl3MOQ_twSJd6Nwml8RRBJUlKB-IZGw9r8y-p7rBk7fYOQc6uHe2sjz4AaOk4GQB05OzSgQqJrxhRExuN18U3PKOiiYAUk9OV8W6eRhdUFomssb9X_4H7okXcf_Wm3RNMla0koWMEKf9Uhxx9jIzDAJl21ps6MqRgzY-TdaWLs)

vẫn bị lỗi

## Prompt:
> server - CS

hãy đọc lại file, chắc chắn sửa đúng lỗi cho tôi

## Prompt:
> ![Preview Image](https://lh3.googleusercontent.com/gg/AIJ2gl9cZHtESGHbaA03cmzT0-QDP0k8XGxcpRIXLx6BZ5Ax8RgyflXbNGvCf73X3n-mQ0KbxpCz8R-ZFU1VIHNKRTUplnTyLXwn2y7Ly0lu_eJmH25h8oitZbp1qt2GhALDN0kKkGc8SbzIh5tQDwXtmpe48GqxwMPICkT593a5SHPQETDzMLG_tEHZ80tTmJTbcviT5ux1FT8qVaZTQwSbDGW2AZtmSRc_Vuvt4RgWCsUXjjyF-BVQB9dTGAJeSvVm8B5CDuuSAkRYGDFedg32ndbaJZJvrMi0Tw)

vẫn bị lỗi ở hàm videoFram

## Prompt:
> ![Preview Image](https://lh3.googleusercontent.com/gg/AIJ2gl_UtdTQlzh0JfuH8V4D_ssbE9U0Zlz7zdTIs36X-_NzfsZtLEJJNStHkVRFYPzZ_pmzdYov2lerdqhVTNcRsX1AYtE7IpfX9F9FMPQdQdqvf8h_ZUzogsCTSCsGhDhrprGtbC445RYjWWxsDjMdjKmZVN8o2OsHjHPIB_qH1OiRKu9RoF1DBfUVnUROusvvCr7A_X74khbKzec0KXLtEu5-uqnLRlkPIPpa111g639vZrXy-wZM3H4gvpTnPXC8UKZCu4f_1iUixfWG1mtqWicQ8W8XjtOzVdE)

có phải lý do là đã chuyển đổi qua mp4 không, nếu vậy thì tôi không cần chuyển đổi nữa

## Prompt:
> ![Preview Image](https://lh3.googleusercontent.com/gg/AIJ2gl-cEKKIDK9r7-EPYF9l9wuRhw_yNhJYwtrb9Rhn0QaaJMBzK521k053wSVrMJB3-cXHG7qliDTzXhzVSLJ2GU_RYlDfxkVpppJPJcbd9gdc7BdkdNoA-IZJ2yLbyD7laTf7P9-aEFZl4lCCy9YlisYqSBQXJkYrbjx0bmoRcRQZhvCXBwV81hqfW0YLCA0EBen2NI0tybeuj9-qlTjEnzO1vNopN1d3AhFAxtO1K9LGs0YSc7tX7F-d8GMccn_3ACeXcsDsh9Xl5hKB9g-Y0wXdm2z-JspDY8k)

> server - CS

> app - PY

> index - HTML

ok bây giờ đã quay video được rồi, nhưng mà khi tôi nhấn nút refresh list ở ở file manager này thì nó hiện dòng chữ màu đỏ như trong ảnh và tôi không thể tải về được, hãy kiểm tra lại logic, tôi sẽ gửi lại cho bạn 3 files quan trọng là app.py và server.cs và index.html

## Prompt:
nếu sửa dòng này như vậy thì code có cần có thể mở rộng thêm nhiều chức năng khác được hay không if command\_type not in \["WEBCAM", "FILE"\]:

writer.write(f"{command\_type}\\n")

writer.flush(), lưu ý là tôi đang hỏi chứ chưa thực hiện bước sửa nào của bạn

## Prompt:
tôi đã sửa theo lời bạn nói nhưng chỉ trong file app.py, vậy còn trong file server.cs thì có còn sửa gì không

## Prompt:
không, chỉ cần sửa chỗ nào hay thêm chỗ nào thì nói tôi thêm chỗ đó, ko được xóa toàn bộ file và tải lại

## Prompt:
> ![Preview Image](https://lh3.googleusercontent.com/gg/AIJ2gl-9mv5wdJk1PQ-pzUSRrd-7U-exiWlxWD6GcczV1vUIvLY2PN4NKomrrZY7_TshWqXulEWFxKBvKJFZ1oeiZCYwmR6-dEtmqwCfsl3zbq1Rb3YXkn1145D0f5aWdGenzF8hLGDXvvR8h9NQcL87cFKDoaI-Q-xRKHcsXWvSyIf4O_5U6Pr5ynHM5WBZZKu1U6u4oQnCCetvR4bFgQcD7CYTJMWryVXMSY11w0bNff55GDEUZYVBFmaR75e66qRExX3kRCYHkiQ6WIhhitRr3jlFpr-yEiDW1lo)

> server - CS

khi tôi nhấn stop record thì bị lỗi này, hãy đọc lại file server.cs này 1 cách cẩn thận, tôi thấy bạn đã sửa lại những chỗ mà trước đó tôi đã sửa, đó là điều không cần thiết

## Prompt:
> ![Preview Image](https://lh3.googleusercontent.com/gg/AIJ2gl-HX-dGwwWjODTe6qJI0PQrUDrSsXuJrStjyLYcXoTOPP6PDTv465wkYCDwN2v9GdnXBdrK9e4vdSpdhpVuANui_7yk7Ww7vlf6SugWlMd7DOAiWWeJi-atExSQ-oW00Bu_4x4Nj6Lly_4ebzXirhH1tHFG4gRFHSVA76_LXZa-60zcLLusaMe2tYNs9VHQ_52x87XtxluGmxxgEEC6ZrFfiC_THq28vGttEJIJ-Mgr08t76aNoVp9qmuoQK3tayALChN2mEnUMNpkHsthPxvr9V1qZq28lq-A)

vẫn bị lỗi

## Prompt:
bây giờ bạn có đề xuất, thêm chức năng gì cho đồ án này không, liệt kê 1 số chức năng hay, khả thi cho đồ án RAT client-server này cho tôi

## Prompt:
> app - PY

> server - CS

ok, bây giờ hãy giúp tôi làm nâng cấp chế độ upload và delete file Manager trước, tôi sẽ gửi lại cho bạn thật kĩ 2 files quan trọng đó là server.cs và app.py, sau khi chỉnh sửa, bổ sung các file này xong thì mới chỉnh sửa file index.html

## Prompt:
không cần phải download package hay thư viện gì mới hết đúng không, hơn thế nữa tôi còn có một đề xuất khác, đó là mình nên tạo 1 chức năng xem các folders có trong từng các ổ đĩa, sau đó mới upload file của mình lên và gõ luôn địa chỉ mà mình muốn file của mình lưu vào máy server ở đâu, và xóa file thì client cần nhập địa chỉ của file mà mình cần xóa, nhập ở html

## Prompt:
khoan, nếu sửa như bạn thì tôi đã mất chức năng download rồi, tôi nghĩ nên bây giờ mình có thể sửa thành như bạn nói, nhưng hãy lưu các ảnh đã chụp màn hình và record và thư mục Rat\_data rồi có thêm chức năng download, nhưng với chức năng download này thì có thể download bất kì file nào trong máy tính. Nhưng tôi cần thêm chức năng đó là "xem các thư mục hiện có trong máy tính" vì giả sử như client không biết cấu trúc tổ chức tệp tin trong máy tính. tôi cần code thật cẩn thận, chi tiết cụ thể cho tôi

## Prompt:
> server - CS

> app - PY

> index - HTML

hãy xem lại 3 files quan trọng này, vì tôi thấy có nhiều chỗ bạn sửa hơi trùng lặp, xem các files thật cẩn thận, tỉ mỉ từng tí cho tôi

## Prompt:
> ![Preview Image](https://lh3.googleusercontent.com/gg/AIJ2gl-wOektO8eHFos4wN1TP0fNiG0Sy1GU4i0OMtHPttZkw11zIKvA0Squujyt8lcFG9HZtEoa9MsfNr8BiYbeX_zsBNw9CB4yobHXpU69np70FJCeF05qFlB75Xq8Wu2O40P1k1e7MAMcCztk1bz_Physcx0KNdLX-oTLoF11w_PS4giv7FkkHWCOJsZqjjhMC4JIgmiW8BtVSQMB7mhjYU3HBmyIu3dUaYEmjkm6ZHLOucKz1m__FRT5qzeTuBHUdUUDCdgCTSLbxCDtznJXxO1tJrmf5QI9utw)

## Prompt:
case "KEYLOG": keylog(); break;

case "PROCESS": process(); break;

case "APPLICATION": application(); break;

case "TAKEPIC": takepic(); break;

case "SHUTDOWN": System.Diagnostics.Process.Start("ShutDown", "-s"); break;

case "RESTART": System.Diagnostics.Process.Start("shutdown", "/r /t 0"); break;

// --- NHÓM LỆNH WEBCAM (MỞ RỘNG DỄ DÀNG) ---

// Nếu sau này bạn muốn thêm tính năng "ZOOM", chỉ cần thêm case "WEBCAM\_ZOOM"

case "WEBCAM\_START":

    isStreaming = true;

    StartWebcam();

    Program.nw.WriteLine("Webcam Started"); // Phản hồi cho Python

    Program.nw.Flush();

    break;

case "WEBCAM\_STOP":

    isStreaming = false;

    isRecording = false;

    StopWebcam();

    Program.nw.WriteLine("Webcam Stopped"); // Phản hồi

    Program.nw.Flush();

    break;

case "WEBCAM\_RECORD\_ON":

    StartRecording();

    Program.nw.WriteLine("Recording Started"); // Phản hồi

    Program.nw.Flush();

    break;

case "WEBCAM\_RECORD\_OFF":

    // 1. Ngắt cờ ghi hình trước

    isRecording = false;

    // 2. QUAN TRỌNG: Tạm dừng 100ms để luồng Camera (video\_NewFrame) kịp nhả file ra

    // Nếu không có dòng này, lệnh Close() bên dưới sẽ đụng độ với lệnh Write() đang chạy dở -\> Sập

    Thread.Sleep(100);

    // 3. Đóng và Hủy biến writer an toàn

    if (writer != null)

    {

        try

        {

            // Dù writer đang mở hay đóng cũng cố gắng Dispose sạch sẽ

            writer.Close();

            writer.Dispose();

        }

        catch { }

        // 4. BẮT BUỘC: Gán về null để hàm StartRecording lần sau biết đường tạo mới

        // Nếu thiếu dòng này, lần quay sau sẽ báo lỗi "Cannot access a disposed object"

        writer = null;

    }

    Program.nw.WriteLine("Recording Saved");

    Program.nw.Flush(); // Đảm bảo gửi tin nhắn về Python ngay

    break;

// --- TRÌNH DUYỆT FILE & Ổ ĐĨA (NÂNG CẤP) ---

case "GET\_FILES":

    try

    {

        string path = Program.nr.ReadLine(); // Đọc đường dẫn Client gửi lên

        List\<string\> items = new List\<string\>();

        // Nếu path là "ROOT" hoặc rỗng -\> Lấy danh sách ổ đĩa

        if (string.IsNullOrEmpty(path) || path == "ROOT")

        {

            DriveInfo\[\] drives = DriveInfo.GetDrives();

            foreach (DriveInfo d in drives)

            {

                if (d.IsReady) items.Add(\$"\[DRIVE\]|{d.Name}|{d.TotalSize}");

            }

        }

        else if (Directory.Exists(path)) // Nếu là thư mục -\> Lấy nội dung

        {

            // 1. Lấy danh sách Thư mục con

            string\[\] dirs = Directory.GetDirectories(path);

            foreach (string d in dirs) items.Add(\$"\[FOLDER\]|{Path.GetFileName(d)}|0");

            // 2. Lấy danh sách File

            string\[\] files = Directory.GetFiles(path);

            foreach (string f in files)

            {

                FileInfo fi = new FileInfo(f);

                items.Add(\$"\[FILE\]|{Path.GetFileName(f)}|{fi.Length}");

            }

        }

        // Gửi về Client

        Program.nw.WriteLine(items.Count.ToString());

        Program.nw.Flush();

        foreach (string item in items) { Program.nw.WriteLine(item); Program.nw.Flush(); }

    }

    catch { Program.nw.WriteLine("0"); Program.nw.Flush(); } // Gửi 0 nếu lỗi truy cập

    break;

case "DELETE\_FILE":

    try

    {

        string targetPath = Program.nr.ReadLine(); // Đọc đường dẫn đầy đủ

        if (File.Exists(targetPath))

        {

            File.Delete(targetPath);

            Program.nw.WriteLine("Đã xóa file.");

        }

        else if (Directory.Exists(targetPath))

        {

            Directory.Delete(targetPath, true); // Xóa thư mục

            Program.nw.WriteLine("Đã xóa thư mục.");

        }

        else Program.nw.WriteLine("Đường dẫn không tồn tại.");

        Program.nw.Flush();

    }

    catch (Exception ex) { Program.nw.WriteLine("Lỗi: " + ex.Message); Program.nw.Flush(); }

    break;

case "DOWNLOAD\_FILE":

    try

    {

        string fullPath = Program.nr.ReadLine(); // Đọc đường dẫn đầy đủ

        if (File.Exists(fullPath))

        {

            FileInfo fi = new FileInfo(fullPath);

            Program.nw.WriteLine(fi.Length.ToString());

            Program.nw.Flush();

            Program.client.SendFile(fullPath);

        }

        else { Program.nw.WriteLine("0"); Program.nw.Flush(); }

    }

    catch { Program.nw.WriteLine("0"); Program.nw.Flush(); }

    break; sửa toàn bộ chỗ này thành từng hàm để cho dễ module cho tôi như nhưng cái này public void application() { ProcessHandler("App"); }

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

            Process\[\] pr = Process.GetProcesses();

            List\<Process\> filteredList = new List\<Process\>();

            foreach (Process p in pr)

            {

                // Nếu mode là App thì chỉ lấy cửa sổ có tiêu đề

                if (mode == "All" || p.MainWindowTitle.Length \> 0) filteredList.Add(p);

            }

            // Sắp xếp danh sách

            if (mode == "App") filteredList = filteredList.OrderBy(p =\> p.MainWindowTitle).ToList();

            else filteredList = filteredList.OrderBy(p =\> p.ProcessName).ToList();

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

                    Program.nw.WriteLine(\$"Successfully killed: {pName} (ID: {id})");

                }

                catch (Exception ex) { Program.nw.WriteLine("Failed: " + ex.Message.Replace("\\n", " ")); }

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

                catch (Exception ex) { Program.nw.WriteLine("Failed: " + ex.Message.Replace("\\n", " ")); }

                Program.nw.Flush();

            }

        }

    }

}



---
Powered by [Gemini Exporter](https://www.ai-chat-exporter.com)