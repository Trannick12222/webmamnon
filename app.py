from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from markupsafe import Markup
from PIL import Image
import os
import uuid
from datetime import datetime
from utils.image_url_handler import process_external_image_url
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
    # Chỉ set Content-Type cho HTML responses, không override XML responses
    if not response.content_type or response.content_type.startswith('text/html'):
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
    album_id = db.Column(db.Integer, db.ForeignKey('gallery_album.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class GalleryAlbum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    is_featured = db.Column(db.Boolean, default=False)
    cover_image_id = db.Column(db.Integer, db.ForeignKey('gallery.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    images = db.relationship('Gallery', backref='album', lazy=True, foreign_keys=[Gallery.album_id])
    cover_image = db.relationship('Gallery', foreign_keys=[cover_image_id], post_update=True)

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

class HomeStats(db.Model):
    """Stats for homepage 'Thành tựu của chúng tôi' section"""
    id = db.Column(db.Integer, primary_key=True)
    stat_key = db.Column(db.String(50), unique=True, nullable=False)  # 'students', 'teachers', etc.
    stat_value = db.Column(db.String(20), nullable=False)  # '200+', '25', etc.
    stat_label = db.Column(db.String(100), nullable=False)  # 'Học sinh', 'Giáo viên'
    stat_description = db.Column(db.String(200))  # 'hiện tại', 'chuyên nghiệp'
    icon_class = db.Column(db.String(100), default='fas fa-users')  # FontAwesome icon
    color_class = db.Column(db.String(50), default='bg-orange-500')  # Tailwind color
    order_index = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class WorkingHours(db.Model):
    """Working hours for contact page and footer"""
    id = db.Column(db.Integer, primary_key=True)
    day_key = db.Column(db.String(20), unique=True, nullable=False)  # 'monday_friday', 'saturday', 'sunday'
    day_label = db.Column(db.String(50), nullable=False)  # 'Thứ 2 - Thứ 6', 'Thứ 7', 'Chủ nhật'
    hours = db.Column(db.String(100), nullable=False)  # '7:00 - 17:00', '7:30 - 11:30', 'Nghỉ'
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

class DecorativeSettings(db.Model):
    __tablename__ = 'decorative_settings'
    id = db.Column(db.Integer, primary_key=True)
    
    # Section identification
    section_name = db.Column(db.String(100), nullable=False)  # 'features', 'video', etc.
    section_title = db.Column(db.String(200), default='Background Decorations')
    
    # Element 1 settings
    element1_enabled = db.Column(db.Boolean, default=True)
    element1_size = db.Column(db.String(20), default='w-80 h-80')  # Tailwind classes
    element1_position = db.Column(db.String(50), default='-top-20 -left-20')  # Tailwind position
    element1_color = db.Column(db.String(50), default='bg-theme-decorative-light')  # Tailwind color
    element1_animation = db.Column(db.String(50), default='animate-pulse')
    element1_delay = db.Column(db.String(20), default='0s')
    
    # Element 2 settings
    element2_enabled = db.Column(db.Boolean, default=True)
    element2_size = db.Column(db.String(20), default='w-60 h-60')
    element2_position = db.Column(db.String(50), default='top-40 -right-20')
    element2_color = db.Column(db.String(50), default='bg-theme-decorative-medium')
    element2_animation = db.Column(db.String(50), default='animate-pulse')
    element2_delay = db.Column(db.String(20), default='2s')
    
    # Element 3 settings
    element3_enabled = db.Column(db.Boolean, default=True)
    element3_size = db.Column(db.String(20), default='w-40 h-40')
    element3_position = db.Column(db.String(50), default='-bottom-10 left-1/3')
    element3_color = db.Column(db.String(50), default='bg-theme-decorative-light')
    element3_animation = db.Column(db.String(50), default='animate-pulse')
    element3_delay = db.Column(db.String(20), default='4s')
    
    # Additional settings
    opacity = db.Column(db.String(20), default='opacity-100')
    blur_effect = db.Column(db.String(30), default='')  # backdrop-blur-sm, etc.
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FeatureItem(db.Model):
    __tablename__ = 'feature_items'
    id = db.Column(db.Integer, primary_key=True)
    
    # Content fields
    icon = db.Column(db.String(100), nullable=False, default='fas fa-shield-alt')  # FontAwesome icon class
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Display settings
    order_index = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    
    # Style settings
    icon_color = db.Column(db.String(50), default='text-primary')  # Tailwind color class
    background_color = db.Column(db.String(50), default='bg-white')  # Tailwind background
    
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

class UserSubmittedImage(db.Model):
    __tablename__ = 'user_submitted_images'
    id = db.Column(db.Integer, primary_key=True)
    sender_name = db.Column(db.String(100), nullable=False)
    sender_email = db.Column(db.String(120), nullable=False)
    sender_phone = db.Column(db.String(20))
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    image_path = db.Column(db.String(500), nullable=False)
    original_filename = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    admin_note = db.Column(db.Text)
    reviewed_by = db.Column(db.String(100))
    reviewed_at = db.Column(db.DateTime)
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AgeGroup(db.Model):
    __tablename__ = 'age_groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age_range = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    icon_class = db.Column(db.String(100), default='fas fa-baby')
    icon_bg_color = db.Column(db.String(50), default='bg-pink-100')
    icon_text_color = db.Column(db.String(50), default='text-pink-600')
    skills = db.Column(db.Text)
    order_index = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProgramFeature(db.Model):
    __tablename__ = 'program_features'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    icon_class = db.Column(db.String(100), default='fas fa-check-circle')
    background_gradient = db.Column(db.String(100), default='from-green-100 to-emerald-100')
    text_color = db.Column(db.String(50), default='text-green-800')
    border_color = db.Column(db.String(50), default='border-green-200')
    order_index = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProgramInfo(db.Model):
    __tablename__ = 'program_info'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    icon_class = db.Column(db.String(100), default='fas fa-users')
    icon_bg_gradient = db.Column(db.String(100), default='from-purple-400 to-pink-500')
    order_index = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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

def generate_article_schema(article):
    """Generate Article schema for news/blog posts"""
    import json
    
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article.title,
        "description": article.excerpt or article.content[:200] + "..." if len(article.content) > 200 else article.content,
        "author": {
            "@type": "Organization",
            "name": "Trường Mầm non Hoa Hướng Dương"
        },
        "publisher": {
            "@type": "EducationalOrganization", 
            "name": "Trường Mầm non Hoa Hướng Dương",
            "logo": {
                "@type": "ImageObject",
                "url": f"{request.url_root.rstrip('/')}/static/images/mnhhd.jpg"
            }
        },
        "datePublished": article.created_at.isoformat(),
        "dateModified": getattr(article, 'updated_at', article.created_at).isoformat(),
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": request.url
        },
        "url": request.url,
        "inLanguage": "vi-VN"
    }
    
    # Add image if exists
    if hasattr(article, 'featured_image') and article.featured_image:
        schema["image"] = {
            "@type": "ImageObject",
            "url": f"{request.url_root.rstrip('/')}/static/uploads/news/{article.featured_image}",
            "width": "800",
            "height": "600"
        }
    
    return json.dumps(schema, ensure_ascii=False, indent=2)

def generate_event_schema(event):
    """Generate Event schema for events"""
    import json
    
    schema = {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": event.title,
        "description": event.description or "Sự kiện tại Trường Mầm non Hoa Hướng Dương",
        "startDate": event.event_date.isoformat(),
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "organizer": {
            "@type": "EducationalOrganization",
            "name": "Trường Mầm non Hoa Hướng Dương",
            "url": request.url_root.rstrip('/')
        },
        "url": request.url,
        "inLanguage": "vi-VN"
    }
    
    # Add location if exists
    if event.location:
        schema["location"] = {
            "@type": "Place",
            "name": event.location,
            "address": event.location
        }
    
    # Add image if exists
    if event.featured_image:
        schema["image"] = {
            "@type": "ImageObject",
            "url": f"{request.url_root.rstrip('/')}/static/{event.featured_image}",
            "width": "800", 
            "height": "600"
        }
    
    return json.dumps(schema, ensure_ascii=False, indent=2)

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
        # Inject decorative settings for global use (background decorations)
        decorative_settings = DecorativeSettings.query.filter_by(is_active=True).all()
        # Inject feature items for global use (features section)
        feature_items = FeatureItem.query.filter_by(is_active=True).order_by(FeatureItem.order_index.asc()).all()
    except:
        unread_contacts = 0
        contact_settings = []
        location_settings = None
        current_theme = None
        system_settings = None
        homepage_settings = None
        decorative_settings = []
        feature_items = []
    return dict(
        unread_contacts=unread_contacts, 
        global_contact_settings=contact_settings, 
        global_location_settings=location_settings, 
        current_theme=current_theme,
        global_system_settings=system_settings,
        global_homepage_settings=homepage_settings,
        global_decorative_settings=decorative_settings,
        global_feature_items=feature_items,
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

def get_working_hours():
    """Helper function to get active working hours"""
    return WorkingHours.query.filter_by(is_active=True).order_by(WorkingHours.order_index.asc()).all()

@app.context_processor
def inject_global_vars():
    """Inject global variables into all templates"""
    return {
        'working_hours': get_working_hours()
    }

@app.before_request
def before_request():
    """Track page visits before processing request"""
    track_page_visit()

@app.route('/')
def index():
    featured_programs = Program.query.filter_by(is_active=True, is_featured=True).limit(6).all()
    latest_news = News.query.filter_by(is_published=True).order_by(News.created_at.desc()).limit(3).all()
    latest_posts = Post.query.filter_by(is_published=True).order_by(Post.created_at.desc()).limit(3).all()
    gallery_images = Gallery.query.filter_by(is_featured=True).limit(8).all()
    upcoming_events = Event.query.filter_by(is_active=True).filter(Event.event_date > datetime.utcnow()).limit(3).all()
    slider_images = Slider.query.filter_by(is_active=True).order_by(Slider.order_index.asc()).all()
    intro_videos = IntroVideo.query.filter_by(is_active=True).order_by(IntroVideo.order_index.asc()).limit(3).all()
    
    # Get contact settings for social links
    contact_settings = ContactSettings.query.filter_by(is_active=True).order_by(ContactSettings.order_index.asc()).all()
    
    # Get about section data
    about_section = AboutSection.query.first()
    about_stats = AboutStats.query.filter_by(is_active=True).order_by(AboutStats.order_index.asc()).all()
    
    # Get home stats for achievements section
    home_stats = HomeStats.query.filter_by(is_active=True).order_by(HomeStats.order_index.asc()).all()
    
    # Get system settings for school information
    system_settings = SystemSettings.query.first()
    
    # Get SEO settings for homepage
    seo_data = get_seo_settings('home')
    
    return render_template('index.html', 
                         featured_programs=featured_programs,
                         latest_news=latest_news,
                         latest_posts=latest_posts,
                         gallery_images=gallery_images,
                         upcoming_events=upcoming_events,
                         slider_images=slider_images,
                         intro_videos=intro_videos,
                         contact_settings=contact_settings,
                         about_section=about_section,
                         about_stats=about_stats,
                         home_stats=home_stats,
                         system_settings=system_settings,
                         seo_data=seo_data)

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
    
    # Add home stats data (same as homepage)
    home_stats = HomeStats.query.filter_by(is_active=True).order_by(HomeStats.order_index.asc()).all()
    
    # Get SEO settings for about page
    seo_data = get_seo_settings('about')
    
    return render_template('about.html', 
                         team_members=team_members,
                         mission_content=mission_content,
                         mission_items=mission_items,
                         history_section=history_section,
                         history_events=history_events,
                         about_stats=home_stats,
                         seo_data=seo_data)

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
    # Get SEO settings for programs page
    seo_data = get_seo_settings('programs')
    
    return render_template('programs.html', programs=programs, special_programs=special_programs, programs_cta=programs_cta, seo_data=seo_data)

@app.route('/chuong-trinh/<int:id>')
def program_detail(id):
    program = Program.query.get(id)
    if not program or not program.is_active:
        return redirect(url_for('programs'))
    return render_template('program_detail.html', program=program)

@app.route('/chuong-trinh-dac-biet/<int:id>')
def special_program_detail(id):
    """Trang chi tiết chương trình đặc biệt"""
    special_program = SpecialProgram.query.get_or_404(id)
    other_programs = SpecialProgram.query.filter(
        SpecialProgram.is_active == True,
        SpecialProgram.id != id
    ).order_by(SpecialProgram.order_index.asc()).limit(3).all()
    return render_template('special_program_detail.html', 
                         special_program=special_program, 
                         other_programs=other_programs)

@app.route('/tin-tuc')
def news():
    page = request.args.get('page', 1, type=int)
    news = News.query.filter_by(is_published=True).order_by(News.created_at.desc()).paginate(
        page=page, per_page=6, error_out=False)
    # Get SEO settings for news page
    seo_data = get_seo_settings('news')
    
    return render_template('news.html', news=news, seo_data=seo_data)

@app.route('/tin-tuc/<int:id>')
def news_detail(id):
    article = News.query.get_or_404(id)
    
    # Lấy tin tức liên quan
    related_news = News.query.filter(
        News.id != id,
        News.is_published == True
    ).order_by(News.created_at.desc()).limit(3).all()
    
    # Get SEO settings for this specific news article
    seo_data = get_seo_settings('news', article.id)
    
    # Generate dynamic schema for this article
    seo_data['schema_markup'] = generate_article_schema(article)
    
    return render_template('news_detail.html', 
                         article=article, 
                         related_news=related_news,
                         seo_data=seo_data)

@app.route('/thu-vien-anh')
def gallery():
    # Lấy tất cả ảnh (bao gồm cả ảnh trong album và ảnh đơn lẻ)
    all_images = Gallery.query.order_by(Gallery.created_at.desc()).all()
    
    # Lấy album để hiển thị riêng
    albums = GalleryAlbum.query.order_by(GalleryAlbum.created_at.desc()).all()
    
    # Lấy ảnh đơn lẻ (không thuộc album nào)
    standalone_images = Gallery.query.filter_by(album_id=None).order_by(Gallery.created_at.desc()).all()
    
    # Lấy categories từ cả album và ảnh đơn lẻ
    categories = db.session.query(Gallery.category).distinct().all()
    album_categories = db.session.query(GalleryAlbum.category).distinct().all()
    all_categories = list(set([cat[0] for cat in categories if cat[0]] + [cat[0] for cat in album_categories if cat[0]]))
    
    return render_template('gallery.html', 
                         images=all_images,  # Để tương thích với template hiện tại
                         albums=albums,
                         standalone_images=standalone_images,
                         categories=all_categories)

@app.route('/thu-vien-anh/album/<int:id>')
def album_detail(id):
    album = GalleryAlbum.query.get_or_404(id)
    return render_template('album_detail.html', album=album)

@app.route('/chia-se-hinh-anh', methods=['GET', 'POST'])
def share_image():
    if request.method == 'POST':
        try:
            # Validate required fields
            if not all([request.form.get('sender_name'), 
                       request.form.get('sender_email'),
                       'image' in request.files]):
                flash('Vui lòng điền đầy đủ thông tin và chọn hình ảnh!', 'error')
                return render_template('share_image.html')
            
            file = request.files['image']
            if file.filename == '':
                flash('Vui lòng chọn hình ảnh!', 'error')
                return render_template('share_image.html')
            
            # Validate file type
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
            if not ('.' in file.filename and 
                   file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
                flash('Chỉ chấp nhận file ảnh (PNG, JPG, JPEG, GIF, WEBP)!', 'error')
                return render_template('share_image.html')
            
            # Create upload directory if not exists
            upload_dir = 'static/uploads/user_submissions'
            os.makedirs(upload_dir, exist_ok=True)
            
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join(upload_dir, unique_filename)
            
            # Save file
            file.save(filepath)
            
            # Get file info
            file_size = os.path.getsize(filepath)
            mime_type = file.content_type
            
            # Create database record
            user_image = UserSubmittedImage(
                sender_name=request.form['sender_name'],
                sender_email=request.form['sender_email'],
                sender_phone=request.form.get('sender_phone', ''),
                title=request.form.get('title', ''),
                description=request.form.get('description', ''),
                image_path=f'uploads/user_submissions/{unique_filename}',
                original_filename=filename,
                file_size=file_size,
                mime_type=mime_type
            )
            
            db.session.add(user_image)
            db.session.commit()
            
            flash('Cảm ơn bạn đã chia sẻ hình ảnh! Chúng tôi sẽ xem xét và duyệt sớm nhất.', 'success')
            return redirect(url_for('share_image'))
            
        except Exception as e:
            flash('Có lỗi xảy ra khi upload hình ảnh. Vui lòng thử lại!', 'error')
            return render_template('share_image.html')
    
    return render_template('share_image.html')

@app.route('/su-kien')
def events():
    upcoming = Event.query.filter_by(is_active=True).filter(Event.event_date > datetime.utcnow()).all()
    past = Event.query.filter_by(is_active=True).filter(Event.event_date <= datetime.utcnow()).all()
    
    # Get SEO settings for events page
    seo_data = get_seo_settings('events')
    
    return render_template('events.html', upcoming=upcoming, past=past, seo_data=seo_data)

@app.route('/su-kien/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Lấy các sự kiện liên quan (cùng thời gian hoặc sắp tới)
    related_events = Event.query.filter(
        Event.id != event_id,
        Event.is_active == True
    ).order_by(Event.event_date.desc()).limit(3).all()
    
    current_time = datetime.utcnow()
    
    # Get SEO settings for this specific event
    seo_data = get_seo_settings('events', event.id)
    
    # Generate dynamic schema for this event
    seo_data['schema_markup'] = generate_event_schema(event)
    
    return render_template('event_detail.html', 
                         event=event, 
                         related_events=related_events,
                         current_time=current_time,
                         seo_data=seo_data)

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

@app.route('/admin/process-external-image', methods=['POST'])
@login_required
def admin_process_external_image():
    """Process external image URL for TinyMCE editor"""
    try:
        from utils.image_url_handler import process_external_image_url, validate_image_url
        
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'No URL provided'}), 400
        
        original_url = data['url'].strip()
        if not original_url:
            return jsonify({'error': 'Empty URL'}), 400
        
        # Xử lý URL
        processed_url = process_external_image_url(original_url)
        
        # Kiểm tra tính hợp lệ của URL
        is_valid, message = validate_image_url(processed_url)
        
        if not is_valid:
            return jsonify({'error': f'Invalid image URL: {message}'}), 400
        
        # Trả về URL đã xử lý
        return jsonify({
            'location': processed_url,
            'original_url': original_url,
            'message': 'External image URL processed successfully'
        })
        
    except ImportError:
        return jsonify({'error': 'Image URL handler not available'}), 500
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/admin/get-supported-services', methods=['GET'])
@login_required
def admin_get_supported_services():
    """Get list of supported external image services"""
    try:
        from utils.image_url_handler import get_supported_services
        return jsonify(get_supported_services())
    except ImportError:
        return jsonify({'error': 'Service list not available'}), 500

@app.route('/admin/settings/external-images')
@login_required
def admin_external_images_settings():
    """Page for external image settings and instructions"""
    return render_template('admin/settings/external_images.html')

@app.route('/blog')
def blog():
    """Blog listing page"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    
    # Base query for published posts
    query = Post.query.filter_by(is_published=True)
    
    # Filter by category if specified
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # Paginate posts
    posts = query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=9, error_out=False
    )
    
    # Get all categories for filter
    categories = Category.query.all()
    
    # Get selected category for display
    selected_category = None
    if category_id:
        selected_category = Category.query.get(category_id)
    
    return render_template('blog.html', 
                         posts=posts, 
                         categories=categories,
                         selected_category=selected_category)

@app.route('/blog/<int:id>')
def blog_detail(id):
    """Blog post detail page"""
    post = Post.query.get_or_404(id)
    
    # Lấy bài viết liên quan (cùng category hoặc mới nhất)
    related_posts = Post.query.filter(
        Post.id != id,
        Post.is_published == True
    ).order_by(Post.created_at.desc()).limit(3).all()
    
    # Get SEO settings for this specific blog post
    seo_data = get_seo_settings('blog', post.id)
    
    # Generate dynamic schema for this blog post
    seo_data['schema_markup'] = generate_article_schema(post)
    
    return render_template('blog_detail.html', 
                         post=post, 
                         related_posts=related_posts,
                         seo_data=seo_data)

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
        
        # Handle image removal first
        if request.form.get('remove_image') == '1':
            if program.featured_image:
                delete_old_image(program.featured_image)
            program.featured_image = None
        
        # Handle file upload
        elif request.form.get('cropped_image_data'):
            # Use cropped image data if available
            delete_old_image(program.featured_image)
            image_path = save_cropped_image(request.form.get('cropped_image_data'), 'programs')
            if image_path:
                program.featured_image = image_path
        elif 'featured_image' in request.files and request.files['featured_image'].filename:
            # Fallback to regular file upload
            delete_old_image(program.featured_image)
            image_path = save_image(request.files['featured_image'], 'programs')
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

# Program Info Management Routes
@app.route('/admin/program-info')
@login_required
def admin_program_info():
    program_info = ProgramInfo.query.order_by(ProgramInfo.order_index.asc(), ProgramInfo.created_at.desc()).all()
    return render_template('admin/program_info/list.html', program_info=program_info)

@app.route('/admin/program-info/create', methods=['GET', 'POST'])
@login_required
def admin_program_info_create():
    if request.method == 'POST':
        program_info = ProgramInfo(
            title=request.form['title'],
            icon_class=request.form.get('icon_class', 'fas fa-users'),
            icon_bg_gradient=request.form.get('icon_bg_gradient', 'from-purple-400 to-pink-500'),
            order_index=int(request.form.get('order_index', 0))
        )
        
        db.session.add(program_info)
        db.session.commit()
        flash('Thông tin chương trình đã được tạo thành công!', 'success')
        return redirect(url_for('admin_program_info'))
    
    return render_template('admin/program_info/create.html')

@app.route('/admin/program-info/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_program_info_edit(id):
    program_info = ProgramInfo.query.get_or_404(id)
    
    if request.method == 'POST':
        program_info.title = request.form['title']
        program_info.icon_class = request.form.get('icon_class', 'fas fa-users')
        program_info.icon_bg_gradient = request.form.get('icon_bg_gradient', 'from-purple-400 to-pink-500')
        program_info.order_index = int(request.form.get('order_index', 0))
        
        db.session.commit()
        flash('Thông tin chương trình đã được cập nhật!', 'success')
        return redirect(url_for('admin_program_info'))
    
    return render_template('admin/program_info/edit.html', program_info=program_info)

@app.route('/admin/program-info/delete/<int:id>', methods=['POST'])
@login_required
def admin_program_info_delete(id):
    program_info = ProgramInfo.query.get_or_404(id)
    db.session.delete(program_info)
    db.session.commit()
    flash('Thông tin chương trình đã được xóa!', 'success')
    return redirect(url_for('admin_program_info'))

# Program Features Management Routes
@app.route('/admin/program-features')
@login_required
def admin_program_features():
    program_features = ProgramFeature.query.order_by(ProgramFeature.order_index.asc(), ProgramFeature.created_at.desc()).all()
    return render_template('admin/program_features/list.html', program_features=program_features)

@app.route('/admin/program-features/create', methods=['GET', 'POST'])
@login_required
def admin_program_features_create():
    if request.method == 'POST':
        program_feature = ProgramFeature(
            title=request.form['title'],
            icon_class=request.form.get('icon_class', 'fas fa-check-circle'),
            background_gradient=request.form.get('background_gradient', 'from-green-100 to-emerald-100'),
            text_color=request.form.get('text_color', 'text-green-800'),
            border_color=request.form.get('border_color', 'border-green-200'),
            order_index=int(request.form.get('order_index', 0))
        )
        
        db.session.add(program_feature)
        db.session.commit()
        flash('Điểm nổi bật đã được tạo thành công!', 'success')
        return redirect(url_for('admin_program_features'))
    
    return render_template('admin/program_features/create.html')

@app.route('/admin/program-features/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_program_features_edit(id):
    program_feature = ProgramFeature.query.get_or_404(id)
    
    if request.method == 'POST':
        program_feature.title = request.form['title']
        program_feature.icon_class = request.form.get('icon_class', 'fas fa-check-circle')
        program_feature.background_gradient = request.form.get('background_gradient', 'from-green-100 to-emerald-100')
        program_feature.text_color = request.form.get('text_color', 'text-green-800')
        program_feature.border_color = request.form.get('border_color', 'border-green-200')
        program_feature.order_index = int(request.form.get('order_index', 0))
        
        db.session.commit()
        flash('Điểm nổi bật đã được cập nhật!', 'success')
        return redirect(url_for('admin_program_features'))
    
    return render_template('admin/program_features/edit.html', program_feature=program_feature)

@app.route('/admin/program-features/delete/<int:id>', methods=['POST'])
@login_required
def admin_program_features_delete(id):
    program_feature = ProgramFeature.query.get_or_404(id)
    db.session.delete(program_feature)
    db.session.commit()
    flash('Điểm nổi bật đã được xóa!', 'success')
    return redirect(url_for('admin_program_features'))

# Age Groups Management Routes
@app.route('/admin/age-groups')
@login_required
def admin_age_groups():
    age_groups = AgeGroup.query.order_by(AgeGroup.order_index.asc(), AgeGroup.created_at.desc()).all()
    return render_template('admin/age_groups/list.html', age_groups=age_groups)

@app.route('/admin/age-groups/create', methods=['GET', 'POST'])
@login_required
def admin_age_groups_create():
    if request.method == 'POST':
        age_group = AgeGroup(
            name=request.form['name'],
            age_range=request.form['age_range'],
            description=request.form.get('description', ''),
            skills=request.form.get('skills', ''),
            icon_class=request.form.get('icon_class', 'fas fa-baby'),
            icon_bg_color=request.form.get('icon_bg_color', 'bg-pink-100'),
            icon_text_color=request.form.get('icon_text_color', 'text-pink-600'),
            order_index=int(request.form.get('order_index', 0)),
            is_active=True
        )
        
        db.session.add(age_group)
        db.session.commit()
        flash('Nhóm độ tuổi đã được tạo thành công!', 'success')
        return redirect(url_for('admin_age_groups'))
    
    return render_template('admin/age_groups/create.html')

@app.route('/admin/age-groups/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_age_groups_edit(id):
    age_group = AgeGroup.query.get_or_404(id)
    
    if request.method == 'POST':
        age_group.name = request.form['name']
        age_group.age_range = request.form['age_range']
        age_group.description = request.form.get('description', '')
        age_group.skills = request.form.get('skills', '')
        age_group.icon_class = request.form.get('icon_class', 'fas fa-baby')
        age_group.icon_bg_color = request.form.get('icon_bg_color', 'bg-pink-100')
        age_group.icon_text_color = request.form.get('icon_text_color', 'text-pink-600')
        age_group.order_index = int(request.form.get('order_index', 0))
        age_group.is_active = bool(request.form.get('is_active', True))
        
        db.session.commit()
        flash('Nhóm độ tuổi đã được cập nhật!', 'success')
        return redirect(url_for('admin_age_groups'))
    
    return render_template('admin/age_groups/edit.html', age_group=age_group)

@app.route('/admin/age-groups/delete/<int:id>', methods=['POST'])
@login_required
def admin_age_groups_delete(id):
    age_group = AgeGroup.query.get_or_404(id)
    db.session.delete(age_group)
    db.session.commit()
    flash('Nhóm độ tuổi đã được xóa!', 'success')
    return redirect(url_for('admin_age_groups'))

@app.route('/admin/gallery')
@login_required
def admin_gallery():
    page = request.args.get('page', 1, type=int)
    
    # Lấy ảnh đơn lẻ (không thuộc album nào)
    standalone_images = Gallery.query.filter_by(album_id=None).order_by(Gallery.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False)
    
    # Lấy tất cả album
    albums = GalleryAlbum.query.order_by(GalleryAlbum.created_at.desc()).all()
    
    return render_template('admin/gallery/list.html', images=standalone_images, albums=albums)

@app.route('/admin/gallery/create', methods=['GET', 'POST'])
@login_required
def admin_gallery_create():
    if request.method == 'POST':
        if 'images' in request.files:
            files = request.files.getlist('images')
            uploaded_count = 0
            album = None
            
            # Nếu upload nhiều hơn 1 ảnh, tạo album
            if len(files) > 1:
                album = GalleryAlbum(
                    title=request.form.get('title', f'Album {datetime.now().strftime("%d/%m/%Y %H:%M")}'),
                    description=request.form.get('description'),
                    category=request.form.get('category'),
                    is_featured=bool(request.form.get('is_featured'))
                )
                db.session.add(album)
                db.session.flush()  # Để có album.id
            
            first_image_id = None
            for file in files:
                if file and allowed_file(file.filename):
                    image_path = save_image(file, 'gallery')
                    if image_path:
                        gallery_item = Gallery(
                            title=request.form.get('title', file.filename) if len(files) == 1 else file.filename,
                            image_path=image_path,
                            description=request.form.get('description') if len(files) == 1 else None,
                            category=request.form.get('category'),
                            is_featured=bool(request.form.get('is_featured')) if len(files) == 1 else False,
                            album_id=album.id if album else None
                        )
                        db.session.add(gallery_item)
                        db.session.flush()  # Để có gallery_item.id
                        
                        # Đặt ảnh đầu tiên làm cover của album
                        if album and first_image_id is None:
                            first_image_id = gallery_item.id
                        
                        uploaded_count += 1
            
            # Cập nhật cover image cho album
            if album and first_image_id:
                album.cover_image_id = first_image_id
            
            db.session.commit()
            
            if album:
                flash(f'Đã tạo album "{album.title}" với {uploaded_count} hình ảnh!', 'success')
            else:
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

# Album management routes
@app.route('/admin/albums')
@login_required
def admin_albums():
    page = request.args.get('page', 1, type=int)
    albums = GalleryAlbum.query.order_by(GalleryAlbum.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False)
    return render_template('admin/albums/list.html', albums=albums)

@app.route('/admin/albums/<int:id>')
@login_required
def admin_album_detail(id):
    album = GalleryAlbum.query.get_or_404(id)
    return render_template('admin/albums/detail.html', album=album)

@app.route('/admin/albums/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def admin_album_edit(id):
    album = GalleryAlbum.query.get_or_404(id)
    
    if request.method == 'POST':
        album.title = request.form.get('title')
        album.description = request.form.get('description')
        album.category = request.form.get('category')
        album.is_featured = bool(request.form.get('is_featured'))
        
        # Xử lý thêm ảnh mới vào album
        if 'new_images' in request.files:
            files = request.files.getlist('new_images')
            added_count = 0
            
            for file in files:
                if file and allowed_file(file.filename):
                    image_path = save_image(file, 'gallery')
                    if image_path:
                        gallery_item = Gallery(
                            title=file.filename,
                            image_path=image_path,
                            category=album.category,
                            album_id=album.id
                        )
                        db.session.add(gallery_item)
                        added_count += 1
            
            if added_count > 0:
                flash(f'Đã thêm {added_count} ảnh vào album!', 'success')
        
        db.session.commit()
        flash('Cập nhật album thành công!', 'success')
        return redirect(url_for('admin_album_detail', id=id))
    
    return render_template('admin/albums/edit.html', album=album)

@app.route('/admin/albums/<int:id>/delete', methods=['POST'])
@login_required
def admin_album_delete(id):
    album = GalleryAlbum.query.get_or_404(id)
    
    # Xóa tất cả ảnh trong album
    for image in album.images:
        delete_old_image(image.image_path)
        db.session.delete(image)
    
    db.session.delete(album)
    db.session.commit()
    flash('Album đã được xóa!', 'success')
    return redirect(url_for('admin_albums'))

@app.route('/admin/albums/<int:album_id>/remove-image/<int:image_id>', methods=['POST'])
@login_required
def admin_album_remove_image(album_id, image_id):
    album = GalleryAlbum.query.get_or_404(album_id)
    image = Gallery.query.get_or_404(image_id)
    
    if image.album_id != album.id:
        flash('Ảnh không thuộc album này!', 'error')
        return redirect(url_for('admin_album_detail', id=album_id))
    
    # Nếu đây là cover image, chọn ảnh khác làm cover
    if album.cover_image_id == image.id:
        remaining_images = Gallery.query.filter_by(album_id=album.id).filter(Gallery.id != image.id).first()
        album.cover_image_id = remaining_images.id if remaining_images else None
    
    delete_old_image(image.image_path)
    db.session.delete(image)
    db.session.commit()
    
    flash('Đã xóa ảnh khỏi album!', 'success')
    return redirect(url_for('admin_album_detail', id=album_id))

@app.route('/admin/albums/<int:album_id>/set-cover/<int:image_id>', methods=['POST'])
@login_required
def admin_album_set_cover(album_id, image_id):
    album = GalleryAlbum.query.get_or_404(album_id)
    image = Gallery.query.get_or_404(image_id)
    
    if image.album_id != album.id:
        flash('Ảnh không thuộc album này!', 'error')
        return redirect(url_for('admin_album_detail', id=album_id))
    
    album.cover_image_id = image.id
    db.session.commit()
    
    flash('Đã đặt ảnh bìa cho album!', 'success')
    return redirect(url_for('admin_album_detail', id=album_id))

# User Submitted Images Routes
@app.route('/admin/user-images')
@login_required
def admin_user_images():
    status_filter = request.args.get('status', 'all')
    
    if status_filter == 'all':
        images = UserSubmittedImage.query.order_by(UserSubmittedImage.created_at.desc()).all()
    else:
        images = UserSubmittedImage.query.filter_by(status=status_filter).order_by(UserSubmittedImage.created_at.desc()).all()
    
    # Statistics
    stats = {
        'total': UserSubmittedImage.query.count(),
        'pending': UserSubmittedImage.query.filter_by(status='pending').count(),
        'approved': UserSubmittedImage.query.filter_by(status='approved').count(),
        'rejected': UserSubmittedImage.query.filter_by(status='rejected').count()
    }
    
    return render_template('admin/user_images/list.html', 
                         images=images, 
                         stats=stats, 
                         current_filter=status_filter)

@app.route('/admin/user-images/approve/<int:id>', methods=['POST'])
@login_required
def admin_user_images_approve(id):
    image = UserSubmittedImage.query.get_or_404(id)
    image.status = 'approved'
    image.reviewed_by = current_user.username
    image.reviewed_at = datetime.utcnow()
    
    # Add to main gallery
    gallery_item = Gallery(
        title=image.title or f'Ảnh từ {image.sender_name}',
        description=image.description or '',
        image_path=image.image_path,
        category='user_submitted'
    )
    db.session.add(gallery_item)
    db.session.commit()
    
    flash('Hình ảnh đã được duyệt và thêm vào thư viện!', 'success')
    return redirect(url_for('admin_user_images'))

@app.route('/admin/user-images/reject/<int:id>', methods=['POST'])
@login_required
def admin_user_images_reject(id):
    image = UserSubmittedImage.query.get_or_404(id)
    image.status = 'rejected'
    image.reviewed_by = current_user.username
    image.reviewed_at = datetime.utcnow()
    image.admin_note = request.form.get('admin_note', '')
    
    db.session.commit()
    flash('Hình ảnh đã bị từ chối!', 'info')
    return redirect(url_for('admin_user_images'))

@app.route('/admin/user-images/delete/<int:id>', methods=['POST'])
@login_required
def admin_user_images_delete(id):
    image = UserSubmittedImage.query.get_or_404(id)
    
    # Delete file
    if image.image_path and os.path.exists(os.path.join('static', image.image_path)):
        os.remove(os.path.join('static', image.image_path))
    
    db.session.delete(image)
    db.session.commit()
    
    flash('Hình ảnh đã được xóa!', 'success')
    return redirect(url_for('admin_user_images'))

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
    categories = Category.query.all()
    return render_template('admin/posts/list.html', posts=posts, categories=categories)

@app.route('/admin/posts/create', methods=['GET', 'POST'])
@login_required
def admin_posts_create():
    categories = Category.query.all()
    
    if request.method == 'POST':
        title = request.form.get('title')
        excerpt = request.form.get('excerpt')
        content = request.form.get('content')
        category_id = request.form.get('category_id')
        is_published = request.form.get('is_published') == 'on'
        featured_image = request.form.get('featured_image')
        
        # Handle file upload
        if 'featured_image_file' in request.files:
            file = request.files['featured_image_file']
            if file and file.filename:
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                
                # Create uploads directory if it doesn't exist
                upload_dir = os.path.join(app.static_folder, 'uploads', 'posts')
                os.makedirs(upload_dir, exist_ok=True)
                
                file_path = os.path.join(upload_dir, unique_filename)
                file.save(file_path)
                featured_image = f"uploads/posts/{unique_filename}"
        
        post = Post(
            title=title,
            excerpt=excerpt,
            content=content,
            category_id=int(category_id) if category_id else None,
            is_published=is_published,
            featured_image=featured_image
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('Bài viết đã được tạo thành công!', 'success')
        return redirect(url_for('admin_posts'))
    
    return render_template('admin/posts/create.html', categories=categories)

@app.route('/admin/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_posts_edit(id):
    post = Post.query.get_or_404(id)
    categories = Category.query.all()
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.excerpt = request.form.get('excerpt')
        post.content = request.form.get('content')
        post.category_id = int(request.form.get('category_id')) if request.form.get('category_id') else None
        post.is_published = request.form.get('is_published') == 'on'
        
        # Handle featured image
        featured_image = request.form.get('featured_image')
        if featured_image:
            post.featured_image = featured_image
        
        # Handle file upload
        if 'featured_image_file' in request.files:
            file = request.files['featured_image_file']
            if file and file.filename:
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                
                # Create uploads directory if it doesn't exist
                upload_dir = os.path.join(app.static_folder, 'uploads', 'posts')
                os.makedirs(upload_dir, exist_ok=True)
                
                file_path = os.path.join(upload_dir, unique_filename)
                file.save(file_path)
                post.featured_image = f"uploads/posts/{unique_filename}"
        
        post.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Bài viết đã được cập nhật!', 'success')
        return redirect(url_for('admin_posts'))
    
    return render_template('admin/posts/edit.html', post=post, categories=categories)

@app.route('/admin/posts/delete/<int:id>', methods=['POST'])
@login_required
def admin_posts_delete(id):
    post = Post.query.get_or_404(id)
    
    # Delete associated image file if exists
    if post.featured_image and not post.featured_image.startswith('http'):
        try:
            image_path = os.path.join(app.static_folder, post.featured_image)
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            print(f"Error deleting image: {e}")
    
    db.session.delete(post)
    db.session.commit()
    
    flash('Bài viết đã được xóa!', 'success')
    return redirect(url_for('admin_posts'))

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

@app.route('/admin/decorative')
@login_required
def admin_decorative():
    # Lấy tất cả decorative settings
    decorative_settings = DecorativeSettings.query.all()
    return render_template('admin/decorative/list.html', decorative_settings=decorative_settings)

@app.route('/admin/decorative/<section_name>', methods=['GET', 'POST'])
@login_required
def admin_decorative_edit(section_name):
    if request.method == 'POST':
        # Lấy hoặc tạo mới decorative settings cho section
        decorative = DecorativeSettings.query.filter_by(section_name=section_name).first()
        if not decorative:
            decorative = DecorativeSettings(section_name=section_name)
            db.session.add(decorative)
        
        # Cập nhật general settings
        decorative.section_title = request.form.get('section_title', decorative.section_title)
        decorative.opacity = request.form.get('opacity', decorative.opacity)
        decorative.blur_effect = request.form.get('blur_effect', decorative.blur_effect)
        
        # Cập nhật Element 1
        decorative.element1_enabled = bool(request.form.get('element1_enabled'))
        decorative.element1_size = request.form.get('element1_size', decorative.element1_size)
        decorative.element1_position = request.form.get('element1_position', decorative.element1_position)
        decorative.element1_color = request.form.get('element1_color', decorative.element1_color)
        decorative.element1_animation = request.form.get('element1_animation', decorative.element1_animation)
        decorative.element1_delay = request.form.get('element1_delay', decorative.element1_delay)
        
        # Cập nhật Element 2
        decorative.element2_enabled = bool(request.form.get('element2_enabled'))
        decorative.element2_size = request.form.get('element2_size', decorative.element2_size)
        decorative.element2_position = request.form.get('element2_position', decorative.element2_position)
        decorative.element2_color = request.form.get('element2_color', decorative.element2_color)
        decorative.element2_animation = request.form.get('element2_animation', decorative.element2_animation)
        decorative.element2_delay = request.form.get('element2_delay', decorative.element2_delay)
        
        # Cập nhật Element 3
        decorative.element3_enabled = bool(request.form.get('element3_enabled'))
        decorative.element3_size = request.form.get('element3_size', decorative.element3_size)
        decorative.element3_position = request.form.get('element3_position', decorative.element3_position)
        decorative.element3_color = request.form.get('element3_color', decorative.element3_color)
        decorative.element3_animation = request.form.get('element3_animation', decorative.element3_animation)
        decorative.element3_delay = request.form.get('element3_delay', decorative.element3_delay)
        
        decorative.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash(f'Hiệu ứng trang trí cho {section_name} đã được cập nhật thành công!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Có lỗi xảy ra khi cập nhật hiệu ứng trang trí!', 'error')
        
        return redirect(url_for('admin_decorative_edit', section_name=section_name))
    
    # GET request - hiển thị form
    decorative = DecorativeSettings.query.filter_by(section_name=section_name).first()
    if not decorative:
        decorative = DecorativeSettings(section_name=section_name)
        db.session.add(decorative)
        db.session.commit()
    
    return render_template('admin/decorative/edit.html', decorative=decorative, section_name=section_name)

@app.route('/admin/features')
@login_required
def admin_features():
    # Lấy tất cả feature items theo thứ tự
    features = FeatureItem.query.order_by(FeatureItem.order_index.asc()).all()
    return render_template('admin/features/list.html', features=features)

@app.route('/admin/features/create', methods=['GET', 'POST'])
@login_required
def admin_features_create():
    if request.method == 'POST':
        # Tạo feature item mới
        feature = FeatureItem(
            icon=request.form.get('icon', 'fas fa-star'),
            title=request.form.get('title'),
            description=request.form.get('description'),
            order_index=int(request.form.get('order_index', 0)),
            icon_color=request.form.get('icon_color', 'text-primary'),
            background_color=request.form.get('background_color', 'bg-white'),
            is_active=bool(request.form.get('is_active'))
        )
        
        try:
            db.session.add(feature)
            db.session.commit()
            flash('Feature đã được tạo thành công!', 'success')
            return redirect(url_for('admin_features'))
        except Exception as e:
            db.session.rollback()
            flash('Có lỗi xảy ra khi tạo feature!', 'error')
    
    return render_template('admin/features/create.html')

@app.route('/admin/features/edit/<int:feature_id>', methods=['GET', 'POST'])
@login_required
def admin_features_edit(feature_id):
    feature = FeatureItem.query.get_or_404(feature_id)
    
    if request.method == 'POST':
        # Cập nhật feature
        feature.icon = request.form.get('icon', feature.icon)
        feature.title = request.form.get('title', feature.title)
        feature.description = request.form.get('description', feature.description)
        feature.order_index = int(request.form.get('order_index', feature.order_index))
        feature.icon_color = request.form.get('icon_color', feature.icon_color)
        feature.background_color = request.form.get('background_color', feature.background_color)
        feature.is_active = bool(request.form.get('is_active'))
        feature.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Feature đã được cập nhật thành công!', 'success')
            return redirect(url_for('admin_features'))
        except Exception as e:
            db.session.rollback()
            flash('Có lỗi xảy ra khi cập nhật feature!', 'error')
    
    return render_template('admin/features/edit.html', feature=feature)

@app.route('/admin/features/delete/<int:feature_id>', methods=['POST'])
@login_required
def admin_features_delete(feature_id):
    feature = FeatureItem.query.get_or_404(feature_id)
    
    try:
        db.session.delete(feature)
        db.session.commit()
        flash('Feature đã được xóa thành công!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Có lỗi xảy ra khi xóa feature!', 'error')
    
    return redirect(url_for('admin_features'))

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

# Home Stats Management Routes
@app.route('/admin/home-stats')
@login_required
def admin_home_stats():
    home_stats = HomeStats.query.order_by(HomeStats.order_index.asc(), HomeStats.created_at.desc()).all()
    return render_template('admin/home_stats/index.html', home_stats=home_stats)

@app.route('/admin/home-stats/create', methods=['GET', 'POST'])
@login_required
def admin_home_stats_create():
    if request.method == 'POST':
        stat_key = request.form['stat_key']
        stat_value = request.form['stat_value']
        stat_label = request.form['stat_label']
        stat_description = request.form.get('stat_description', '')
        icon_class = request.form['icon_class']
        color_class = request.form['color_class']
        order_index = int(request.form.get('order_index', 0))
        is_active = bool(request.form.get('is_active'))
        
        home_stat = HomeStats(
            stat_key=stat_key,
            stat_value=stat_value,
            stat_label=stat_label,
            stat_description=stat_description,
            icon_class=icon_class,
            color_class=color_class,
            order_index=order_index,
            is_active=is_active
        )
        
        db.session.add(home_stat)
        db.session.commit()
        
        flash('Thống kê trang chủ đã được thêm!', 'success')
        return redirect(url_for('admin_home_stats'))
    
    return render_template('admin/home_stats/create.html')

@app.route('/admin/home-stats/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_home_stats_edit(id):
    home_stat = HomeStats.query.get_or_404(id)
    
    if request.method == 'POST':
        home_stat.stat_key = request.form['stat_key']
        home_stat.stat_value = request.form['stat_value']
        home_stat.stat_label = request.form['stat_label']
        home_stat.stat_description = request.form.get('stat_description', '')
        home_stat.icon_class = request.form['icon_class']
        home_stat.color_class = request.form['color_class']
        home_stat.order_index = int(request.form.get('order_index', 0))
        home_stat.is_active = bool(request.form.get('is_active'))
        
        db.session.commit()
        flash('Thống kê trang chủ đã được cập nhật!', 'success')
        return redirect(url_for('admin_home_stats'))
    
    return render_template('admin/home_stats/edit.html', home_stat=home_stat)

@app.route('/admin/home-stats/delete/<int:id>', methods=['POST'])
@login_required
def admin_home_stats_delete(id):
    home_stat = HomeStats.query.get_or_404(id)
    db.session.delete(home_stat)
    db.session.commit()
    
    flash('Thống kê trang chủ đã được xóa!', 'success')
    return redirect(url_for('admin_home_stats'))

# Working Hours Management Routes
@app.route('/admin/working-hours')
@login_required
def admin_working_hours():
    working_hours = WorkingHours.query.order_by(WorkingHours.order_index.asc(), WorkingHours.created_at.desc()).all()
    return render_template('admin/working_hours/index.html', working_hours=working_hours)

@app.route('/admin/working-hours/create', methods=['GET', 'POST'])
@login_required
def admin_working_hours_create():
    if request.method == 'POST':
        day_key = request.form['day_key']
        day_label = request.form['day_label']
        hours = request.form['hours']
        order_index = int(request.form.get('order_index', 0))
        is_active = bool(request.form.get('is_active'))
        
        working_hour = WorkingHours(
            day_key=day_key,
            day_label=day_label,
            hours=hours,
            order_index=order_index,
            is_active=is_active
        )
        
        db.session.add(working_hour)
        db.session.commit()
        
        flash('Giờ làm việc đã được thêm!', 'success')
        return redirect(url_for('admin_working_hours'))
    
    return render_template('admin/working_hours/create.html')

@app.route('/admin/working-hours/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_working_hours_edit(id):
    working_hour = WorkingHours.query.get_or_404(id)
    
    if request.method == 'POST':
        working_hour.day_key = request.form['day_key']
        working_hour.day_label = request.form['day_label']
        working_hour.hours = request.form['hours']
        working_hour.order_index = int(request.form.get('order_index', 0))
        working_hour.is_active = bool(request.form.get('is_active'))
        
        db.session.commit()
        flash('Giờ làm việc đã được cập nhật!', 'success')
        return redirect(url_for('admin_working_hours'))
    
    return render_template('admin/working_hours/edit.html', working_hour=working_hour)

@app.route('/admin/working-hours/delete/<int:id>', methods=['POST'])
@login_required
def admin_working_hours_delete(id):
    working_hour = WorkingHours.query.get_or_404(id)
    db.session.delete(working_hour)
    db.session.commit()
    
    flash('Giờ làm việc đã được xóa!', 'success')
    return redirect(url_for('admin_working_hours'))

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
        
        # Handle image removal first
        if request.form.get('remove_image') == '1':
            if special_program.image_path:
                delete_old_image(special_program.image_path)
            special_program.image_path = None
        
        # Handle image upload
        elif 'image' in request.files and request.files['image'].filename:
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

def init_blog_categories():
    """Initialize default blog categories"""
    default_categories = [
        {'name': 'Giáo dục trẻ em', 'slug': 'giao-duc-tre-em'},
        {'name': 'Dinh dưỡng', 'slug': 'dinh-duong'},
        {'name': 'Tâm lý trẻ em', 'slug': 'tam-ly-tre-em'},
        {'name': 'Hoạt động vui chơi', 'slug': 'hoat-dong-vui-choi'},
        {'name': 'Kỹ năng sống', 'slug': 'ky-nang-song'},
        {'name': 'Sức khỏe trẻ em', 'slug': 'suc-khoe-tre-em'}
    ]
    
    for cat_data in default_categories:
        existing = Category.query.filter_by(name=cat_data['name']).first()
        if not existing:
            category = Category(name=cat_data['name'], slug=cat_data['slug'])
            db.session.add(category)
    
    try:
        db.session.commit()
        print("✅ Blog categories initialized successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error initializing categories: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Initialize blog categories
        init_blog_categories()
        
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

# Custom Jinja2 Filters
def nl2br(value):
    """Convert newlines to <br> tags"""
    if not value:
        return value
    return Markup(str(value).replace('\n', '<br>\n'))

app.jinja_env.filters['nl2br'] = nl2br

def from_json(value):
    """Parse JSON string to Python object"""
    import json
    try:
        if isinstance(value, str):
            return json.loads(value)
        return value
    except (json.JSONDecodeError, TypeError):
        return []

app.jinja_env.filters['from_json'] = from_json

@app.route('/proxy-image')
def proxy_image():
    """Proxy route để bypass CORS cho image preview"""
    import requests
    import base64
    
    url = request.args.get('url')
    print(f"Proxy request for URL: {url}")
    
    if not url:
        print("No URL provided")
        abort(400)
    
    try:
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            print("Invalid URL format")
            abort(400)
        
        # Process URL through our handler
        processed_url = process_external_image_url(url)
        print(f"Processed URL: {processed_url}")
        
        # Fetch image
        response = requests.get(processed_url, timeout=10)
        print(f"Response status: {response.status_code}")
        print(f"Response content-type: {response.headers.get('content-type')}")
        print(f"Response content-length: {len(response.content)}")
        
        response.raise_for_status()
        
        # Return base64 encoded image
        import base64
        content_type = response.headers.get('content-type', 'image/jpeg')
        if not content_type.startswith('image/'):
            content_type = 'image/jpeg'
        
        # Encode to base64
        base64_data = base64.b64encode(response.content).decode('utf-8')
        data_url = f"data:{content_type};base64,{base64_data}"
        
        # Return as JSON with data URL
        return jsonify({
            'success': True,
            'data_url': data_url,
            'content_type': content_type,
            'size': len(response.content)
        })
        
    except Exception as e:
        print(f"Proxy image error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/sitemap.xml')
def dynamic_sitemap():
    """Generate dynamic sitemap.xml with all pages"""
    from flask import Response
    from datetime import datetime
    import xml.etree.ElementTree as ET
    
    try:
        # Create sitemap root element
        urlset = ET.Element('urlset')
        urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        
        # Base URL - adjust this to your domain
        base_url = request.url_root.rstrip('/')
        
        # Add main pages with proper priority and frequency
        main_pages = [
            {'url': '/', 'priority': '1.0', 'changefreq': 'daily'},
            {'url': '/gioi-thieu', 'priority': '0.9', 'changefreq': 'monthly'},
            {'url': '/chuong-trinh', 'priority': '0.9', 'changefreq': 'weekly'},
            {'url': '/tin-tuc', 'priority': '0.8', 'changefreq': 'daily'},
            {'url': '/su-kien', 'priority': '0.8', 'changefreq': 'weekly'},
            {'url': '/blog', 'priority': '0.8', 'changefreq': 'daily'},
            {'url': '/thu-vien-anh', 'priority': '0.7', 'changefreq': 'weekly'},
            {'url': '/lien-he', 'priority': '0.6', 'changefreq': 'monthly'},
        ]
        
        for page in main_pages:
            url_elem = ET.SubElement(urlset, 'url')
            ET.SubElement(url_elem, 'loc').text = base_url + page['url']
            ET.SubElement(url_elem, 'lastmod').text = datetime.now().strftime('%Y-%m-%d')
            ET.SubElement(url_elem, 'changefreq').text = page['changefreq']
            ET.SubElement(url_elem, 'priority').text = page['priority']
        
        # Add individual news articles (limit to recent ones for sitemap performance)
        news_articles = News.query.filter_by(is_published=True).order_by(News.created_at.desc()).limit(50).all()
        for article in news_articles:
            url_elem = ET.SubElement(urlset, 'url')
            ET.SubElement(url_elem, 'loc').text = f"{base_url}/tin-tuc/{article.id}"
            # Use updated_at if available, otherwise created_at
            lastmod_date = getattr(article, 'updated_at', article.created_at)
            ET.SubElement(url_elem, 'lastmod').text = lastmod_date.strftime('%Y-%m-%d')
            ET.SubElement(url_elem, 'changefreq').text = 'monthly'
            ET.SubElement(url_elem, 'priority').text = '0.6'
        
        # Add individual events (only active and future/recent events)
        from datetime import timedelta
        recent_cutoff = datetime.utcnow() - timedelta(days=90)  # Last 90 days
        events = Event.query.filter(
            Event.is_active == True,
            Event.event_date >= recent_cutoff
        ).order_by(Event.event_date.desc()).limit(30).all()
        
        for event in events:
            url_elem = ET.SubElement(urlset, 'url')
            ET.SubElement(url_elem, 'loc').text = f"{base_url}/su-kien/{event.id}"
            ET.SubElement(url_elem, 'lastmod').text = event.created_at.strftime('%Y-%m-%d')
            # Higher priority for upcoming events
            if event.event_date > datetime.utcnow():
                ET.SubElement(url_elem, 'priority').text = '0.7'
                ET.SubElement(url_elem, 'changefreq').text = 'weekly'
            else:
                ET.SubElement(url_elem, 'priority').text = '0.5'
                ET.SubElement(url_elem, 'changefreq').text = 'yearly'
        
        # Add individual blog posts (recent ones)
        blog_posts = Post.query.filter_by(is_published=True).order_by(Post.created_at.desc()).limit(50).all()
        for post in blog_posts:
            url_elem = ET.SubElement(urlset, 'url')
            ET.SubElement(url_elem, 'loc').text = f"{base_url}/blog/{post.id}"
            lastmod_date = getattr(post, 'updated_at', post.created_at)
            ET.SubElement(url_elem, 'lastmod').text = lastmod_date.strftime('%Y-%m-%d')
            ET.SubElement(url_elem, 'changefreq').text = 'monthly'
            ET.SubElement(url_elem, 'priority').text = '0.6'
        
        # Add individual programs (all active programs)
        programs = Program.query.filter_by(is_active=True).all()
        for program in programs:
            url_elem = ET.SubElement(urlset, 'url')
            ET.SubElement(url_elem, 'loc').text = f"{base_url}/chuong-trinh/{program.id}"
            ET.SubElement(url_elem, 'lastmod').text = program.created_at.strftime('%Y-%m-%d')
            ET.SubElement(url_elem, 'changefreq').text = 'monthly'
            ET.SubElement(url_elem, 'priority').text = '0.7'
        
        # Convert to string
        ET.indent(urlset, space="  ", level=0)
        xml_str = ET.tostring(urlset, encoding='utf-8', xml_declaration=True).decode('utf-8')
        
        # Create response
        response = Response(xml_str, mimetype='application/xml')
        response.headers['Content-Type'] = 'application/xml; charset=utf-8'
        
        return response
        
    except Exception as e:
        print(f"Error generating dynamic sitemap: {e}")
        # Fallback to static sitemap if dynamic fails
        sitemap_path = os.path.join(app.root_path, 'sitemap.xml')
        if os.path.exists(sitemap_path):
            with open(sitemap_path, 'r', encoding='utf-8') as f:
                content = f.read()
            response = Response(content, mimetype='application/xml')
            response.headers['Content-Type'] = 'application/xml; charset=utf-8'
            return response
        else:
            return Response("Sitemap generation failed", status=500)

@app.route('/robots.txt')
def robots():
    """Serve dynamic robots.txt file"""
    from flask import Response
    
    # Get base URL dynamically
    base_url = request.url_root.rstrip('/')
    
    robots_content = f"""User-agent: *
Allow: /

# Disallow admin and sensitive pages
Disallow: /admin/
Disallow: /admin/*
Disallow: /login
Disallow: /logout

# Disallow API endpoints and utility routes
Disallow: /proxy-image
Disallow: /health
Disallow: /debug-*
Disallow: /test-*
Disallow: /_uploads/
Disallow: /static/uploads/

# Disallow search and filter parameters
Disallow: /*?*
Disallow: /*/search
Disallow: /*/filter

# Allow important pages explicitly
Allow: /
Allow: /gioi-thieu
Allow: /chuong-trinh
Allow: /chuong-trinh/*
Allow: /tin-tuc
Allow: /tin-tuc/*
Allow: /su-kien
Allow: /su-kien/*
Allow: /blog
Allow: /blog/*
Allow: /thu-vien-anh
Allow: /lien-he

# Allow static resources
Allow: /static/css/*
Allow: /static/js/*
Allow: /static/images/*
Allow: /static/fonts/*

# Crawl delay for politeness
Crawl-delay: 1

# Sitemap location
Sitemap: {base_url}/sitemap.xml

# Additional sitemaps (if needed in future)
# Sitemap: {base_url}/sitemap-news.xml
# Sitemap: {base_url}/sitemap-images.xml"""

    response = Response(robots_content, mimetype='text/plain')
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response

if __name__ == '__main__':
    # Lấy port từ environment variable hoặc dùng 5000 làm default
    port = int(os.environ.get('PORT', 5000))
    # Chỉ bật debug mode khi không phải production
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)