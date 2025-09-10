# Hướng Dẫn Sử Dụng Tính Năng Album

## 🎯 Tổng Quan

Tính năng Album đã được thêm vào hệ thống gallery, cho phép:

- **Upload 1 ảnh**: Tạo ảnh đơn lẻ (như trước)
- **Upload nhiều ảnh**: Tự động tạo album với mô tả chung
- **Quản lý album**: Thêm, sửa, xóa ảnh trong album
- **Hiển thị frontend**: Album và ảnh đơn lẻ được hiển thị riêng biệt

## 🚀 Cách Thực Hiện Migration

### Bước 1: Chạy Migration Script

```bash
python migrate_album_feature.py
```

**Lưu ý**: Cần cấu hình database trong file `migrate_album_feature.py` trước khi chạy:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',        # Thay đổi theo cấu hình của bạn
    'password': '',        # Thay đổi theo cấu hình của bạn  
    'database': 'webmamnon'  # Thay đổi theo tên database của bạn
}
```

### Bước 2: Restart Application

```bash
python app.py
```

## 📋 Các Tính Năng Mới

### 1. Upload Logic Mới

- **1 ảnh**: Tạo ảnh đơn lẻ với title, description riêng
- **Nhiều ảnh**: Tự động tạo album với:
  - Title từ form hoặc auto-generate
  - Description chung cho album
  - Ảnh đầu tiên làm cover
  - Các ảnh con không có description riêng

### 2. Admin Panel

#### Quản Lý Gallery (`/admin/gallery`)
- Hiển thị album và ảnh đơn lẻ riêng biệt
- Button "Quản lý Album" để chuyển sang trang album

#### Quản Lý Album (`/admin/albums`)
- Danh sách tất cả album
- Xem chi tiết, chỉnh sửa, xóa album

#### Chi Tiết Album (`/admin/albums/<id>`)
- Xem tất cả ảnh trong album
- Đặt ảnh bìa
- Xóa ảnh khỏi album
- Copy URL ảnh

#### Chỉnh Sửa Album (`/admin/albums/<id>/edit`)
- Sửa thông tin album
- Thêm ảnh mới vào album
- Xóa album (cùng tất cả ảnh)

### 3. Frontend

#### Trang Gallery (`/thu-vien-anh`)
- Section "Album Ảnh": Hiển thị tất cả album
- Section "Ảnh Đơn Lẻ": Hiển thị ảnh không thuộc album

#### Chi Tiết Album (`/thu-vien-anh/album/<id>`)
- Xem tất cả ảnh trong album
- Lightbox với navigation
- Thông tin album đầy đủ

## 🗃️ Cấu Trúc Database

### Bảng `gallery_album`
```sql
CREATE TABLE gallery_album (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    is_featured TINYINT(1) DEFAULT 0,
    cover_image_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Bảng `gallery` (đã cập nhật)
```sql
ALTER TABLE gallery 
ADD COLUMN album_id INT NULL,
ADD FOREIGN KEY (album_id) REFERENCES gallery_album(id);
```

## 🎮 Cách Sử Dụng

### Tạo Album Mới
1. Vào `/admin/gallery/create`
2. Nhập title, description, category
3. Upload **nhiều ảnh** (2+ ảnh)
4. Hệ thống tự động tạo album

### Tạo Ảnh Đơn Lẻ
1. Vào `/admin/gallery/create`
2. Nhập title, description cho ảnh
3. Upload **1 ảnh duy nhất**
4. Ảnh được tạo như ảnh đơn lẻ

### Quản Lý Album
1. Vào `/admin/albums` để xem danh sách
2. Click "Xem chi tiết" để xem ảnh trong album
3. Click "Chỉnh sửa" để:
   - Sửa thông tin album
   - Thêm ảnh mới
   - Đặt ảnh bìa
   - Xóa ảnh

### Xem Frontend
1. Vào `/thu-vien-anh` để xem gallery
2. Click vào album để xem chi tiết
3. Click vào ảnh để mở lightbox

## 🔧 API Routes Mới

### Admin Routes
- `GET /admin/albums` - Danh sách album
- `GET /admin/albums/<id>` - Chi tiết album  
- `GET/POST /admin/albums/<id>/edit` - Chỉnh sửa album
- `POST /admin/albums/<id>/delete` - Xóa album
- `POST /admin/albums/<album_id>/remove-image/<image_id>` - Xóa ảnh khỏi album
- `POST /admin/albums/<album_id>/set-cover/<image_id>` - Đặt ảnh bìa

### Frontend Routes
- `GET /thu-vien-anh` - Gallery (đã cập nhật)
- `GET /thu-vien-anh/album/<id>` - Chi tiết album

## 🎨 Templates Mới

- `templates/admin/albums/list.html` - Danh sách album admin
- `templates/admin/albums/detail.html` - Chi tiết album admin
- `templates/admin/albums/edit.html` - Chỉnh sửa album admin
- `templates/album_detail.html` - Chi tiết album frontend

## ⚠️ Lưu Ý Quan Trọng

1. **Backup Database**: Luôn backup trước khi chạy migration
2. **Test Environment**: Test trên môi trường dev trước
3. **Permissions**: Đảm bảo quyền ghi file uploads
4. **Foreign Keys**: Migration sẽ tạo foreign key constraints
5. **Existing Data**: Ảnh cũ sẽ trở thành ảnh đơn lẻ (album_id = NULL)

## 🐛 Troubleshooting

### Migration Lỗi
```bash
# Kiểm tra kết nối database
python -c "import mysql.connector; print('MySQL connector OK')"

# Kiểm tra quyền user
SHOW GRANTS FOR 'your_user'@'localhost';
```

### Foreign Key Lỗi
```sql
-- Tắt foreign key check tạm thời
SET FOREIGN_KEY_CHECKS = 0;
-- Chạy migration
-- Bật lại
SET FOREIGN_KEY_CHECKS = 1;
```

### Template Lỗi
- Đảm bảo tất cả templates được tạo đúng thư mục
- Kiểm tra import trong app.py
- Clear browser cache

## 🎉 Hoàn Thành!

Tính năng album đã được tích hợp hoàn chỉnh. Bạn có thể:

✅ Upload 1 ảnh → Tạo ảnh đơn lẻ  
✅ Upload nhiều ảnh → Tạo album tự động  
✅ Quản lý album (thêm/sửa/xóa ảnh)  
✅ Hiển thị album trên frontend  
✅ Lightbox với navigation trong album  

Enjoy your new Album feature! 🚀
