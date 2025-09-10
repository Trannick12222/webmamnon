#!/usr/bin/env python3
"""
Script để migrate gallery hiện tại trên Railway thành album system
- Kết nối tới Railway MySQL database
- Tìm các ảnh có cùng description
- Tạo album và gom các ảnh có cùng mô tả
"""

import mysql.connector
from mysql.connector import Error
import sys
from datetime import datetime
from collections import defaultdict

# Railway MySQL Configuration
RAILWAY_DB_CONFIG = {
    'host': 'crossover.proxy.rlwy.net',
    'port': 29685,
    'user': 'root',
    'password': 'JUMlghRDGtVSaVSZoLgpelgXeTfNpAbp',
    'database': 'railway'
}

def create_railway_connection():
    """Tạo kết nối đến Railway MySQL database"""
    try:
        connection = mysql.connector.connect(**RAILWAY_DB_CONFIG)
        if connection.is_connected():
            print("✅ Kết nối Railway database thành công!")
            return connection
    except Error as e:
        print(f"❌ Lỗi kết nối Railway database: {e}")
        return None

def check_album_tables_exist(connection):
    """Kiểm tra xem các bảng album đã tồn tại chưa"""
    cursor = connection.cursor()
    
    try:
        # Kiểm tra bảng gallery_album
        cursor.execute("SHOW TABLES LIKE 'gallery_album'")
        album_table_exists = cursor.fetchone() is not None
        
        # Kiểm tra cột album_id trong bảng gallery
        cursor.execute("DESCRIBE gallery")
        columns = [row[0] for row in cursor.fetchall()]
        album_id_column_exists = 'album_id' in columns
        
        return album_table_exists and album_id_column_exists
        
    except Error as e:
        print(f"❌ Lỗi kiểm tra bảng: {e}")
        return False
    finally:
        cursor.close()

def create_album_tables(connection):
    """Tạo các bảng cần thiết cho album system"""
    cursor = connection.cursor()
    
    try:
        print("📝 Tạo bảng gallery_album...")
        
        create_album_table_query = """
        CREATE TABLE IF NOT EXISTS gallery_album (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            category VARCHAR(100),
            is_featured TINYINT(1) DEFAULT 0,
            cover_image_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_created_at (created_at),
            INDEX idx_category (category),
            INDEX idx_is_featured (is_featured)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        cursor.execute(create_album_table_query)
        
        print("📝 Thêm cột album_id vào bảng gallery...")
        try:
            add_album_id_query = """
            ALTER TABLE gallery 
            ADD COLUMN album_id INT NULL,
            ADD INDEX idx_album_id (album_id);
            """
            cursor.execute(add_album_id_query)
        except Error as e:
            if "Duplicate column name 'album_id'" in str(e):
                print("⚠️  Cột album_id đã tồn tại, bỏ qua...")
            else:
                raise e
        
        print("📝 Thêm foreign key constraints...")
        try:
            fk_gallery_album_query = """
            ALTER TABLE gallery 
            ADD CONSTRAINT fk_gallery_album 
            FOREIGN KEY (album_id) REFERENCES gallery_album(id) 
            ON DELETE SET NULL ON UPDATE CASCADE;
            """
            cursor.execute(fk_gallery_album_query)
        except Error as e:
            if "foreign key constraint already exists" in str(e) or "Duplicate foreign key" in str(e):
                print("⚠️  Foreign key fk_gallery_album đã tồn tại, bỏ qua...")
            else:
                print(f"⚠️  Lỗi tạo foreign key gallery->album: {e}")
        
        try:
            fk_album_cover_query = """
            ALTER TABLE gallery_album 
            ADD CONSTRAINT fk_album_cover_image 
            FOREIGN KEY (cover_image_id) REFERENCES gallery(id) 
            ON DELETE SET NULL ON UPDATE CASCADE;
            """
            cursor.execute(fk_album_cover_query)
        except Error as e:
            if "foreign key constraint already exists" in str(e) or "Duplicate foreign key" in str(e):
                print("⚠️  Foreign key fk_album_cover_image đã tồn tại, bỏ qua...")
            else:
                print(f"⚠️  Lỗi tạo foreign key album->cover: {e}")
        
        connection.commit()
        print("✅ Tạo bảng album thành công!")
        return True
        
    except Error as e:
        print(f"❌ Lỗi tạo bảng album: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()

def get_gallery_data(connection):
    """Lấy dữ liệu gallery hiện tại"""
    cursor = connection.cursor(dictionary=True)
    
    try:
        query = """
        SELECT id, title, image_path, description, category, is_featured, created_at
        FROM gallery 
        WHERE album_id IS NULL OR album_id = 0
        ORDER BY created_at DESC
        """
        cursor.execute(query)
        images = cursor.fetchall()
        
        print(f"📊 Tìm thấy {len(images)} ảnh chưa được gom vào album")
        return images
        
    except Error as e:
        print(f"❌ Lỗi lấy dữ liệu gallery: {e}")
        return []
    finally:
        cursor.close()

def group_images_by_description(images):
    """Gom các ảnh theo description"""
    grouped = defaultdict(list)
    
    for image in images:
        desc = image['description']
        if desc and desc.strip():  # Chỉ gom những ảnh có description
            desc_key = desc.strip().lower()
            grouped[desc_key].append(image)
    
    # Chỉ giữ lại những nhóm có từ 2 ảnh trở lên
    result = {}
    for desc, imgs in grouped.items():
        if len(imgs) >= 2:
            result[desc] = imgs
    
    return result

def create_albums_from_groups(connection, grouped_images):
    """Tạo album từ các nhóm ảnh"""
    cursor = connection.cursor()
    created_albums = 0
    processed_images = 0
    
    try:
        for description, images in grouped_images.items():
            print(f"\n📁 Tạo album cho mô tả: '{description}' ({len(images)} ảnh)")
            
            # Tạo title cho album từ description (lấy 50 ký tự đầu)
            album_title = description[:50] + "..." if len(description) > 50 else description
            
            # Lấy category từ ảnh đầu tiên
            category = images[0]['category']
            
            # Tạo album
            create_album_query = """
            INSERT INTO gallery_album (title, description, category, is_featured, created_at)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(create_album_query, (
                album_title,
                description,
                category,
                False,  # is_featured = False
                datetime.now()
            ))
            
            album_id = cursor.lastrowid
            print(f"   ✅ Tạo album ID {album_id}: {album_title}")
            
            # Cập nhật các ảnh để thuộc về album này
            image_ids = [img['id'] for img in images]
            update_images_query = """
            UPDATE gallery 
            SET album_id = %s 
            WHERE id IN ({})
            """.format(','.join(['%s'] * len(image_ids)))
            
            cursor.execute(update_images_query, [album_id] + image_ids)
            
            # Đặt ảnh đầu tiên làm cover
            cover_image_id = images[0]['id']
            update_cover_query = """
            UPDATE gallery_album 
            SET cover_image_id = %s 
            WHERE id = %s
            """
            cursor.execute(update_cover_query, (cover_image_id, album_id))
            
            print(f"   📸 Đặt ảnh ID {cover_image_id} làm cover")
            print(f"   📋 Gom {len(images)} ảnh vào album")
            
            created_albums += 1
            processed_images += len(images)
        
        connection.commit()
        return created_albums, processed_images
        
    except Error as e:
        print(f"❌ Lỗi tạo album: {e}")
        connection.rollback()
        return 0, 0
    finally:
        cursor.close()

