# Website Trường Mầm Non Hoa Hướng Dương

Một website hoàn chỉnh cho trường mầm non với hệ thống quản lý nội dung chuyên nghiệp.

## 🌟 Tính năng chính

### Website công khai
- **Trang chủ**: Giới thiệu tổng quan, các chương trình nổi bật, tin tức mới nhất
- **Giới thiệu**: Lịch sử, sứ mệnh, đội ngũ giáo viên
- **Chương trình học**: Chi tiết các lớp học theo độ tuổi
- **Tin tức**: Cập nhật thông tin mới nhất
- **Thư viện ảnh**: Hình ảnh hoạt động của trường
- **Sự kiện**: Các hoạt động sắp tới và đã diễn ra
- **Liên hệ**: Form liên hệ và thông tin chi tiết

### Hệ thống Admin
- **Dashboard tổng quan**: Thống kê và quản lý
- **Quản lý tin tức**: Đăng, sửa, xóa bài viết
- **Quản lý chương trình**: CRUD các chương trình học
- **Thư viện ảnh**: Upload và quản lý hình ảnh với tính năng crop
- **Quản lý sự kiện**: Tạo và quản lý các sự kiện
- **Tin nhắn liên hệ**: Xem và phản hồi tin nhắn

### Tính năng đặc biệt
- **Image Cropping**: Chỉnh sửa ảnh trực tiếp trên browser
- **Responsive Design**: Tương thích mọi thiết bị
- **SEO Friendly**: Tối ưu cho công cụ tìm kiếm
- **Bảo mật**: Hệ thống đăng nhập an toàn
- **Multilingual**: Hỗ trợ tiếng Việt đầy đủ

## 🚀 Công nghệ sử dụng

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Tailwind CSS
- **Icons**: Font Awesome
- **Image Processing**: Cropper.js, Pillow
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF

## 📋 Yêu cầu hệ thống

- Python 3.8+
- MySQL 8.0+
- Node.js (cho Tailwind CSS)

## 🛠️ Cài đặt

### 1. Clone repository
```bash
git clone <repository-url>
cd webmamnon
```

### 2. Tạo virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình database
```bash
# Tạo database MySQL
mysql -u root -p
CREATE DATABASE hoa_huong_duong CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Import database schema
mysql -u root -p hoa_huong_duong < database_setup.sql
```

### 5. Cấu hình environment
```bash
# Chỉnh sửa file .env với thông tin database của bạn
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=hoa_huong_duong
```

### 6. Khởi chạy ứng dụng
```bash
python app.py
```

Website sẽ chạy tại: http://localhost:5000

## 👤 Đăng nhập Admin

**URL**: http://localhost:5000/admin/login
- **Username**: admin
- **Password**: admin123

## 📁 Cấu trúc project

```
webmamnon/
├── app.py                 # File chính của ứng dụng
├── requirements.txt       # Dependencies Python
├── database_setup.sql     # Database schema
├── .env                  # Cấu hình environment
├── static/               # File tĩnh
│   ├── css/
│   ├── js/
│   ├── images/
│   └── uploads/          # Thư mục upload
└── templates/            # Templates HTML
    ├── base.html
    ├── index.html
    ├── about.html
    ├── programs.html
    ├── contact.html
    └── admin/            # Templates admin
        ├── base.html
        ├── login.html
        ├── dashboard.html
        ├── news/
        ├── programs/
        ├── gallery/
        ├── events/
        └── contacts/
```

## 📸 Tính năng Image Cropping

Hệ thống tích hợp sẵn Cropper.js cho phép:
- Crop ảnh với tỷ lệ khác nhau (16:9, 4:3, 1:1, tự do)
- Xoay ảnh trái/phải
- Zoom in/out
- Reset về trạng thái ban đầu
- Preview trước khi lưu

## 🔧 Tùy chỉnh

### Thay đổi màu chủ đạo
Chỉnh sửa trong `templates/base.html`:
```css
.bg-primary { background-color: #ff6b35; }
.bg-secondary { background-color: #f7931e; }
```

### Thêm chương trình học mới
1. Đăng nhập admin
2. Vào "Chương trình" → "Thêm mới"
3. Điền thông tin và upload ảnh
4. Lưu và xuất bản

### Cập nhật thông tin trường
Chỉnh sửa trong database bảng `settings` hoặc qua admin panel.

## 🐛 Troubleshooting

### Lỗi database connection
- Kiểm tra thông tin database trong `.env`
- Đảm bảo MySQL service đang chạy
- Kiểm tra quyền user MySQL

### Lỗi upload ảnh
- Kiểm tra quyền ghi thư mục `static/uploads/`
- Đảm bảo Pillow được cài đặt đúng
- Kiểm tra dung lượng file (max 16MB)

### Lỗi 404 trang admin
- Đảm bảo đã tạo user admin trong database
- Check URL: `/admin/login` (có dấu gạch chéo)

## 📞 Hỗ trợ

Nếu gặp vấn đề trong quá trình cài đặt hoặc sử dụng, vui lòng tạo issue hoặc liên hệ trực tiếp.

## 📝 License

Dự án này được phát triển cho mục đích giáo dục và thương mại. Vui lòng tuân thủ các quy định về bản quyền khi sử dụng.

---

**Phát triển bởi**: Claude AI Assistant
**Ngày tạo**: 2024
**Phiên bản**: 1.0.0