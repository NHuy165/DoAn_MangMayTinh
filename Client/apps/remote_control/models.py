"""
Models for Remote Control App
Lưu trữ metadata của các recordings (Webcam, Screen)
"""

from django.db import models


# ==================== WEBCAM RECORDING ====================

class WebcamRecording(models.Model):
    """
    Model lưu metadata của video recordings từ webcam
    File video thực tế được lưu trong media/webcam/
    """
    
    # Fields
    server_ip = models.CharField(max_length=50, help_text="IP của C# Server")
    filename = models.CharField(max_length=255, help_text="Tên file video")
    file_path = models.FileField(upload_to='webcam/%Y/%m/%d/', help_text="Đường dẫn file trong media/")
    recorded_at = models.DateTimeField(auto_now_add=True, help_text="Thời gian ghi")
    file_size = models.IntegerField(help_text="Kích thước file (bytes)")
    duration = models.IntegerField(default=0, help_text="Độ dài video (giây)")
    
    class Meta:
        ordering = ['-recorded_at']
        verbose_name = "Webcam Recording"
        verbose_name_plural = "Webcam Recordings"
    
    def __str__(self):
        return f"{self.server_ip} - {self.filename}"
    
    def get_file_size_display(self):
        """Format file size thành MB/KB"""
        if self.file_size >= 1024 * 1024:
            return f"{self.file_size / (1024 * 1024):.2f} MB"
        elif self.file_size >= 1024:
            return f"{self.file_size / 1024:.2f} KB"
        return f"{self.file_size} bytes"
    
    def get_duration_display(self):
        """Format duration thành MM:SS"""
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes:02d}:{seconds:02d}"


# ==================== SCREEN RECORDING ====================

class ScreenRecording(models.Model):
    """
    Model lưu metadata của video recordings từ màn hình
    File video thực tế được lưu trong media/screen_recordings/
    """
    
    # Fields
    server_ip = models.CharField(max_length=50, help_text="IP của C# Server")
    filename = models.CharField(max_length=255, help_text="Tên file video")
    file_path = models.FileField(upload_to='screen_recordings/%Y/%m/%d/', help_text="Đường dẫn file trong media/")
    recorded_at = models.DateTimeField(auto_now_add=True, help_text="Thời gian ghi")
    file_size = models.IntegerField(help_text="Kích thước file (bytes)")
    duration = models.IntegerField(default=0, help_text="Độ dài video (giây)")
    
    class Meta:
        ordering = ['-recorded_at']
        verbose_name = "Screen Recording"
        verbose_name_plural = "Screen Recordings"
    
    def __str__(self):
        return f"{self.server_ip} - {self.filename}"
    
    def get_file_size_display(self):
        """Format file size thành MB/KB"""
        if self.file_size >= 1024 * 1024:
            return f"{self.file_size / (1024 * 1024):.2f} MB"
        elif self.file_size >= 1024:
            return f"{self.file_size / 1024:.2f} KB"
        return f"{self.file_size} bytes"