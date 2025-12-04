using System;
using System.Windows.Forms;

namespace ServerApp
{
    static class Program
    {
        // Các biến Socket toàn cục để chia sẻ kết nối giữa các Form/Lớp
        static public System.Net.Sockets.Socket server;
        static public System.Net.Sockets.Socket client;
        static public System.Net.Sockets.NetworkStream ns;
        static public System.IO.StreamReader nr;
        static public System.IO.StreamWriter nw;

        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new server());
        }
    }
}