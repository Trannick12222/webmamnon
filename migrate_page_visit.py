#!/usr/bin/env python3
"""
Migration script để tạo bảng page_visit
Tương thích với cả local và Railway database
"""

import os
import sys
from datetime import datetime

def run_migration():
    """Chạy migration để tạo bảng page_visit"""
    try:
        # Import Flask app
        from app import app, db, PageVisit
        
        print("🚀 Page Visit Migration Script")
        print("=" * 50)
        print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Kiểm tra environment
        env = os.environ.get('RAILWAY_ENVIRONMENT', 'local')
        print(f"🌍 Environment: {env}")
        
        with app.app_context():
            # Kiểm tra xem bảng đã tồn tại chưa
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'page_visit' in tables:
                print("✅ Bảng page_visit đã tồn tại!")
                
                # Kiểm tra cấu trúc bảng
                columns = inspector.get_columns('page_visit')
                print(f"📋 Bảng có {len(columns)} cột:")
                for col in columns:
                    print(f"  - {col['name']}: {col['type']}")
                    
                # Đếm số bản ghi
                count = db.session.execute(db.text("SELECT COUNT(*) FROM page_visit")).scalar()
                print(f"📊 Số bản ghi hiện tại: {count}")
                
            else:
                print("📊 Đang tạo bảng page_visit...")
                
                # Tạo bảng
                db.create_all()
                
                # Kiểm tra lại
                inspector = db.inspect(db.engine)
                tables = inspector.get_table_names()
                
                if 'page_visit' in tables:
                    print("✅ Tạo bảng page_visit thành công!")
                    
                    # Hiển thị cấu trúc
                    columns = inspector.get_columns('page_visit')
                    print(f"📋 Bảng có {len(columns)} cột:")
                    for col in columns:
                        print(f"  - {col['name']}: {col['type']}")
                else:
                    print("❌ Không thể tạo bảng page_visit!")
                    return False
        
        print("\n🎉 Migration hoàn thành thành công!")
        return True
        
    except ImportError as e:
        print(f"❌ Lỗi import: {e}")
        print("💡 Đảm bảo bạn đang chạy script từ thư mục chứa app.py")
        return False
        
    except Exception as e:
        print(f"❌ Lỗi migration: {e}")
        return False

def check_tracking_functionality():
    """Kiểm tra tính năng tracking có hoạt động không"""
    try:
        from app import app, db, PageVisit
        
        print("\n🧪 Đang test tính năng tracking...")
        
        with app.app_context():
            # Tạo một bản ghi test
            test_visit = PageVisit(
                ip_address='127.0.0.1',
                user_agent='Migration Test Script',
                page_url='/test-migration',
                referrer='',
                is_unique=True
            )
            
            db.session.add(test_visit)
            db.session.commit()
            
            # Kiểm tra bản ghi đã được tạo
            count = PageVisit.query.count()
            print(f"✅ Test thành công! Tổng số bản ghi: {count}")
            
            # Xóa bản ghi test
            db.session.delete(test_visit)
            db.session.commit()
            
            print("🧹 Đã xóa dữ liệu test")
            
        return True
        
    except Exception as e:
        print(f"❌ Lỗi test tracking: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Starting Page Visit Migration...")
    
    # Chạy migration
    if run_migration():
        # Test tính năng
        if check_tracking_functionality():
            print("\n✨ Tất cả đều hoạt động tốt!")
            print("💡 Bây giờ website có thể tracking lượt truy cập!")
            print("🌐 Truy cập /admin để xem thống kê")
        else:
            print("\n⚠️  Migration thành công nhưng có vấn đề với tracking")
    else:
        print("\n💥 Migration thất bại!")
        sys.exit(1)

