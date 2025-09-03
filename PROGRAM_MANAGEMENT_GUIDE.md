# 📚 Hướng dẫn Quản lý Chương trình

## 🎯 Tổng quan
Hệ thống quản lý chương trình đã được tích hợp hoàn toàn vào trang `/admin/programs` với giao diện tabs, cho phép bạn quản lý:

- **Chương trình**: Các khóa học chính
- **Nhóm độ tuổi**: Hướng dẫn cho phụ huynh về các độ tuổi
- **Điểm nổi bật**: Các tính năng nổi bật hiển thị trên mỗi chương trình  
- **Thông tin chương trình**: Thông tin cố định (lớp học nhỏ, giáo viên, etc.)

## 🚀 Cách sử dụng

### 1. Truy cập trang quản lý
Vào `http://127.0.0.1:5000/admin/programs`

### 2. Sử dụng Tabs
- **Tab "Chương trình"**: Quản lý các khóa học (như cũ)
- **Tab "Nhóm độ tuổi"**: Tạo/sửa thông tin cho từng độ tuổi
- **Tab "Điểm nổi bật"**: Quản lý các badge hiển thị dưới mỗi chương trình
- **Tab "Thông tin chương trình"**: Quản lý thông tin cố định

### 3. Thêm/Sửa/Xóa dữ liệu
- **Thêm mới**: Click nút "Thêm ..." trên mỗi tab
- **Chỉnh sửa**: Click nút "Sửa" trên từng item
- **Xóa**: Click nút "Xóa" (có xác nhận)

## 📋 Các tính năng chính

### Nhóm độ tuổi
- Tên lớp (VD: Lớp Mầm, Lớp Chồi)
- Độ tuổi (VD: 18-24 tháng)
- Icon và màu sắc tùy chỉnh
- Danh sách kỹ năng phát triển
- Thứ tự hiển thị

### Điểm nổi bật
- Tiêu đề (VD: Phát triển toàn diện)
- Icon Font Awesome
- Màu gradient, viền, chữ tùy chỉnh
- Thứ tự hiển thị

### Thông tin chương trình
- Tiêu đề (VD: Lớp học nhỏ 8-12 trẻ)
- Icon Font Awesome
- Gradient nền tùy chỉnh
- Thứ tự hiển thị

## ✨ Tính năng đặc biệt
- **Live Preview**: Xem trước khi tạo/sửa
- **AJAX Loading**: Tải nhanh không cần reload trang
- **Responsive**: Giao diện đẹp trên mọi thiết bị
- **Fallback Data**: Vẫn hiển thị mặc định nếu chưa có dữ liệu

## 🎨 Tùy chỉnh màu sắc
Hệ thống hỗ trợ các màu Tailwind CSS:
- Pink, Green, Blue, Yellow, Purple, Orange
- Gradient backgrounds cho icons
- Border colors matching

## 📱 Kết quả
Xem thay đổi tại: `http://127.0.0.1:5000/chuong-trinh`

---
*Tất cả dữ liệu đều được lưu trong database và có thể quản lý hoàn toàn từ admin panel.*

