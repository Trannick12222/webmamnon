#!/usr/bin/env python3
"""
Script để cập nhật database Railway với bảng page_visit mới
"""

import os
import mysql.connector
from datetime import datetime

# Thông tin kết nối Railway MySQL
RAILWAY_CONFIG = {
    'host': 'crossover.proxy.rlwy.net',
    'port': 29685,
    'user': 'root',
    'password': 'JUMlghRDGtVSaVSZoLgpelgXeTfNpAbp',
    'database': 'railway',
    'charset': 'utf8mb4'
}

def create_page_visit_table():
    """Tạo bảng page_visit trên Railway database"""
    
    # SQL để tạo bảng page_visit
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS page_visit (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ip_address VARCHAR(45) NULL COMMENT 'Hỗ trợ IPv6',
        user_agent TEXT NULL COMMENT 'Thông tin trình duyệt',
        page_url VARCHAR(500) NULL COMMENT 'URL trang được truy cập',
        referrer VARCHAR(500) NULL COMMENT 'Trang giới thiệu',
        visit_date DATE NULL COMMENT 'Ngày truy cập',
        visit_time DATETIME NULL COMMENT 'Thời gian truy cập',
        is_unique BOOLEAN DEFAULT TRUE COMMENT 'Lượt truy cập duy nhất trong ngày',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_ip_date (ip_address, visit_date),
        INDEX idx_visit_date (visit_date),
        INDEX idx_visit_time (visit_time)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    
    try:
        print("🔗 Đang kết nối đến Railway MySQL...")
        
        # Kết nối đến database
        connection = mysql.connector.connect(**RAILWAY_CONFIG)
        cursor = connection.cursor()
        
        print("✅ Kết nối thành công!")
        
        # Tạo bảng page_visit
        print("📊 Đang tạo bảng page_visit...")
        cursor.execute(create_table_sql)
        
        # Kiểm tra bảng đã được tạo
        cursor.execute("SHOW TABLES LIKE 'page_visit'")
        result = cursor.fetchone()
        
        if result:
            print("✅ Bảng page_visit đã được tạo thành công!")
            
            # Hiển thị cấu trúc bảng
            print("\n📋 Cấu trúc bảng page_visit:")
            cursor.execute("DESCRIBE page_visit")
            columns = cursor.fetchall()
            
            print("┌─────────────────┬─────────────────┬──────┬─────┬─────────┬────────────────┐")
            print("│ Field           │ Type            │ Null │ Key │ Default │ Extra          │")
            print("├─────────────────┼─────────────────┼──────┼─────┼─────────┼────────────────┤")
            
            for column in columns:
                field = column[0][:15].ljust(15)
                type_info = column[1][:15].ljust(15)
                null_info = column[2][:4].ljust(4)
                key_info = column[3][:3].ljust(3)
                default_info = str(column[4])[:7].ljust(7) if column[4] else "NULL".ljust(7)
                extra_info = column[5][:14].ljust(14)
                
                print(f"│ {field} │ {type_info} │ {null_info} │ {key_info} │ {default_info} │ {extra_info} │")
            
            print("└─────────────────┴─────────────────┴──────┴─────┴─────────┴────────────────┘")
            
            # Kiểm tra số lượng bản ghi hiện tại
            cursor.execute("SELECT COUNT(*) FROM page_visit")
            count = cursor.fetchone()[0]
            print(f"\n📈 Số lượng bản ghi hiện tại: {count}")
            
        else:
            print("❌ Không thể tạo bảng page_visit!")
            
    except mysql.connector.Error as err:
        print(f"❌ Lỗi MySQL: {err}")
        return False
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
        print("🔌 Đã đóng kết nối database")
    
    return True

def test_connection():
    """Test kết nối đến Railway database"""
    try:
        print("🧪 Đang test kết nối...")
        connection = mysql.connector.connect(**RAILWAY_CONFIG)
        cursor = connection.cursor()
        
        # Test query
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        print(f"✅ Kết nối thành công! MySQL version: {version}")
        
        # Hiển thị danh sách bảng hiện có
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"\n📋 Danh sách bảng hiện có ({len(tables)} bảng):")
        for table in tables:
            print(f"  - {table[0]}")
            
        cursor.close()
        connection.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ Lỗi kết nối: {err}")
        return False

if __name__ == "__main__":
    print("🚀 Railway Database Update Script")
    print("=" * 50)
    print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Mục tiêu: Tạo bảng page_visit cho tracking lượt truy cập")
    print()
    
    # Test kết nối trước
    if test_connection():
        print("\n" + "=" * 50)
        
        # Tạo bảng page_visit
        if create_page_visit_table():
            print("\n🎉 Cập nhật database thành công!")
            print("💡 Bây giờ website có thể tracking lượt truy cập!")
        else:
            print("\n💥 Cập nhật database thất bại!")
    else:
        print("\n💥 Không thể kết nối đến database!")
