#!/usr/bin/env python3
"""
Script to initialize About section data
Run this after creating the database to populate default About section data
"""

from app import app, db, AboutSection, AboutStats

def init_about_data():
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if AboutSection already exists
        if not AboutSection.query.first():
            about_section = AboutSection(
                title='Về chúng tôi',
                subtitle='Trường Mầm non Hoa Hướng Dương',
                description_1='Trường Mầm non Hoa Hướng Dương là ngôi trường tiên phong trong việc áp dụng phương pháp giáo dục hiện đại, tập trung phát triển toàn diện cho trẻ em.',
                description_2='Với đội ngũ giáo viên được đào tạo chuyên nghiệp và cơ sở vật chất hiện đại, chúng tôi cam kết mang đến môi trường học tập an toàn, vui tươi và sáng tạo.',
                experience_years='10+',
                experience_text='Năm kinh nghiệm',
                is_active=True
            )
            db.session.add(about_section)
            print("✅ Created AboutSection")
        else:
            print("ℹ️  AboutSection already exists")
        
        # Check if AboutStats already exist
        if not AboutStats.query.first():
            # Create default stats
            stats_data = [
                {
                    'stat_key': 'students',
                    'stat_value': '200+',
                    'stat_label': 'Học sinh',
                    'icon_class': 'fas fa-users',
                    'color_class': 'bg-primary',
                    'order_index': 1
                },
                {
                    'stat_key': 'teachers',
                    'stat_value': '25',
                    'stat_label': 'Giáo viên',
                    'icon_class': 'fas fa-chalkboard-teacher',
                    'color_class': 'bg-secondary',
                    'order_index': 2
                },
                {
                    'stat_key': 'classes',
                    'stat_value': '12',
                    'stat_label': 'Lớp học',
                    'icon_class': 'fas fa-school',
                    'color_class': 'bg-blue-500',
                    'order_index': 3
                },
                {
                    'stat_key': 'activities',
                    'stat_value': '50+',
                    'stat_label': 'Hoạt động',
                    'icon_class': 'fas fa-gamepad',
                    'color_class': 'bg-green-500',
                    'order_index': 4
                }
            ]
            
            for stat_data in stats_data:
                stat = AboutStats(**stat_data, is_active=True)
                db.session.add(stat)
            
            print("✅ Created default AboutStats")
        else:
            print("ℹ️  AboutStats already exist")
        
        # Commit all changes
        db.session.commit()
        print("🎉 About section data initialized successfully!")

if __name__ == '__main__':
    init_about_data()
