#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script khởi tạo TOÀN BỘ dữ liệu mẫu cho website Trường Mầm non Hoa Hướng Dương
"""

from app import app, db
from app import (User, News, Program, Gallery, Event, Contact, Slider, 
                ContactSettings, TeamMember, MissionItem, MissionContent,
                HistorySection, HistoryEvent, AboutSection, AboutStats,
                FAQ, SpecialProgram, CallToAction, IntroVideo)
from datetime import datetime, timedelta
import random

def clear_all_data():
    """Xóa toàn bộ dữ liệu cũ (trừ User admin)"""
    print("🗑️ Đang xóa dữ liệu cũ...")
    
    # Xóa tất cả dữ liệu (trừ User)
    News.query.delete()
    Program.query.delete()
    Gallery.query.delete()
    Event.query.delete()
    Contact.query.delete()
    Slider.query.delete()
    TeamMember.query.delete()
    MissionItem.query.delete()
    MissionContent.query.delete()
    HistoryEvent.query.delete()
    HistorySection.query.delete()
    AboutStats.query.delete()
    AboutSection.query.delete()
    FAQ.query.delete()
    SpecialProgram.query.delete()
    CallToAction.query.delete()
    IntroVideo.query.delete()
    
    db.session.commit()
    print("✅ Đã xóa dữ liệu cũ")

def create_news_data():
    """Tạo dữ liệu tin tức"""
    print("📰 Tạo dữ liệu tin tức...")
    
    news_data = [
        {
            'title': 'Khai giảng năm học mới 2024-2025 - Chào đón 150 học sinh mới',
            'content': '''
            <h2>Lễ khai giảng năm học 2024-2025</h2>
            <p>Sáng ngày 05/09/2024, Trường Mầm non Hoa Hướng Dương đã tổ chức lễ khai giảng năm học mới 2024-2025 với sự tham gia của hơn 200 phụ huynh và 150 học sinh mới.</p>
            
            <h3>Chương trình lễ khai giảng</h3>
            <ul>
                <li>Chào cờ và hát quốc ca</li>
                <li>Phát biểu của Ban Giám hiệu</li>
                <li>Giới thiệu đội ngũ giáo viên mới</li>
                <li>Hoạt động vui chơi cho các em</li>
                <li>Trao quà cho học sinh mới</li>
            </ul>
            
            <p>Năm học này, trường đã đầu tư thêm nhiều trang thiết bị hiện đại và mở rộng không gian học tập để phục vụ tốt hơn cho các em học sinh.</p>
            
            <blockquote>
                <p>"Chúng tôi cam kết mang đến cho các em một môi trường học tập an toàn, vui tươi và phát triển toàn diện" - Cô Nguyễn Thị Lan, Hiệu trưởng</p>
            </blockquote>
            ''',
            'summary': 'Trường Mầm non Hoa Hướng Dương tổ chức lễ khai giảng năm học 2024-2025 với nhiều hoạt động ý nghĩa và chào đón 150 học sinh mới.',
            'featured_image': 'uploads/news/khai-giang-2024.jpg',
            'is_published': True,
            'publish_date': datetime.now() - timedelta(days=5)
        },
        {
            'title': 'Chương trình ngoại khóa tháng 10 - Khám phá thiên nhiên',
            'content': '''
            <h2>Hoạt động ngoại khóa phong phú</h2>
            <p>Trong tháng 10, trường sẽ tổ chức nhiều hoạt động ngoại khóa bổ ích giúp các em khám phá thế giới xung quanh.</p>
            
            <h3>Các hoạt động chính:</h3>
            <ol>
                <li><strong>Tham quan vườn bách thảo:</strong> Giúp trẻ tìm hiểu về các loài thực vật</li>
                <li><strong>Học nấu ăn đơn giản:</strong> Phát triển kỹ năng sống cơ bản</li>
                <li><strong>Trò chơi tập thể:</strong> Tăng cường tinh thần đoàn kết</li>
                <li><strong>Hoạt động nghệ thuật:</strong> Vẽ tranh, làm đồ thủ công</li>
            </ol>
            
            <p>Tất cả hoạt động đều được thiết kế phù hợp với lứa tuổi mầm non, đảm bảo an toàn và mang tính giáo dục cao.</p>
            ''',
            'summary': 'Các hoạt động ngoại khóa phong phú trong tháng 10 giúp trẻ phát triển toàn diện về thể chất và tinh thần.',
            'is_published': True,
            'publish_date': datetime.now() - timedelta(days=10)
        },
        {
            'title': 'Hội thảo "Nuôi dưỡng trẻ mầm non" dành cho phụ huynh',
            'content': '''
            <h2>Hội thảo bổ ích cho phụ huynh</h2>
            <p>Ngày 15/10/2024, trường tổ chức hội thảo "Nuôi dưỡng và giáo dục trẻ mầm non" với sự tham gia của các chuyên gia hàng đầu.</p>
            
            <h3>Nội dung hội thảo:</h3>
            <ul>
                <li>Dinh dưỡng cho trẻ mầm non</li>
                <li>Phát triển tâm lý trẻ em</li>
                <li>Kỹ năng giao tiếp với trẻ</li>
                <li>Xử lý các tình huống khó khăn</li>
            </ul>
            
            <p>Hội thảo hoàn toàn miễn phí cho phụ huynh có con đang học tại trường.</p>
            ''',
            'summary': 'Hội thảo miễn phí về nuôi dưỡng trẻ em dành cho phụ huynh với các chuyên gia tâm lý và dinh dưỡng.',
            'is_published': True,
            'publish_date': datetime.now() - timedelta(days=15)
        },
        {
            'title': 'Lễ hội Trung Thu 2024 - Đêm hội ánh trăng',
            'content': '''
            <h2>Đêm hội Trung Thu đầy màu sắc</h2>
            <p>Trường đã tổ chức thành công đêm hội Trung Thu với nhiều hoạt động thú vị cho các em học sinh và gia đình.</p>
            
            <h3>Các hoạt động nổi bật:</h3>
            <ul>
                <li>Múa lân sư rồng</li>
                <li>Diễu hành đèn lồng</li>
                <li>Thưởng thức bánh trung thu</li>
                <li>Kể chuyện cổ tích</li>
                <li>Thi làm đèn lồng</li>
            </ul>
            
            <p>Sự kiện đã thu hút hơn 300 người tham gia và để lại nhiều kỷ niệm đẹp.</p>
            ''',
            'summary': 'Lễ hội Trung Thu 2024 với nhiều hoạt động văn hóa truyền thống và hiện đại.',
            'is_published': True,
            'publish_date': datetime.now() - timedelta(days=20)
        },
        {
            'title': 'Tuyển sinh năm học 2025-2026 - Ưu đãi đặc biệt',
            'content': '''
            <h2>Thông báo tuyển sinh</h2>
            <p>Trường Mầm non Hoa Hướng Dương chính thức mở đăng ký tuyển sinh năm học 2025-2026.</p>
            
            <h3>Ưu đãi đặc biệt:</h3>
            <ul>
                <li>Giảm 20% học phí tháng đầu cho học sinh mới</li>
                <li>Miễn phí đồng phục và dụng cụ học tập</li>
                <li>Tặng bộ sách giáo dục sớm</li>
            </ul>
            
            <h3>Điều kiện tuyển sinh:</h3>
            <ul>
                <li>Trẻ từ 18 tháng đến 5 tuổi</li>
                <li>Có giấy khai sinh</li>
                <li>Có sổ tiêm chủng đầy đủ</li>
            </ul>
            
            <p><strong>Hạn đăng ký:</strong> 31/12/2024</p>
            ''',
            'summary': 'Thông báo tuyển sinh năm học 2025-2026 với nhiều ưu đãi hấp dẫn cho học sinh mới.',
            'is_published': True,
            'publish_date': datetime.now() - timedelta(days=2)
        }
    ]
    
    for news_item in news_data:
        news = News(**news_item)
        db.session.add(news)
        print(f"✅ Đã tạo tin tức: {news_item['title'][:50]}...")
    
    db.session.commit()

def create_programs_data():
    """Tạo dữ liệu chương trình học"""
    print("🎓 Tạo dữ liệu chương trình học...")
    
    programs_data = [
        {
            'name': 'Lớp Mầm (18-24 tháng)',
            'description': '''Chương trình giáo dục đặc biệt dành cho trẻ 18-24 tháng tuổi, tập trung phát triển:
            
• Kỹ năng vận động thô và tinh
• Ngôn ngữ cơ bản qua các bài hát, thơ
• Khả năng tương tác xã hội đầu tiên
• Thói quen sinh hoạt tự lập
• Khám phá thế giới xung quanh qua các hoạt động cảm quan

Với tỷ lệ giáo viên/học sinh là 1:6, đảm bảo sự chăm sóc tận tình cho từng bé.''',
            'age_group': '18-24 tháng',
            'featured_image': 'uploads/programs/lop-mam.jpg',
            'price': '2.500.000 VNĐ/tháng',
            'duration': 'Cả năm học',
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Lớp Chồi (2-3 tuổi)',
            'description': '''Chương trình toàn diện cho trẻ 2-3 tuổi với các hoạt động:

• Phát triển ngôn ngữ qua kể chuyện, hát
• Hoạt động vận động và thể dục nhịp điệu
• Học qua chơi với đồ chơi giáo dục
• Rèn luyện kỹ năng xã hội cơ bản
• Làm quen với các khái niệm số đếm, màu sắc, hình khối

Môi trường học tập an toàn, thân thiện với nhiều góc học tập đa dạng.''',
            'age_group': '2-3 tuổi',
            'featured_image': 'uploads/programs/lop-choi.jpg',
            'price': '2.800.000 VNĐ/tháng',
            'duration': 'Cả năm học',
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Lớp Lá (3-4 tuổi)',
            'description': '''Chuẩn bị cho trẻ 3-4 tuổi với các kỹ năng cần thiết:

• Phát triển khả năng tư duy logic
• Học chữ cái và số đếm cơ bản
• Rèn luyện kỹ năng vận động tinh
• Hoạt động nghệ thuật: vẽ, hát, múa
• Kỹ năng sống: tự phục vụ bản thân
• Chuẩn bị tâm lý cho bậc học cao hơn

Chương trình được thiết kế theo phương pháp STEAM hiện đại.''',
            'age_group': '3-4 tuổi',
            'featured_image': 'uploads/programs/lop-la.jpg',
            'price': '3.000.000 VNĐ/tháng',
            'duration': 'Cả năm học',
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Lớp Lúa (4-5 tuổi)',
            'description': '''Chương trình chuẩn bị vào lớp 1 cho trẻ 4-5 tuổi:

• Học chữ cái, âm vần và đọc đơn giản
• Toán học cơ bản: đếm, cộng, trừ trong phạm vi 20
• Phát triển tư duy khoa học qua thí nghiệm đơn giản
• Kỹ năng thuyết trình và giao tiếp
• Hoạt động nhóm và làm việc độc lập
• Chuẩn bị tâm lý và kiến thức cho tiểu học

Đội ngũ giáo viên có chuyên môn cao, kinh nghiệm lâu năm.''',
            'age_group': '4-5 tuổi',
            'featured_image': 'uploads/programs/lop-lua.jpg',
            'price': '3.200.000 VNĐ/tháng',
            'duration': 'Cả năm học',
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Lớp Tiếng Anh',
            'description': '''Chương trình tiếng Anh cho trẻ em từ 3-5 tuổi:

• Phương pháp giảng dạy sinh động, phù hợp lứa tuổi
• Học qua bài hát, trò chơi và hoạt động tương tác
• Phát triển 4 kỹ năng: nghe, nói, đọc, viết cơ bản
• Giáo viên nước ngoài và Việt Nam có trình độ cao
• Tài liệu học tập hiện đại, đa phương tiện
• Tổ chức các hoạt động văn hóa nước ngoài

Giúp trẻ làm quen với ngôn ngữ quốc tế từ sớm.''',
            'age_group': '3-5 tuổi',
            'featured_image': 'uploads/programs/lop-anh.jpg',
            'price': '1.500.000 VNĐ/tháng',
            'duration': '3 buổi/tuần',
            'is_active': True,
            'is_featured': True
        },
        {
            'name': 'Lớp Năng khiếu',
            'description': '''Các lớp học năng khiếu đa dạng:

• Vẽ tranh: Phát triển tư duy sáng tạo và thẩm mỹ
• Múa: Rèn luyện sự dẻo dai và nhịp điệu
• Hát: Phát triển giọng hát và cảm xúc âm nhạc
• Đàn piano: Học nhạc cụ cơ bản
• Thể dục nghệ thuật: Phát triển thể chất toàn diện
• Cờ vua: Rèn luyện tư duy logic

Giáo viên chuyên môn cao, có kinh nghiệm giảng dạy trẻ em.''',
            'age_group': '3-5 tuổi',
            'featured_image': 'uploads/programs/lop-nang-khieu.jpg',
            'price': '1.000.000 VNĐ/tháng',
            'duration': '2 buổi/tuần',
            'is_active': True,
            'is_featured': False
        }
    ]
    
    for program_data in programs_data:
        program = Program(**program_data)
        db.session.add(program)
        print(f"✅ Đã tạo chương trình: {program_data['name']}")
    
    db.session.commit()

def create_events_data():
    """Tạo dữ liệu sự kiện"""
    print("📅 Tạo dữ liệu sự kiện...")
    
    # Sự kiện sắp tới
    upcoming_events = [
        {
            'title': 'Ngày hội thể thao mầm non 2024',
            'description': '''Ngày hội thể thao năm 2024 với các môn thi đấu phù hợp lứa tuổi mầm non:
            
• Chạy 30m, 50m
• Nhảy bao bố
• Kéo co
• Ném bóng vào rổ
• Chạy tiếp sức
• Các trò chơi dân gian

Tất cả học sinh đều được tham gia và nhận quà lưu niệm.''',
            'event_date': datetime.now() + timedelta(days=15),
            'location': 'Sân vận động trường',
            'featured_image': 'uploads/events/ngay-hoi-the-thao.jpg',
            'is_active': True
        },
        {
            'title': 'Biểu diễn văn nghệ cuối năm 2024',
            'description': '''Chương trình biểu diễn văn nghệ cuối năm học với sự tham gia của tất cả các lớp:

• Múa dân gian và hiện đại
• Hát solo và hát nhóm
• Kịch ngắn
• Thời trang trẻ em
• Trình diễn tài năng cá nhân

Chương trình được tổ chức trang trọng với sự tham gia của phụ huynh.''',
            'event_date': datetime.now() + timedelta(days=45),
            'location': 'Hội trường trường học',
            'featured_image': 'uploads/events/bieu-dien-cuoi-nam.jpg',
            'is_active': True
        },
        {
            'title': 'Dã ngoại cuối năm - Khám phá thiên nhiên',
            'description': '''Chuyến dã ngoại cuối năm học tại khu du lịch sinh thái:

• Tham quan vườn thú
• Hoạt động ngoài trời
• Picnic cùng gia đình
• Trò chơi tập thể
• Học tập về thiên nhiên

An toàn tuyệt đối với xe đưa đón và bảo hiểm đầy đủ.''',
            'event_date': datetime.now() + timedelta(days=60),
            'location': 'Khu du lịch Đại Nam',
            'featured_image': 'uploads/events/da-ngoai.jpg',
            'is_active': True
        }
    ]
    
    # Sự kiện đã qua
    past_events = [
        {
            'title': 'Lễ Trung Thu 2024 - Đêm hội ánh trăng',
            'description': 'Tổ chức đêm hội Trung Thu với nhiều hoạt động vui chơi, múa lân, thưởng thức bánh kẹo và đèn lồng cho các em học sinh.',
            'event_date': datetime.now() - timedelta(days=30),
            'location': 'Sân trường Hoa Hướng Dương',
            'featured_image': 'uploads/events/trung-thu.jpg',
            'is_active': True
        },
        {
            'title': 'Khai giảng năm học 2024-2025',
            'description': 'Lễ khai giảng năm học mới với sự tham gia của học sinh, phụ huynh và đội ngũ giáo viên.',
            'event_date': datetime.now() - timedelta(days=60),
            'location': 'Hội trường trường học',
            'featured_image': 'uploads/events/khai-giang.jpg',
            'is_active': True
        }
    ]
    
    all_events = upcoming_events + past_events
    
    for event_data in all_events:
        event = Event(**event_data)
        db.session.add(event)
        print(f"✅ Đã tạo sự kiện: {event_data['title']}")
    
    db.session.commit()

def create_slider_data():
    """Tạo dữ liệu slider"""
    print("🖼️ Tạo dữ liệu slider...")
    
    slider_data = [
        {
            'title': 'Chào mừng đến với Hoa Hướng Dương',
            'description': 'Nơi nuôi dưỡng tâm hồn và phát triển tài năng của trẻ em',
            'image_path': 'uploads/slider/slider-1.jpg',
            'is_active': True,
            'order_index': 1
        },
        {
            'title': 'Môi trường học tập hiện đại',
            'description': 'Cơ sở vật chất đầy đủ, an toàn cho sự phát triển của trẻ',
            'image_path': 'uploads/slider/slider-2.jpg',
            'is_active': True,
            'order_index': 2
        },
        {
            'title': 'Đội ngũ giáo viên chuyên nghiệp',
            'description': 'Giáo viên được đào tạo bài bản, yêu thương trẻ như con em mình',
            'image_path': 'uploads/slider/slider-3.jpg',
            'is_active': True,
            'order_index': 3
        }
    ]
    
    for slider_item in slider_data:
        slider = Slider(**slider_item)
        db.session.add(slider)
        print(f"✅ Đã tạo slider: {slider_item['title']}")
    
    db.session.commit()

def create_team_data():
    """Tạo dữ liệu đội ngũ"""
    print("👥 Tạo dữ liệu đội ngũ...")
    
    team_data = [
        {
            'name': 'Cô Nguyễn Thị Lan',
            'position': 'Hiệu trưởng',
            'description': 'Thạc sĩ Giáo dục Mầm non, 15 năm kinh nghiệm trong lĩnh vực giáo dục. Tận tâm với nghề, luôn đặt lợi ích của trẻ em lên hàng đầu.',
            'image_path': 'uploads/team/hieu-truong.jpg',
            'order_index': 1,
            'is_active': True
        },
        {
            'name': 'Cô Trần Thị Mai',
            'position': 'Phó Hiệu trưởng',
            'description': 'Cử nhân Sư phạm Mầm non, chuyên gia về phát triển chương trình giáo dục. 12 năm kinh nghiệm giảng dạy và quản lý.',
            'image_path': 'uploads/team/pho-hieu-truong.jpg',
            'order_index': 2,
            'is_active': True
        },
        {
            'name': 'Cô Lê Thị Hoa',
            'position': 'Trưởng phòng Đào tạo',
            'description': 'Thạc sĩ Tâm lý học Trẻ em, chuyên về phát triển tâm lý và hành vi trẻ mầm non. Có nhiều nghiên cứu về giáo dục sớm.',
            'image_path': 'uploads/team/truong-phong-dao-tao.jpg',
            'order_index': 3,
            'is_active': True
        },
        {
            'name': 'Cô Phạm Thị Linh',
            'position': 'Giáo viên chủ nhiệm lớp Lúa',
            'description': 'Cử nhân Sư phạm Mầm non, 8 năm kinh nghiệm. Chuyên về phương pháp giảng dạy sáng tạo và phát triển ngôn ngữ cho trẻ.',
            'image_path': 'uploads/team/giao-vien-1.jpg',
            'order_index': 4,
            'is_active': True
        },
        {
            'name': 'Cô Vũ Thị Nga',
            'position': 'Giáo viên Tiếng Anh',
            'description': 'Cử nhân Ngôn ngữ Anh, chứng chỉ TESOL. Có kinh nghiệm giảng dạy tiếng Anh cho trẻ em với phương pháp vui nhộn, hiệu quả.',
            'image_path': 'uploads/team/giao-vien-anh.jpg',
            'order_index': 5,
            'is_active': True
        },
        {
            'name': 'Thầy Nguyễn Văn Đức',
            'position': 'Giáo viên Thể dục',
            'description': 'Cử nhân Giáo dục Thể chất, chuyên về phát triển vận động cho trẻ mầm non. Tổ chức nhiều hoạt động thể thao thú vị.',
            'image_path': 'uploads/team/giao-vien-the-duc.jpg',
            'order_index': 6,
            'is_active': True
        }
    ]
    
    for member_data in team_data:
        member = TeamMember(**member_data)
        db.session.add(member)
        print(f"✅ Đã tạo thành viên: {member_data['name']} - {member_data['position']}")
    
    db.session.commit()

def create_mission_data():
    """Tạo dữ liệu sứ mệnh"""
    print("🎯 Tạo dữ liệu sứ mệnh...")
    
    # Tạo Mission Content
    mission_content = MissionContent(
        main_title='Sứ mệnh của chúng tôi',
        main_image='uploads/mission/mission-hero.jpg',
        stats_number='100%',
        stats_text='Hài lòng',
        is_active=True
    )
    db.session.add(mission_content)
    
    # Tạo Mission Items
    mission_items = [
        {
            'title': 'Nuôi dưỡng tâm hồn',
            'description': 'Chúng tôi tin rằng mỗi trẻ em đều là những viên kim cương quý giá. Sứ mệnh của chúng tôi là tạo ra một môi trường ấm áp, an toàn để trẻ có thể phát triển một cách tự nhiên và hạnh phúc.',
            'icon': 'fas fa-heart',
            'color': 'bg-primary',
            'order_index': 1,
            'is_active': True
        },
        {
            'title': 'Phát triển tài năng',
            'description': 'Mỗi trẻ em đều có những tài năng và tiềm năng riêng. Chúng tôi cam kết khám phá và phát triển những tài năng ấy thông qua các hoạt động giáo dục đa dạng và sáng tạo.',
            'icon': 'fas fa-lightbulb',
            'color': 'bg-secondary',
            'order_index': 2,
            'is_active': True
        },
        {
            'title': 'Giáo dục toàn diện',
            'description': 'Chúng tôi không chỉ dạy kiến thức mà còn giúp trẻ phát triển về mặt cảm xúc, xã hội và đạo đức, tạo nền tảng vững chắc cho tương lai của các em.',
            'icon': 'fas fa-seedling',
            'color': 'bg-green-500',
            'order_index': 3,
            'is_active': True
        }
    ]
    
    for item_data in mission_items:
        item = MissionItem(**item_data)
        db.session.add(item)
        print(f"✅ Đã tạo mục tiêu sứ mệnh: {item_data['title']}")
    
    db.session.commit()

def create_history_data():
    """Tạo dữ liệu lịch sử hình thành"""
    print("📜 Tạo dữ liệu lịch sử...")
    
    # Tạo History Section
    history_section = HistorySection(
        main_title='Lịch sử hình thành',
        subtitle='Hành trình 10 năm xây dựng và phát triển của Trường Mầm non Hoa Hướng Dương',
        is_active=True
    )
    db.session.add(history_section)
    
    # Tạo các sự kiện lịch sử
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
    
    for event_data in history_events:
        event = HistoryEvent(**event_data)
        db.session.add(event)
        print(f"✅ Đã tạo sự kiện lịch sử: {event_data['year']} - {event_data['title']}")
    
    db.session.commit()

def create_about_data():
    """Tạo dữ liệu về chúng tôi"""
    print("ℹ️ Tạo dữ liệu về chúng tôi...")
    
    # Tạo About Section
    about_section = AboutSection(
        title='Về chúng tôi',
        subtitle='Trường Mầm non Hoa Hướng Dương',
        description_1='Trường Mầm non Hoa Hướng Dương là ngôi trường tiên phong trong việc áp dụng phương pháp giáo dục hiện đại, tập trung phát triển toàn diện cho trẻ em từ 18 tháng đến 5 tuổi.',
        description_2='Với đội ngũ giáo viên được đào tạo chuyên nghiệp và cơ sở vật chất hiện đại, chúng tôi cam kết mang đến môi trường học tập an toàn, vui tươi và sáng tạo cho các em.',
        image_1='uploads/about/about-1.jpg',
        image_2='uploads/about/about-2.jpg',
        experience_years='10+',
        experience_text='Năm kinh nghiệm',
        is_active=True
    )
    db.session.add(about_section)
    
    # Tạo About Stats
    stats_data = [
        {
            'stat_key': 'students',
            'stat_value': '200+',
            'stat_label': 'Học sinh',
            'icon_class': 'fas fa-users',
            'color_class': 'bg-primary',
            'order_index': 1,
            'is_active': True
        },
        {
            'stat_key': 'teachers',
            'stat_value': '25',
            'stat_label': 'Giáo viên',
            'icon_class': 'fas fa-chalkboard-teacher',
            'color_class': 'bg-secondary',
            'order_index': 2,
            'is_active': True
        },
        {
            'stat_key': 'programs',
            'stat_value': '15+',
            'stat_label': 'Chương trình',
            'icon_class': 'fas fa-graduation-cap',
            'color_class': 'bg-green-500',
            'order_index': 3,
            'is_active': True
        },
        {
            'stat_key': 'satisfaction',
            'stat_value': '98%',
            'stat_label': 'Hài lòng',
            'icon_class': 'fas fa-star',
            'color_class': 'bg-yellow-500',
            'order_index': 4,
            'is_active': True
        }
    ]
    
    for stat_data in stats_data:
        stat = AboutStats(**stat_data)
        db.session.add(stat)
        print(f"✅ Đã tạo thống kê: {stat_data['stat_label']} - {stat_data['stat_value']}")
    
    db.session.commit()

def create_faq_data():
    """Tạo dữ liệu FAQ"""
    print("❓ Tạo dữ liệu FAQ...")
    
    faq_data = [
        {
            'question': 'Trường nhận trẻ từ độ tuổi nào?',
            'answer': 'Trường nhận trẻ từ 18 tháng tuổi đến 5 tuổi. Chúng tôi có các lớp phù hợp với từng độ tuổi: Lớp Mầm (18-24 tháng), Lớp Chồi (2-3 tuổi), Lớp Lá (3-4 tuổi), và Lớp Lúa (4-5 tuổi).',
            'category': 'general',
            'order_index': 1,
            'is_active': True
        },
        {
            'question': 'Học phí của trường như thế nào?',
            'answer': 'Học phí dao động từ 2.500.000 - 3.200.000 VNĐ/tháng tùy theo độ tuổi. Chúng tôi có các chương trình ưu đãi cho học sinh mới và anh chị em trong gia đình. Vui lòng liên hệ để được tư vấn chi tiết.',
            'category': 'tuition',
            'order_index': 2,
            'is_active': True
        },
        {
            'question': 'Thời gian học của trẻ như thế nào?',
            'answer': 'Trường mở cửa từ 7:00 - 17:00 từ thứ 2 đến thứ 6. Phụ huynh có thể đưa đón trẻ linh hoạt trong khung giờ này. Chúng tôi cũng có dịch vụ đưa đón tận nhà.',
            'category': 'schedule',
            'order_index': 3,
            'is_active': True
        },
        {
            'question': 'Trường có dịch vụ ăn uống không?',
            'answer': 'Có, trường cung cấp 3 bữa chính và 2 bữa phụ mỗi ngày. Thực đơn được dinh dưỡng gia tư vấn, đảm bảo đầy đủ chất dinh dưỡng cho sự phát triển của trẻ. Chúng tôi cũng có thực đơn riêng cho trẻ dị ứng.',
            'category': 'services',
            'order_index': 4,
            'is_active': True
        },
        {
            'question': 'Làm thế nào để đăng ký tham quan trường?',
            'answer': 'Phụ huynh có thể đăng ký tham quan qua hotline 028-3823-4567, email info@hoahuongduong.edu.vn hoặc trực tiếp tại trường. Chúng tôi tổ chức tham quan vào các ngày trong tuần từ 8:00 - 16:00.',
            'category': 'admission',
            'order_index': 5,
            'is_active': True
        },
        {
            'question': 'Trường có chương trình ngoại khóa không?',
            'answer': 'Có, trường có nhiều chương trình ngoại khóa phong phú như: tiếng Anh, năng khiếu (vẽ, múa, hát, đàn piano), thể dục, bơi lội. Các hoạt động này giúp phát triển toàn diện tài năng của trẻ.',
            'category': 'programs',
            'order_index': 6,
            'is_active': True
        }
    ]
    
    for faq_item in faq_data:
        faq = FAQ(**faq_item)
        db.session.add(faq)
        print(f"✅ Đã tạo FAQ: {faq_item['question'][:50]}...")
    
    db.session.commit()

def create_special_programs_data():
    """Tạo dữ liệu chương trình đặc biệt"""
    print("⭐ Tạo dữ liệu chương trình đặc biệt...")
    
    special_programs_data = [
        {
            'title': 'Chương trình STEAM',
            'description': 'Phương pháp giáo dục tích hợp Khoa học, Công nghệ, Kỹ thuật, Nghệ thuật và Toán học, giúp trẻ phát triển tư duy sáng tạo và giải quyết vấn đề.',
            'icon_class': 'fas fa-rocket',
            'background_gradient': 'from-blue-50 to-purple-50',
            'border_color': 'border-blue-200',
            'icon_bg_color': 'bg-blue-500',
            'features': '["Thí nghiệm khoa học đơn giản", "Lắp ráp robot cơ bản", "Hoạt động nghệ thuật sáng tạo", "Toán học qua trò chơi"]',
            'image_path': 'uploads/special_programs/steam.jpg',
            'order_index': 1,
            'is_active': True
        },
        {
            'title': 'Chương trình Montessori',
            'description': 'Phương pháp giáo dục Montessori giúp trẻ học tập tự chủ, phát triển khả năng tự lập và tư duy độc lập thông qua môi trường học tập được chuẩn bị kỹ lưỡng.',
            'icon_class': 'fas fa-seedling',
            'background_gradient': 'from-green-50 to-blue-50',
            'border_color': 'border-green-200',
            'icon_bg_color': 'bg-green-500',
            'features': '["Học tập tự chủ", "Phát triển giác quan", "Kỹ năng sống thực tế", "Môi trường chuẩn bị"]',
            'image_path': 'uploads/special_programs/montessori.jpg',
            'order_index': 2,
            'is_active': True
        },
        {
            'title': 'Chương trình Bilingual',
            'description': 'Chương trình song ngữ Việt-Anh giúp trẻ phát triển khả năng ngôn ngữ tự nhiên, tạo nền tảng vững chắc cho việc học tập trong môi trường quốc tế.',
            'icon_class': 'fas fa-globe',
            'background_gradient': 'from-yellow-50 to-orange-50',
            'border_color': 'border-yellow-200',
            'icon_bg_color': 'bg-yellow-500',
            'features': '["Giáo viên bản ngữ", "Môi trường ngôn ngữ tự nhiên", "Văn hóa đa quốc gia", "Chứng chỉ quốc tế"]',
            'image_path': 'uploads/special_programs/bilingual.jpg',
            'order_index': 3,
            'is_active': True
        },
        {
            'title': 'Chương trình Năng khiếu',
            'description': 'Phát hiện và phát triển tài năng đặc biệt của trẻ trong các lĩnh vực nghệ thuật, thể thao, và khoa học thông qua các hoạt động chuyên sâu.',
            'icon_class': 'fas fa-star',
            'background_gradient': 'from-pink-50 to-purple-50',
            'border_color': 'border-pink-200',
            'icon_bg_color': 'bg-pink-500',
            'features': '["Âm nhạc và hội họa", "Thể dục nghệ thuật", "Khoa học nhỏ", "Tài năng cá nhân"]',
            'image_path': 'uploads/special_programs/talent.jpg',
            'order_index': 4,
            'is_active': True
        }
    ]
    
    for program_data in special_programs_data:
        program = SpecialProgram(**program_data)
        db.session.add(program)
        print(f"✅ Đã tạo chương trình đặc biệt: {program_data['title']}")
    
    db.session.commit()

def create_cta_data():
    """Tạo dữ liệu Call-to-Action"""
    print("📢 Tạo dữ liệu Call-to-Action...")
    
    cta_data = [
        {
            'section_name': 'programs_cta',
            'main_title': 'Sẵn sàng đăng ký cho con yêu?',
            'subtitle': 'Liên hệ ngay để được tư vấn chi tiết về chương trình học phù hợp với độ tuổi của con bạn',
            'phone_number': '028-3823-4567',
            'email': 'info@hoahuongduong.edu.vn',
            'working_hours': 'Thứ 2 - Thứ 6: 7:00 - 17:00',
            'email_response_time': 'Phản hồi trong 24h',
            'visit_note': 'Đặt lịch tham quan trước 1 ngày',
            'promotion_title': 'Ưu đãi đặc biệt cho học sinh mới',
            'promotion_description': 'Đăng ký trong tháng này để nhận ưu đãi 20% học phí tháng đầu và miễn phí đồng phục!',
            'promotion_note': 'Ưu đãi có hạn đến hết tháng này',
            'is_active': True
        },
        {
            'section_name': 'home_cta',
            'main_title': 'Bắt đầu hành trình học tập cùng chúng tôi',
            'subtitle': 'Đăng ký tham quan để trực tiếp trải nghiệm môi trường học tập tuyệt vời tại Hoa Hướng Dương',
            'phone_number': '028-3823-4567',
            'email': 'info@hoahuongduong.edu.vn',
            'working_hours': 'Thứ 2 - Thứ 6: 7:00 - 17:00',
            'email_response_time': 'Phản hồi trong 2h',
            'visit_note': 'Tham quan miễn phí mọi ngày trong tuần',
            'promotion_title': 'Tháng vàng tuyển sinh',
            'promotion_description': 'Nhiều ưu đãi hấp dẫn cho phụ huynh đăng ký sớm!',
            'promotion_note': 'Số lượng có hạn',
            'is_active': True
        }
    ]
    
    for cta_item in cta_data:
        cta = CallToAction(**cta_item)
        db.session.add(cta)
        print(f"✅ Đã tạo CTA: {cta_item['section_name']}")
    
    db.session.commit()

def create_videos_data():
    """Tạo dữ liệu video giới thiệu"""
    print("🎥 Tạo dữ liệu video...")
    
    videos_data = [
        {
            'title': 'Giới thiệu Trường Mầm non Hoa Hướng Dương',
            'description': 'Video tổng quan về cơ sở vật chất, đội ngũ giáo viên và hoạt động học tập tại trường',
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',  # Sample YouTube URL
            'thumbnail_image': 'uploads/videos/intro-video.jpg',
            'order_index': 1,
            'is_active': True
        },
        {
            'title': 'Một ngày của bé tại trường',
            'description': 'Theo dõi hoạt động học tập và vui chơi của các em trong một ngày học điển hình',
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'thumbnail_image': 'uploads/videos/day-at-school.jpg',
            'order_index': 2,
            'is_active': True
        },
        {
            'title': 'Chương trình STEAM cho trẻ mầm non',
            'description': 'Khám phá phương pháp giáo dục STEAM hiện đại được áp dụng tại trường',
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'thumbnail_image': 'uploads/videos/steam-program.jpg',
            'order_index': 3,
            'is_active': True
        }
    ]
    
    for video_data in videos_data:
        video = IntroVideo(**video_data)
        db.session.add(video)
        print(f"✅ Đã tạo video: {video_data['title']}")
    
    db.session.commit()

def create_sample_contacts():
    """Tạo dữ liệu liên hệ mẫu"""
    print("📧 Tạo dữ liệu liên hệ mẫu...")
    
    contacts_data = [
        {
            'name': 'Nguyễn Thị Hương',
            'email': 'huong.nguyen@email.com',
            'phone': '0901234567',
            'subject': 'Tư vấn chương trình học cho bé 3 tuổi',
            'message': 'Chào trường, tôi muốn tìm hiểu về chương trình học dành cho bé 3 tuổi. Bé nhà tôi khá nhút nhát, không biết trường có phương pháp nào giúp bé hòa nhập không ạ?',
            'is_read': False,
            'created_at': datetime.now() - timedelta(days=1)
        },
        {
            'name': 'Trần Văn Minh',
            'email': 'minh.tran@email.com',
            'phone': '0912345678',
            'subject': 'Đăng ký tham quan trường',
            'message': 'Tôi muốn đăng ký lịch tham quan trường vào cuối tuần này. Gia đình tôi đang tìm hiểu trường mầm non cho con trai 4 tuổi.',
            'is_read': True,
            'created_at': datetime.now() - timedelta(days=3)
        },
        {
            'name': 'Lê Thị Mai',
            'email': 'mai.le@email.com',
            'phone': '0923456789',
            'subject': 'Hỏi về học phí và chương trình học',
            'message': 'Xin chào, tôi muốn biết thông tin chi tiết về học phí các lớp và chương trình ngoại khóa. Con tôi đang 2 tuổi 8 tháng.',
            'is_read': False,
            'created_at': datetime.now() - timedelta(hours=12)
        }
    ]
    
    for contact_data in contacts_data:
        contact = Contact(**contact_data)
        db.session.add(contact)
        print(f"✅ Đã tạo liên hệ từ: {contact_data['name']}")
    
    db.session.commit()

def main():
    """Hàm chính để chạy tất cả"""
    print("🚀 BẮT ĐẦU KHỞI TẠO TOÀN BỘ DỮ LIỆU MẪU")
    print("=" * 60)
    
    with app.app_context():
        # Xóa dữ liệu cũ
        clear_all_data()
        
        # Tạo từng loại dữ liệu
        create_news_data()
        create_programs_data()
        create_events_data()
        create_slider_data()
        create_team_data()
        create_mission_data()
        create_history_data()  # Thêm dữ liệu lịch sử
        create_about_data()
        create_faq_data()
        create_special_programs_data()
        create_cta_data()
        create_videos_data()
        create_sample_contacts()
        
        print("\n" + "=" * 60)
        print("🎉 HOÀN THÀNH! Đã tạo toàn bộ dữ liệu mẫu")
        print("\n📋 TỔNG KẾT:")
        print(f"   📰 Tin tức: {News.query.count()} bài")
        print(f"   🎓 Chương trình: {Program.query.count()} chương trình")
        print(f"   📅 Sự kiện: {Event.query.count()} sự kiện")
        print(f"   🖼️ Slider: {Slider.query.count()} slide")
        print(f"   👥 Đội ngũ: {TeamMember.query.count()} thành viên")
        print(f"   🎯 Sứ mệnh: {MissionItem.query.count()} mục tiêu")
        print(f"   📜 Lịch sử: {HistoryEvent.query.count()} sự kiện")
        print(f"   ℹ️ Thống kê: {AboutStats.query.count()} số liệu")
        print(f"   ❓ FAQ: {FAQ.query.count()} câu hỏi")
        print(f"   ⭐ Chương trình đặc biệt: {SpecialProgram.query.count()} chương trình")
        print(f"   📢 Call-to-Action: {CallToAction.query.count()} section")
        print(f"   🎥 Video: {IntroVideo.query.count()} video")
        print(f"   📧 Liên hệ mẫu: {Contact.query.count()} tin nhắn")
        
        print(f"\n🔗 KIỂM TRA KẾT QUẢ:")
        print(f"   🏠 Trang chủ: http://127.0.0.1:5000/")
        print(f"   🔧 Admin panel: http://127.0.0.1:5000/admin/")
        print(f"   📰 Tin tức: http://127.0.0.1:5000/tin-tuc")
        print(f"   🎓 Chương trình: http://127.0.0.1:5000/chuong-trinh")
        print(f"   ℹ️ Giới thiệu: http://127.0.0.1:5000/gioi-thieu")
        print(f"   📞 Liên hệ: http://127.0.0.1:5000/lien-he")

if __name__ == "__main__":
    main()
