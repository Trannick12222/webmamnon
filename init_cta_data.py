#!/usr/bin/env python3
"""
Script to initialize Call-to-Action data
Run this after creating the database to populate default CTA data
"""

from app import app, db, CallToAction

def init_cta_data():
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if CTA already exists
        if not CallToAction.query.first():
            # Create default CTA for programs page
            programs_cta = CallToAction(
                section_name='programs_cta',
                main_title='🌻 Hành trình học tập tuyệt vời đang chờ bé! 🌻',
                subtitle='Mỗi bé là một bông hoa nhỏ đặc biệt. Hãy để chúng tôi giúp bé nở rộ với những chương trình học phù hợp và đầy yêu thương.',
                phone_number='0123 456 789',
                email='info@hoahuongduong.edu.vn',
                working_hours='Thứ 2 - Thứ 6: 7:00 - 17:00',
                email_response_time='Phản hồi trong 24h',
                visit_note='Đặt lịch trước 1 ngày',
                promotion_title='Ưu đãi đặc biệt cho phụ huynh mới',
                promotion_description='Đăng ký tham quan trong tháng này để nhận ưu đãi 20% học phí tháng đầu!',
                promotion_note='Ưu đãi có hạn đến hết tháng này',
                is_active=True
            )
            
            db.session.add(programs_cta)
            print("✅ Created programs_cta")
            
            # Create default CTA for home page
            home_cta = CallToAction(
                section_name='home_cta',
                main_title='🌈 Cùng bé khám phá thế giới tuyệt vời! 🌈',
                subtitle='Trường Mầm non Hoa Hướng Dương - nơi nuôi dưỡng những ước mơ và phát triển toàn diện cho trẻ em từ 18 tháng đến 5 tuổi.',
                phone_number='0123 456 789',
                email='info@hoahuongduong.edu.vn',
                working_hours='Thứ 2 - Thứ 6: 7:00 - 17:00',
                email_response_time='Phản hồi trong 24h',
                visit_note='Đặt lịch trước 1 ngày',
                promotion_title='Chào mừng gia đình mới',
                promotion_description='Tham quan trường và nhận tư vấn miễn phí về chương trình học phù hợp cho bé!',
                promotion_note='Luôn sẵn sàng đón tiếp các gia đình',
                is_active=True
            )
            
            db.session.add(home_cta)
            print("✅ Created home_cta")
            
            # Create default CTA for about page
            about_cta = CallToAction(
                section_name='about_cta',
                main_title='💖 Hãy để chúng tôi đồng hành cùng bé! 💖',
                subtitle='Với đội ngũ giáo viên tận tâm và môi trường học tập an toàn, chúng tôi cam kết mang đến cho bé những trải nghiệm học tập tốt nhất.',
                phone_number='0123 456 789',
                email='info@hoahuongduong.edu.vn',
                working_hours='Thứ 2 - Thứ 6: 7:00 - 17:00',
                email_response_time='Phản hồi trong 24h',
                visit_note='Đặt lịch trước 1 ngày',
                promotion_title='Tìm hiểu thêm về chúng tôi',
                promotion_description='Đến thăm trường để cảm nhận trực tiếp môi trường học tập và gặp gỡ đội ngũ giáo viên!',
                promotion_note='Chúng tôi luôn chào đón phụ huynh',
                is_active=True
            )
            
            db.session.add(about_cta)
            print("✅ Created about_cta")
            
        else:
            print("ℹ️  Call-to-Action data already exists")
        
        # Commit all changes
        db.session.commit()
        print("🎉 Call-to-Action data initialized successfully!")

if __name__ == '__main__':
    init_cta_data()
