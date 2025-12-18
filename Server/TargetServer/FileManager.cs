using System;
using System.IO;
using System.Text;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms; // Thêm cái này để dùng Application.StartupPath nếu cần

namespace ServerApp
{
    public class FileManager
    {
        // Giao thức trả về: "TYPE|NAME|SIZE_OR_INFO"
        // TYPE: "DRIVE", "DIR", "FILE", "ERROR", "OK"

        public void HandleFileCommand()
        {
            string cmd = "";
            while (true)
            {
                // --- SỬA LỖI Ở ĐÂY: Đọc trực tiếp từ NetworkReader thay vì gọi hàm receiveSignal ---
                try
                {
                    cmd = Program.nr.ReadLine();
                    if (cmd == null) cmd = "QUIT";
                }
                catch { cmd = "QUIT"; }
                // --------------------------------------------------------------------------------

                if (cmd == "QUIT") return;

                try
                {
                    switch (cmd)
                    {
                        case "GET_DRIVES":
                            SendDrives();
                            break;

                        case "GET_DIR":
                            string path = Program.nr.ReadLine(); // Nhận đường dẫn
                            SendDirectory(path);
                            break;

                        case "DELETE":
                            string pathDel = Program.nr.ReadLine();
                            DeleteFileOrFolder(pathDel);
                            break;

                        case "DOWNLOAD":
                            string pathDown = Program.nr.ReadLine();
                            SendFile(pathDown);
                            break;
                    }
                }
                catch (Exception ex)
                {
                    // Gửi lỗi về để Client không bị treo
                    try
                    {
                        Program.nw.WriteLine("ERROR");
                        Program.nw.WriteLine(ex.Message);
                        Program.nw.Flush();
                    }
                    catch { }
                }
            }
        }

        private void SendDrives()
        {
            try
            {
                DriveInfo[] allDrives = DriveInfo.GetDrives();
                Program.nw.WriteLine(allDrives.Length.ToString()); // Gửi số lượng
                Program.nw.Flush();

                foreach (DriveInfo d in allDrives)
                {
                    if (d.IsReady)
                    {
                        // Format: "C:\|Fixed|100GB Free"
                        string info = $"{d.Name}|{d.DriveType}|{FormatSize(d.TotalFreeSpace)} free of {FormatSize(d.TotalSize)}";
                        Program.nw.WriteLine(info);
                    }
                    else
                    {
                        Program.nw.WriteLine($"{d.Name}|{d.DriveType}|Not Ready");
                    }
                    Program.nw.Flush();
                }
            }
            catch (Exception ex) { Error(ex.Message); }
        }

        private void SendDirectory(string path)
        {
            try
            {
                if (!Directory.Exists(path))
                {
                    Program.nw.WriteLine("0"); // Gửi 0 item nếu lỗi
                    Program.nw.Flush();
                    return;
                }

                DirectoryInfo di = new DirectoryInfo(path);
                DirectoryInfo[] dirs = di.GetDirectories();
                FileInfo[] files = di.GetFiles();
                int total = dirs.Length + files.Length;

                Program.nw.WriteLine(total.ToString());
                Program.nw.Flush();

                // Gửi danh sách Folder trước
                foreach (var d in dirs)
                {
                    // Format: "DIR|FolderName|CreateDate"
                    Program.nw.WriteLine($"DIR|{d.Name}|{d.CreationTime}");
                    Program.nw.Flush();
                }

                // Gửi danh sách File sau
                foreach (var f in files)
                {
                    // Format: "FILE|FileName|SizeString"
                    Program.nw.WriteLine($"FILE|{f.Name}|{FormatSize(f.Length)}");
                    Program.nw.Flush();
                }
            }
            catch { Program.nw.WriteLine("0"); Program.nw.Flush(); }
        }

        private void DeleteFileOrFolder(string path)
        {
            try
            {
                if (File.Exists(path))
                {
                    File.Delete(path);
                    Program.nw.WriteLine("SUCCESS");
                    Program.nw.WriteLine("Deleted File successfully");
                }
                else if (Directory.Exists(path))
                {
                    Directory.Delete(path, true); // True = xóa đệ quy
                    Program.nw.WriteLine("SUCCESS");
                    Program.nw.WriteLine("Deleted Folder successfully");
                }
                else
                {
                    Program.nw.WriteLine("ERROR");
                    Program.nw.WriteLine("Path not found");
                }
            }
            catch (Exception ex)
            {
                Program.nw.WriteLine("ERROR");
                Program.nw.WriteLine(ex.Message);
            }
            Program.nw.Flush();
        }

        private void SendFile(string path)
        {
            try
            {
                if (!File.Exists(path))
                {
                    Program.nw.WriteLine("0"); // File không tồn tại hoặc size = 0
                    Program.nw.Flush();
                    return;
                }

                // Đọc file thành byte array
                byte[] data = File.ReadAllBytes(path);
                Program.nw.WriteLine(data.Length.ToString()); // Gửi kích thước
                Program.nw.Flush();

                // Gửi Binary qua socket
                Program.client.Send(data);
            }
            catch
            {
                Program.nw.WriteLine("0");
                Program.nw.Flush();
            }
        }

        private void Error(string msg)
        {
            try
            {
                Program.nw.WriteLine("0");
                Program.nw.Flush();
            }
            catch { }
        }

        // Helper format dung lượng (Bytes -> KB, MB)
        private string FormatSize(long bytes)
        {
            string[] suffixes = { "B", "KB", "MB", "GB", "TB" };
            int counter = 0;
            decimal number = (decimal)bytes;
            while (Math.Round(number / 1024) >= 1)
            {
                number = number / 1024;
                counter++;
            }
            return string.Format("{0:n1} {1}", number, suffixes[counter]);
        }
    }
}