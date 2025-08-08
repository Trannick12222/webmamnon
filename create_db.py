#!/usr/bin/env python3
"""
Script tạo database cho website Trường Mầm non Hoa Hướng Dương
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Tạo database và các bảng"""
    try:
        # Kết nối MySQL (không chỉ định database)
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', '127.0.0.1'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '!QAZxsw2#EDC')
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Tạo database
            database_name = os.getenv('DB_NAME', 'hoa_huong_duong')
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ Database '{database_name}' đã được tạo")
            
            # Chuyển sang database vừa tạo
            cursor.execute(f"USE {database_name}")
            
            # Đọc và thực thi file SQL
            with open('database_setup.sql', 'r', encoding='utf-8') as sql_file:
                sql_script = sql_file.read()
                
                # Tách các câu lệnh SQL
                sql_commands = sql_script.split(';')
                
                for command in sql_commands:
                    command = command.strip()
                    if command and not command.startswith('--') and not command.startswith('CREATE DATABASE'):
                        if command.startswith('USE'):
                            continue  # Bỏ qua lệnh USE
                        try:
                            cursor.execute(command)
                        except Error as e:
                            if "already exists" not in str(e):
                                print(f"⚠️  Cảnh báo: {e}")
            
            connection.commit()
            print("✅ Đã tạo tất cả bảng và dữ liệu mẫu")
            
    except Error as e:
        print(f"❌ Lỗi MySQL: {e}")
        if "Access denied" in str(e):
            print("\n💡 Hướng dẫn khắc phục:")
            print("1. Kiểm tra mật khẩu MySQL trong file .env")
            print("2. Hoặc đặt mật khẩu rỗng: DB_PASSWORD=")
            print("3. Hoặc chạy: mysql -u root -p")
            print("   Rồi tạo database bằng tay:")
            print("   CREATE DATABASE hoa_huong_duong CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        return False
        
    except FileNotFoundError:
        print("❌ Không tìm thấy file database_setup.sql")
        return False
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
    return True

if __name__ == '__main__':
    print("🗄️  Tạo database cho Website Trường Mầm non Hoa Hướng Dương")
    print("=" * 60)
    
    if create_database():
        print("\n🎉 Setup database hoàn tất!")
        print("📝 Bây giờ bạn có thể chạy: python run.py")
    else:
        print("\n❌ Setup database thất bại!")
        print("📝 Vui lòng kiểm tra lại cấu hình MySQL")