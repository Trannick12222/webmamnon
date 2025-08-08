#!/usr/bin/env python3
"""
Script to initialize Special Programs data
Run this after creating the database to populate default Special Programs data
"""

from app import app, db, SpecialProgram

def init_special_programs_data():
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if Special Programs already exist
        if not SpecialProgram.query.first():
            # Create default Special Programs
            special_programs_data = [
                {
                    'title': 'Tiếng Anh cho trẻ em',
                    'description': 'Học tiếng Anh qua các hoạt động vui chơi, bài hát và trò chơi tương tác.',
                    'icon_class': 'fas fa-language',
                    'background_gradient': 'from-blue-50 to-purple-50',
                    'border_color': 'border-blue-200',
                    'icon_bg_color': 'bg-blue-500',
                    'features': '• Giáo viên bản ngữ\n• Lớp học nhỏ (6-8 trẻ)\n• Phương pháp TPR',
                    'order_index': 1
                },
                {
                    'title': 'Mỹ thuật sáng tạo',
                    'description': 'Phát triển khả năng sáng tạo và thẩm mỹ qua các hoạt động vẽ, nặn, thủ công.',
                    'icon_class': 'fas fa-paint-brush',
                    'background_gradient': 'from-green-50 to-yellow-50',
                    'border_color': 'border-green-200',
                    'icon_bg_color': 'bg-green-500',
                    'features': '• Vật liệu an toàn cho trẻ\n• Kỹ thuật đa dạng\n• Triển lãm tác phẩm',
                    'order_index': 2
                },
                {
                    'title': 'Âm nhạc & Múa',
                    'description': 'Phát triển năng khiếu âm nhạc và vận động thông qua các bài hát, điệu múa.',
                    'icon_class': 'fas fa-music',
                    'background_gradient': 'from-pink-50 to-red-50',
                    'border_color': 'border-pink-200',
                    'icon_bg_color': 'bg-pink-500',
                    'features': '• Nhạc cụ phù hợp trẻ em\n• Múa dân gian & hiện đại\n• Biểu diễn cuối khóa',
                    'order_index': 3
                },
                {
                    'title': 'Thể thao & Vận động',
                    'description': 'Phát triển thể chất và kỹ năng vận động qua các hoạt động thể thao phù hợp.',
                    'icon_class': 'fas fa-running',
                    'background_gradient': 'from-purple-50 to-indigo-50',
                    'border_color': 'border-purple-200',
                    'icon_bg_color': 'bg-purple-500',
                    'features': '• Bơi lội cơ bản\n• Yoga trẻ em\n• Các trò chơi vận động',
                    'order_index': 4
                },
                {
                    'title': 'Khoa học khám phá',
                    'description': 'Khơi dậy tò mò và khả năng tư duy logic qua các thí nghiệm khoa học đơn giản.',
                    'icon_class': 'fas fa-flask',
                    'background_gradient': 'from-yellow-50 to-orange-50',
                    'border_color': 'border-yellow-200',
                    'icon_bg_color': 'bg-yellow-500',
                    'features': '• Thí nghiệm an toàn\n• Quan sát thiên nhiên\n• Tư duy logic',
                    'order_index': 5
                },
                {
                    'title': 'Kỹ năng sống',
                    'description': 'Dạy trẻ các kỹ năng cần thiết trong cuộc sống hàng ngày và giao tiếp xã hội.',
                    'icon_class': 'fas fa-heart',
                    'background_gradient': 'from-rose-50 to-pink-50',
                    'border_color': 'border-rose-200',
                    'icon_bg_color': 'bg-rose-500',
                    'features': '• Tự phục vụ bản thân\n• Giao tiếp lịch sự\n• Làm việc nhóm',
                    'order_index': 6
                }
            ]
            
            for program_data in special_programs_data:
                special_program = SpecialProgram(**program_data, is_active=True)
                db.session.add(special_program)
            
            print("✅ Created default Special Programs")
        else:
            print("ℹ️  Special Programs already exist")
        
        # Commit all changes
        db.session.commit()
        print("🎉 Special Programs data initialized successfully!")

if __name__ == '__main__':
    init_special_programs_data()
