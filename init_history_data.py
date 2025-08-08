#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để khởi tạo dữ liệu mẫu cho phần lịch sử hình thành
"""

from app import app, db, HistorySection, HistoryEvent

def init_history_data():
    """Khởi tạo dữ liệu mẫu cho lịch sử"""
    
    with app.app_context():
        print("🚀 Bắt đầu khởi tạo dữ liệu lịch sử...")
        
        # 1. Tạo hoặc cập nhật History Section
        history_section = HistorySection.query.first()
        if not history_section:
            history_section = HistorySection()
            db.session.add(history_section)
        
        history_section.main_title = "Lịch sử hình thành"
        history_section.subtitle = "Hành trình 10 năm xây dựng và phát triển của Trường Mầm non Hoa Hướng Dương"
        history_section.is_active = True
        
        print("✅ Đã cập nhật thông tin chung phần lịch sử")
        
        # 2. Xóa dữ liệu cũ (nếu có)
        HistoryEvent.query.delete()
        print("🗑️ Đã xóa dữ liệu lịch sử cũ")
        
        # 3. Tạo các sự kiện lịch sử mẫu
        history_events = [
            {
                'year': '2014',
                'title': 'Thành lập trường',
                'description': 'Trường Mầm non Hoa Hướng Dương được thành lập với 50 học sinh và 8 giáo viên, khởi đầu cho hành trình giáo dục ý nghĩa. Với tầm nhìn trở thành ngôi trường mầm non hàng đầu, chúng tôi bắt đầu từ những bước đi đầu tiên.',
                'color': 'bg-primary',
                'order_index': 1,
                'is_active': True
            },
            {
                'year': '2016',
                'title': 'Đạt chuẩn chất lượng',
                'description': 'Trường đạt chuẩn chất lượng giáo dục mầm non cấp quận, khẳng định sự nỗ lực không ngừng trong việc nâng cao chất lượng giáo dục. Đây là bước đệm quan trọng cho những thành tựu lớn hơn.',
                'color': 'bg-blue-500',
                'order_index': 2,
                'is_active': True
            },
            {
                'year': '2017',
                'title': 'Mở rộng cơ sở vật chất',
                'description': 'Mở rộng cơ sở vật chất với khuôn viên rộng 2000m², bổ sung thêm các phòng học chuyên dụng, sân chơi hiện đại và khu vực sinh hoạt ngoài trời. Tạo môi trường học tập lý tưởng cho các em.',
                'color': 'bg-secondary',
                'order_index': 3,
                'is_active': True
            },
            {
                'year': '2019',
                'title': 'Ứng dụng công nghệ giáo dục',
                'description': 'Tiên phong ứng dụng công nghệ thông tin vào giảng dạy với hệ thống bảng tương tác thông minh, phần mềm học tập và ứng dụng quản lý học sinh hiện đại.',
                'color': 'bg-purple-500',
                'order_index': 4,
                'is_active': True
            },
            {
                'year': '2020',
                'title': 'Đạt chuẩn quốc gia',
                'description': 'Trường đạt chuẩn mầm non quốc gia, khẳng định chất lượng giáo dục và cam kết phục vụ cộng đồng. Đây là thành tựu to lớn, ghi nhận sự đầu tư bài bản và chuyên nghiệp.',
                'color': 'bg-green-500',
                'order_index': 5,
                'is_active': True
            },
            {
                'year': '2022',
                'title': 'Chương trình giáo dục STEAM',
                'description': 'Ra mắt chương trình giáo dục STEAM (Science, Technology, Engineering, Arts, Mathematics) đầu tiên tại khu vực, giúp trẻ phát triển tư duy logic và sáng tạo từ sớm.',
                'color': 'bg-indigo-500',
                'order_index': 6,
                'is_active': True
            },
            {
                'year': '2024',
                'title': 'Phát triển vượt bậc',
                'description': 'Với hơn 200 học sinh và 25 giáo viên chuyên nghiệp, trường tiếp tục đổi mới và nâng cao chất lượng giáo dục. Mở rộng thêm các chương trình ngoại khóa và hoạt động phát triển kỹ năng sống.',
                'color': 'bg-pink-500',
                'order_index': 7,
                'is_active': True
            }
        ]
        
        # Thêm từng sự kiện vào database
        for event_data in history_events:
            event = HistoryEvent(**event_data)
            db.session.add(event)
            print(f"✅ Đã thêm sự kiện: {event_data['year']} - {event_data['title']}")
        
        # Lưu tất cả thay đổi
        db.session.commit()
        
        print(f"\n🎉 HOÀN THÀNH! Đã tạo {len(history_events)} sự kiện lịch sử")
        print("📋 Danh sách sự kiện đã tạo:")
        
        for i, event in enumerate(history_events, 1):
            print(f"   {i}. {event['year']} - {event['title']}")
        
        print(f"\n🔗 Kiểm tra kết quả:")
        print(f"   - Admin panel: http://127.0.0.1:5000/admin/history")
        print(f"   - Trang giới thiệu: http://127.0.0.1:5000/gioi-thieu")

if __name__ == "__main__":
    init_history_data()
