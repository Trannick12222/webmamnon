from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from PIL import Image
import os
import uuid
from datetime import datetime
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hoa-huong-duong-secret-key-2023'
# Database configuration helper function
def _e(keys, default=None):
    """Get environment variable from multiple possible keys"""
    for key in keys:
        value = os.environ.get(key)
        if value:
            return value
    return default
#test commit
# Database configuration - Local MySQL by default, Railway MySQL when deployed
mysql_host = _e(["MYSQL_HOST", "MYSQLHOST"], "127.0.0.1")
mysql_port = int(_e(["MYSQL_PORT", "MYSQLPORT"], 3306))
mysql_user = _e(["MYSQL_USER", "MYSQLUSER"], "root")
mysql_password = _e(["MYSQL_PASSWORD", "MYSQLPASSWORD", "MYSQL_ROOT_PASSWORD"], "173915Snow")
mysql_database = _e(["MYSQL_DATABASE"], "hoa_huong_duong")

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = SQLAlchemy(app)

@app.after_request
def after_request(response):
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/uploads/gallery', exist_ok=True)
os.makedirs('static/uploads/news', exist_ok=True)
os.makedirs('static/uploads/programs', exist_ok=True)
os.makedirs('static/uploads/special_programs', exist_ok=True)
os.makedirs('static/uploads/slider', exist_ok=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    featured_image = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    age_group = db.Column(db.String(50))
    featured_image = db.Column(db.String(200))
    price = db.Column(db.String(100))
    duration = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    image_path = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)
    featured_image = db.Column(db.String(200))
    is_published = db.Column(db.Boolean, default=True)
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    featured_image = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Slider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image_path = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ContactSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Column(db.Text)
    setting_type = db.Column(db.String(50), default='text')  # text, url, phone, email
    display_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    position = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image_path = db.Column(db.String(255))
    order_index = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MissionItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(100), default='fas fa-heart')  # FontAwesome icon class
    color = db.Column(db.String(50), default='bg-primary')  # Tailwind color class
    order_index = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MissionContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_title = db.Column(db.String(200), default='Sứ mệnh của chúng tôi')
    main_image = db.Column(db.String(255))  # Hero image path
    stats_number = db.Column(db.String(10), default='100%')
    stats_text = db.Column(db.String(100), default='Hài lòng')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HistorySection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_title = db.Column(db.String(200), default='Lịch sử hình thành')
    subtitle = db.Column(db.Text, default='Hành trình 10 năm xây dựng và phát triển của Trường Mầm non Hoa Hướng Dương')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HistoryEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(10), nullable=False)  # e.g., "2014", "2017"
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    color = db.Column(db.String(50), default='bg-primary')  # Tailwind color class
    image_path = db.Column(db.String(255))  # Optional image for the event
    order_index = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AboutSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), default='Về chúng tôi')
    subtitle = db.Column(db.Text, default='Trường Mầm non Hoa Hướng Dương')
    description_1 = db.Column(db.Text, default='Trường Mầm non Hoa Hướng Dương là ngôi trường tiên phong trong việc áp dụng phương pháp giáo dục hiện đại, tập trung phát triển toàn diện cho trẻ em.')
    description_2 = db.Column(db.Text, default='Với đội ngũ giáo viên được đào tạo chuyên nghiệp và cơ sở vật chất hiện đại, chúng tôi cam kết mang đến môi trường học tập an toàn, vui tươi và sáng tạo.')
    image_1 = db.Column(db.String(255))  # First image
    image_2 = db.Column(db.String(255))  # Second image
    experience_years = db.Column(db.String(10), default='10+')
    experience_text = db.Column(db.String(100), default='Năm kinh nghiệm')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AboutStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stat_key = db.Column(db.String(50), unique=True, nullable=False)  # 'students', 'teachers', etc.
    stat_value = db.Column(db.String(20), nullable=False)  # '200+', '25', etc.
    stat_label = db.Column(db.String(100), nullable=False)  # 'Học sinh', 'Giáo viên'
    icon_class = db.Column(db.String(100), default='fas fa-users')  # FontAwesome icon
    color_class = db.Column(db.String(50), default='bg-primary')  # Tailwind color
    order_index = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)  # Câu hỏi
    answer = db.Column(db.Text, nullable=False)  # Câu trả lời
    order_index = db.Column(db.Integer, default=0)  # Thứ tự hiển thị
    is_active = db.Column(db.Boolean, default=True)  # Hiển thị hay không
    category = db.Column(db.String(100), default='general')  # Danh mục (general, tuition, schedule, etc.)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SpecialProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # Tên chương trình
    description = db.Column(db.Text, nullable=False)  # Mô tả chương trình
    icon_class = db.Column(db.String(100), default='fas fa-star')  # FontAwesome icon
    background_gradient = db.Column(db.String(100), default='from-blue-50 to-purple-50')  # Tailwind gradient
    border_color = db.Column(db.String(50), default='border-blue-200')  # Tailwind border color
    icon_bg_color = db.Column(db.String(50), default='bg-blue-500')  # Icon background color
    features = db.Column(db.Text)  # JSON string of features list
    image_path = db.Column(db.String(255))  # Đường dẫn ảnh (optional)
    order_index = db.Column(db.Integer, default=0)  # Thứ tự hiển thị
    is_active = db.Column(db.Boolean, default=True)  # Hiển thị hay không
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CallToAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_name = db.Column(db.String(100), unique=True, nullable=False)  # 'programs_cta', 'home_cta', etc.
    main_title = db.Column(db.String(255), nullable=False)  # Tiêu đề chính
    subtitle = db.Column(db.Text, nullable=False)  # Mô tả phụ
    phone_number = db.Column(db.String(20), default='0123 456 789')  # Số điện thoại
    email = db.Column(db.String(100), default='info@hoahuongduong.edu.vn')  # Email
    working_hours = db.Column(db.String(100), default='Thứ 2 - Thứ 6: 7:00 - 17:00')  # Giờ làm việc
    email_response_time = db.Column(db.String(50), default='Phản hồi trong 24h')  # Thời gian phản hồi email
    visit_note = db.Column(db.String(100), default='Đặt lịch trước 1 ngày')  # Ghi chú tham quan
    promotion_title = db.Column(db.String(255), default='Ưu đãi đặc biệt cho phụ huynh mới')  # Tiêu đề ưu đãi
    promotion_description = db.Column(db.Text, default='Đăng ký tham quan trong tháng này để nhận ưu đãi 20% học phí tháng đầu!')  # Mô tả ưu đãi
    promotion_note = db.Column(db.String(100), default='Ưu đãi có hạn đến hết tháng này')  # Ghi chú ưu đãi
    is_active = db.Column(db.Boolean, default=True)  # Hiển thị hay không
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class IntroVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(500), nullable=False)  # YouTube URL
    thumbnail_image = db.Column(db.String(200))  # Optional custom thumbnail
    is_active = db.Column(db.Boolean, default=True)
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SEOSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_type = db.Column(db.String(50), nullable=False)  # 'global', 'home', 'about', 'news', 'programs', etc.
    page_id = db.Column(db.Integer, nullable=True)  # ID của trang cụ thể (nếu có)
    meta_title = db.Column(db.String(255))  # SEO title
    meta_description = db.Column(db.Text)  # SEO description
    meta_keywords = db.Column(db.Text)  # SEO keywords
    og_title = db.Column(db.String(255))  # Open Graph title
    og_description = db.Column(db.Text)  # Open Graph description
    og_image = db.Column(db.String(255))  # Open Graph image
    canonical_url = db.Column(db.String(500))  # Canonical URL
    robots_meta = db.Column(db.String(100), default='index,follow')  # robots meta tag
    schema_markup = db.Column(db.Text)  # JSON-LD schema markup
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class LocationSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.Text, nullable=False)  # Địa chỉ đầy đủ
    latitude = db.Column(db.Float)  # Vĩ độ
    longitude = db.Column(db.Float)  # Kinh độ
    google_maps_api_key = db.Column(db.String(255))  # Google Maps API Key
    google_maps_embed = db.Column(db.Text)  # Google Maps iframe embed code
    map_zoom_level = db.Column(db.Integer, default=15)  # Mức zoom mặc định
    map_style = db.Column(db.String(50), default='roadmap')  # roadmap, satellite, hybrid, terrain
    show_in_footer = db.Column(db.Boolean, default=True)  # Hiển thị trong footer
    map_height = db.Column(db.String(20), default='300px')  # Chiều cao bản đồ
    marker_title = db.Column(db.String(200), default='Trường Mầm non Hoa Hướng Dương')  # Tiêu đề marker
    marker_info = db.Column(db.Text)  # Thông tin hiển thị khi click marker
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ThemeSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme_name = db.Column(db.String(100), nullable=False)  # Tên theme
    primary_color = db.Column(db.String(7), nullable=False)  # Màu chính (hex)
    secondary_color = db.Column(db.String(7), nullable=False)  # Màu phụ (hex)
    accent_color = db.Column(db.String(7))  # Màu nhấn (hex)
    background_color = db.Column(db.String(7))  # Màu nền (hex)
    text_color = db.Column(db.String(7))  # Màu chữ (hex)
    is_active = db.Column(db.Boolean, default=False)  # Theme đang được sử dụng
    is_default = db.Column(db.Boolean, default=False)  # Theme mặc định
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SystemSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(200), default='Trường Mầm non Hoa Hướng Dương')
    school_address = db.Column(db.Text, default='123 Đường Hoa Hướng Dương, Quận 1, TP.HCM')
    school_phone = db.Column(db.String(20), default='028-3823-4567')
    school_email = db.Column(db.String(100), default='info@hoahuongduong.edu.vn')
    maintenance_mode = db.Column(db.Boolean, default=False)
    allow_registration = db.Column(db.Boolean, default=True)
    website_version = db.Column(db.String(20), default='v1.0.0')
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HomePageSettings(db.Model):
    __tablename__ = 'homepage_settings'
    id = db.Column(db.Integer, primary_key=True)
    
    # Hero Section - Original fields for backward compatibility
    hero_title = db.Column(db.Text, default='Chào mừng đến với<br><span class="text-yellow-300">ngôi trường của chúng tôi</span>')
    hero_subtitle = db.Column(db.Text, default='Nơi nuôi dưỡng tâm hồn và phát triển tài năng của trẻ em từ 18 tháng đến 5 tuổi')
    hero_cta_text_1 = db.Column(db.String(100), default='Xem chương trình học')
    hero_cta_text_2 = db.Column(db.String(100), default='Liên hệ tư vấn')
    
    # Hero Section - New simple fields
    hero_title_line1 = db.Column(db.String(200), default='Chào mừng đến với')
    hero_title_line2 = db.Column(db.String(200), default='ngôi trường của chúng tôi')
    
    # Video Section - Original fields for backward compatibility
    video_section_badge = db.Column(db.String(100), default='🎥 Video giới thiệu')
    video_section_title = db.Column(db.String(200), default='Khám phá thế giới <span class="text-primary">Hoa Hướng Dương</span>')
    video_section_description = db.Column(db.Text, default='Cùng tham quan và tìm hiểu về môi trường học tập tuyệt vời dành cho các bé')
    video_cta_text = db.Column(db.String(100), default='Đặt lịch tham quan')
    video_contact_text = db.Column(db.String(100), default='hoặc gọi 📞 0123 456 789')
    
    # Video Section - New simple fields
    video_section_title_normal = db.Column(db.String(200), default='Khám phá thế giới')
    video_section_title_highlight = db.Column(db.String(200), default='Hoa Hướng Dương')
    
    # Programs Section - Original fields for backward compatibility
    programs_section_title = db.Column(db.String(200), default='<span class="text-primary font-patrick">Chương trình học</span>')
    programs_section_description = db.Column(db.Text, default='Các chương trình giáo dục được thiết kế phù hợp với từng độ tuổi, giúp trẻ phát triển toàn diện về thể chất, trí tuệ và cảm xúc')
    programs_cta_text = db.Column(db.String(100), default='Xem tất cả chương trình')
    
    # Programs Section - New simple fields
    programs_section_title_text = db.Column(db.String(200), default='Chương trình học')
    
    # Features Section
    features_section_badge = db.Column(db.String(100), default='✨ Điểm khác biệt của chúng tôi')
    features_section_title = db.Column(db.String(200), default='Tại sao chọn Hoa Hướng Dương?')
    features_section_description = db.Column(db.Text, default='Chúng tôi mang đến những giá trị giáo dục tốt nhất cho sự phát triển toàn diện của trẻ')
    features_cta_text = db.Column(db.String(100), default='Đăng ký tham quan ngay')
    features_contact_text = db.Column(db.String(100), default='hoặc gọi 📞 1900-xxxx')
    
    # News Section - Original fields for backward compatibility
    news_section_title = db.Column(db.String(200), default='<span class="text-primary font-patrick">Tin tức mới nhất</span>')
    news_section_description = db.Column(db.Text, default='Cập nhật những thông tin mới nhất từ trường Hoa Hướng Dương')
    news_cta_text = db.Column(db.String(100), default='Xem tất cả tin tức')
    
    # News Section - New simple fields
    news_section_title_text = db.Column(db.String(200), default='Tin tức mới nhất')
    
    # Gallery Section - Original fields for backward compatibility
    gallery_section_title = db.Column(db.String(200), default='<span class="text-primary font-patrick">Khoảnh khắc đáng nhớ</span>')
    gallery_section_description = db.Column(db.Text, default='Những hình ảnh sinh động về cuộc sống học tập và vui chơi của các em')
    gallery_cta_text = db.Column(db.String(100), default='Xem thêm hình ảnh')
    
    # Gallery Section - New simple fields
    gallery_section_title_text = db.Column(db.String(200), default='Khoảnh khắc đáng nhớ')
    
    # Events Section - Original fields for backward compatibility
    events_section_title = db.Column(db.String(200), default='<span class="text-primary font-patrick">Sự kiện sắp tới</span>')
    events_section_description = db.Column(db.Text, default='Đừng bỏ lỡ những sự kiện thú vị dành cho các em học sinh')
    events_cta_text = db.Column(db.String(100), default='Xem tất cả sự kiện')
    
    # Events Section - New simple fields
    events_section_title_text = db.Column(db.String(200), default='Sự kiện sắp tới')
    
    # Final CTA Section
    cta_title = db.Column(db.String(200), default='Sẵn sàng cho con bước vào hành trình học tập?')
    cta_description = db.Column(db.Text, default='Hãy liên hệ với chúng tôi để được tư vấn chi tiết về chương trình học phù hợp với độ tuổi của con bạn')
    cta_button_1 = db.Column(db.String(100), default='Liên hệ ngay')
    cta_button_2 = db.Column(db.String(100), default='Tìm hiểu chương trình')
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PageVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45))  # Hỗ trợ IPv6
    user_agent = db.Column(db.Text)  # Thông tin trình duyệt
    page_url = db.Column(db.String(500))  # URL trang được truy cập
    referrer = db.Column(db.String(500))  # Trang giới thiệu
    visit_date = db.Column(db.Date, default=datetime.utcnow)  # Ngày truy cập
    visit_time = db.Column(db.DateTime, default=datetime.utcnow)  # Thời gian truy cập
    is_unique = db.Column(db.Boolean, default=True)  # Lượt truy cập duy nhất trong ngày

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_current_theme():
    """Lấy theme hiện tại đang được sử dụng"""
    theme = ThemeSettings.query.filter_by(is_active=True).first()
    if not theme:
        # Nếu không có theme nào được kích hoạt, trả về theme mặc định
        theme = ThemeSettings.query.filter_by(is_default=True).first()
        if not theme:
            # Nếu không có theme mặc định, tạo theme cam mặc định
            init_default_themes()
            theme = ThemeSettings.query.filter_by(is_default=True).first()
    return theme

