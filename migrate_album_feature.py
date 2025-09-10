#!/usr/bin/env python3
"""
Migration script to add album feature to the gallery system.
This script adds the necessary database tables and columns for album functionality.
"""

import mysql.connector
from mysql.connector import Error
import sys
import os
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '173915Snow',  # Từ app.py
    'database': 'hoa_huong_duong'  # Từ app.py
}

def create_connection():
    """Tạo kết nối đến MySQL database"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("✅ Kết nối database thành công!")
            return connection
    except Error as e:
        print(f"❌ Lỗi kết nối database: {e}")
        return None

def execute_migration(connection):
    """Thực hiện migration"""
    cursor = connection.cursor()
    
    try:
        print("🚀 Bắt đầu migration...")
        
        # 1. Tạo bảng gallery_album
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
        
        # 2. Thêm cột album_id vào bảng gallery
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
        
        # 3. Thêm foreign key constraints
        print("📝 Thêm foreign key constraints...")
        try:
            # Foreign key từ gallery.album_id -> gallery_album.id
            fk_gallery_album_query = """
            ALTER TABLE gallery 
            ADD CONSTRAINT fk_gallery_album 
            FOREIGN KEY (album_id) REFERENCES gallery_album(id) 
            ON DELETE SET NULL ON UPDATE CASCADE;
            """
            cursor.execute(fk_gallery_album_query)
        except Error as e:
            if "Duplicate foreign key constraint name" in str(e) or "foreign key constraint already exists" in str(e):
                print("⚠️  Foreign key fk_gallery_album đã tồn tại, bỏ qua...")
            else:
                print(f"⚠️  Lỗi tạo foreign key gallery->album: {e}")
        
        try:
            # Foreign key từ gallery_album.cover_image_id -> gallery.id  
            fk_album_cover_query = """
            ALTER TABLE gallery_album 
            ADD CONSTRAINT fk_album_cover_image 
            FOREIGN KEY (cover_image_id) REFERENCES gallery(id) 
            ON DELETE SET NULL ON UPDATE CASCADE;
            """
            cursor.execute(fk_album_cover_query)
        except Error as e:
            if "Duplicate foreign key constraint name" in str(e) or "foreign key constraint already exists" in str(e):
                print("⚠️  Foreign key fk_album_cover_image đã tồn tại, bỏ qua...")
            else:
                print(f"⚠️  Lỗi tạo foreign key album->cover: {e}")
        
        # 4. Commit tất cả thay đổi
        connection.commit()
        print("✅ Migration hoàn thành thành công!")
        
        # 5. Hiển thị thống kê
        cursor.execute("SELECT COUNT(*) FROM gallery WHERE album_id IS NULL")
        standalone_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM gallery_album")
        album_count = cursor.fetchone()[0]
        
        print(f"📊 Thống kê sau migration:")
        print(f"   - Ảnh đơn lẻ: {standalone_count}")
        print(f"   - Album: {album_count}")
        
    except Error as e:
        print(f"❌ Lỗi trong quá trình migration: {e}")
        connection.rollback()
        raise e
    finally:
        cursor.close()

def verify_migration(connection):
    """Kiểm tra migration đã thành công chưa"""
    cursor = connection.cursor()
    
    try:
        print("🔍 Kiểm tra migration...")
        
        # Kiểm tra bảng gallery_album
        cursor.execute("SHOW TABLES LIKE 'gallery_album'")
        if cursor.fetchone():
            print("✅ Bảng gallery_album đã được tạo")
        else:
            print("❌ Bảng gallery_album chưa được tạo")
            return False
            
        # Kiểm tra cột album_id trong bảng gallery
        cursor.execute("DESCRIBE gallery")
        columns = [row[0] for row in cursor.fetchall()]
        if 'album_id' in columns:
            print("✅ Cột album_id đã được thêm vào bảng gallery")
        else:
            print("❌ Cột album_id chưa được thêm vào bảng gallery")
            return False
            
        print("✅ Migration đã được thực hiện thành công!")
        return True
        
    except Error as e:
        print(f"❌ Lỗi kiểm tra migration: {e}")
        return False
    finally:
        cursor.close()

def main():
    """Hàm chính"""
    print("🎯 Album Feature Migration Script")
    print("=" * 50)
    
    # Tạo kết nối
    connection = create_connection()
    if not connection:
        sys.exit(1)
    
    try:
        # Thực hiện migration
        execute_migration(connection)
        
        # Kiểm tra migration
        if verify_migration(connection):
            print("\n🎉 Migration hoàn thành thành công!")
            print("📋 Bạn có thể bắt đầu sử dụng tính năng album ngay bây giờ.")
            print("\n📌 Hướng dẫn sử dụng:")
            print("   1. Upload 1 ảnh → Tạo ảnh đơn lẻ")
            print("   2. Upload nhiều ảnh → Tự động tạo album")
            print("   3. Truy cập /admin/albums để quản lý album")
        else:
            print("\n❌ Migration không thành công!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Lỗi nghiêm trọng: {e}")
        sys.exit(1)
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("\n🔌 Đã đóng kết nối database")

if __name__ == "__main__":
    main()
