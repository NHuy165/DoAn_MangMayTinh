# ✅ Testing Checklist

> Checklist kiểm tra đầy đủ các tính năng của hệ thống Remote Control

---

## 📋 Hướng Dẫn Sử Dụng

- ✅ = Passed (Đạt)
- ❌ = Failed (Lỗi)
- ⏳ = In Progress (Đang test)
- ⏭️ = Skipped (Bỏ qua)

---

## 🔌 1. Kết Nối Cơ Bản

### 1.1 Server Startup
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 1.1.1 | Mở Visual Studio và build project thành công | ☐ | |
| 1.1.2 | Chạy TargetServer.exe không báo lỗi | ☐ | |
| 1.1.3 | Bấm "Open Server" hiển thị trạng thái Listening | ☐ | |
| 1.1.4 | Form không bị treo/freeze khi đang listen | ☐ | |

### 1.2 Client Startup
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 1.2.1 | `pip install -r requirements.txt` thành công | ☐ | |
| 1.2.2 | `python manage.py migrate` không lỗi | ☐ | |
| 1.2.3 | `python manage.py runserver 0.0.0.0:8000` chạy được | ☐ | |
| 1.2.4 | Truy cập `http://localhost:8000` hiển thị trang web | ☐ | |

### 1.3 Server Discovery
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 1.3.1 | Bấm "Discover" tìm được server trong LAN | ☐ | |
| 1.3.2 | Hiển thị đúng IP và hostname của server | ☐ | |
| 1.3.3 | Discover nhiều server (nếu có) hiển thị đầy đủ | ☐ | |
| 1.3.4 | Timeout đúng khi không tìm thấy server | ☐ | |

### 1.4 Connection
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 1.4.1 | Bấm "Connect" kết nối thành công | ☐ | |
| 1.4.2 | Hiển thị trạng thái "Connected" sau khi kết nối | ☐ | |
| 1.4.3 | Server hiển thị client đã kết nối | ☐ | |
| 1.4.4 | Bấm "Disconnect" ngắt kết nối thành công | ☐ | |
| 1.4.5 | Kết nối lại sau khi disconnect hoạt động | ☐ | |

---

## 🖥️ 2. Quản Lý Hệ Thống

### 2.1 Applications
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 2.1.1 | Bấm "Refresh" hiển thị danh sách applications | ☐ | |
| 2.1.2 | Danh sách hiển thị đúng tên ứng dụng đang chạy | ☐ | |
| 2.1.3 | Bấm "Stop" dừng được ứng dụng đã chọn | ☐ | |
| 2.1.4 | Danh sách cập nhật sau khi stop ứng dụng | ☐ | |
| 2.1.5 | Start Menu scan hiển thị danh sách apps | ☐ | |
| 2.1.6 | Bấm vào app từ Start Menu khởi động thành công | ☐ | |

### 2.2 Processes
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 2.2.1 | Bấm "Refresh" hiển thị danh sách processes | ☐ | |
| 2.2.2 | Hiển thị đúng PID và tên process | ☐ | |
| 2.2.3 | Bấm "Kill" kết thúc process đã chọn | ☐ | |
| 2.2.4 | Không cho kill các process hệ thống quan trọng | ☐ | |
| 2.2.5 | Start process bằng tên hoạt động | ☐ | |
| 2.2.6 | Start process bằng đường dẫn hoạt động | ☐ | |

### 2.3 Power Control
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 2.3.1 | Trang Power hiển thị đúng giao diện | ☐ | |
| 2.3.2 | Bấm "Shutdown" gửi lệnh shutdown (**cẩn thận**) | ☐ | ⚠️ Test cuối |
| 2.3.3 | Bấm "Restart" gửi lệnh restart (**cẩn thận**) | ☐ | ⚠️ Test cuối |
| 2.3.4 | Confirmation dialog hiển thị trước khi thực hiện | ☐ | |

---

## 📷 3. Giám Sát

### 3.1 Screenshot
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 3.1.1 | Bấm "Capture" chụp ảnh màn hình | ☐ | |
| 3.1.2 | Ảnh hiển thị đúng nội dung màn hình server | ☐ | |
| 3.1.3 | Ảnh có độ phân giải đầy đủ | ☐ | |
| 3.1.4 | Bấm "Download" tải ảnh về máy | ☐ | |
| 3.1.5 | File ảnh mở được và hiển thị đúng | ☐ | |

### 3.2 Screen Recording
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 3.2.1 | Bấm "Start Stream" bắt đầu stream | ☐ | |
| 3.2.2 | Preview hiển thị màn hình realtime | ☐ | |
| 3.2.3 | Bấm "Start Recording" bắt đầu ghi | ☐ | |
| 3.2.4 | Trạng thái hiển thị "Recording..." | ☐ | |
| 3.2.5 | Bấm "Stop Recording" dừng ghi | ☐ | |
| 3.2.6 | File recording xuất hiện trong danh sách | ☐ | |
| 3.2.7 | Download recording hoạt động | ☐ | |
| 3.2.8 | File video phát được (VLC, Windows Media) | ☐ | |
| 3.2.9 | Delete recording xóa file thành công | ☐ | |

### 3.3 Webcam
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 3.3.1 | Bấm "Turn On Webcam" bật camera | ☐ | |
| 3.3.2 | Preview hiển thị hình ảnh từ webcam | ☐ | |
| 3.3.3 | Bấm "Start Recording" ghi hình | ☐ | |
| 3.3.4 | Trạng thái hiển thị "Recording..." | ☐ | |
| 3.3.5 | Bấm "Stop Recording" dừng ghi | ☐ | |
| 3.3.6 | File xuất hiện trong danh sách recordings | ☐ | |
| 3.3.7 | Bấm "Turn Off Webcam" tắt camera | ☐ | |
| 3.3.8 | Download và delete hoạt động | ☐ | |

