#!/usr/bin/env python3
"""
Khởi chạy ứng dụng website Trường Mầm non Hoa Hướng Dương
"""

import os
import sys
from app import app, db
from werkzeug.security import generate_password_hash

def create_admin_user():
    """Tạo tài khoản admin mặc định"""
    from app import User
    
    # Kiểm tra xem đã có admin chưa
    existing_admin = User.query.filter_by(username='admin').first()
    if not existing_admin:
        admin = User(
            username='admin',
            email='admin@hoahuongduong.edu.vn',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Đã tạo tài khoản admin mặc định")
        print("   Username: admin")
        print("   Password: admin123")
    else:
        print("✅ Tài khoản admin đã tồn tại")

def create_directories():
    """Tạo các thư mục cần thiết"""
    directories = [
        'static/uploads',
        'static/uploads/news',
        'static/uploads/programs', 
        'static/uploads/gallery',
        'static/uploads/events'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Đã tạo các thư mục cần thiết")

def check_requirements():
    """Kiểm tra các yêu cầu cần thiết"""
    try:
        import mysql.connector
        print("✅ MySQL connector đã cài đặt")
    except ImportError:
        print("❌ Chưa cài đặt mysql-connector-python")
        print("   Chạy: pip install mysql-connector-python")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow đã cài đặt")
    except ImportError:
        print("❌ Chưa cài đặt Pillow")
        print("   Chạy: pip install Pillow")
        return False
    
    return True

def main():
    """Hàm chính"""
    print("🌻 Khởi động Website Trường Mầm non Hoa Hướng Dương")
    print("=" * 60)
    
    # Kiểm tra yêu cầu
    if not check_requirements():
        sys.exit(1)
    
    # Tạo các thư mục
    create_directories()
    
    # Khởi tạo database và tạo bảng
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database đã được khởi tạo")
            
            # Tạo admin user
            create_admin_user()
            
        except Exception as e:
            print(f"❌ Lỗi database: {e}")
            print("   Kiểm tra kết nối MySQL và cấu hình trong .env")
            sys.exit(1)
    
    print("\n🚀 Khởi động server...")
    print(f"📱 Website: http://localhost:5000")
    print(f"🔧 Admin: http://localhost:5000/admin")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n👋 Nhấn Ctrl+C để dừng server")
    print("=" * 60)
    
    # Khởi chạy ứng dụng
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 Đã dừng server")
    except Exception as e:
        print(f"❌ Lỗi khởi chạy: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()