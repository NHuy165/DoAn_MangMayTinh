using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Threading;

using Accord.Video.FFMPEG;
using AForge.Video;
using AForge.Video.DirectShow;

namespace WebcamRecorder
{
    /// <summary>
    /// WebcamCapture - Chụp và ghi video từ webcam
    /// Hỗ trợ: Camera Preview, Live Streaming và Recording
    /// </summary>
    public class WebcamCapture
    {
        // ==================== STATIC FIELDS ====================

        public static string outputFolder = Path.Combine(Path.GetTempPath(), "webcam_recordings");
        public static string currentVideoPath = "";

        // ==================== PRIVATE FIELDS ====================

        // Camera và Video Writer
        private VideoCaptureDevice videoSource;
        private VideoFileWriter videoWriter;
        private Bitmap currentFrame;

        // Locks
        private object frameLock = new object();
        private object videoWriteLock = new object();

        // State flags
        private volatile bool isRecording = false;
        private bool isCameraOn = false;

        // Video Specs
        private int actualWidth = 640;
        private int actualHeight = 480;

        // Recording metadata
        private DateTime recordingStartTime;

        // ==================== CONSTANTS ====================

        private const int TARGET_FPS = 25;
        private const int VIDEO_BITRATE = 1000000;

        // ==================== CONSTRUCTOR ====================

        public WebcamCapture()
        {
            if (!Directory.Exists(outputFolder)) Directory.CreateDirectory(outputFolder);
        }

        // ==================== CAMERA CONTROL ====================

        public string TurnOn()
        {
            try
            {
                if (isCameraOn) return "ERROR: Camera is already ON";

                FilterInfoCollection videoDevices = new FilterInfoCollection(FilterCategory.VideoInputDevice);
                if (videoDevices.Count == 0) return "ERROR: No camera found";

                videoSource = new VideoCaptureDevice(videoDevices[0].MonikerString);

                if (videoSource.VideoCapabilities.Length > 0)
                {
                    var capability = videoSource.VideoCapabilities
                        .OrderBy(c => Math.Abs(c.FrameSize.Width - 640))
                        .First();
                    videoSource.VideoResolution = capability;
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

        // ==================== FRAME CAPTURE ====================

        private void OnNewFrame(object sender, NewFrameEventArgs eventArgs)
        {
            try
            {
                Bitmap videoFrame = null;
                lock (frameLock)
                {
                    if (currentFrame != null) currentFrame.Dispose();
                    currentFrame = (Bitmap)eventArgs.Frame.Clone();
                    if (isRecording) videoFrame = (Bitmap)eventArgs.Frame.Clone();
                }

                if (videoFrame != null)
                {
                    if (videoFrame.Width != actualWidth || videoFrame.Height != actualHeight)
                    {
                        videoFrame.Dispose();
                        return;
                    }

                    lock (videoWriteLock)
                    {
                        if (isRecording && videoWriter != null && videoWriter.IsOpen)
                        {
                            try
                            {
                                videoWriter.WriteVideoFrame(videoFrame);
                            }
                            catch { }
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

        // ==================== RECORDING ====================

        public string StartRecording()
        {
            try
            {
                if (!isCameraOn) return "ERROR: Camera is not ON";
                if (isRecording) return "ERROR: Already recording";

                string timestamp = DateTime.Now.ToString("yyyyMMdd_HHmmss");
                currentVideoPath = Path.Combine(outputFolder, $"webcam_{timestamp}.avi");

                lock (videoWriteLock)
                {
                    videoWriter = new VideoFileWriter();
                    videoWriter.Open(currentVideoPath, actualWidth, actualHeight, TARGET_FPS, VideoCodec.MPEG4, VIDEO_BITRATE);
                }

                isRecording = true;
                recordingStartTime = DateTime.Now;

                return "RECORDING_STARTED";
            }
            catch (Exception ex)
            {
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

                int duration = (int)(DateTime.Now - recordingStartTime).TotalSeconds;
                long fileSize = File.Exists(currentVideoPath) ? new FileInfo(currentVideoPath).Length : 0;
                string fileName = Path.GetFileName(currentVideoPath);
                
                return $"RECORDING_STOPPED|{fileName}|{fileSize}|{duration}";
            }
            catch (Exception ex) { return "ERROR: " + ex.Message; }
        }

        // ==================== STATUS & UTILITY METHODS ====================

        public string GetStatus()
        {
            return $"camera_on:{isCameraOn.ToString().ToLower()}|recording:{isRecording.ToString().ToLower()}";
        }

        public byte[] GetVideoBytes(string filename)
        {
            try
            {
                if (string.IsNullOrEmpty(filename)) return null;
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
    }
}