def init_default_themes():
    """Khởi tạo các theme mặc định"""
    default_themes = [
        {
            'theme_name': 'Cam Hướng Dương',
            'primary_color': '#ff6b35',
            'secondary_color': '#f7931e',
            'accent_color': '#ffd700',
            'background_color': '#ffffff',
            'text_color': '#333333',
            'is_default': True,
            'is_active': True
        },
        {
            'theme_name': 'Xanh Biển',
            'primary_color': '#2563eb',
            'secondary_color': '#3b82f6',
            'accent_color': '#60a5fa',
            'background_color': '#ffffff',
            'text_color': '#1f2937',
            'is_default': False,
            'is_active': False
        },
        {
            'theme_name': 'Tím Lavender',
            'primary_color': '#7c3aed',
            'secondary_color': '#a855f7',
            'accent_color': '#c084fc',
            'background_color': '#ffffff',
            'text_color': '#374151',
            'is_default': False,
            'is_active': False
        },
        {
            'theme_name': 'Đỏ Cherry',
            'primary_color': '#dc2626',
            'secondary_color': '#ef4444',
            'accent_color': '#f87171',
            'background_color': '#ffffff',
            'text_color': '#1f2937',
            'is_default': False,
            'is_active': False
        },
        {
            'theme_name': 'Xanh Lá',
            'primary_color': '#059669',
            'secondary_color': '#10b981',
            'accent_color': '#34d399',
            'background_color': '#ffffff',
            'text_color': '#1f2937',
            'is_default': False,
            'is_active': False
        },
        {
            'theme_name': 'Hồng Pastel',
            'primary_color': '#ec4899',
            'secondary_color': '#f472b6',
            'accent_color': '#f9a8d4',
            'background_color': '#ffffff',
            'text_color': '#374151',
            'is_default': False,
            'is_active': False
        }
    ]
    
    for theme_data in default_themes:
        # Kiểm tra xem theme đã tồn tại chưa
        existing_theme = ThemeSettings.query.filter_by(theme_name=theme_data['theme_name']).first()
        if not existing_theme:
            theme = ThemeSettings(**theme_data)
            db.session.add(theme)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing themes: {e}")

def switch_theme(theme_id):
    """Chuyển đổi theme"""
    try:
        # Tắt tất cả theme hiện tại
        ThemeSettings.query.update({'is_active': False})
        
        # Kích hoạt theme mới
        new_theme = ThemeSettings.query.get(theme_id)
        if new_theme:
            new_theme.is_active = True
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        print(f"Error switching theme: {e}")
        return False

def get_seo_settings(page_type, page_id=None):
    """Lấy SEO settings cho trang cụ thể"""
    # Tìm SEO settings cho trang cụ thể
    seo = SEOSettings.query.filter_by(page_type=page_type, page_id=page_id, is_active=True).first()
    
    # Nếu không có, lấy SEO settings global
    if not seo:
        seo = SEOSettings.query.filter_by(page_type='global', is_active=True).first()
    
    # Nếu vẫn không có, tạo default
    if not seo:
        return {
            'meta_title': 'Trường Mầm non Hoa Hướng Dương',
            'meta_description': 'Trường Mầm non Hoa Hướng Dương - Nuôi dưỡng tâm hồn, phát triển tài năng. Môi trường giáo dục an toàn, chất lượng cao cho trẻ em.',
            'meta_keywords': 'trường mầm non, giáo dục mầm non, hoa hướng dương, trẻ em, giáo dục',
            'og_title': 'Trường Mầm non Hoa Hướng Dương',
            'og_description': 'Trường Mầm non Hoa Hướng Dương - Nuôi dưỡng tâm hồn, phát triển tài năng.',
            'og_image': '/static/images/mnhhd.jpg',
            'canonical_url': '',
            'robots_meta': 'index,follow',
            'schema_markup': ''
        }
    
    return {
        'meta_title': seo.meta_title,
        'meta_description': seo.meta_description,
        'meta_keywords': seo.meta_keywords,
        'og_title': seo.og_title,
        'og_description': seo.og_description,
        'og_image': seo.og_image,
        'canonical_url': seo.canonical_url,
        'robots_meta': seo.robots_meta,
        'schema_markup': seo.schema_markup
    }

@app.context_processor
def inject_unread_contacts():
    try:
        unread_contacts = Contact.query.filter_by(is_read=False).count()
        # Also inject contact settings for global use (header, footer)
        contact_settings = ContactSettings.query.filter_by(is_active=True).order_by(ContactSettings.order_index.asc()).all()
        # Inject location settings for global use (footer)
        location_settings = LocationSettings.query.filter_by(is_active=True).first()
        # Inject current theme for global use
        current_theme = get_current_theme()
        # Inject system settings for global use (school info)
        system_settings = SystemSettings.query.first()
        # Inject homepage settings for global use (homepage content)
        homepage_settings = HomePageSettings.query.first()
    except:
        unread_contacts = 0
        contact_settings = []
        location_settings = None
        current_theme = None
        system_settings = None
        homepage_settings = None
    return dict(
        unread_contacts=unread_contacts, 
        global_contact_settings=contact_settings, 
        global_location_settings=location_settings, 
        current_theme=current_theme,
        global_system_settings=system_settings,
        global_homepage_settings=homepage_settings,
        get_seo_settings=get_seo_settings
    )

# Custom Jinja2 filter to extract YouTube video ID
def extract_youtube_id(url):
    """Extract YouTube video ID from URL"""
    import re
    pattern = r'(?:youtu\.be/|v/|u/\w/|embed/|watch\?v=|&v=)([^#&?]*)'
    match = re.search(pattern, url)
    return match.group(1) if match and len(match.group(1)) == 11 else None

app.jinja_env.filters['youtube_id'] = extract_youtube_id

def normalize_path(path):
    """Normalize file path to use forward slashes for URLs"""
    if not path:
        return path
    return path.replace('\\', '/')

app.jinja_env.filters['normalize_path'] = normalize_path

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def delete_old_image(image_path):
    """Delete old image file from static folder"""
    if image_path:
        try:
            old_file_path = os.path.join('static', image_path)
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
                print(f"Deleted old image: {old_file_path}")
        except Exception as e:
            print(f"Error deleting old image {image_path}: {e}")

