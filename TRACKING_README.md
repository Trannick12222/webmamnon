# 📊 Hệ thống Tracking Lượt Truy Cập Website

## 🎯 Tổng quan

Hệ thống tracking lượt truy cập đã được tích hợp vào website mầm non Hoa Hướng Dương để theo dõi và phân tích lưu lượng truy cập.

## ✨ Tính năng

### 📈 Thống kê hiển thị trong Admin Dashboard
- **Tổng lượt truy cập**: Tổng số lần trang web được truy cập
- **Lượt truy cập hôm nay**: Số lượt truy cập trong ngày hiện tại
- **Khách duy nhất hôm nay**: Số IP duy nhất truy cập trong ngày
- **Lượt truy cập tuần này**: Thống kê 7 ngày gần nhất
- **Lượt truy cập tháng này**: Thống kê 30 ngày gần nhất

### 🔍 Dữ liệu được thu thập
- **IP Address**: Địa chỉ IP của người truy cập (được ẩn một phần để bảo mật)
- **User Agent**: Thông tin trình duyệt và thiết bị
- **Page URL**: Trang được truy cập
- **Referrer**: Trang giới thiệu (nếu có)
- **Thời gian truy cập**: Ngày và giờ chính xác
- **Unique Visitor**: Đánh dấu lượt truy cập duy nhất trong ngày

## 🏗️ Cấu trúc Database

### Bảng `page_visit`
```sql
CREATE TABLE page_visit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip_address VARCHAR(45) NULL,           -- Hỗ trợ IPv6
    user_agent TEXT NULL,                  -- Thông tin trình duyệt
    page_url VARCHAR(500) NULL,            -- URL trang được truy cập
    referrer VARCHAR(500) NULL,            -- Trang giới thiệu
    visit_date DATE NULL,                  -- Ngày truy cập
    visit_time DATETIME NULL,              -- Thời gian truy cập
    is_unique BOOLEAN DEFAULT TRUE,        -- Lượt truy cập duy nhất trong ngày
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 Cách hoạt động

### 1. Tracking tự động
- Mỗi khi có người truy cập website, hệ thống tự động ghi nhận
- Chỉ track các trang public (không track admin và static files)
- Xử lý unique visitors: 1 IP/ngày = 1 unique visitor

### 2. Hiển thị thống kê
- Admin dashboard tại `/admin` hiển thị card "Lượt truy cập"
- Thống kê chi tiết trong phần "Thống kê nội dung"
- Cập nhật real-time khi có lượt truy cập mới

## 🛠️ Scripts hỗ trợ

### 1. `update_railway_db.py`
- Tạo bảng `page_visit` trên Railway database
- Kiểm tra kết nối và cấu trúc bảng

### 2. `test_railway_tracking.py`
- Test tính năng tracking trên production
- Hiển thị thống kê chi tiết
- Xem danh sách truy cập gần nhất

### 3. `migrate_page_visit.py`
- Migration script tương thích local và production
- Test tính năng tracking

## 📊 Cách xem thống kê

### 1. Admin Dashboard
```
https://mamnon.hoahuongduong.org/admin
```

### 2. Card "Lượt truy cập"
- Hiển thị tổng lượt truy cập
- Lượt truy cập hôm nay
- Icon: `fas fa-chart-line`
- Màu: Teal

### 3. Thống kê chi tiết
- Lượt truy cập tuần này
- Khách duy nhất hôm nay
- Tổng lượt truy cập

## 🔧 Cấu hình

### Environment Variables (Railway)
```
MYSQLHOST=crossover.proxy.rlwy.net
MYSQLPORT=29685
MYSQLUSER=root
MYSQLPASSWORD=JUMlghRDGtVSaVSZoLgpelgXeTfNpAbp
MYSQLDATABASE=railway
```

### Local Development
```
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=173915Snow
MYSQL_DATABASE=hoa_huong_duong
```

## 🔒 Bảo mật và Privacy

### 1. Dữ liệu được bảo vệ
- IP address được mask khi hiển thị
- Không lưu thông tin cá nhân
- Chỉ admin mới xem được thống kê

### 2. Tuân thủ quy định
- Không track thông tin nhạy cảm
- Dữ liệu chỉ dùng cho mục đích thống kê
- Có thể xóa dữ liệu theo yêu cầu

## 🚀 Deployment

### 1. Local
```bash
python migrate_page_visit.py
python app.py
```

### 2. Railway
```bash
python update_railway_db.py
# Deploy code lên Railway
```

## 📈 Monitoring

### 1. Kiểm tra thống kê
```bash
python test_railway_tracking.py
```

### 2. Database health check
```bash
python update_railway_db.py
```

## 🐛 Troubleshooting

### 1. Bảng không tồn tại
```bash
python update_railway_db.py
```

### 2. Tracking không hoạt động
```bash
python migrate_page_visit.py
```

### 3. Kết nối database lỗi
- Kiểm tra environment variables
- Kiểm tra network connectivity
- Xem logs trong Railway dashboard

## 📞 Hỗ trợ

Nếu có vấn đề với hệ thống tracking, vui lòng:
1. Chạy script test để kiểm tra
2. Xem logs trong Railway dashboard
3. Kiểm tra database connection
4. Liên hệ developer để hỗ trợ

---

**Lưu ý**: Hệ thống tracking được thiết kế để không ảnh hưởng đến hiệu suất website. Nếu có lỗi tracking, website vẫn hoạt động bình thường.

