# Railway Database Migration Instructions

Để cập nhật Railway database với cột sort_order mới, bạn cần chạy các lệnh SQL sau:

## Bước 1: Kết nối Railway Database
```bash
# Sử dụng Railway CLI hoặc truy cập Railway Dashboard
railway connect
```

## Bước 2: Chạy các lệnh SQL sau:

```sql
-- Thêm cột sort_order vào bảng gallery
ALTER TABLE gallery ADD COLUMN sort_order INT DEFAULT 0;

-- Cập nhật sort_order cho các record hiện có
-- (Sắp xếp theo album_id và created_at)
SET @row_number = 0;
UPDATE gallery 
SET sort_order = (@row_number:=@row_number + 1)
ORDER BY album_id, created_at ASC;

-- Tạo index để tối ưu performance
CREATE INDEX idx_gallery_album_sort ON gallery(album_id, sort_order);
```

## Bước 3: Kiểm tra
```sql
-- Kiểm tra cột đã được thêm
DESCRIBE gallery;

-- Kiểm tra dữ liệu sort_order
SELECT id, title, album_id, sort_order, created_at 
FROM gallery 
WHERE album_id IS NOT NULL 
ORDER BY album_id, sort_order;
```

## Lưu ý
- Backup database trước khi chạy migration
- Các ảnh hiện tại sẽ giữ nguyên thứ tự theo created_at
- Ảnh mới thêm vào sẽ có sort_order tự động tăng dần
