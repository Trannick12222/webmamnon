#!/usr/bin/env python3
"""
Railway deployment setup script
Khởi tạo database và dữ liệu mặc định cho Railway
"""

import os
import sys
from app import app, db, init_default_themes

def setup_database():
    """Khởi tạo database và dữ liệu mặc định"""
    with app.app_context():
        try:
            print("🚀 Starting Railway database setup...")
            
            # Tạo thư mục uploads nếu chưa có
            print("📁 Creating upload directories...")
            upload_dirs = [
                'static/uploads',
                'static/uploads/gallery', 
                'static/uploads/news',
                'static/uploads/programs',
                'static/uploads/special_programs',
                'static/uploads/slider',
                'static/uploads/events',
                'static/uploads/history',
                'static/uploads/mission',
                'static/uploads/team',
                'static/uploads/videos',
                'static/uploads/editor'
            ]
            
            for dir_path in upload_dirs:
                os.makedirs(dir_path, exist_ok=True)
                print(f"  ✅ Created {dir_path}")
            
            # Tạo tất cả các bảng
            print("📊 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Khởi tạo themes mặc định
            print("🎨 Initializing default themes...")
            init_default_themes()
            print("✅ Default themes initialized successfully")
            
            # Kiểm tra themes đã được tạo
            from app import ThemeSettings
            themes = ThemeSettings.query.all()
            print(f"✅ Created {len(themes)} themes")
            
            for theme in themes:
                status = "🟢 ACTIVE" if theme.is_active else "⚪ INACTIVE"
                default = "⭐ DEFAULT" if theme.is_default else ""
                print(f"  - {theme.theme_name} {status} {default}")
            
            print("🎉 Railway setup completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)
