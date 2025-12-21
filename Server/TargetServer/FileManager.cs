using System;
using System.IO;
using System.Windows.Forms;

namespace ServerApp
{
    /// <summary>
    /// FileManager - Xử lý các lệnh quản lý file từ Client
    /// Giao thức trả về: "TYPE|NAME|SIZE_OR_INFO"
    /// TYPE: "DRIVE", "DIR", "FILE", "ERROR", "OK"
    /// </summary>
    public class FileManager
    {
        // ==================== MAIN HANDLER ====================

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

        // ==================== DRIVE OPERATIONS ====================

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

        // ==================== DIRECTORY OPERATIONS ====================

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
            catch
            {
                Program.nw.WriteLine("0");
                Program.nw.Flush();
            }
        }

        // ==================== FILE OPERATIONS ====================

        private void DeleteFileOrFolder(string path)
        {
            try
            {
                bool isFile = File.Exists(path);
                bool isDir = Directory.Exists(path);
                
                if (isFile) File.Delete(path);
                else if (isDir) Directory.Delete(path, true);
                
                Program.nw.WriteLine(isFile || isDir ? "SUCCESS" : "ERROR");
                Program.nw.WriteLine(isFile ? "Deleted File successfully" : 
                                     isDir ? "Deleted Folder successfully" : "Path not found");
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

        // ==================== HELPER FUNCTIONS ====================

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