using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Threading;
using AForge.Video;
using AForge.Video.DirectShow;
using Accord.Video.FFMPEG;

namespace WebcamRecorder
{
    public class WebcamCapture
    {
        // Thư mục lưu video tạm
        public static string outputFolder = Path.Combine(Path.GetTempPath(), "webcam_recordings");
        public static string currentVideoPath = "";

        private VideoCaptureDevice videoSource;
        private VideoFileWriter videoWriter;
        private Bitmap currentFrame;

        // --- CÁC BIẾN KHÓA (LOCK) ĐỂ TRÁNH XUNG ĐỘT ---
        private object frameLock = new object();      // Khóa khi truy cập ảnh hiện tại
        private object videoWriteLock = new object(); // Khóa riêng cho việc ghi video

        private volatile bool isRecording = false;
        private bool isCameraOn = false;

        // --- BIẾN LƯU KÍCH THƯỚC THẬT CỦA CAMERA ---
        // Quan trọng: Phải lưu lại kích thước thật để tạo video đúng kích thước đó
        private int actualWidth = 640;
        private int actualHeight = 480;

        private const int TARGET_FPS = 25;     // 25 FPS là chuẩn an toàn cho webcam
        private const int VIDEO_BITRATE = 1000000; // 1 Mbps (Đủ nét, file nhẹ, không lag mạng)

        public WebcamCapture()
        {
            if (!Directory.Exists(outputFolder)) Directory.CreateDirectory(outputFolder);
        }

        public string TurnOn()
        {
            try
            {
                if (isCameraOn) return "ERROR: Camera is already ON";

                FilterInfoCollection videoDevices = new FilterInfoCollection(FilterCategory.VideoInputDevice);
                if (videoDevices.Count == 0) return "ERROR: No camera found";

                videoSource = new VideoCaptureDevice(videoDevices[0].MonikerString);

                // --- TỰ ĐỘNG CHỌN ĐỘ PHÂN GIẢI PHÙ HỢP ---
                // Ưu tiên chọn độ phân giải gần 640x480 nhất để nhẹ mạng LAN
                if (videoSource.VideoCapabilities.Length > 0)
                {
                    var capability = videoSource.VideoCapabilities
                        .OrderBy(c => Math.Abs(c.FrameSize.Width - 640))
                        .First();

                    videoSource.VideoResolution = capability;

                    // CẬP NHẬT KÍCH THƯỚC THẬT VÀO BIẾN
                    actualWidth = capability.FrameSize.Width;
                    actualHeight = capability.FrameSize.Height;
                }

                videoSource.NewFrame += new NewFrameEventHandler(OnNewFrame);
                videoSource.Start();
                isCameraOn = true;
                return "CAMERA_ON";
            }
            catch (Exception ex) { return "ERROR: " + ex.Message; }
        }

        public string TurnOff()
        {
            try
            {
                if (isRecording) StopRecording();

                if (videoSource != null && videoSource.IsRunning)
                {
                    videoSource.SignalToStop();
                    // Đợi tối đa 1 giây để camera tắt hẳn
                    for (int i = 0; i < 10; i++)
                    {
                        if (!videoSource.IsRunning) break;
                        Thread.Sleep(100);
                    }
                    videoSource.Stop();
                    videoSource.NewFrame -= OnNewFrame;
                    videoSource = null;
                }

                isCameraOn = false;
                lock (frameLock)
                {
                    if (currentFrame != null) { currentFrame.Dispose(); currentFrame = null; }
                }

                return "CAMERA_OFF";
            }
            catch (Exception ex) { return "ERROR: " + ex.Message; }
        }

        private void OnNewFrame(object sender, NewFrameEventArgs eventArgs)
        {
            try
            {
                Bitmap videoFrame = null;

                // 1. Clone frame để hiển thị (giữ lock cực nhanh)
                lock (frameLock)
                {
                    if (currentFrame != null) currentFrame.Dispose();
                    currentFrame = (Bitmap)eventArgs.Frame.Clone();

                    // Nếu đang ghi hình, clone thêm 1 bản để ghi
                    if (isRecording) videoFrame = (Bitmap)eventArgs.Frame.Clone();
                }

                // 2. Ghi video (Thực hiện ngoài lock frame để không chặn streaming)
                if (videoFrame != null)
                {
                    // Kiểm tra an toàn: Nếu kích thước ảnh bị đổi đột ngột thì bỏ qua để tránh Crash
                    if (videoFrame.Width != actualWidth || videoFrame.Height != actualHeight)
                    {
                        videoFrame.Dispose();
                        return;
                    }

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

        public string StartRecording()
        {
            try
            {
                if (!isCameraOn) return "ERROR: Camera is not ON";
                if (isRecording) return "ERROR: Already recording";

                string timestamp = DateTime.Now.ToString("yyyyMMdd_HHmmss");
                currentVideoPath = Path.Combine(outputFolder, $"webcam_{timestamp}.avi");

                // --- KHỞI TẠO VIDEO WRITER VỚI KÍCH THƯỚC THẬT ---
                lock (videoWriteLock)
                {
                    videoWriter = new VideoFileWriter();

                    // QUAN TRỌNG NHẤT:
                    // Sử dụng actualWidth và actualHeight đã lấy từ lúc TurnOn()
                    // Điều này đảm bảo kích thước file video KHỚP 100% với kích thước Camera
                    // => KHÔNG BAO GIỜ BỊ TREO (HANG)
                    videoWriter.Open(currentVideoPath, actualWidth, actualHeight, TARGET_FPS, VideoCodec.MPEG4, VIDEO_BITRATE);
                }

                isRecording = true;
                return "RECORDING_STARTED";
            }
            catch (Exception ex)
            {
                // Reset nếu lỗi
                isRecording = false;
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

                // Đợi 0.5s để frame cuối cùng được ghi xong
                Thread.Sleep(500);

                lock (videoWriteLock)
                {
                    if (videoWriter != null)
                    {
                        if (videoWriter.IsOpen) videoWriter.Close();
                        videoWriter.Dispose();
                        videoWriter = null;
                    }
                }

                if (File.Exists(currentVideoPath))
                {
                    long fileSize = new FileInfo(currentVideoPath).Length;
                    return $"RECORDING_STOPPED|{Path.GetFileName(currentVideoPath)}|{fileSize}";
                }

                return "RECORDING_STOPPED||0";
            }
            catch (Exception ex) { return "ERROR: " + ex.Message; }
        }

        public string GetStatus()
        {
            return $"camera_on:{isCameraOn.ToString().ToLower()}|recording:{isRecording.ToString().ToLower()}";
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

        public string ClearAllRecordings()
        {
            try
            {
                if (Directory.Exists(outputFolder))
                {
                    string[] files = Directory.GetFiles(outputFolder, "*.avi");
                    foreach (string file in files) try { File.Delete(file); } catch { }
                }
                return "CLEARED";
            }
            catch (Exception ex) { return "ERROR: " + ex.Message; }
        }
    }
}