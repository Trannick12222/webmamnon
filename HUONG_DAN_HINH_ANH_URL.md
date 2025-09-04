# 🖼️ Hướng dẫn sử dụng hình ảnh từ URL bên ngoài

## 🎯 Mục đích
Thay vì upload hình ảnh trực tiếp lên server (tốn dung lượng), bạn có thể sử dụng hình ảnh từ các dịch vụ cloud storage như Google Drive, OneDrive, Dropbox.

## ✅ Ưu điểm
- **Tiết kiệm dung lượng server**: Không lưu trữ file trên server
- **Tốc độ nhanh**: Tải hình ảnh từ CDN của các dịch vụ lớn
- **Dễ quản lý**: Quản lý hình ảnh từ dịch vụ cloud quen thuộc
- **Không giới hạn**: Không lo về dung lượng server

## 🌐 Dịch vụ được hỗ trợ

### 1. Google Drive ⭐ (Khuyến nghị)
**Cách lấy link:**
1. Upload hình ảnh lên Google Drive
2. Chuột phải → "Get link" → "Anyone with the link"
3. Copy link có dạng: `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`

**Tự động chuyển đổi thành:** `https://drive.google.com/uc?export=view&id=FILE_ID`

### 2. Google Photos ⚠️ (Beta - Có hạn chế)
**Cách lấy link:**
1. Mở Google Photos
2. Chọn ảnh → Nhấn nút Share → "Create link"
3. Copy link có dạng: `https://photos.app.goo.gl/...` hoặc `https://photos.google.com/share/...`

**⚠️ Lưu ý quan trọng:**
- Google Photos có chính sách bảo mật nghiêm ngặt
- Một số ảnh có thể yêu cầu authentication
- Link có thể hết hạn sau một thời gian
- **Khuyến nghị:** Upload lên Google Drive thay vì Google Photos

**Tự động xử lý:**
- Hệ thống sẽ cố gắng trích xuất direct URL từ `lh3.googleusercontent.com`
- Thêm parameter `=s1600` để lấy ảnh chất lượng cao

### 3. OneDrive
**Cách lấy link:**
1. Upload hình ảnh lên OneDrive
2. Chuột phải → "Share" → Copy link
3. Link có dạng: `https://1drv.ms/i/s!...`

### 4. Dropbox
**Cách lấy link:**
1. Upload hình ảnh lên Dropbox
2. Chuột phải → "Copy Dropbox link"
3. Link có dạng: `https://www.dropbox.com/s/...?dl=0`

**Tự động chuyển đổi thành:** `...?dl=1` hoặc `...?raw=1`

### 5. Imgur
**Cách sử dụng:**
1. Truy cập imgur.com
2. Upload hình ảnh
3. Copy direct link: `https://imgur.com/IMAGE_ID`

### 6. GitHub
**Cách sử dụng:**
1. Upload hình ảnh vào repository
2. Mở file → "Raw" → Copy URL
3. Link có dạng: `https://raw.githubusercontent.com/user/repo/branch/image.jpg`

## 🚀 Cách sử dụng trong Admin

### Trong TinyMCE Editor:
1. Nhấn nút "Insert Image" trong toolbar
2. Chọn "Cancel" khi hỏi upload file
3. Hộp thoại "External Image Picker" sẽ xuất hiện
4. Dán URL vào ô input
5. Xem trước hình ảnh
6. Nhấn "Chèn hình ảnh"

### Fallback (nếu không có modal):
1. Nhấn nút "Insert Image" trong toolbar
2. Chọn "Cancel" khi hỏi upload file
3. Nhập URL vào prompt
4. Hệ thống tự động xử lý và chèn

## 🛠️ Công cụ kiểm tra URL

Truy cập: `/admin/settings/external-images`

Trang này cung cấp:
- Hướng dẫn chi tiết từng dịch vụ
- Công cụ test URL
- Ví dụ cụ thể

## ⚠️ Lưu ý quan trọng

