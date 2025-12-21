using System;
using System.IO;
using System.Net.Sockets;
using System.Windows.Forms;

namespace ServerApp
{
    static class Program
    {
        // ==================== GLOBAL SOCKET VARIABLES ====================
        // Các biến Socket toàn cục để chia sẻ kết nối giữa các Form/Lớp

        static public Socket server;
        static public Socket client;
        static public NetworkStream ns;
        static public StreamReader nr;
        static public StreamWriter nw;

        // ==================== ENTRY POINT ====================

        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new server());
        }
    }
}