#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from app import app, db, Program, News, Category, Event, Settings, ContactSettings

def fix_encoding():
    """Fix encoding issues in database"""
    with app.app_context():
        print("Starting to fix encoding issues...")
        
        # Fix Programs
        print("Fixing programs...")
        programs_data = [
            (1, 'Lớp Mầm (18-24 tháng)', 'Chương trình giáo dục cho trẻ 18-24 tháng tuổi, tập trung phát triển kỹ năng vận động thô, tinh và ngôn ngữ cơ bản.', '18-24 tháng', '2,500,000 VNĐ/tháng', 'Cả năm học'),
            (2, 'Lớp Chồi (2-3 tuổi)', 'Chương trình giáo dục toàn diện cho trẻ 2-3 tuổi với các hoạt động vui chơi, học tập và phát triển tính cách.', '2-3 tuổi', '2,800,000 VNĐ/tháng', 'Cả năm học'),
            (3, 'Lớp Lá (3-4 tuổi)', 'Chuẩn bị cho trẻ 3-4 tuổi với các kỹ năng cần thiết trước khi vào mẫu giáo lớn.', '3-4 tuổi', '3,000,000 VNĐ/tháng', 'Cả năm học'),
            (4, 'Lớp Lúa (4-5 tuổi)', 'Chương trình chuẩn bị vào lớp 1 cho trẻ 4-5 tuổi với các hoạt động học tập có hệ thống.', '4-5 tuổi', '3,200,000 VNĐ/tháng', 'Cả năm học'),
            (5, 'Lớp Ngoại ngữ', 'Lớp học tiếng Anh cho trẻ em từ 3-5 tuổi với phương pháp giảng dạy sinh động, phù hợp lứa tuổi.', '3-5 tuổi', '1,500,000 VNĐ/tháng', '3 buổi/tuần'),
            (6, 'Lớp Năng khiếu', 'Các lớp học năng khiếu như vẽ, múa, hát, đàn piano giúp phát triển tài năng của trẻ.', '3-5 tuổi', '1,000,000 VNĐ/tháng', '2 buổi/tuần'),
            (7, 'Lớp Chồi Non', 'Chương trình đặc biệt dành cho trẻ có năng khiếu xuất sắc.', 'Đa tuổi', '5,000,000 VNĐ/tháng', 'Cả năm học')
        ]
        
        for program_id, name, description, age_group, price, duration in programs_data:
            program = Program.query.get(program_id)
            if program:
                program.name = name
                program.description = description
                program.age_group = age_group
                program.price = price
                program.duration = duration
                print(f"Updated program {program_id}: {name}")
        
        # Fix News
        print("Fixing news...")
        news_data = [
            (1, 'Khai giảng năm học mới 2024-2025', 'Trường Mầm non Hoa Hướng Dương xin thông báo lễ khai giảng năm học mới 2024-2025 sẽ được tổ chức vào ngày 05/09/2024. Chương trình gồm có các hoạt động như chào cờ, phát biểu của Ban Giám hiệu, giới thiệu đội ngũ giáo viên mới và các hoạt động vui chơi cho các em học sinh.', 'Thông báo về lễ khai giảng năm học mới 2024-2025 diễn ra vào ngày 05/09/2024'),
            (2, 'Chương trình ngoại khóa tháng 10', 'Trong tháng 10, trường sẽ tổ chức nhiều hoạt động ngoại khóa bổ ích cho các em như: tham quan vườn bách thảo, học nấu ăn đơn giản, và các trò chơi tập thể. Các hoạt động này nhằm giúp trẻ phát triển toàn diện về thể chất lẫn tinh thần.', 'Các hoạt động ngoại khóa phong phú trong tháng 10 dành cho học sinh'),
            (3, 'Hội thảo nuôi dưỡng trẻ cho phụ huynh', 'Trường tổ chức hội thảo "Nuôi dưỡng và giáo dục trẻ mầm non" dành cho các bậc phụ huynh vào ngày 15/10/2024. Hội thảo do các chuyên gia tâm lý và dinh dưỡng trẻ em hàng đầu thực hiện, giúp cha mẹ hiểu rõ hơn về cách chăm sóc con trẻ ở độ tuổi mầm non.', 'Hội thảo bổ ích về nuôi dưỡng trẻ em dành cho phụ huynh')
        ]
        
        for news_id, title, content, summary in news_data:
            news = News.query.get(news_id)
            if news:
                news.title = title
                news.content = content
                news.summary = summary
                print(f"Updated news {news_id}: {title}")
        
        # Fix Categories
        print("Fixing categories...")
        categories_data = [
            (1, 'Hoạt động học tập'),
            (2, 'Sự kiện trường'),
            (3, 'Thông báo'),
            (4, 'Tin tức chung')
        ]
        
        for cat_id, name in categories_data:
            category = Category.query.get(cat_id)
            if category:
                category.name = name
                print(f"Updated category {cat_id}: {name}")
        
        # Fix Events
        print("Fixing events...")
        events_data = [
            (1, 'Lễ Trung Thu 2024', 'Tổ chức đêm hội Trung Thu với nhiều hoạt động vui chơi, múa lân, thưởng thức bánh kẹo và đèn lồng cho các em học sinh.', 'Sân trường Hoa Hướng Dương'),
            (2, 'Ngày hội thể thao', 'Ngày hội thể thao năm 2024 với các môn thi đấu phù hợp lứa tuổi mầm non như chạy, nhảy bao bố, kéo co.', 'Sân vận động trường'),
            (3, 'Biểu diễn cuối năm', 'Chương trình biểu diễn văn nghệ cuối năm học với sự tham gia của tất cả các lớp, thể hiện những gì các em đã học được.', 'Hội trường trường học')
        ]
        
        for event_id, title, description, location in events_data:
            event = Event.query.get(event_id)
            if event:
                event.title = title
                event.description = description
                event.location = location
                print(f"Updated event {event_id}: {title}")
        
        # Fix Settings
        print("Fixing settings...")
        settings_data = [
            ('school_name', 'Trường Mầm non Hoa Hướng Dương'),
            ('school_address', '123 Đường Hoa Hướng Dương, Quận 1, TP.HCM'),
            ('school_hours', 'Thứ 2 - Thứ 6: 7:00 - 17:00'),
            ('school_motto', 'Nuôi dưỡng tâm hồn - Phát triển tài năng')
        ]
        
        for key, value in settings_data:
            setting = Settings.query.filter_by(setting_key=key).first()
            if setting:
                setting.setting_value = value
                print(f"Updated setting {key}: {value}")
        
        # Fix Contact Settings
        print("Fixing contact settings...")
        contact_settings_data = [
            ('phone_main', 'Số điện thoại chính', 'Hotline tư vấn và hỗ trợ'),
            ('email_main', 'Email chính', 'Email liên hệ chính thức'),
            ('facebook', 'Facebook', 'Trang Facebook chính thức của trường'),
            ('zalo', 'Zalo', 'Chat Zalo để tư vấn nhanh'),
            ('youtube', 'YouTube', 'Kênh YouTube với các hoạt động của trường')
        ]
        
        for key, display_name, description in contact_settings_data:
            contact_setting = ContactSettings.query.filter_by(setting_key=key).first()
            if contact_setting:
                contact_setting.display_name = display_name
                contact_setting.description = description
                print(f"Updated contact setting {key}: {display_name}")
        
        # Commit all changes
        try:
            db.session.commit()
            print("✅ All encoding fixes applied successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error applying fixes: {e}")

if __name__ == '__main__':
    fix_encoding()
