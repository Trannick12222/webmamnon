#!/usr/bin/env python3
"""
Script khởi tạo bảng user_submitted_images
"""

import os
import sys
from app import app, db

def main():
    """Hàm chính"""
    print("🖼️  Khởi tạo bảng User Submitted Images")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Tạo bảng mới
            db.create_all()
            print("✅ Đã tạo bảng user_submitted_images")
            
            # Tạo thư mục upload nếu chưa có
            upload_folder = os.path.join('static', 'uploads', 'user_submissions')
            os.makedirs(upload_folder, exist_ok=True)
            print("✅ Đã tạo thư mục uploads/user_submissions")
            
            print("\n🎉 Hoàn thành khởi tạo!")
            print("👉 Bây giờ người dùng có thể:")
            print("   • Gửi hình ảnh tại /chia-se-hinh-anh")
            print("   • Admin xem xét tại /admin/user-images")
            
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            sys.exit(1)

if __name__ == '__main__':
    main()

