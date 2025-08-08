#!/usr/bin/env python3
"""
Script to initialize FAQ data
Run this after creating the database to populate default FAQ data
"""

from app import app, db, FAQ

def init_faq_data():
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if FAQ already exists
        if not FAQ.query.first():
            # Create default FAQs
            faqs_data = [
                {
                    'question': 'Trường nhận trẻ từ độ tuổi nào?',
                    'answer': 'Trường Mầm non Hoa Hướng Dương nhận trẻ từ 18 tháng tuổi đến 5 tuổi. Chúng tôi có các lớp phù hợp với từng độ tuổi để đảm bảo sự phát triển tốt nhất cho trẻ.',
                    'category': 'admission',
                    'order_index': 1
                },
                {
                    'question': 'Học phí một tháng là bao nhiêu?',
                    'answer': 'Học phí dao động từ 2.500.000 - 3.200.000 VNĐ/tháng tùy theo độ tuổi và chương trình học. Đã bao gồm ăn sáng, ăn trưa, ăn xế và các hoạt động ngoại khóa.',
                    'category': 'tuition',
                    'order_index': 2
                },
                {
                    'question': 'Trường có xe đưa đón không?',
                    'answer': 'Có, trường có dịch vụ xe đưa đón với các chú tài xế kinh nghiệm và cô giáo đi kèm. Phụ huynh có thể đăng ký thêm dịch vụ này với chi phí bổ sung.',
                    'category': 'transport',
                    'order_index': 3
                },
                {
                    'question': 'Thời gian học trong ngày như thế nào?',
                    'answer': 'Trường hoạt động từ 7:00 - 17:00 từ thứ 2 đến thứ 6. Thời gian học chính thức từ 8:00 - 16:00, các hoạt động trước và sau giờ học được bố trí linh hoạt.',
                    'category': 'schedule',
                    'order_index': 4
                },
                {
                    'question': 'Phụ huynh có thể tham quan trường không?',
                    'answer': 'Hoàn toàn có thể. Chúng tôi khuyến khích phụ huynh đến tham quan và trải nghiệm môi trường học tập. Vui lòng liên hệ trước để được sắp xếp thời gian phù hợp.',
                    'category': 'general',
                    'order_index': 5
                },
                {
                    'question': 'Trường có chương trình học tiếng Anh không?',
                    'answer': 'Có, chúng tôi có chương trình học tiếng Anh tích hợp với giáo viên bản ngữ. Trẻ sẽ được tiếp xúc với tiếng Anh qua các hoạt động vui chơi, ca hát và trò chơi phù hợp với lứa tuổi.',
                    'category': 'activities',
                    'order_index': 6
                },
                {
                    'question': 'Trường có bác sĩ thường trú không?',
                    'answer': 'Trường có y tá thường trú và bác sĩ đến thăm khám định kỳ hàng tuần. Chúng tôi cũng có liên kết với bệnh viện gần nhất để xử lý các tình huống khẩn cấp.',
                    'category': 'health',
                    'order_index': 7
                },
                {
                    'question': 'Cơ sở vật chất của trường như thế nào?',
                    'answer': 'Trường được trang bị đầy đủ các phòng học hiện đại, sân chơi an toàn, phòng ăn sạch sẽ, phòng y tế, và các khu vực vui chơi ngoài trời. Tất cả đều được thiết kế phù hợp với trẻ em.',
                    'category': 'facilities',
                    'order_index': 8
                }
            ]
            
            for faq_data in faqs_data:
                faq = FAQ(**faq_data, is_active=True)
                db.session.add(faq)
            
            print("✅ Created default FAQs")
        else:
            print("ℹ️  FAQs already exist")
        
        # Commit all changes
        db.session.commit()
        print("🎉 FAQ data initialized successfully!")

if __name__ == '__main__':
    init_faq_data()