def show_statistics(connection):
    """Hiển thị thống kê sau khi migrate"""
    cursor = connection.cursor()
    
    try:
        # Đếm album
        cursor.execute("SELECT COUNT(*) FROM gallery_album")
        album_count = cursor.fetchone()[0]
        
        # Đếm ảnh trong album
        cursor.execute("SELECT COUNT(*) FROM gallery WHERE album_id IS NOT NULL")
        images_in_albums = cursor.fetchone()[0]
        
        # Đếm ảnh đơn lẻ
        cursor.execute("SELECT COUNT(*) FROM gallery WHERE album_id IS NULL")
        standalone_images = cursor.fetchone()[0]
        
        print(f"\n📊 Thống kê sau khi migrate:")
        print(f"   - Tổng số album: {album_count}")
        print(f"   - Ảnh trong album: {images_in_albums}")
        print(f"   - Ảnh đơn lẻ: {standalone_images}")
        
    except Error as e:
        print(f"❌ Lỗi lấy thống kê: {e}")
    finally:
        cursor.close()

def main():
    """Hàm chính"""
    print("🚀 Railway Gallery to Albums Migration")
    print("=" * 50)
    
    # Kết nối Railway database
    connection = create_railway_connection()
    if not connection:
        sys.exit(1)
    
    try:
        # Kiểm tra và tạo bảng album nếu cần
        if not check_album_tables_exist(connection):
            print("📋 Các bảng album chưa tồn tại, tạo mới...")
            if not create_album_tables(connection):
                print("❌ Không thể tạo bảng album!")
                sys.exit(1)
        else:
            print("✅ Các bảng album đã tồn tại")
        
        # Lấy dữ liệu gallery
        images = get_gallery_data(connection)
        if not images:
            print("⚠️  Không có ảnh nào để xử lý")
            return
        
        # Gom ảnh theo description
        grouped_images = group_images_by_description(images)
        
        if not grouped_images:
            print("⚠️  Không tìm thấy ảnh nào có cùng mô tả")
            return
        
        print(f"\n🔍 Tìm thấy {len(grouped_images)} nhóm ảnh có cùng mô tả:")
        for desc, imgs in grouped_images.items():
            print(f"   - '{desc}': {len(imgs)} ảnh")
        
        # Xác nhận từ user
        confirm = input(f"\n❓ Bạn có muốn tạo {len(grouped_images)} album từ các nhóm này? (y/N): ")
        if confirm.lower() != 'y':
            print("❌ Hủy bỏ migration")
            return
        
        # Tạo album
        created_albums, processed_images = create_albums_from_groups(connection, grouped_images)
        
        print(f"\n🎉 Migration hoàn thành!")
        print(f"   ✅ Đã tạo {created_albums} album")
        print(f"   📸 Đã xử lý {processed_images} ảnh")
        
        # Hiển thị thống kê
        show_statistics(connection)
        
    except Exception as e:
        print(f"\n💥 Lỗi nghiêm trọng: {e}")
        sys.exit(1)
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("\n🔌 Đã đóng kết nối Railway database")

if __name__ == "__main__":
    main()
