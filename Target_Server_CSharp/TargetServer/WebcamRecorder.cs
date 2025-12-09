using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using AForge.Video;
using AForge.Video.DirectShow;
using Accord.Video.FFMPEG;

namespace WebcamRecorder
{
    /// <summary>
    /// Class quản lý webcam: Bật/Tắt camera, Live preview, Recording video
    /// Architecture: Tách biệt Camera ON/OFF và Recording START/STOP
    /// </summary>
    public class WebcamCapture
    {
        // ==================== STATIC VARIABLES ====================
        public static string outputFolder = Path.Combine(Path.GetTempPath(), "webcam_recordings");
        public static string currentVideoPath = "";
        
        // ==================== INSTANCE VARIABLES ====================
        private VideoCaptureDevice videoSource;
        private VideoFileWriter videoWriter;
        private Bitmap currentFrame;
        private object frameLock = new object();
        private bool isRecording = false;
        private bool isCameraOn = false;
        
        // Video settings - HIGH QUALITY
        private const int TARGET_FPS = 30;
        private const int VIDEO_BITRATE = 4000000; // 4 Mbps - High quality
        
        /// <summary>
        /// Constructor: Tạo thư mục output nếu chưa có
        /// </summary>
        public WebcamCapture()
        {
            if (!Directory.Exists(outputFolder))
            {
                Directory.CreateDirectory(outputFolder);
            }
        }
        
        // ==================== CAMERA CONTROL ====================
        
        /// <summary>
        /// Bật camera - Bắt đầu capture frames (CHƯA ghi video)
        /// Return: "CAMERA_ON" hoặc "ERROR:..."
        /// </summary>
        public string TurnOn()
        {
            try
            {
                if (isCameraOn)
                {
                    return "ERROR: Camera is already ON";
                }
                
                // Lấy danh sách cameras có sẵn
                FilterInfoCollection videoDevices = new FilterInfoCollection(FilterCategory.VideoInputDevice);
                
                if (videoDevices.Count == 0)
                {
                    return "ERROR: No camera found";
                }
                
                // Chọn camera đầu tiên
                videoSource = new VideoCaptureDevice(videoDevices[0].MonikerString);
                
                // Chọn resolution CAO NHẤT mà camera hỗ trợ
                if (videoSource.VideoCapabilities.Length > 0)
                {
                    VideoCapabilities bestCapability = videoSource.VideoCapabilities
                        .OrderByDescending(c => c.FrameSize.Width * c.FrameSize.Height)
                        .ThenByDescending(c => c.AverageFrameRate)
                        .First();
                    
                    videoSource.VideoResolution = bestCapability;
                }
                
                // Đăng ký event handler để nhận frames
                videoSource.NewFrame += new NewFrameEventHandler(OnNewFrame);
                
                // Bật camera
                videoSource.Start();
                isCameraOn = true;
                
                return "CAMERA_ON";
            }
            catch (Exception ex)
            {
                return "ERROR: " + ex.Message;
            }
        }
        
        /// <summary>
        /// Tắt camera - Dừng capture frames
        /// Tự động dừng recording nếu đang ghi
        /// Return: "CAMERA_OFF"
        /// </summary>
        public string TurnOff()
        {
            try
            {
                // Dừng recording nếu đang ghi
                if (isRecording)
                {
                    StopRecording();
                }
                
                if (videoSource != null && videoSource.IsRunning)
                {
                    videoSource.SignalToStop();
                    videoSource.WaitForStop();
                    videoSource.NewFrame -= OnNewFrame;
                    videoSource = null;
                }
                
                isCameraOn = false;
                currentFrame = null;
                
                return "CAMERA_OFF";
            }
            catch (Exception ex)
            {
                return "ERROR: " + ex.Message;
            }
        }
        
        /// <summary>
        /// Event handler: Được gọi mỗi khi có frame mới từ camera
        /// Lưu frame vào currentFrame để streaming
        /// Ghi vào video nếu đang recording
        /// </summary>
        private void OnNewFrame(object sender, NewFrameEventArgs eventArgs)
        {
            try
            {
                lock (frameLock)
                {
                    // Clone frame để tránh disposed
                    currentFrame?.Dispose();
                    currentFrame = (Bitmap)eventArgs.Frame.Clone();
                    
                    // Nếu đang recording → Ghi frame vào video
                    if (isRecording && videoWriter != null && videoWriter.IsOpen)
                    {
                        videoWriter.WriteVideoFrame(currentFrame);
                    }
                }
            }
            catch { }
        }
        
        // ==================== FRAME STREAMING ====================
        