def save_image(file, folder='uploads', max_size=(800, 800), quality=85):
    """Save and optimize uploaded image"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + '_' + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], folder, unique_filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save original file first
        file.save(filepath)
        
        # Optimize image if it's an image file
        try:
            from PIL import Image
            with Image.open(filepath) as img:
                # Convert to RGB if necessary (for PNG with transparency)
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Resize if image is larger than max_size
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Save optimized image
                img.save(filepath, 'JPEG', quality=quality, optimize=True)
                
        except Exception as e:
            print(f"Image optimization error: {e}")
            # If optimization fails, keep the original file
        
        return f'uploads/{folder}/{unique_filename}'
    return None

def save_cropped_image(base64_data, folder='uploads'):
    """Save cropped image from base64 data"""
    import base64
    import io
    
    try:
        # Remove data URL prefix (data:image/jpeg;base64,)
        if ',' in base64_data:
            base64_data = base64_data.split(',')[1]
        
        # Decode base64 data
        image_data = base64.b64decode(base64_data)
        
        # Create unique filename
        unique_filename = str(uuid.uuid4()) + '.jpg'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], folder, unique_filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save image
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        return f'uploads/{folder}/{unique_filename}'
        
    except Exception as e:
        print(f"Error saving cropped image: {e}")
        return None

def track_page_visit():
    """Track page visit for analytics"""
    try:
        # Chỉ track các trang public, không track admin và static files
        if (request.endpoint and 
            not request.endpoint.startswith('admin') and 
            not request.endpoint.startswith('static') and
            not request.path.startswith('/static')):
            
            ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            if ip_address and ',' in ip_address:
                ip_address = ip_address.split(',')[0].strip()
            
            user_agent = request.headers.get('User-Agent', '')
            page_url = request.url
            referrer = request.headers.get('Referer', '')
            today = datetime.utcnow().date()
            
            # Kiểm tra xem IP này đã truy cập trong ngày hôm nay chưa
            existing_visit = PageVisit.query.filter_by(
                ip_address=ip_address,
                visit_date=today
            ).first()
            
            is_unique = existing_visit is None
            
            # Lưu lượt truy cập
            visit = PageVisit(
                ip_address=ip_address,
                user_agent=user_agent,
                page_url=page_url,
                referrer=referrer,
                visit_date=today,
                visit_time=datetime.utcnow(),
                is_unique=is_unique
            )
            
            db.session.add(visit)
            db.session.commit()
            
    except Exception as e:
        print(f"Error tracking page visit: {e}")
        # Không làm gián đoạn request nếu có lỗi tracking

@app.before_request
def before_request():
    """Track page visits before processing request"""
    track_page_visit()

@app.route('/')
def index():
    featured_programs = Program.query.filter_by(is_active=True, is_featured=True).limit(6).all()
    latest_news = News.query.filter_by(is_published=True).order_by(News.created_at.desc()).limit(3).all()
    gallery_images = Gallery.query.filter_by(is_featured=True).limit(8).all()
    upcoming_events = Event.query.filter_by(is_active=True).filter(Event.event_date > datetime.utcnow()).limit(3).all()
    slider_images = Slider.query.filter_by(is_active=True).order_by(Slider.order_index.asc()).all()
    intro_videos = IntroVideo.query.filter_by(is_active=True).order_by(IntroVideo.order_index.asc()).limit(3).all()
    
    # Get contact settings for social links
    contact_settings = ContactSettings.query.filter_by(is_active=True).order_by(ContactSettings.order_index.asc()).all()
    
    # Get about section data
    about_section = AboutSection.query.first()
    about_stats = AboutStats.query.filter_by(is_active=True).order_by(AboutStats.order_index.asc()).all()
    
    # Get system settings for school information
    system_settings = SystemSettings.query.first()
    
    return render_template('index.html', 
                         featured_programs=featured_programs,
                         latest_news=latest_news,
                         gallery_images=gallery_images,
                         upcoming_events=upcoming_events,
                         slider_images=slider_images,
                         intro_videos=intro_videos,
                         contact_settings=contact_settings,
                         about_section=about_section,
                         about_stats=about_stats,
                         system_settings=system_settings)

@app.route('/health')
def health_check():
    """Health check endpoint for Railway deployment"""
    try:
        # Simple database connectivity check
        db.session.execute('SELECT 1')
        return {'status': 'healthy', 'database': 'connected'}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500

@app.route('/gioi-thieu')
def about():
    team_members = TeamMember.query.filter_by(is_active=True).order_by(TeamMember.order_index.asc(), TeamMember.created_at.asc()).all()
    mission_content = MissionContent.query.first()
    mission_items = MissionItem.query.filter_by(is_active=True).order_by(MissionItem.order_index.asc(), MissionItem.created_at.asc()).all()
    
    # Add history data
    history_section = HistorySection.query.first()
    history_events = HistoryEvent.query.filter_by(is_active=True).order_by(HistoryEvent.order_index.asc(), HistoryEvent.year.asc()).all()
    
    return render_template('about.html', 
                         team_members=team_members,
                         mission_content=mission_content,
                         mission_items=mission_items,
                         history_section=history_section,
                         history_events=history_events)

@app.route('/debug-programs')
def debug_programs():
    programs = Program.query.filter_by(is_active=True).all()
    result = []
    for program in programs:
        result.append({
            'name': program.name,
            'featured_image': program.featured_image,
            'has_image': bool(program.featured_image)
        })
    return jsonify(result)

@app.route('/test-programs')
def test_programs():
    programs = Program.query.filter_by(is_active=True).all()
    return render_template('test-programs.html', programs=programs)

@app.route('/test-image')
def test_image():
    return '''
    <html>
    <body>
        <h1>Direct Image Test</h1>
        <img src="/static/uploads/programs/25185b08-c16a-4374-b328-9a22e3082848_loi-thoi.jpg" alt="Test" style="max-width: 300px;">
        <br>
        <a href="/static/uploads/programs/25185b08-c16a-4374-b328-9a22e3082848_loi-thoi.jpg">Direct link to image</a>
    </body>
    </html>
    '''

@app.route('/chuong-trinh')
def programs():
    programs = Program.query.filter_by(is_active=True).all()
    special_programs = SpecialProgram.query.filter_by(is_active=True).order_by(SpecialProgram.order_index.asc(), SpecialProgram.created_at.asc()).all()
    
    # Get CTA data for programs page
    programs_cta = CallToAction.query.filter_by(section_name='programs_cta', is_active=True).first()
    
    # Debug: Print program images
    for program in programs:
        if program.featured_image:
            print(f"Program {program.name} has image: {program.featured_image}")
            print(f"Full path: {os.path.join(app.config['UPLOAD_FOLDER'], program.featured_image.replace('uploads/', ''))}")
    return render_template('programs.html', programs=programs, special_programs=special_programs, programs_cta=programs_cta)

@app.route('/chuong-trinh/<int:id>')
def program_detail(id):
    program = Program.query.get_or_404(id)
    return render_template('program_detail.html', program=program)

@app.route('/tin-tuc')
def news():
    page = request.args.get('page', 1, type=int)
    news = News.query.filter_by(is_published=True).order_by(News.created_at.desc()).paginate(
        page=page, per_page=6, error_out=False)
    return render_template('news.html', news=news)

@app.route('/tin-tuc/<int:id>')
def news_detail(id):
    article = News.query.get_or_404(id)
    related_news = News.query.filter(News.id != id, News.is_published == True).limit(3).all()
    return render_template('news_detail.html', article=article, related_news=related_news)

@app.route('/thu-vien-anh')
def gallery():
    images = Gallery.query.order_by(Gallery.created_at.desc()).all()
    categories = db.session.query(Gallery.category).distinct().all()
    return render_template('gallery.html', images=images, categories=categories)

@app.route('/su-kien')
def events():
    upcoming = Event.query.filter_by(is_active=True).filter(Event.event_date > datetime.utcnow()).all()
    past = Event.query.filter_by(is_active=True).filter(Event.event_date <= datetime.utcnow()).all()
    return render_template('events.html', upcoming=upcoming, past=past)

@app.route('/lien-he', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        contact = Contact(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form.get('phone'),
            subject=request.form['subject'],
            message=request.form['message']
        )
        db.session.add(contact)
        db.session.commit()
        flash('Cảm ơn bạn đã liên hệ! Chúng tôi sẽ phản hồi sớm nhất có thể.', 'success')
        return redirect(url_for('contact'))
    
    # Get contact settings for display
    contact_settings = ContactSettings.query.filter_by(is_active=True).order_by(ContactSettings.order_index.asc()).all()
    
    # Get FAQ data
    faqs = FAQ.query.filter_by(is_active=True).order_by(FAQ.order_index.asc(), FAQ.created_at.asc()).all()
    
    # Get location settings for map rendering
    location_settings = LocationSettings.query.first()
    
    return render_template('contact.html', contact_settings=contact_settings, faqs=faqs, location_settings=location_settings)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Tên đăng nhập hoặc mật khẩu không đúng', 'error')
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    from datetime import datetime, timedelta
    
    # Thống kê cơ bản
    stats = {
        'posts': News.query.count(),  # Sửa từ Post thành News
        'programs': Program.query.count(),
        'gallery': Gallery.query.count(),
        'contacts': Contact.query.filter_by(is_read=False).count(),
        'news': News.query.count(),
        'events': Event.query.count(),
        'slider': Slider.query.count(),
        'total_visits': 0,  # Sẽ được cập nhật sau
        'visits_today': 0   # Sẽ được cập nhật sau
    }
    
    # Thống kê theo thời gian
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    # Tin tức mới trong tuần
    news_this_week = News.query.filter(News.created_at >= week_ago).count()
    news_this_month = News.query.filter(News.created_at >= month_ago).count()
    
    # Hình ảnh mới trong tuần
    gallery_this_week = Gallery.query.filter(Gallery.created_at >= week_ago).count()
    
    # Liên hệ mới trong tuần
    contacts_this_week = Contact.query.filter(Contact.created_at >= week_ago).count()
    
    # Thống kê lượt truy cập
    today = datetime.now().date()
    total_visits = PageVisit.query.count()
    unique_visitors_today = PageVisit.query.filter_by(visit_date=today, is_unique=True).count()
    visits_today = PageVisit.query.filter_by(visit_date=today).count()
    visits_this_week = PageVisit.query.filter(PageVisit.visit_date >= week_ago.date()).count()
    visits_this_month = PageVisit.query.filter(PageVisit.visit_date >= month_ago.date()).count()
    
    # Hoạt động gần đây (5 hoạt động mới nhất)
    recent_activities = []
    
    # Tin tức mới nhất
    latest_news = News.query.order_by(News.created_at.desc()).limit(2).all()
    for news in latest_news:
        recent_activities.append({
            'type': 'news',
            'icon': 'fas fa-newspaper',
            'color': 'blue',
            'title': f'Đã đăng tin tức "{news.title[:50]}..."',
            'time': news.created_at
        })
    
    # Hình ảnh mới nhất
    latest_gallery = Gallery.query.order_by(Gallery.created_at.desc()).limit(2).all()
    for gallery in latest_gallery:
        recent_activities.append({
            'type': 'gallery',
            'icon': 'fas fa-images',
            'color': 'purple',
            'title': f'Đã thêm hình ảnh "{gallery.title[:50]}..."',
            'time': gallery.created_at
        })
    
    # Liên hệ mới nhất
    latest_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(1).all()
    for contact in latest_contacts:
        recent_activities.append({
            'type': 'contact',
            'icon': 'fas fa-envelope',
            'color': 'orange',
            'title': f'Nhận liên hệ từ {contact.name}',
            'time': contact.created_at
        })
    
    # Sắp xếp theo thời gian và lấy 5 hoạt động mới nhất
    recent_activities.sort(key=lambda x: x['time'], reverse=True)
    recent_activities = recent_activities[:5]
    
    # Liên hệ chưa đọc
    unread_contacts = Contact.query.filter_by(is_read=False).count()
    
    # Cập nhật stats với dữ liệu lượt truy cập
    stats['total_visits'] = total_visits
    stats['visits_today'] = visits_today
    
    # Thống kê bổ sung
    additional_stats = {
        'news_this_week': news_this_week,
        'news_this_month': news_this_month,
        'gallery_this_week': gallery_this_week,
        'contacts_this_week': contacts_this_week,
        'total_contacts': Contact.query.count(),
        'unique_visitors_today': unique_visitors_today,
        'visits_this_week': visits_this_week,
        'visits_this_month': visits_this_month
    }
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         unread_contacts=unread_contacts,
                         recent_activities=recent_activities,
                         additional_stats=additional_stats)

@app.route('/admin/news')
@login_required
def admin_news():
    page = request.args.get('page', 1, type=int)
    news = News.query.order_by(News.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('admin/news/list.html', news=news)

@app.route('/admin/news/create', methods=['GET', 'POST'])
@login_required
def admin_news_create():
    if request.method == 'POST':
        news = News(
            title=request.form['title'],
            content=request.form['content'],
            summary=request.form.get('summary'),
            is_published=bool(request.form.get('is_published'))
        )
        
        if 'featured_image' in request.files:
            image_path = save_image(request.files['featured_image'], 'news')
            if image_path:
                news.featured_image = image_path
        
        db.session.add(news)
        db.session.commit()
        flash('Tin tức đã được tạo thành công!', 'success')
        return redirect(url_for('admin_news'))
    
    return render_template('admin/news/create.html')

@app.route('/admin/news/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_news_edit(id):
    news = News.query.get_or_404(id)
    
    if request.method == 'POST':
        news.title = request.form['title']
        news.content = request.form['content']
        news.summary = request.form.get('summary')
        news.is_published = bool(request.form.get('is_published'))
        
        if 'featured_image' in request.files and request.files['featured_image'].filename:
            # Delete old image before saving new one
            delete_old_image(news.featured_image)
            image_path = save_image(request.files['featured_image'], 'news')
            if image_path:
                news.featured_image = image_path
        
        db.session.commit()
        flash('Tin tức đã được cập nhật!', 'success')
        return redirect(url_for('admin_news'))
    
    return render_template('admin/news/edit.html', news=news)

@app.route('/admin/news/delete/<int:id>', methods=['POST'])
@login_required
def admin_news_delete(id):
    news = News.query.get_or_404(id)
    # Delete associated image if exists
    delete_old_image(news.featured_image)
    db.session.delete(news)
    db.session.commit()
    flash('Tin tức đã được xóa!', 'success')
    return redirect(url_for('admin_news'))

@app.route('/admin/upload-image', methods=['POST'])
@login_required
def admin_upload_image():
    """Upload image for TinyMCE editor"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Generate unique filename
            filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
            
            # Create editor images directory
            editor_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'editor')
            os.makedirs(editor_dir, exist_ok=True)
            
            # Save original file
            filepath = os.path.join(editor_dir, filename)
            file.save(filepath)
            
            # Optimize image
            try:
                with Image.open(filepath) as img:
                    # Convert to RGB if necessary
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    
                    # Resize if too large (max 1200px width)
                    if img.width > 1200:
                        ratio = 1200 / img.width
                        new_height = int(img.height * ratio)
                        img = img.resize((1200, new_height), Image.Resampling.LANCZOS)
                    
                    # Save optimized image
                    img.save(filepath, 'JPEG', quality=85, optimize=True)
            except Exception as e:
                print(f"Image optimization error: {e}")
            
            # Return the URL for TinyMCE
            image_url = url_for('static', filename=f'uploads/editor/{filename}')
            return jsonify({'location': image_url})
            
        except Exception as e:
            return jsonify({'error': f'Upload failed: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/admin/programs')
@login_required
def admin_programs():
    programs = Program.query.order_by(Program.created_at.desc()).all()
    return render_template('admin/programs/list.html', programs=programs)

@app.route('/admin/programs/create', methods=['GET', 'POST'])
@login_required
def admin_programs_create():
    if request.method == 'POST':
        program = Program(
            name=request.form['name'],
            description=request.form['description'],
            age_group=request.form['age_group'],
            price=request.form['price'],
            duration=request.form['duration'],
            is_active=bool(request.form.get('is_active')),
            is_featured=bool(request.form.get('is_featured'))
        )
        
        # Handle file upload
        if request.form.get('cropped_image_data'):
            # Use cropped image data if available
            image_path = save_cropped_image(request.form.get('cropped_image_data'), 'programs')
            if image_path:
                program.featured_image = image_path
        elif 'featured_image' in request.files and request.files['featured_image'].filename:
            # Fallback to regular file upload
            image_path = save_image(request.files['featured_image'], 'programs')
            if image_path:
                program.featured_image = image_path
        
        db.session.add(program)
        db.session.commit()
        flash('Chương trình đã được tạo thành công!', 'success')
        return redirect(url_for('admin_programs'))
    
    return render_template('admin/programs/create.html')

@app.route('/admin/programs/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_programs_edit(id):
    program = Program.query.get_or_404(id)
    
    if request.method == 'POST':
        program.name = request.form['name']
        program.description = request.form['description']
        program.age_group = request.form['age_group']
        program.price = request.form['price']
        program.duration = request.form['duration']
        program.is_active = bool(request.form.get('is_active'))
        program.is_featured = bool(request.form.get('is_featured'))
        
        # Handle file upload
        print(f"DEBUG: cropped_image_data exists: {bool(request.form.get('cropped_image_data'))}")
        print(f"DEBUG: featured_image file exists: {'featured_image' in request.files and request.files['featured_image'].filename}")
        
        if request.form.get('cropped_image_data'):
            # Use cropped image data if available
            print("DEBUG: Using cropped image data")
            delete_old_image(program.featured_image)
            image_path = save_cropped_image(request.form.get('cropped_image_data'), 'programs')
            print(f"DEBUG: Cropped image saved to: {image_path}")
            if image_path:
                program.featured_image = image_path
        elif 'featured_image' in request.files and request.files['featured_image'].filename:
            # Fallback to regular file upload
            print("DEBUG: Using regular file upload")
            delete_old_image(program.featured_image)
            image_path = save_image(request.files['featured_image'], 'programs')
            print(f"DEBUG: Regular image saved to: {image_path}")
            if image_path:
                program.featured_image = image_path
        
        db.session.commit()
        flash('Chương trình đã được cập nhật!', 'success')
        return redirect(url_for('admin_programs'))
    
    return render_template('admin/programs/edit.html', program=program)

@app.route('/admin/programs/delete/<int:id>', methods=['POST'])
@login_required
def admin_programs_delete(id):
    program = Program.query.get_or_404(id)
    # Delete associated image if exists
    delete_old_image(program.featured_image)
    db.session.delete(program)
    db.session.commit()
    flash('Chương trình đã được xóa!', 'success')
    return redirect(url_for('admin_programs'))

@app.route('/admin/gallery')
@login_required
def admin_gallery():
    page = request.args.get('page', 1, type=int)
    images = Gallery.query.order_by(Gallery.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False)
    return render_template('admin/gallery/list.html', images=images)

@app.route('/admin/gallery/create', methods=['GET', 'POST'])
@login_required
def admin_gallery_create():
    if request.method == 'POST':
        if 'images' in request.files:
            files = request.files.getlist('images')
            uploaded_count = 0
            
            for file in files:
                if file and allowed_file(file.filename):
                    image_path = save_image(file, 'gallery')
                    if image_path:
                        gallery_item = Gallery(
                            title=request.form.get('title', file.filename),
                            image_path=image_path,
                            description=request.form.get('description'),
                            category=request.form.get('category'),
                            is_featured=bool(request.form.get('is_featured'))
                        )
                        db.session.add(gallery_item)
                        uploaded_count += 1
            
            db.session.commit()
            flash(f'Đã tải lên {uploaded_count} hình ảnh thành công!', 'success')
            return redirect(url_for('admin_gallery'))
    
    return render_template('admin/gallery/create.html')

@app.route('/admin/gallery/delete/<int:id>', methods=['POST'])
@login_required
def admin_gallery_delete(id):
    image = Gallery.query.get_or_404(id)
    # Delete associated image if exists
    delete_old_image(image.image_path)
    db.session.delete(image)
    db.session.commit()
    flash('Hình ảnh đã được xóa!', 'success')
    return redirect(url_for('admin_gallery'))

@app.route('/admin/events')
@login_required
def admin_events():
    events = Event.query.order_by(Event.event_date.desc()).all()
    return render_template('admin/events/list.html', events=events)

@app.route('/admin/events/create', methods=['GET', 'POST'])
@login_required
def admin_events_create():
    if request.method == 'POST':
        event_date = datetime.strptime(
            f"{request.form['event_date']} {request.form['event_time']}", 
            '%Y-%m-%d %H:%M'
        )
        
        event = Event(
            title=request.form['title'],
            description=request.form['description'],
            event_date=event_date,
            location=request.form.get('location'),
            is_active=bool(request.form.get('is_active'))
        )
        
        if 'featured_image' in request.files:
            image_path = save_image(request.files['featured_image'], 'events')
            if image_path:
                event.featured_image = image_path
        
        db.session.add(event)
        db.session.commit()
        flash('Sự kiện đã được tạo thành công!', 'success')
        return redirect(url_for('admin_events'))
    
    return render_template('admin/events/create.html')

@app.route('/admin/events/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_events_edit(id):
    event = Event.query.get_or_404(id)
    
    if request.method == 'POST':
        # Parse datetime-local input
        event_date = datetime.strptime(request.form['event_date'], '%Y-%m-%dT%H:%M')
        
        event.title = request.form['title']
        event.description = request.form['description']
        event.event_date = event_date
        event.location = request.form.get('location')
        event.is_active = bool(request.form.get('is_active'))
        
        # Handle image upload
        if 'image' in request.files and request.files['image'].filename:
            # Delete old image before saving new one
            if event.featured_image:
                delete_old_image(event.featured_image)
            image_path = save_image(request.files['image'], 'events')
            if image_path:
                event.featured_image = image_path
        
        # Handle image removal
        if request.form.get('remove_image') == '1':
            if event.featured_image:
                delete_old_image(event.featured_image)
            event.featured_image = None
        
        db.session.commit()
        flash('Sự kiện đã được cập nhật!', 'success')
        return redirect(url_for('admin_events'))
    
    return render_template('admin/events/edit.html', event=event)

@app.route('/admin/events/delete/<int:id>', methods=['POST'])
@login_required
def admin_events_delete(id):
    event = Event.query.get_or_404(id)
    # Delete associated image if exists
    if event.featured_image:
        delete_old_image(event.featured_image)
    db.session.delete(event)
    db.session.commit()
    flash('Sự kiện đã được xóa!', 'success')
    return redirect(url_for('admin_events'))

@app.route('/admin/contacts')
@login_required
def admin_contacts():
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts/list.html', contacts=contacts)

@app.route('/admin/contacts/mark-read/<int:id>')
@login_required
def admin_contacts_mark_read(id):
    contact = Contact.query.get_or_404(id)
    contact.is_read = True
    db.session.commit()
    return redirect(url_for('admin_contacts'))

@app.route('/admin/contacts/delete/<int:id>', methods=['POST'])
@login_required
def admin_contacts_delete(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('Tin nhắn đã được xóa!', 'success')
    return redirect(url_for('admin_contacts'))

@app.route('/admin/posts')
@login_required
def admin_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/posts/list.html', posts=posts)

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    if request.method == 'POST':
        # Lấy hoặc tạo mới system settings
        settings = SystemSettings.query.first()
        if not settings:
            settings = SystemSettings()
            db.session.add(settings)
        
        # Cập nhật thông tin trường
        settings.school_name = request.form.get('school_name', settings.school_name)
        settings.school_address = request.form.get('school_address', settings.school_address)
        settings.school_phone = request.form.get('school_phone', settings.school_phone)
        settings.school_email = request.form.get('school_email', settings.school_email)
        
        # Cập nhật cài đặt website
        settings.maintenance_mode = bool(request.form.get('maintenance_mode'))
        settings.allow_registration = bool(request.form.get('allow_registration'))
        
        settings.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Cài đặt đã được lưu thành công!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Có lỗi xảy ra khi lưu cài đặt!', 'error')
        
        return redirect(url_for('admin_settings'))
    
    # GET request - hiển thị form
    settings = SystemSettings.query.first()
    if not settings:
        settings = SystemSettings()
        db.session.add(settings)
        db.session.commit()
    
    return render_template('admin/settings.html', settings=settings)

@app.route('/admin/homepage', methods=['GET', 'POST'])
@login_required
def admin_homepage():
    if request.method == 'POST':
        # Lấy hoặc tạo mới homepage settings
        homepage = HomePageSettings.query.first()
        if not homepage:
            homepage = HomePageSettings()
            db.session.add(homepage)
        
        # Cập nhật Hero Section - both old and new fields
        homepage.hero_subtitle = request.form.get('hero_subtitle', homepage.hero_subtitle)
        homepage.hero_cta_text_1 = request.form.get('hero_cta_text_1', homepage.hero_cta_text_1)
        homepage.hero_cta_text_2 = request.form.get('hero_cta_text_2', homepage.hero_cta_text_2)
        
        # New simple hero fields
        homepage.hero_title_line1 = request.form.get('hero_title_line1', homepage.hero_title_line1)
        homepage.hero_title_line2 = request.form.get('hero_title_line2', homepage.hero_title_line2)
        
        # Auto-generate hero_title from simple fields
        if homepage.hero_title_line1 and homepage.hero_title_line2:
            homepage.hero_title = f'{homepage.hero_title_line1}<br><span class="text-yellow-300">{homepage.hero_title_line2}</span>'
        
        # Cập nhật Video Section
        homepage.video_section_badge = request.form.get('video_section_badge', homepage.video_section_badge)
        homepage.video_section_description = request.form.get('video_section_description', homepage.video_section_description)
        homepage.video_cta_text = request.form.get('video_cta_text', homepage.video_cta_text)
        homepage.video_contact_text = request.form.get('video_contact_text', homepage.video_contact_text)
        
        # New simple video fields
        homepage.video_section_title_normal = request.form.get('video_section_title_normal', homepage.video_section_title_normal)
        homepage.video_section_title_highlight = request.form.get('video_section_title_highlight', homepage.video_section_title_highlight)
        
        # Auto-generate video_section_title from simple fields
        if homepage.video_section_title_normal and homepage.video_section_title_highlight:
            homepage.video_section_title = f'{homepage.video_section_title_normal} <span class="text-primary">{homepage.video_section_title_highlight}</span>'
        
        # Cập nhật Programs Section
        homepage.programs_section_description = request.form.get('programs_section_description', homepage.programs_section_description)
        homepage.programs_cta_text = request.form.get('programs_cta_text', homepage.programs_cta_text)
        
        # New simple programs fields
        homepage.programs_section_title_text = request.form.get('programs_section_title_text', homepage.programs_section_title_text)
        
        # Auto-generate programs_section_title from simple fields
        if homepage.programs_section_title_text:
            homepage.programs_section_title = f'<span class="text-primary font-patrick">{homepage.programs_section_title_text}</span>'
        
        # Cập nhật Features Section
        homepage.features_section_badge = request.form.get('features_section_badge', homepage.features_section_badge)
        homepage.features_section_title = request.form.get('features_section_title', homepage.features_section_title)
        homepage.features_section_description = request.form.get('features_section_description', homepage.features_section_description)
        homepage.features_cta_text = request.form.get('features_cta_text', homepage.features_cta_text)
        homepage.features_contact_text = request.form.get('features_contact_text', homepage.features_contact_text)
        
        # Cập nhật News Section
        homepage.news_section_description = request.form.get('news_section_description', homepage.news_section_description)
        homepage.news_cta_text = request.form.get('news_cta_text', homepage.news_cta_text)
        
        # New simple news fields
        homepage.news_section_title_text = request.form.get('news_section_title_text', homepage.news_section_title_text)
        
        # Auto-generate news_section_title from simple fields
        if homepage.news_section_title_text:
            homepage.news_section_title = f'<span class="text-primary font-patrick">{homepage.news_section_title_text}</span>'
        
        # Cập nhật Gallery Section
        homepage.gallery_section_description = request.form.get('gallery_section_description', homepage.gallery_section_description)
        homepage.gallery_cta_text = request.form.get('gallery_cta_text', homepage.gallery_cta_text)
        
        # New simple gallery fields
        homepage.gallery_section_title_text = request.form.get('gallery_section_title_text', homepage.gallery_section_title_text)
        
        # Auto-generate gallery_section_title from simple fields
        if homepage.gallery_section_title_text:
            homepage.gallery_section_title = f'<span class="text-primary font-patrick">{homepage.gallery_section_title_text}</span>'
        
        # Cập nhật Events Section
        homepage.events_section_description = request.form.get('events_section_description', homepage.events_section_description)
        homepage.events_cta_text = request.form.get('events_cta_text', homepage.events_cta_text)
        
        # New simple events fields
        homepage.events_section_title_text = request.form.get('events_section_title_text', homepage.events_section_title_text)
        
        # Auto-generate events_section_title from simple fields
        if homepage.events_section_title_text:
            homepage.events_section_title = f'<span class="text-primary font-patrick">{homepage.events_section_title_text}</span>'
        
        # Cập nhật Final CTA Section
        homepage.cta_title = request.form.get('cta_title', homepage.cta_title)
        homepage.cta_description = request.form.get('cta_description', homepage.cta_description)
        homepage.cta_button_1 = request.form.get('cta_button_1', homepage.cta_button_1)
        homepage.cta_button_2 = request.form.get('cta_button_2', homepage.cta_button_2)
        
        homepage.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Nội dung trang chủ đã được cập nhật thành công!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Có lỗi xảy ra khi cập nhật nội dung trang chủ!', 'error')
        
        return redirect(url_for('admin_homepage'))
    
    # GET request - hiển thị form
    homepage = HomePageSettings.query.first()
    if not homepage:
        homepage = HomePageSettings()
        db.session.add(homepage)
        db.session.commit()
    
    return render_template('admin/homepage.html', homepage=homepage)

@app.route('/admin/slider')
@login_required
def admin_slider():
    sliders = Slider.query.order_by(Slider.order_index.asc()).all()
    return render_template('admin/slider/list.html', sliders=sliders)

@app.route('/admin/slider/create', methods=['GET', 'POST'])
@login_required
def admin_slider_create():
    if request.method == 'POST':
        slider = Slider(
            title=request.form['title'],
            description=request.form.get('description'),
            order_index=int(request.form.get('order_index', 0)),
            is_active=bool(request.form.get('is_active'))
        )
        
        if 'image' in request.files:
            image_path = save_image(request.files['image'], 'slider')
            if image_path:
                slider.image_path = image_path
            else:
                flash('Vui lòng chọn hình ảnh hợp lệ!', 'error')
                return render_template('admin/slider/create.html')
        else:
            flash('Vui lòng chọn hình ảnh!', 'error')
            return render_template('admin/slider/create.html')
        
        db.session.add(slider)
        db.session.commit()
        flash('Slider đã được tạo thành công!', 'success')
        return redirect(url_for('admin_slider'))
    
    return render_template('admin/slider/create.html')

@app.route('/admin/slider/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_slider_edit(id):
    slider = Slider.query.get_or_404(id)
    
    if request.method == 'POST':
        slider.title = request.form['title']
        slider.description = request.form.get('description')
        slider.order_index = int(request.form.get('order_index', 0))
        slider.is_active = bool(request.form.get('is_active'))
        
        if 'image' in request.files and request.files['image'].filename:
            # Delete old image before saving new one
            delete_old_image(slider.image_path)
            image_path = save_image(request.files['image'], 'slider')
            if image_path:
                slider.image_path = image_path
        
        db.session.commit()
        flash('Slider đã được cập nhật!', 'success')
        return redirect(url_for('admin_slider'))
    
    return render_template('admin/slider/edit.html', slider=slider)

@app.route('/admin/slider/delete/<int:id>', methods=['POST'])
@login_required
def admin_slider_delete(id):
    slider = Slider.query.get_or_404(id)
    # Delete associated image if exists
    delete_old_image(slider.image_path)
    db.session.delete(slider)
    db.session.commit()
    flash('Slider đã được xóa!', 'success')
    return redirect(url_for('admin_slider'))

@app.route('/admin/contact-settings')
@login_required
def admin_contact_settings():
    settings = ContactSettings.query.order_by(ContactSettings.order_index.asc()).all()
    return render_template('admin/contact_settings/list.html', settings=settings)

@app.route('/admin/contact-settings/create', methods=['GET', 'POST'])
@login_required
def admin_contact_settings_create():
    if request.method == 'POST':
        setting = ContactSettings(
            setting_key=request.form['setting_key'],
            setting_value=request.form['setting_value'],
            setting_type=request.form['setting_type'],
            display_name=request.form['display_name'],
            description=request.form.get('description'),
            is_active=bool(request.form.get('is_active')),
            order_index=int(request.form.get('order_index', 0))
        )
        
        db.session.add(setting)
        db.session.commit()
        flash('Thông tin liên hệ đã được tạo thành công!', 'success')
        return redirect(url_for('admin_contact_settings'))
    
    return render_template('admin/contact_settings/create.html')

@app.route('/admin/contact-settings/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_contact_settings_edit(id):
    setting = ContactSettings.query.get_or_404(id)
    
    if request.method == 'POST':
        setting.setting_key = request.form['setting_key']
        setting.setting_value = request.form['setting_value']
        setting.setting_type = request.form['setting_type']
        setting.display_name = request.form['display_name']
        setting.description = request.form.get('description')
        setting.is_active = bool(request.form.get('is_active'))
        setting.order_index = int(request.form.get('order_index', 0))
        
        db.session.commit()
        flash('Thông tin liên hệ đã được cập nhật!', 'success')
        return redirect(url_for('admin_contact_settings'))
    
    return render_template('admin/contact_settings/edit.html', setting=setting)

@app.route('/admin/contact-settings/delete/<int:id>', methods=['POST'])
@login_required
def admin_contact_settings_delete(id):
    setting = ContactSettings.query.get_or_404(id)
    db.session.delete(setting)
    db.session.commit()
    flash('Thông tin liên hệ đã được xóa!', 'success')
    return redirect(url_for('admin_contact_settings'))

# Theme Management Routes
@app.route('/admin/themes')
@login_required
def admin_themes():
    themes = ThemeSettings.query.order_by(ThemeSettings.created_at.desc()).all()
    return render_template('admin/themes/list.html', themes=themes)

@app.route('/admin/themes/switch/<int:theme_id>', methods=['POST'])
@login_required
def admin_theme_switch(theme_id):
    if switch_theme(theme_id):
        flash('Theme đã được thay đổi thành công!', 'success')
    else:
        flash('Có lỗi xảy ra khi thay đổi theme!', 'error')
    return redirect(url_for('admin_themes'))

@app.route('/admin/themes/create', methods=['GET', 'POST'])
@login_required
def admin_theme_create():
    if request.method == 'POST':
        theme_name = request.form['theme_name']
        primary_color = request.form['primary_color']
        secondary_color = request.form['secondary_color']
        accent_color = request.form.get('accent_color', '')
        background_color = request.form.get('background_color', '#ffffff')
        text_color = request.form.get('text_color', '#333333')
        
        theme = ThemeSettings(
            theme_name=theme_name,
            primary_color=primary_color,
            secondary_color=secondary_color,
            accent_color=accent_color,
            background_color=background_color,
            text_color=text_color
        )
        
        db.session.add(theme)
        db.session.commit()
        flash('Theme mới đã được tạo thành công!', 'success')
        return redirect(url_for('admin_themes'))
    
    return render_template('admin/themes/create.html')

@app.route('/admin/themes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_theme_edit(id):
    theme = ThemeSettings.query.get_or_404(id)
    
    if request.method == 'POST':
        theme.theme_name = request.form['theme_name']
        theme.primary_color = request.form['primary_color']
        theme.secondary_color = request.form['secondary_color']
        theme.accent_color = request.form.get('accent_color', '')
        theme.background_color = request.form.get('background_color', '#ffffff')
        theme.text_color = request.form.get('text_color', '#333333')
        
        db.session.commit()
        flash('Theme đã được cập nhật thành công!', 'success')
        return redirect(url_for('admin_themes'))
    
    return render_template('admin/themes/edit.html', theme=theme)

@app.route('/admin/themes/delete/<int:id>', methods=['POST'])
@login_required
def admin_theme_delete(id):
    theme = ThemeSettings.query.get_or_404(id)
    
    # Không cho phép xóa theme đang được sử dụng hoặc theme mặc định
    if theme.is_active:
        flash('Không thể xóa theme đang được sử dụng!', 'error')
        return redirect(url_for('admin_themes'))
    
    if theme.is_default:
        flash('Không thể xóa theme mặc định!', 'error')
        return redirect(url_for('admin_themes'))
    
    db.session.delete(theme)
    db.session.commit()
    flash('Theme đã được xóa thành công!', 'success')
    return redirect(url_for('admin_themes'))

# API endpoint for theme switching (for frontend)
@app.route('/api/switch-theme', methods=['POST'])
def api_switch_theme():
    try:
        data = request.get_json()
        theme_id = data.get('theme_id')
        
        if not theme_id:
            return jsonify({'success': False, 'message': 'Theme ID is required'})
        
        if switch_theme(theme_id):
            return jsonify({'success': True, 'message': 'Theme switched successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to switch theme'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# API endpoint to get all themes
@app.route('/api/themes', methods=['GET'])
def api_get_themes():
    try:
        themes = ThemeSettings.query.all()
        themes_data = []
        for theme in themes:
            themes_data.append({
                'id': theme.id,
                'theme_name': theme.theme_name,
                'primary_color': theme.primary_color,
                'secondary_color': theme.secondary_color,
                'accent_color': theme.accent_color,
                'is_active': theme.is_active,
                'is_default': theme.is_default
            })
        return jsonify({'success': True, 'themes': themes_data})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Team Management Routes
@app.route('/admin/team')
@login_required
def admin_team():
    team_members = TeamMember.query.order_by(TeamMember.order_index.asc(), TeamMember.created_at.desc()).all()
    return render_template('admin/team/list.html', team_members=team_members)

@app.route('/admin/team/create', methods=['GET', 'POST'])
@login_required
def admin_team_create():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        description = request.form.get('description', '')
        order_index = int(request.form.get('order_index', 0))
        is_active = bool(request.form.get('is_active'))
        
        # Handle file upload
        image_path = None
        if request.form.get('cropped_image_data'):
            # Use cropped image data if available
            image_path = save_cropped_image(request.form.get('cropped_image_data'), 'team')
        elif 'image' in request.files and request.files['image'].filename:
            # Fallback to regular file upload
            image_path = save_image(request.files['image'], 'team')
        
        team_member = TeamMember(
            name=name,
            position=position,
            description=description,
            image_path=image_path,
            order_index=order_index,
            is_active=is_active
        )
        
        db.session.add(team_member)
        db.session.commit()
        
        flash('Thành viên đội ngũ đã được thêm!', 'success')
        return redirect(url_for('admin_team'))
    
    return render_template('admin/team/create.html')

@app.route('/admin/team/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_team_edit(id):
    team_member = TeamMember.query.get_or_404(id)
    
    if request.method == 'POST':
        team_member.name = request.form['name']
        team_member.position = request.form['position']
        team_member.description = request.form.get('description', '')
        team_member.order_index = int(request.form.get('order_index', 0))
        team_member.is_active = bool(request.form.get('is_active'))
        
        # Handle file upload
        if request.form.get('cropped_image_data'):
            # Use cropped image data if available
            delete_old_image(team_member.image_path)
            image_path = save_cropped_image(request.form.get('cropped_image_data'), 'team')
            if image_path:
                team_member.image_path = image_path
        elif 'image' in request.files and request.files['image'].filename:
            # Fallback to regular file upload
            delete_old_image(team_member.image_path)
            image_path = save_image(request.files['image'], 'team')
            if image_path:
                team_member.image_path = image_path
        
        db.session.commit()
        flash('Thông tin thành viên đã được cập nhật!', 'success')
        return redirect(url_for('admin_team'))
    
    return render_template('admin/team/edit.html', team_member=team_member)

@app.route('/admin/team/delete/<int:id>', methods=['POST'])
@login_required
def admin_team_delete(id):
    team_member = TeamMember.query.get_or_404(id)
    
    # Delete image file if exists
    delete_old_image(team_member.image_path)
    
    db.session.delete(team_member)
    db.session.commit()
    
    flash('Thành viên đội ngũ đã được xóa!', 'success')
    return redirect(url_for('admin_team'))

# Mission Management Routes
@app.route('/admin/mission')
@login_required
def admin_mission():
    mission_content = MissionContent.query.first()
    mission_items = MissionItem.query.order_by(MissionItem.order_index.asc(), MissionItem.created_at.desc()).all()
    return render_template('admin/mission/index.html', mission_content=mission_content, mission_items=mission_items)

@app.route('/admin/mission/content', methods=['GET', 'POST'])
@login_required
def admin_mission_content():
    mission_content = MissionContent.query.first()
    if not mission_content:
        mission_content = MissionContent()
        db.session.add(mission_content)
        db.session.commit()
    
    if request.method == 'POST':
        mission_content.main_title = request.form['main_title']
        mission_content.stats_number = request.form['stats_number']
        mission_content.stats_text = request.form['stats_text']
        
        # Handle file upload
        if 'main_image' in request.files and request.files['main_image'].filename:
            # Delete old image before saving new one
            delete_old_image(mission_content.main_image)
            image_path = save_image(request.files['main_image'], 'mission')
            if image_path:
                mission_content.main_image = image_path
        
        db.session.commit()
        flash('Nội dung sứ mệnh đã được cập nhật!', 'success')
        return redirect(url_for('admin_mission'))
    
    return render_template('admin/mission/content.html', mission_content=mission_content)

@app.route('/admin/mission/items/create', methods=['GET', 'POST'])
@login_required
def admin_mission_item_create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        icon = request.form['icon']
        color = request.form['color']
        order_index = int(request.form.get('order_index', 0))
        is_active = bool(request.form.get('is_active'))
        
        mission_item = MissionItem(
            title=title,
            description=description,
            icon=icon,
            color=color,
            order_index=order_index,
            is_active=is_active
        )
        
        db.session.add(mission_item)
        db.session.commit()
        
        flash('Mục tiêu sứ mệnh đã được thêm!', 'success')
        return redirect(url_for('admin_mission'))
    
    return render_template('admin/mission/item_create.html')

@app.route('/admin/mission/items/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_mission_item_edit(id):
    mission_item = MissionItem.query.get_or_404(id)
    
    if request.method == 'POST':
        mission_item.title = request.form['title']
        mission_item.description = request.form['description']
        mission_item.icon = request.form['icon']
        mission_item.color = request.form['color']
        mission_item.order_index = int(request.form.get('order_index', 0))
        mission_item.is_active = bool(request.form.get('is_active'))
        
        db.session.commit()
        flash('Mục tiêu sứ mệnh đã được cập nhật!', 'success')
        return redirect(url_for('admin_mission'))
    
    return render_template('admin/mission/item_edit.html', mission_item=mission_item)

@app.route('/admin/mission/items/delete/<int:id>', methods=['POST'])
@login_required
def admin_mission_item_delete(id):
    mission_item = MissionItem.query.get_or_404(id)
    db.session.delete(mission_item)
    db.session.commit()
    
    flash('Mục tiêu sứ mệnh đã được xóa!', 'success')
    return redirect(url_for('admin_mission'))

# History Management Routes
@app.route('/admin/history')
@login_required
def admin_history():
    history_section = HistorySection.query.first()
    history_events = HistoryEvent.query.order_by(HistoryEvent.order_index.asc(), HistoryEvent.year.asc()).all()
    return render_template('admin/history/index.html', history_section=history_section, history_events=history_events)

@app.route('/admin/history/section', methods=['GET', 'POST'])
@login_required
def admin_history_section():
    history_section = HistorySection.query.first()
    if not history_section:
        history_section = HistorySection()
        db.session.add(history_section)
        db.session.commit()
    
    if request.method == 'POST':
        history_section.main_title = request.form['main_title']
        history_section.subtitle = request.form['subtitle']
        
        db.session.commit()
        flash('Thông tin phần lịch sử đã được cập nhật!', 'success')
        return redirect(url_for('admin_history'))
    
    return render_template('admin/history/section.html', history_section=history_section)

@app.route('/admin/history/events/create', methods=['GET', 'POST'])
@login_required
def admin_history_event_create():
    if request.method == 'POST':
        year = request.form['year']
        title = request.form['title']
        description = request.form['description']
        color = request.form['color']
        order_index = int(request.form.get('order_index', 0))
        is_active = bool(request.form.get('is_active'))
        
        # Handle file upload
        image_path = None
        if 'image' in request.files:
            image_path = save_image(request.files['image'], 'history')
        
        history_event = HistoryEvent(
            year=year,
            title=title,
            description=description,
            color=color,
            image_path=image_path,
            order_index=order_index,
            is_active=is_active
        )
        
        db.session.add(history_event)
        db.session.commit()
        
        flash('Sự kiện lịch sử đã được thêm!', 'success')
        return redirect(url_for('admin_history'))
    
    return render_template('admin/history/event_create.html')

@app.route('/admin/history/events/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_history_event_edit(id):
    history_event = HistoryEvent.query.get_or_404(id)
    
    if request.method == 'POST':
        history_event.year = request.form['year']
        history_event.title = request.form['title']
        history_event.description = request.form['description']
        history_event.color = request.form['color']
        history_event.order_index = int(request.form.get('order_index', 0))
        history_event.is_active = bool(request.form.get('is_active'))
        
        # Handle file upload
        if 'image' in request.files and request.files['image'].filename:
            # Delete old image before saving new one
            delete_old_image(history_event.image_path)
            image_path = save_image(request.files['image'], 'history')
            if image_path:
                history_event.image_path = image_path
        
        db.session.commit()
        flash('Sự kiện lịch sử đã được cập nhật!', 'success')
        return redirect(url_for('admin_history'))
    
    return render_template('admin/history/event_edit.html', history_event=history_event)

@app.route('/admin/history/events/delete/<int:id>', methods=['POST'])
@login_required
def admin_history_event_delete(id):
    history_event = HistoryEvent.query.get_or_404(id)
    
    # Delete image file if exists
    delete_old_image(history_event.image_path)
    
    db.session.delete(history_event)
    db.session.commit()
    
    flash('Sự kiện lịch sử đã được xóa!', 'success')
    return redirect(url_for('admin_history'))

# About Section Management Routes
@app.route('/admin/about')
@login_required
def admin_about():
    about_section = AboutSection.query.first()
    about_stats = AboutStats.query.order_by(AboutStats.order_index.asc(), AboutStats.created_at.desc()).all()
    return render_template('admin/about/index.html', about_section=about_section, about_stats=about_stats)

@app.route('/admin/about/content', methods=['GET', 'POST'])
@login_required
def admin_about_content():
    about_section = AboutSection.query.first()
    if not about_section:
        about_section = AboutSection()
        db.session.add(about_section)
        db.session.commit()
    
    if request.method == 'POST':
        about_section.title = request.form['title']
        about_section.subtitle = request.form['subtitle']
        about_section.description_1 = request.form['description_1']
        about_section.description_2 = request.form['description_2']
        about_section.experience_years = request.form['experience_years']
        about_section.experience_text = request.form['experience_text']
        
        # Handle image uploads
        if 'image_1' in request.files and request.files['image_1'].filename:
            # Delete old image before saving new one
            delete_old_image(about_section.image_1)
            image_path = save_image(request.files['image_1'], 'about')
            if image_path:
                about_section.image_1 = image_path
        
        if 'image_2' in request.files and request.files['image_2'].filename:
            # Delete old image before saving new one
            delete_old_image(about_section.image_2)
            image_path = save_image(request.files['image_2'], 'about')
            if image_path:
                about_section.image_2 = image_path
        
        db.session.commit()
        flash('Nội dung "Về chúng tôi" đã được cập nhật!', 'success')
        return redirect(url_for('admin_about'))
    
    return render_template('admin/about/content.html', about_section=about_section)

@app.route('/admin/about/stats/create', methods=['GET', 'POST'])
@login_required
def admin_about_stats_create():
    if request.method == 'POST':
        stat_key = request.form['stat_key']
        stat_value = request.form['stat_value']
        stat_label = request.form['stat_label']
        icon_class = request.form['icon_class']
        color_class = request.form['color_class']
        order_index = int(request.form.get('order_index', 0))
        is_active = bool(request.form.get('is_active'))
        
        about_stat = AboutStats(
            stat_key=stat_key,
            stat_value=stat_value,
            stat_label=stat_label,
            icon_class=icon_class,
            color_class=color_class,
            order_index=order_index,
            is_active=is_active
        )
        
        db.session.add(about_stat)
        db.session.commit()
        
        flash('Thống kê đã được thêm!', 'success')
        return redirect(url_for('admin_about'))
    
    return render_template('admin/about/stats_create.html')

@app.route('/admin/about/stats/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_about_stats_edit(id):
    about_stat = AboutStats.query.get_or_404(id)
    
    if request.method == 'POST':
        about_stat.stat_key = request.form['stat_key']
        about_stat.stat_value = request.form['stat_value']
        about_stat.stat_label = request.form['stat_label']
        about_stat.icon_class = request.form['icon_class']
        about_stat.color_class = request.form['color_class']
        about_stat.order_index = int(request.form.get('order_index', 0))
        about_stat.is_active = bool(request.form.get('is_active'))
        
        db.session.commit()
        flash('Thống kê đã được cập nhật!', 'success')
        return redirect(url_for('admin_about'))
    
    return render_template('admin/about/stats_edit.html', about_stat=about_stat)

@app.route('/admin/about/stats/delete/<int:id>', methods=['POST'])
@login_required
def admin_about_stats_delete(id):
    about_stat = AboutStats.query.get_or_404(id)
    db.session.delete(about_stat)
    db.session.commit()
    
    flash('Thống kê đã được xóa!', 'success')
    return redirect(url_for('admin_about'))

# FAQ Management Routes
@app.route('/admin/faq')
@login_required
def admin_faq():
    faqs = FAQ.query.order_by(FAQ.order_index.asc(), FAQ.created_at.desc()).all()
    return render_template('admin/faq/index.html', faqs=faqs)

@app.route('/admin/faq/create', methods=['GET', 'POST'])
@login_required
def admin_faq_create():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        category = request.form.get('category', 'general')
        order_index = int(request.form.get('order_index', 0))
        is_active = bool(request.form.get('is_active'))
        
        faq = FAQ(
            question=question,
            answer=answer,
            category=category,
            order_index=order_index,
            is_active=is_active
        )
        
        db.session.add(faq)
        db.session.commit()
        
        flash('Câu hỏi thường gặp đã được thêm!', 'success')
        return redirect(url_for('admin_faq'))
    
    return render_template('admin/faq/create.html')

@app.route('/admin/faq/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_faq_edit(id):
    faq = FAQ.query.get_or_404(id)
    
    if request.method == 'POST':
        faq.question = request.form['question']
        faq.answer = request.form['answer']
        faq.category = request.form.get('category', 'general')
        faq.order_index = int(request.form.get('order_index', 0))
        faq.is_active = bool(request.form.get('is_active'))
        
        db.session.commit()
        flash('Câu hỏi thường gặp đã được cập nhật!', 'success')
        return redirect(url_for('admin_faq'))
    
    return render_template('admin/faq/edit.html', faq=faq)

@app.route('/admin/faq/delete/<int:id>', methods=['POST'])
@login_required
def admin_faq_delete(id):
    faq = FAQ.query.get_or_404(id)
    db.session.delete(faq)
    db.session.commit()
    
    flash('Câu hỏi thường gặp đã được xóa!', 'success')
    return redirect(url_for('admin_faq'))

# Special Programs Management Routes
@app.route('/admin/special-programs')
@login_required
def admin_special_programs():
    special_programs = SpecialProgram.query.order_by(SpecialProgram.order_index.asc(), SpecialProgram.created_at.desc()).all()
    return render_template('admin/special_programs/index.html', special_programs=special_programs)

@app.route('/admin/special-programs/create', methods=['GET', 'POST'])
@login_required
def admin_special_programs_create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        icon_class = request.form.get('icon_class', 'fas fa-star')
        background_gradient = request.form.get('background_gradient', 'from-blue-50 to-purple-50')
        border_color = request.form.get('border_color', 'border-blue-200')
        icon_bg_color = request.form.get('icon_bg_color', 'bg-blue-500')
        features = request.form.get('features', '')
        order_index = int(request.form.get('order_index', 0))
        is_active = bool(request.form.get('is_active'))
        
        # Handle image upload
        image_path = None
        if 'image' in request.files and request.files['image'].filename:
            image_path = save_image(request.files['image'], 'special_programs')
        
        special_program = SpecialProgram(
            title=title,
            description=description,
            icon_class=icon_class,
            background_gradient=background_gradient,
            border_color=border_color,
            icon_bg_color=icon_bg_color,
            features=features,
            image_path=image_path,
            order_index=order_index,
            is_active=is_active
        )
        
        db.session.add(special_program)
        db.session.commit()
        
        flash('Chương trình đặc biệt đã được thêm!', 'success')
        return redirect(url_for('admin_special_programs'))
    
    return render_template('admin/special_programs/create.html')

@app.route('/admin/special-programs/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_special_programs_edit(id):
    special_program = SpecialProgram.query.get_or_404(id)
    
    if request.method == 'POST':
        special_program.title = request.form['title']
        special_program.description = request.form['description']
        special_program.icon_class = request.form.get('icon_class', 'fas fa-star')
        special_program.background_gradient = request.form.get('background_gradient', 'from-blue-50 to-purple-50')
        special_program.border_color = request.form.get('border_color', 'border-blue-200')
        special_program.icon_bg_color = request.form.get('icon_bg_color', 'bg-blue-500')
        special_program.features = request.form.get('features', '')
        special_program.order_index = int(request.form.get('order_index', 0))
        special_program.is_active = bool(request.form.get('is_active'))
        
        # Handle image upload
        if 'image' in request.files and request.files['image'].filename:
            # Delete old image before saving new one
            delete_old_image(special_program.image_path)
            special_program.image_path = save_image(request.files['image'], 'special_programs')
        
        db.session.commit()
        flash('Chương trình đặc biệt đã được cập nhật!', 'success')
        return redirect(url_for('admin_special_programs'))
    
    return render_template('admin/special_programs/edit.html', special_program=special_program)

@app.route('/admin/special-programs/delete/<int:id>', methods=['POST'])
@login_required
def admin_special_programs_delete(id):
    special_program = SpecialProgram.query.get_or_404(id)
    
    # Delete associated image if exists
    delete_old_image(special_program.image_path)
    
    db.session.delete(special_program)
    db.session.commit()
    
    flash('Chương trình đặc biệt đã được xóa!', 'success')
    return redirect(url_for('admin_special_programs'))

# Call-to-Action Management Routes
@app.route('/admin/call-to-action')
@login_required
def admin_cta():
    cta_sections = CallToAction.query.order_by(CallToAction.section_name.asc()).all()
    return render_template('admin/cta/index.html', cta_sections=cta_sections)

@app.route('/admin/call-to-action/create', methods=['GET', 'POST'])
@login_required
def admin_cta_create():
    if request.method == 'POST':
        section_name = request.form['section_name']
        main_title = request.form['main_title']
        subtitle = request.form['subtitle']
        phone_number = request.form.get('phone_number', '0123 456 789')
        email = request.form.get('email', 'info@hoahuongduong.edu.vn')
        working_hours = request.form.get('working_hours', 'Thứ 2 - Thứ 6: 7:00 - 17:00')
        email_response_time = request.form.get('email_response_time', 'Phản hồi trong 24h')
        visit_note = request.form.get('visit_note', 'Đặt lịch trước 1 ngày')
        promotion_title = request.form.get('promotion_title', 'Ưu đãi đặc biệt cho phụ huynh mới')
        promotion_description = request.form.get('promotion_description', '')
        promotion_note = request.form.get('promotion_note', 'Ưu đãi có hạn đến hết tháng này')
        is_active = bool(request.form.get('is_active'))
        
        cta = CallToAction(
            section_name=section_name,
            main_title=main_title,
            subtitle=subtitle,
            phone_number=phone_number,
            email=email,
            working_hours=working_hours,
            email_response_time=email_response_time,
            visit_note=visit_note,
            promotion_title=promotion_title,
            promotion_description=promotion_description,
            promotion_note=promotion_note,
            is_active=is_active
        )
        
        db.session.add(cta)
        db.session.commit()
        
        flash('Call-to-Action đã được thêm!', 'success')
        return redirect(url_for('admin_cta'))
    
    return render_template('admin/cta/create.html')

@app.route('/admin/call-to-action/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_cta_edit(id):
    cta = CallToAction.query.get_or_404(id)
    
    if request.method == 'POST':
        cta.section_name = request.form['section_name']
        cta.main_title = request.form['main_title']
        cta.subtitle = request.form['subtitle']
        cta.phone_number = request.form.get('phone_number', '0123 456 789')
        cta.email = request.form.get('email', 'info@hoahuongduong.edu.vn')
        cta.working_hours = request.form.get('working_hours', 'Thứ 2 - Thứ 6: 7:00 - 17:00')
        cta.email_response_time = request.form.get('email_response_time', 'Phản hồi trong 24h')
        cta.visit_note = request.form.get('visit_note', 'Đặt lịch trước 1 ngày')
        cta.promotion_title = request.form.get('promotion_title', 'Ưu đãi đặc biệt cho phụ huynh mới')
        cta.promotion_description = request.form.get('promotion_description', '')
        cta.promotion_note = request.form.get('promotion_note', 'Ưu đãi có hạn đến hết tháng này')
        cta.is_active = bool(request.form.get('is_active'))
        
        db.session.commit()
        flash('Call-to-Action đã được cập nhật!', 'success')
        return redirect(url_for('admin_cta'))
    
    return render_template('admin/cta/edit.html', cta=cta)

@app.route('/admin/call-to-action/delete/<int:id>', methods=['POST'])
@login_required
def admin_cta_delete(id):
    cta = CallToAction.query.get_or_404(id)
    db.session.delete(cta)
    db.session.commit()
    
    flash('Call-to-Action đã được xóa!', 'success')
    return redirect(url_for('admin_cta'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        if not User.query.first():
            admin = User(
                username='admin',
                email='admin@hoahuongduong.edu.vn',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()
        
        # Add default contact settings if none exist
        if not ContactSettings.query.first():
            default_settings = [
                ContactSettings(
                    setting_key='phone_main',
                    setting_value='028-3823-4567',
                    setting_type='phone',
                    display_name='Số điện thoại chính',
                    description='Hotline tư vấn và hỗ trợ',
                    order_index=1
                ),
                ContactSettings(
                    setting_key='email_main',
                    setting_value='info@hoahuongduong.edu.vn',
                    setting_type='email',
                    display_name='Email chính',
                    description='Email liên hệ chính thức',
                    order_index=2
                ),
                ContactSettings(
                    setting_key='facebook',
                    setting_value='https://facebook.com/truongmamnonhoahuongduong',
                    setting_type='url',
                    display_name='Facebook',
                    description='Trang Facebook chính thức của trường',
                    order_index=3
                ),
                ContactSettings(
                    setting_key='zalo',
                    setting_value='https://zalo.me/0901234567',
                    setting_type='url',
                    display_name='Zalo',
                    description='Chat Zalo để tư vấn nhanh',
                    order_index=4
                ),
                ContactSettings(
                    setting_key='youtube',
                    setting_value='https://youtube.com/@hoahuongduong',
                    setting_type='url',
                    display_name='YouTube',
                    description='Kênh YouTube với các hoạt động của trường',
                    order_index=5
                )
            ]
            
            for setting in default_settings:
                db.session.add(setting)
            db.session.commit()
        
        # Add default location settings if none exist
        if not LocationSettings.query.first():
            default_location = LocationSettings(
                address='123 Đường Hoa Hướng Dương, Quận 1, TP.HCM',
                latitude=10.7769,  # Tọa độ mẫu của TP.HCM
                longitude=106.7009,
                map_zoom_level=15,
                map_style='roadmap',
                show_in_footer=True,
                map_height='300px',
                marker_title='Trường Mầm non Hoa Hướng Dương',
                marker_info='Trường Mầm non Hoa Hướng Dương - Nuôi dưỡng tâm hồn, phát triển tài năng',
                is_active=True
            )
            db.session.add(default_location)
            db.session.commit()

# Video Management Routes
@app.route('/admin/videos')
@login_required
def admin_videos():
    videos = IntroVideo.query.order_by(IntroVideo.order_index.asc()).all()
    return render_template('admin/videos/list.html', videos=videos)

@app.route('/admin/videos/create', methods=['GET', 'POST'])
@login_required
def admin_videos_create():
    if request.method == 'POST':
        video = IntroVideo(
            title=request.form['title'],
            description=request.form.get('description'),
            video_url=request.form['video_url'],
            order_index=int(request.form.get('order_index', 0)),
            is_active=bool(request.form.get('is_active'))
        )
        
        if 'thumbnail_image' in request.files:
            image_path = save_image(request.files['thumbnail_image'], 'videos')
            if image_path:
                video.thumbnail_image = image_path
        
        db.session.add(video)
        db.session.commit()
        flash('Video đã được tạo thành công!', 'success')
        return redirect(url_for('admin_videos'))
    
    return render_template('admin/videos/create.html')

@app.route('/admin/videos/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_videos_edit(id):
    video = IntroVideo.query.get_or_404(id)
    
    if request.method == 'POST':
        video.title = request.form['title']
        video.description = request.form.get('description')
        video.video_url = request.form['video_url']
        video.order_index = int(request.form.get('order_index', 0))
        video.is_active = bool(request.form.get('is_active'))
        video.updated_at = datetime.utcnow()
        
        if 'thumbnail_image' in request.files and request.files['thumbnail_image'].filename:
            # Delete old image before saving new one
            delete_old_image(video.thumbnail_image)
            image_path = save_image(request.files['thumbnail_image'], 'videos')
            if image_path:
                video.thumbnail_image = image_path
        
        db.session.commit()
        flash('Video đã được cập nhật thành công!', 'success')
        return redirect(url_for('admin_videos'))
    
    # Add headers to help with iframe loading
    response = render_template('admin/videos/edit.html', video=video)
    return response

@app.route('/admin/videos/delete/<int:id>', methods=['POST'])
@login_required
def admin_videos_delete(id):
    video = IntroVideo.query.get_or_404(id)
    # Delete associated thumbnail image if exists
    delete_old_image(video.thumbnail_image)
    db.session.delete(video)
    db.session.commit()
    flash('Video đã được xóa thành công!', 'success')
    return redirect(url_for('admin_videos'))

# SEO Management Routes
@app.route('/admin/seo')
@login_required
def admin_seo():
    seo_settings = SEOSettings.query.order_by(SEOSettings.page_type.asc()).all()
    return render_template('admin/seo/list.html', seo_settings=seo_settings)

@app.route('/admin/seo/create', methods=['GET', 'POST'])
@login_required
def admin_seo_create():
    if request.method == 'POST':
        seo = SEOSettings(
            page_type=request.form['page_type'],
            page_id=request.form.get('page_id') if request.form.get('page_id') else None,
            meta_title=request.form.get('meta_title'),
            meta_description=request.form.get('meta_description'),
            meta_keywords=request.form.get('meta_keywords'),
            og_title=request.form.get('og_title'),
            og_description=request.form.get('og_description'),
            og_image=request.form.get('og_image'),
            canonical_url=request.form.get('canonical_url'),
            robots_meta=request.form.get('robots_meta', 'index,follow'),
            schema_markup=request.form.get('schema_markup'),
            is_active=bool(request.form.get('is_active'))
        )
        db.session.add(seo)
        db.session.commit()
        flash('Đã thêm cài đặt SEO thành công!', 'success')
        return redirect(url_for('admin_seo'))
    return render_template('admin/seo/create.html')

@app.route('/admin/seo/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def admin_seo_edit(id):
    seo = SEOSettings.query.get_or_404(id)
    if request.method == 'POST':
        seo.page_type = request.form['page_type']
        seo.page_id = request.form.get('page_id') if request.form.get('page_id') else None
        seo.meta_title = request.form.get('meta_title')
        seo.meta_description = request.form.get('meta_description')
        seo.meta_keywords = request.form.get('meta_keywords')
        seo.og_title = request.form.get('og_title')
        seo.og_description = request.form.get('og_description')
        seo.og_image = request.form.get('og_image')
        seo.canonical_url = request.form.get('canonical_url')
        seo.robots_meta = request.form.get('robots_meta', 'index,follow')
        seo.schema_markup = request.form.get('schema_markup')
        seo.is_active = bool(request.form.get('is_active'))
        seo.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Đã cập nhật cài đặt SEO thành công!', 'success')
        return redirect(url_for('admin_seo'))
    return render_template('admin/seo/edit.html', seo=seo)

@app.route('/admin/seo/<int:id>/delete', methods=['POST'])
@login_required
def admin_seo_delete(id):
    seo = SEOSettings.query.get_or_404(id)
    db.session.delete(seo)
    db.session.commit()
    flash('Đã xóa cài đặt SEO thành công!', 'success')
    return redirect(url_for('admin_seo'))

@app.route('/admin/seo/auto-generate', methods=['POST'])
@login_required
def admin_seo_auto_generate():
    """Tự động tạo SEO cho các trang chưa có"""
    
    # SEO cho trang chủ
    if not SEOSettings.query.filter_by(page_type='home').first():
        home_seo = SEOSettings(
            page_type='home',
            meta_title='Trường Mầm non Hoa Hướng Dương - Giáo dục chất lượng cao',
            meta_description='Trường Mầm non Hoa Hướng Dương cung cấp môi trường giáo dục an toàn, chất lượng cao với đội ngũ giáo viên chuyên nghiệp. Đăng ký ngay hôm nay!',
            meta_keywords='trường mầm non, giáo dục mầm non, hoa hướng dương, trẻ em, giáo dục chất lượng',
            og_title='Trường Mầm non Hoa Hướng Dương',
            og_description='Môi trường giáo dục an toàn, chất lượng cao cho trẻ em',
            og_image='/static/images/mnhhd.jpg',
            robots_meta='index,follow'
        )
        db.session.add(home_seo)
    
    # SEO cho trang giới thiệu
    if not SEOSettings.query.filter_by(page_type='about').first():
        about_seo = SEOSettings(
            page_type='about',
            meta_title='Giới thiệu - Trường Mầm non Hoa Hướng Dương',
            meta_description='Tìm hiểu về lịch sử, sứ mệnh và đội ngũ giáo viên của Trường Mầm non Hoa Hướng Dương. Hơn 10 năm kinh nghiệm trong giáo dục mầm non.',
            meta_keywords='giới thiệu trường mầm non, lịch sử, sứ mệnh, đội ngũ giáo viên',
            og_title='Giới thiệu - Trường Mầm non Hoa Hướng Dương',
            og_description='Tìm hiểu về lịch sử, sứ mệnh và đội ngũ giáo viên',
            og_image='/static/images/mnhhd.jpg',
            robots_meta='index,follow'
        )
        db.session.add(about_seo)
    
    # SEO cho trang chương trình
    if not SEOSettings.query.filter_by(page_type='programs').first():
        programs_seo = SEOSettings(
            page_type='programs',
            meta_title='Chương trình học - Trường Mầm non Hoa Hướng Dương',
            meta_description='Khám phá các chương trình học đa dạng, phù hợp với từng độ tuổi tại Trường Mầm non Hoa Hướng Dương. Phát triển toàn diện cho trẻ.',
            meta_keywords='chương trình học, giáo dục mầm non, phát triển trẻ em',
            og_title='Chương trình học - Trường Mầm non Hoa Hướng Dương',
            og_description='Các chương trình học đa dạng, phù hợp với từng độ tuổi',
            og_image='/static/images/mnhhd.jpg',
            robots_meta='index,follow'
        )
        db.session.add(programs_seo)
    
    # SEO cho trang tin tức
    if not SEOSettings.query.filter_by(page_type='news').first():
        news_seo = SEOSettings(
            page_type='news',
            meta_title='Tin tức - Trường Mầm non Hoa Hướng Dương',
            meta_description='Cập nhật tin tức mới nhất về hoạt động, sự kiện và thành tích của Trường Mầm non Hoa Hướng Dương.',
            meta_keywords='tin tức trường mầm non, hoạt động, sự kiện, thành tích',
            og_title='Tin tức - Trường Mầm non Hoa Hướng Dương',
            og_description='Tin tức mới nhất về hoạt động và sự kiện của trường',
            og_image='/static/images/mnhhd.jpg',
            robots_meta='index,follow'
        )
        db.session.add(news_seo)
    
    # SEO cho trang liên hệ
    if not SEOSettings.query.filter_by(page_type='contact').first():
        contact_seo = SEOSettings(
            page_type='contact',
            meta_title='Liên hệ - Trường Mầm non Hoa Hướng Dương',
            meta_description='Liên hệ với Trường Mầm non Hoa Hướng Dương để được tư vấn về chương trình học và đăng ký nhập học cho bé.',
            meta_keywords='liên hệ trường mầm non, tư vấn, đăng ký nhập học',
            og_title='Liên hệ - Trường Mầm non Hoa Hướng Dương',
            og_description='Liên hệ để được tư vấn và đăng ký nhập học',
            og_image='/static/images/mnhhd.jpg',
            robots_meta='index,follow'
        )
        db.session.add(contact_seo)
    
    db.session.commit()
    flash('Đã tự động tạo SEO cho các trang chưa có!', 'success')
    return redirect(url_for('admin_seo'))

# Location Settings Management Routes
@app.route('/admin/location')
@login_required
def admin_location():
    location_settings = LocationSettings.query.first()
    return render_template('admin/location/index.html', location_settings=location_settings)

@app.route('/admin/location/edit', methods=['GET', 'POST'])
@login_required
def admin_location_edit():
    location_settings = LocationSettings.query.first()
    if not location_settings:
        location_settings = LocationSettings()
        db.session.add(location_settings)
        db.session.commit()
    
    if request.method == 'POST':
        location_settings.address = request.form.get('address', '')
        location_settings.latitude = float(request.form['latitude']) if request.form.get('latitude') else None
        location_settings.longitude = float(request.form['longitude']) if request.form.get('longitude') else None
        location_settings.google_maps_api_key = request.form.get('google_maps_api_key', '')
        location_settings.google_maps_embed = request.form.get('google_maps_embed', '')  # Save iframe code
        location_settings.map_zoom_level = int(request.form.get('map_zoom_level', 15))
        location_settings.map_style = request.form.get('map_style', 'roadmap')
        location_settings.show_in_footer = request.form.get('show_in_footer') == 'true'
        location_settings.map_height = request.form.get('map_height', '400px')
        location_settings.marker_title = request.form.get('marker_title', '')
        location_settings.marker_info = request.form.get('marker_info', '')
        location_settings.is_active = request.form.get('is_active') == 'true'
        location_settings.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Cài đặt vị trí đã được cập nhật!', 'success')
        return redirect(url_for('admin_location'))
    
    return render_template('admin/location/edit.html', location_settings=location_settings)

@app.route('/debug/team-images')
def debug_team_images():
    """Debug route to check team member image URLs"""
    team_members = TeamMember.query.all()
    debug_info = []
    
    for member in team_members:
        if member.image_path:
            debug_info.append({
                'id': member.id,
                'name': member.name,
                'image_path_raw': member.image_path,
                'image_path_repr': repr(member.image_path),
                'url_for_result': url_for('static', filename=member.image_path),
                'has_backslash': '\\' in member.image_path,
                'file_exists': os.path.exists(os.path.join('static', member.image_path))
            })
    
    return f"<pre>{debug_info}</pre>"

if __name__ == '__main__':
    # Lấy port từ environment variable hoặc dùng 5000 làm default
    port = int(os.environ.get('PORT', 5000))
    # Chỉ bật debug mode khi không phải production
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)