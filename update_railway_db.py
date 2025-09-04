#!/usr/bin/env python3
"""
Script để cập nhật Railway database với các models mới
Sử dụng thông tin từ Railway environment variables
"""

import os
import mysql.connector
from mysql.connector import Error

# Railway Database Configuration
RAILWAY_DB_CONFIG = {
    'host': 'crossover.proxy.rlwy.net',
    'port': 29685,
    'user': 'root',
    'password': 'JUMlghRDGtVSaVSZoLgpelgXeTfNpAbp',
    'database': 'railway'
}

def create_railway_database():
    """Tạo database Railway nếu chưa có"""
    try:
        # Kết nối không chỉ định database
        connection = mysql.connector.connect(
            host=RAILWAY_DB_CONFIG['host'],
            port=RAILWAY_DB_CONFIG['port'],
            user=RAILWAY_DB_CONFIG['user'],
            password=RAILWAY_DB_CONFIG['password']
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Tạo database nếu chưa có
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {RAILWAY_DB_CONFIG['database']}")
            print(f"✅ Database '{RAILWAY_DB_CONFIG['database']}' đã sẵn sàng")
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"❌ Lỗi kết nối database: {e}")
        return False
    
    return True

def create_new_tables():
    """Tạo các tables mới trên Railway"""
    try:
        connection = mysql.connector.connect(**RAILWAY_DB_CONFIG)
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            print("🔄 Đang tạo các tables mới...")
            
            # 1. UserSubmittedImage table
            user_submitted_images_sql = """
            CREATE TABLE IF NOT EXISTS user_submitted_images (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sender_name VARCHAR(100) NOT NULL,
                sender_email VARCHAR(120) NOT NULL,
                sender_phone VARCHAR(20),
                title VARCHAR(200),
                description TEXT,
                image_path VARCHAR(500) NOT NULL,
                original_filename VARCHAR(200),
                status VARCHAR(20) DEFAULT 'pending',
                admin_note TEXT,
                reviewed_by VARCHAR(100),
                reviewed_at DATETIME,
                file_size INT,
                mime_type VARCHAR(50),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            # 2. AgeGroup table
            age_groups_sql = """
            CREATE TABLE IF NOT EXISTS age_groups (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age_range VARCHAR(50) NOT NULL,
                description TEXT,
                icon_class VARCHAR(100) DEFAULT 'fas fa-baby',
                icon_bg_color VARCHAR(50) DEFAULT 'bg-pink-100',
                icon_text_color VARCHAR(50) DEFAULT 'text-pink-600',
                skills TEXT,
                order_index INT DEFAULT 0,
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            # 3. ProgramFeature table
            program_features_sql = """
            CREATE TABLE IF NOT EXISTS program_features (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                icon_class VARCHAR(100) DEFAULT 'fas fa-check-circle',
                background_gradient VARCHAR(100) DEFAULT 'from-green-100 to-emerald-100',
                text_color VARCHAR(50) DEFAULT 'text-green-800',
                border_color VARCHAR(50) DEFAULT 'border-green-200',
                order_index INT DEFAULT 0,
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            # 4. ProgramInfo table
            program_info_sql = """
            CREATE TABLE IF NOT EXISTS program_info (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                icon_class VARCHAR(100) DEFAULT 'fas fa-users',
                icon_bg_gradient VARCHAR(100) DEFAULT 'from-purple-400 to-pink-500',
                order_index INT DEFAULT 0,
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            # Thực thi tạo tables
            tables_sql = [
                ("user_submitted_images", user_submitted_images_sql),
                ("age_groups", age_groups_sql),
                ("program_features", program_features_sql),
                ("program_info", program_info_sql)
            ]
            
            for table_name, sql in tables_sql:
                try:
                    cursor.execute(sql)
                    print(f"✅ Table '{table_name}' đã được tạo")
                except Error as e:
                    if "already exists" in str(e).lower():
                        print(f"ℹ️  Table '{table_name}' đã tồn tại")
                    else:
                        print(f"❌ Lỗi tạo table '{table_name}': {e}")
            
            # Commit changes
            connection.commit()
            print("✅ Tất cả tables đã được tạo thành công!")
            
            cursor.close()
            connection.close()
            
            return True
            
    except Error as e:
        print(f"❌ Lỗi tạo tables: {e}")
        return False

def insert_sample_data():
    """Thêm dữ liệu mẫu vào các tables mới"""
    try:
        connection = mysql.connector.connect(**RAILWAY_DB_CONFIG)
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            print("🔄 Đang thêm dữ liệu mẫu...")
            
            # Sample data cho AgeGroup
            age_groups_data = [
                ("Nhóm 18-24 tháng", "18-24 tháng", "Nhóm tuổi đầu tiên, phát triển kỹ năng cơ bản", "fas fa-baby", "bg-pink-100", "text-pink-600", "Vận động cơ bản, nhận thức đơn giản", 1),
                ("Nhóm 25-36 tháng", "25-36 tháng", "Nhóm tuổi thứ hai, phát triển ngôn ngữ", "fas fa-child", "bg-blue-100", "text-blue-600", "Ngôn ngữ, giao tiếp, vận động", 2),
                ("Nhóm 37-48 tháng", "37-48 tháng", "Nhóm tuổi thứ ba, phát triển tư duy", "fas fa-users", "bg-green-100", "text-green-600", "Tư duy logic, sáng tạo, kỹ năng xã hội", 3),
                ("Nhóm 49-60 tháng", "49-60 tháng", "Nhóm tuổi cuối, chuẩn bị vào lớp 1", "fas fa-graduation-cap", "bg-purple-100", "text-purple-600", "Chuẩn bị học tập, kỹ năng tự lập", 4)
            ]
            
            for age_group in age_groups_data:
                cursor.execute("""
                    INSERT IGNORE INTO age_groups (name, age_range, description, icon_class, icon_bg_color, icon_text_color, skills, order_index)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, age_group)
            
            # Sample data cho ProgramFeature
            program_features_data = [
                ("Giáo dục toàn diện", "fas fa-star", "from-blue-100 to-indigo-100", "text-blue-800", "border-blue-200", 1),
                ("Phát triển kỹ năng", "fas fa-heart", "from-green-100 to-emerald-100", "text-green-800", "border-green-200", 2),
                ("Môi trường an toàn", "fas fa-shield-alt", "from-yellow-100 to-orange-100", "text-yellow-800", "border-yellow-200", 3)
            ]
            
            for feature in program_features_data:
                cursor.execute("""
                    INSERT IGNORE INTO program_features (title, icon_class, background_gradient, text_color, border_color, order_index)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, feature)
            
            # Sample data cho ProgramInfo
            program_info_data = [
                ("Đội ngũ giáo viên", "fas fa-chalkboard-teacher", "from-purple-400 to-pink-500", 1),
                ("Cơ sở vật chất", "fas fa-building", "from-blue-400 to-cyan-500", 2)
            ]
            
            for info in program_info_data:
                cursor.execute("""
                    INSERT IGNORE INTO program_info (title, icon_class, icon_bg_gradient, order_index)
                    VALUES (%s, %s, %s, %s)
                """, info)
            
            # Commit changes
            connection.commit()
            print("✅ Dữ liệu mẫu đã được thêm thành công!")
            
            cursor.close()
            connection.close()
            
            return True
            
    except Error as e:
        print(f"❌ Lỗi thêm dữ liệu mẫu: {e}")
        return False

def verify_tables():
    """Kiểm tra xem các tables đã được tạo thành công chưa"""
    try:
        connection = mysql.connector.connect(**RAILWAY_DB_CONFIG)
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Kiểm tra tables
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            
            print("\n=== KIỂM TRA TABLES TRÊN RAILWAY ===")
            expected_tables = ['user_submitted_images', 'age_groups', 'program_features', 'program_info']
            
            for table in expected_tables:
                if table in tables:
                    # Kiểm tra số records
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"✅ {table}: {count} records")
                else:
                    print(f"❌ {table}: KHÔNG TỒN TẠI")
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"❌ Lỗi kiểm tra tables: {e}")

def main():
    """Main function để cập nhật Railway database"""
    print("🚀 BẮT ĐẦU CẬP NHẬT RAILWAY DATABASE")
    print("=" * 50)
    
    # Bước 1: Tạo database
    if not create_railway_database():
        print("❌ Không thể tạo database. Dừng cập nhật.")
        return
    
    # Bước 2: Tạo tables
    if not create_new_tables():
        print("❌ Không thể tạo tables. Dừng cập nhật.")
        return
    
    # Bước 3: Thêm dữ liệu mẫu
    if not insert_sample_data():
        print("❌ Không thể thêm dữ liệu mẫu.")
        return
    
    # Bước 4: Kiểm tra kết quả
    verify_tables()
    
    print("\n" + "=" * 50)
    print("🎉 CẬP NHẬT RAILWAY DATABASE HOÀN TẤT!")
    print("✅ Website đã sẵn sàng hoạt động trên Railway")

if __name__ == "__main__":
    main()