### 3.4 Keylogger
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 3.4.1 | Bấm "Start Keylogger" bắt đầu ghi phím | ☐ | |
| 3.4.2 | Gõ phím trên server và kiểm tra | ☐ | |
| 3.4.3 | Bấm "Get Keylog" hiển thị các phím đã ghi | ☐ | |
| 3.4.4 | Các phím đặc biệt (Enter, Shift, Ctrl) hiển thị đúng | ☐ | |
| 3.4.5 | Bấm "Clear" xóa log hiện tại | ☐ | |
| 3.4.6 | Bấm "Stop Keylogger" dừng ghi | ☐ | |

---

## 🛠️ 4. Quản Lý Nâng Cao

### 4.1 Remote Shell (CMD)
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 4.1.1 | Trang Shell hiển thị terminal interface | ☐ | |
| 4.1.2 | Gõ `dir` hiển thị danh sách file | ☐ | |
| 4.1.3 | Gõ `cd ..` thay đổi thư mục | ☐ | |
| 4.1.4 | Gõ `ipconfig` hiển thị network info | ☐ | |
| 4.1.5 | Gõ `echo Hello` hiển thị "Hello" | ☐ | |
| 4.1.6 | Command có output dài hiển thị đầy đủ | ☐ | |
| 4.1.7 | Command không tồn tại hiển thị lỗi phù hợp | ☐ | |

### 4.2 File Manager
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 4.2.1 | Trang hiển thị danh sách ổ đĩa (C:, D:, ...) | ☐ | |
| 4.2.2 | Click vào ổ đĩa hiển thị nội dung | ☐ | |
| 4.2.3 | Click vào folder để vào bên trong | ☐ | |
| 4.2.4 | Bấm "Up Level" quay lại thư mục cha | ☐ | |
| 4.2.5 | Download file hoạt động | ☐ | |
| 4.2.6 | File download đúng nội dung | ☐ | |
| 4.2.7 | Delete file hoạt động | ☐ | |
| 4.2.8 | Không cho truy cập đường dẫn không hợp lệ | ☐ | |

### 4.3 Home Dashboard
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 4.3.1 | Hiển thị CPU usage realtime | ☐ | |
| 4.3.2 | Hiển thị RAM usage realtime | ☐ | |
| 4.3.3 | Hiển thị Disk space | ☐ | |
| 4.3.4 | Hiển thị thông tin phần cứng (CPU, GPU) | ☐ | |
| 4.3.5 | Hiển thị Hostname và IP | ☐ | |
| 4.3.6 | Thông tin cập nhật định kỳ | ☐ | |

---

## 🌐 5. Truy Cập Từ Xa

### 5.1 Cross-Device Access
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 5.1.1 | Truy cập từ máy tính khác trong LAN | ☐ | |
| 5.1.2 | Truy cập từ điện thoại (cùng WiFi) | ☐ | |
| 5.1.3 | Giao diện responsive trên mobile | ☐ | |
| 5.1.4 | Các tính năng hoạt động đúng trên mobile | ☐ | |

### 5.2 Multi-Session
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 5.2.1 | Nhiều browser tabs hoạt động độc lập | ☐ | |
| 5.2.2 | Mỗi tab có session riêng | ☐ | |
| 5.2.3 | Disconnect 1 tab không ảnh hưởng tab khác | ☐ | |

---

## 🔒 6. Error Handling

### 6.1 Connection Errors
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 6.1.1 | Tắt server → Client hiển thị lỗi phù hợp | ☐ | |
| 6.1.2 | Reconnect sau khi server restart | ☐ | |
| 6.1.3 | Timeout khi server không phản hồi | ☐ | |

### 6.2 Input Validation
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 6.2.1 | Start process với tên rỗng → lỗi phù hợp | ☐ | |
| 6.2.2 | Kill process không tồn tại → lỗi phù hợp | ☐ | |
| 6.2.3 | Truy cập file không tồn tại → lỗi phù hợp | ☐ | |

---

## 📊 7. Performance

### 7.1 Response Time
| # | Test Case | Mục tiêu | Kết quả | Ghi chú |
|---|-----------|----------|---------|---------|
| 7.1.1 | Screenshot capture time | < 3s | ☐ | |
| 7.1.2 | Process list load time | < 2s | ☐ | |
| 7.1.3 | File listing load time | < 2s | ☐ | |
| 7.1.4 | Shell command response | < 5s | ☐ | |

### 7.2 Stability
| # | Test Case | Kết quả | Ghi chú |
|---|-----------|---------|---------|
| 7.2.1 | Sử dụng liên tục 30 phút không crash | ☐ | |
| 7.2.2 | Ghi hình 10 phút không lỗi | ☐ | |
| 7.2.3 | Nhiều operations liên tiếp không treo | ☐ | |

---

## 📝 Ghi Chú Test

### Ngày test: ________________

### Người test: ________________

### Môi trường:
- **Server OS:** ________________
- **Client OS:** ________________
- **Python version:** ________________
- **Browser:** ________________

### Tổng kết:
- **Passed:** ___ / ___
- **Failed:** ___ / ___
- **Skipped:** ___ / ___

### Issues phát hiện:
1. ________________________________________________________________
2. ________________________________________________________________
3. ________________________________________________________________

---

**🎓 Đồ án Môn Mạng Máy Tính - 2025**