        /// <summary>
        /// Lấy frame hiện tại dưới dạng JPEG bytes (để streaming lên web)
        /// Return: byte[] hoặc null nếu không có frame
        /// </summary>
        public byte[] GetCurrentFrameAsJpeg()
        {
            try
            {
                lock (frameLock)
                {
                    if (currentFrame == null)
                    {
                        return null;
                    }
                    
                    using (MemoryStream ms = new MemoryStream())
                    {
                        currentFrame.Save(ms, ImageFormat.Jpeg);
                        return ms.ToArray();
                    }
                }
            }
            catch
            {
                return null;
            }
        }
        
        // ==================== VIDEO RECORDING ====================
        
        /// <summary>
        /// Bắt đầu ghi video (camera phải đã BẬT trước)
        /// Return: "RECORDING_STARTED" hoặc "ERROR:..."
        /// </summary>
        public string StartRecording()
        {
            try
            {
                if (!isCameraOn)
                {
                    return "ERROR: Camera is not ON";
                }
                
                if (isRecording)
                {
                    return "ERROR: Already recording";
                }
                
                if (currentFrame == null)
                {
                    return "ERROR: No frame available. Wait a moment and try again.";
                }
                
                // Tạo tên file với timestamp
                string timestamp = DateTime.Now.ToString("yyyyMMdd_HHmmss");
                currentVideoPath = Path.Combine(outputFolder, $"webcam_{timestamp}.avi");
                
                // Khởi tạo VideoFileWriter với codec H.264
                videoWriter = new VideoFileWriter();
                
                lock (frameLock)
                {
                    if (currentFrame != null)
                    {
                        // Mở file với cấu hình HIGH QUALITY
                        videoWriter.Open(
                            currentVideoPath,
                            currentFrame.Width,
                            currentFrame.Height,
                            TARGET_FPS,
                            VideoCodec.MPEG4,
                            VIDEO_BITRATE
                        );
                    }
                }
                
                isRecording = true;
                return "RECORDING_STARTED";
            }
            catch (Exception ex)
            {
                return "ERROR: " + ex.Message;
            }
        }
        
        /// <summary>
        /// Dừng ghi video, đóng file
        /// Return: "RECORDING_STOPPED|filename|filesize" hoặc "ERROR:..."
        /// </summary>
        public string StopRecording()
        {
            try
            {
                if (!isRecording)
                {
                    return "ERROR: Not recording";
                }
                
                isRecording = false;
                
                // Đóng video writer
                if (videoWriter != null)
                {
                    videoWriter.Close();
                    videoWriter.Dispose();
                    videoWriter = null;
                }
                
                // Lấy thông tin file
                if (File.Exists(currentVideoPath))
                {
                    FileInfo fileInfo = new FileInfo(currentVideoPath);
                    string filename = Path.GetFileName(currentVideoPath);
                    long fileSize = fileInfo.Length;
                    
                    return $"RECORDING_STOPPED|{filename}|{fileSize}";
                }
                
                return "RECORDING_STOPPED||0";
            }
            catch (Exception ex)
            {
                return "ERROR: " + ex.Message;
            }
        }
        
        // ==================== STATUS & UTILITY ====================
        
        /// <summary>
        /// Lấy trạng thái hiện tại
        /// Return: "camera_on:true/false|recording:true/false"
        /// </summary>
        public string GetStatus()
        {
            return $"camera_on:{isCameraOn.ToString().ToLower()}|recording:{isRecording.ToString().ToLower()}";
        }
        
        /// <summary>
        /// Đọc file video và trả về bytes
        /// Return: byte[] hoặc null
        /// </summary>
        public byte[] GetVideoBytes(string filename)
        {
            try
            {
                string filePath = Path.Combine(outputFolder, filename);
                
                if (File.Exists(filePath))
                {
                    return File.ReadAllBytes(filePath);
                }
                
                return null;
            }
            catch
            {
                return null;
            }
        }
        
        /// <summary>
        /// Xóa tất cả file video trong thư mục
        /// Return: "CLEARED"
        /// </summary>
        public string ClearAllRecordings()
        {
            try
            {
                if (Directory.Exists(outputFolder))
                {
                    string[] files = Directory.GetFiles(outputFolder, "*.avi");
                    foreach (string file in files)
                    {
                        try
                        {
                            File.Delete(file);
                        }
                        catch { }
                    }
                }
                
                return "CLEARED";
            }
            catch (Exception ex)
            {
                return "ERROR: " + ex.Message;
            }
        }
        
        /// <summary>
        /// Cleanup resources
        /// </summary>
        public void Dispose()
        {
            TurnOff();
            currentFrame?.Dispose();
        }
    }
}