### Quyền truy cập:
- **Google Drive**: Phải set "Anyone with the link can view" ⭐
- **Google Photos**: Cần public sharing, có thể yêu cầu authentication ⚠️
- **OneDrive**: Phải tạo public sharing link
- **Dropbox**: Phải tạo public link

### Giới hạn:
- Kích thước file tối đa: 10MB
- Timeout: 10 giây
- Chỉ chấp nhận file hình ảnh (image/*)

### Bảo mật:
- URL sẽ được validate trước khi sử dụng
- Kiểm tra Content-Type
- Kiểm tra kích thước file

## 🔧 API Endpoints

### POST `/admin/process-external-image`
Xử lý URL hình ảnh từ bên ngoài

**Request:**
```json
{
    "url": "https://drive.google.com/file/d/..."
}
```

**Response:**
```json
{
    "location": "https://drive.google.com/uc?export=view&id=...",
    "original_url": "https://drive.google.com/file/d/...",
    "message": "External image URL processed successfully"
}
```

### GET `/admin/get-supported-services`
Lấy danh sách dịch vụ được hỗ trợ

## 🔧 Xử lý đặc biệt cho Google Photos

### Tại sao Google Photos khó sử dụng?
- **Chính sách bảo mật**: Google Photos ưu tiên privacy hơn public sharing
- **Authentication**: Nhiều ảnh yêu cầu đăng nhập Google
- **Link expiry**: Link có thể hết hạn theo thời gian
- **CORS policy**: Trình duyệt có thể block cross-origin requests

### Giải pháp thay thế:
1. **Khuyến nghị chính**: Upload ảnh lên **Google Drive** thay vì Google Photos
2. **Cách làm**: Google Photos → Download → Upload lên Google Drive → Get link
3. **Lợi ích**: Stable, reliable, không hết hạn

### Khi nào Google Photos có thể hoạt động:
- ✅ Ảnh được set "Anyone with the link"
- ✅ Album public
- ✅ Không có copyright restrictions
- ❌ Ảnh cá nhân/private
- ❌ Ảnh có face recognition
- ❌ Ảnh trong album riêng tư

## 📝 Ví dụ thực tế

### Google Drive URL:
```
Input:  https://drive.google.com/file/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/view?usp=sharing
Output: https://drive.google.com/uc?export=view&id=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
```

### Dropbox URL:
```
Input:  https://www.dropbox.com/s/abc123/image.jpg?dl=0
Output: https://www.dropbox.com/s/abc123/image.jpg?dl=1
```

### Google Photos URL (khi hoạt động):
```
Input:  https://photos.app.goo.gl/XYZ123
Output: https://lh3.googleusercontent.com/abc123...=s1600
```

## 🎨 Tích hợp vào templates khác

Để thêm tính năng này vào template khác (news/edit.html, events/create.html, v.v.):

1. Thêm script:
```html
<script src="{{ url_for('static', filename='js/external-image-picker.js') }}"></script>
```

2. Cập nhật TinyMCE config:
```javascript
file_picker_callback: function(callback, value, meta) {
    if (meta.filetype === 'image') {
        const choice = confirm('Chọn "OK" để upload file từ máy tính\nChọn "Cancel" để sử dụng URL hình ảnh từ internet');
        
        if (choice) {
            // Upload logic
        } else {
            // External URL logic
            if (window.ExternalImagePicker) {
                const picker = new ExternalImagePicker(callback);
                picker.showModal();
            }
        }
    }
}
```

## 🔍 Troubleshooting

### Lỗi thường gặp:
1. **"Invalid image URL"**: URL không trỏ đến hình ảnh hợp lệ
2. **"Request timeout"**: URL phản hồi quá chậm
3. **"HTTP 403/404"**: Không có quyền truy cập hoặc file không tồn tại

### Giải pháp:
1. Kiểm tra quyền chia sẻ của file
2. Thử URL trên trình duyệt trước
3. Sử dụng công cụ test URL trong admin

---

🎉 **Chúc bạn sử dụng hiệu quả!**
