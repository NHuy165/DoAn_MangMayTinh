using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Threading;
using System.Windows.Forms;

using Accord.Video.FFMPEG;

namespace ScreenRecorder
{
    /// <summary>
    /// ScreenCapture - Chụp và ghi video màn hình
    /// Hỗ trợ: Live Streaming và Recording
    /// </summary>
    public class ScreenCapture
    {
        // ==================== STATIC FIELDS ====================

        // Thư mục lưu video tạm
        public static string outputFolder = Path.Combine(Path.GetTempPath(), "screen_recordings");
        public static string currentVideoPath = "";

        // ==================== PRIVATE FIELDS ====================

        // Thread và Writer
        private Thread captureThread;
        private VideoFileWriter videoWriter;
        private Bitmap currentFrame;

        // Khóa luồng (Locks)
        private object frameLock = new object();
        private object videoWriteLock = new object();

        // Biến trạng thái
        private volatile bool isRecording = false;
        private volatile bool isStreaming = false;

        // Thông số màn hình
        private int screenWidth;
        private int screenHeight;

        // Recording metadata
        private DateTime recordingStartTime;

        // ==================== CONSTANTS ====================

        private const int INTERVAL = 100;           // 100ms = 10 FPS (Đủ mượt cho Remote, nhẹ máy)
        private const int VIDEO_BITRATE = 1000000;  // 1 Mbps

        // ==================== CONSTRUCTOR ====================

        public ScreenCapture()
        {
            // Tạo thư mục nếu chưa có
            if (!Directory.Exists(outputFolder)) Directory.CreateDirectory(outputFolder);

            // Lấy độ phân giải màn hình máy thầy/máy server
            Rectangle bounds = Screen.PrimaryScreen.Bounds;
            screenWidth = bounds.Width;
            screenHeight = bounds.Height;
        }

        // ==================== STREAMING METHODS ====================

        public string StartStream()
        {
            try
            {
                if (isStreaming) return "ERROR: Stream already active";

                isStreaming = true;

                // Tạo luồng riêng để chụp màn hình liên tục
                captureThread = new Thread(CaptureLoop);
                captureThread.IsBackground = true; // Tự tắt khi tắt app
                captureThread.Start();

                return "STREAM_ON";
            }
            catch (Exception ex) { return "ERROR: " + ex.Message; }
        }

        public string StopStream()
        {
            try
            {
                if (isRecording) StopRecording();

                isStreaming = false; // Đặt cờ false để vòng lặp tự thoát

                // Đợi luồng tắt hẳn (timeout 0.5s)
                if (captureThread != null && captureThread.IsAlive)
                {
                    captureThread.Join(500);
                }
                captureThread = null;

                // Dọn dẹp bộ nhớ
                lock (frameLock)
                {
                    if (currentFrame != null) { currentFrame.Dispose(); currentFrame = null; }
                }

                return "STREAM_OFF";
            }
            catch (Exception ex) { return "ERROR: " + ex.Message; }
        }

        // Vòng lặp chụp màn hình (Thay thế cho AForge)
        private void CaptureLoop()
        {
            while (isStreaming)
            {
                try
                {
                    // 1. Tạo ảnh trống kích thước màn hình
                    Bitmap bmp = new Bitmap(screenWidth, screenHeight);

                    // 2. Chụp màn hình đè vào ảnh đó
                    using (Graphics g = Graphics.FromImage(bmp))
                    {
                        g.CopyFromScreen(0, 0, 0, 0, new Size(screenWidth, screenHeight));
                    }

                    // 3. Xử lý ảnh (Lưu preview và ghi video)
                    ProcessFrame(bmp);

                    // 4. Nghỉ 100ms
                    Thread.Sleep(INTERVAL);
                }
                catch
                {
                    // Bỏ qua frame lỗi
                }
            }
        }

        private void ProcessFrame(Bitmap bmp)
        {
            try
            {
                Bitmap videoFrame = null;
                lock (frameLock)
                {
                    if (currentFrame != null) currentFrame.Dispose();
                    currentFrame = (Bitmap)bmp.Clone(); // Clone cho Live View

                    if (isRecording) videoFrame = (Bitmap)bmp.Clone(); // Clone cho Record
                }

                bmp.Dispose(); // Xóa ảnh gốc

                if (videoFrame != null)
                {
                    lock (videoWriteLock)
                    {
                        if (isRecording && videoWriter != null && videoWriter.IsOpen)
                        {
                            try { videoWriter.WriteVideoFrame(videoFrame); } catch { }
                        }
                    }
                    videoFrame.Dispose();
                }
            }
            catch { }
        }

        public byte[] GetCurrentFrameAsJpeg()
        {
            try
            {
                lock (frameLock)
                {
                    if (currentFrame == null) return null;
                    using (MemoryStream ms = new MemoryStream())
                    {
                        currentFrame.Save(ms, ImageFormat.Jpeg);
                        return ms.ToArray();
                    }
                }
            }
            catch { return null; }
        }

        // ==================== RECORDING METHODS ====================

        public string StartRecording()
        {
            try
            {
                if (!isStreaming) return "ERROR: Stream not ON";
                if (isRecording) return "ERROR: Already recording";

                string timestamp = DateTime.Now.ToString("yyyyMMdd_HHmmss");
                currentVideoPath = Path.Combine(outputFolder, $"screen_{timestamp}.avi");

                lock (videoWriteLock)
                {
                    videoWriter = new VideoFileWriter();

                    // Accord bắt buộc width/height phải là số chẵn
                    int w = screenWidth % 2 == 0 ? screenWidth : screenWidth - 1;
                    int h = screenHeight % 2 == 0 ? screenHeight : screenHeight - 1;

                    // Mở file video
                    videoWriter.Open(currentVideoPath, w, h, 1000 / INTERVAL, VideoCodec.MPEG4, VIDEO_BITRATE);
                }

                isRecording = true;
                recordingStartTime = DateTime.Now;

                return "RECORDING_STARTED";
            }
            catch (Exception ex)
            {
                isRecording = false;
                // Cleanup nếu lỗi
                lock (videoWriteLock)
                {
                    if (videoWriter != null) { videoWriter.Dispose(); videoWriter = null; }
                }
                return "ERROR: " + ex.Message;
            }
        }

        public string StopRecording()
        {
            try
            {
                if (!isRecording) return "ERROR: Not recording";

                isRecording = false;
                Thread.Sleep(500); // Chờ ghi nốt frame cuối

                lock (videoWriteLock)
                {
                    if (videoWriter != null)
                    {
                        if (videoWriter.IsOpen) videoWriter.Close();
                        videoWriter.Dispose();
                        videoWriter = null;
                    }
                }

                int durationSeconds = (int)(DateTime.Now - recordingStartTime).TotalSeconds;

                if (File.Exists(currentVideoPath))
                {
                    long fileSize = new FileInfo(currentVideoPath).Length;
                    return $"RECORDING_STOPPED|{Path.GetFileName(currentVideoPath)}|{fileSize}|{durationSeconds}";
                }

                return "RECORDING_STOPPED||0|0";
            }
            catch (Exception ex) { return "ERROR: " + ex.Message; }
        }

        // ==================== STATUS & UTILITY METHODS ====================

        public string GetStatus()
        {
            return $"stream_on:{isStreaming.ToString().ToLower()}|recording:{isRecording.ToString().ToLower()}";
        }

        public byte[] GetVideoBytes(string filename)
        {
            try
            {
                string filePath = Path.Combine(outputFolder, filename);
                if (File.Exists(filePath)) return File.ReadAllBytes(filePath);
                return null;
            }
            catch { return null; }
        }
    }
}