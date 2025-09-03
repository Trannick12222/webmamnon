#!/usr/bin/env python3
"""
Script khởi tạo dữ liệu mẫu cho Age Groups, Program Features và Program Info
"""

import os
import sys
from app import app, db, AgeGroup, ProgramFeature, ProgramInfo

def init_age_groups():
    """Khởi tạo dữ liệu mẫu cho Age Groups"""
    print("🎯 Khởi tạo Age Groups...")
    
    age_groups_data = [
        {
            'name': 'Lớp Mầm',
            'age_range': '18-24 tháng',
            'description': 'Chương trình giáo dục cho trẻ nhỏ nhất, tập trung phát triển các kỹ năng cơ bản',
            'icon_class': 'fas fa-baby',
            'icon_bg_color': 'bg-pink-100',
            'icon_text_color': 'text-pink-600',
            'skills': '• Phát triển vận động cơ bản\n• Học tự lập trong ăn uống\n• Giao tiếp đơn giản\n• Khám phá thế giới xung quanh',
            'order_index': 1
        },
        {
            'name': 'Lớp Chồi',
            'age_range': '2-3 tuổi',
            'description': 'Phát triển toàn diện với các hoạt động vui chơi và học tập phù hợp',
            'icon_class': 'fas fa-seedling',
            'icon_bg_color': 'bg-green-100',
            'icon_text_color': 'text-green-600',
            'skills': '• Phân biệt màu sắc, hình khối\n• Học quy tắc xã hội cơ bản\n• Phát triển từ vựng\n• Hoạt động nghệ thuật đơn giản',
            'order_index': 2
        },
        {
            'name': 'Lớp Lá',
            'age_range': '3-4 tuổi',
            'description': 'Chuẩn bị cho trẻ với các kỹ năng cần thiết trước khi vào mẫu giáo lớn',
            'icon_class': 'fas fa-leaf',
            'icon_bg_color': 'bg-blue-100',
            'icon_text_color': 'text-blue-600',
            'skills': '• Học đếm số cơ bản\n• Kể chuyện và nghe hiểu\n• Hoạt động nhóm\n• Rèn luyện tính kỷ luật',
            'order_index': 3
        },
        {
            'name': 'Lớp Lúa',
            'age_range': '4-5 tuổi',
            'description': 'Chuẩn bị toàn diện cho việc vào lớp 1 với đầy đủ kỹ năng cần thiết',
            'icon_class': 'fas fa-graduation-cap',
            'icon_bg_color': 'bg-yellow-100',
            'icon_text_color': 'text-yellow-600',
            'skills': '• Chuẩn bị vào lớp 1\n• Học chữ cái, số đếm\n• Kỹ năng tự phục vụ\n• Phát triển tư duy logic',
            'order_index': 4
        }
    ]
    
    for data in age_groups_data:
        existing = AgeGroup.query.filter_by(name=data['name']).first()
        if not existing:
            age_group = AgeGroup(**data)
            db.session.add(age_group)
            print(f"  ✅ Đã tạo: {data['name']} ({data['age_range']})")
        else:
            print(f"  ⏭️  Đã tồn tại: {data['name']}")
    
    db.session.commit()

def init_program_features():
    """Khởi tạo dữ liệu mẫu cho Program Features"""
    print("🌟 Khởi tạo Program Features...")
    
    features_data = [
        {
            'title': 'Phát triển toàn diện',
            'icon_class': 'fas fa-check-circle',
            'background_gradient': 'from-green-100 to-emerald-100',
            'text_color': 'text-green-800',
            'border_color': 'border-green-200',
            'order_index': 1
        },
        {
            'title': 'Học qua chơi',
            'icon_class': 'fas fa-gamepad',
            'background_gradient': 'from-purple-100 to-pink-100',
            'text_color': 'text-purple-800',
            'border_color': 'border-purple-200',
            'order_index': 2
        },
        {
            'title': 'Môi trường an toàn',
            'icon_class': 'fas fa-shield-alt',
            'background_gradient': 'from-orange-100 to-yellow-100',
            'text_color': 'text-orange-800',
            'border_color': 'border-orange-200',
            'order_index': 3
        }
    ]
    
    for data in features_data:
        existing = ProgramFeature.query.filter_by(title=data['title']).first()
        if not existing:
            feature = ProgramFeature(**data)
            db.session.add(feature)
            print(f"  ✅ Đã tạo: {data['title']}")
        else:
            print(f"  ⏭️  Đã tồn tại: {data['title']}")
    
    db.session.commit()

def init_program_info():
    """Khởi tạo dữ liệu mẫu cho Program Info"""
    print("📋 Khởi tạo Program Info...")
    
    info_data = [
        {
            'title': 'Lớp học nhỏ (8-12 trẻ)',
            'icon_class': 'fas fa-users',
            'icon_bg_gradient': 'from-purple-400 to-pink-500',
            'order_index': 1
        },
        {
            'title': 'Giáo viên có chứng chỉ',
            'icon_class': 'fas fa-certificate',
            'icon_bg_gradient': 'from-yellow-400 to-orange-500',
            'order_index': 2
        }
    ]
    
    for data in info_data:
        existing = ProgramInfo.query.filter_by(title=data['title']).first()
        if not existing:
            info = ProgramInfo(**data)
            db.session.add(info)
            print(f"  ✅ Đã tạo: {data['title']}")
        else:
            print(f"  ⏭️  Đã tồn tại: {data['title']}")
    
    db.session.commit()

def main():
    """Hàm chính"""
    print("🌻 Khởi tạo dữ liệu Program cho Website Mầm non")
    print("=" * 60)
    
    with app.app_context():
        try:
            # Tạo bảng nếu chưa có
            db.create_all()
            print("✅ Database đã được khởi tạo")
            
            # Khởi tạo dữ liệu
            init_age_groups()
            init_program_features()
            init_program_info()
            
            print("\n🎉 Hoàn thành khởi tạo dữ liệu!")
            print("👉 Bây giờ bạn có thể:")
            print("   • Truy cập /admin/age-groups để quản lý nhóm độ tuổi")
            print("   • Truy cập /admin/program-features để quản lý điểm nổi bật")
            print("   • Truy cập /admin/program-info để quản lý thông tin chương trình")
            print("   • Xem kết quả tại /chuong-trinh")
            
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            sys.exit(1)

if __name__ == '__main__':
    main()

