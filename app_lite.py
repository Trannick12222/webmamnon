from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hoa-huong-duong-secret-key-2023'

# Context processor để cung cấp biến global cho templates
@app.context_processor
def inject_globals():
    return {
        'unread_contacts': 0,  # Số lượng tin nhắn chưa đọc
        'current_user': {'username': 'admin'} if session.get('admin_logged_in') else None
    }

# Dữ liệu mẫu (thay thế database)
sample_programs = [
    {
        'id': 1,
        'name': 'Lớp Mầm (18-24 tháng)',
        'description': 'Chương trình giáo dục cho trẻ 18-24 tháng tuổi, tập trung phát triển kỹ năng vận động thô, tinh và ngôn ngữ cơ bản.',
        'age_group': '18-24 tháng',
        'price': '2,500,000 VNĐ/tháng',
        'duration': 'Cả năm học',
        'featured_image': 'https://images.unsplash.com/photo-1544717297-fa95b6ee9643?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'is_active': True
    },
    {
        'id': 2,
        'name': 'Lớp Chồi (2-3 tuổi)',
        'description': 'Chương trình giáo dục toàn diện cho trẻ 2-3 tuổi với các hoạt động vui chơi, học tập và phát triển tính cách.',
        'age_group': '2-3 tuổi',
        'price': '2,800,000 VNĐ/tháng',
        'duration': 'Cả năm học',
        'featured_image': 'https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'is_active': True
    },
    {
        'id': 3,
        'name': 'Lớp Lá (3-4 tuổi)',
        'description': 'Chuẩn bị cho trẻ 3-4 tuổi với các kỹ năng cần thiết trước khi vào mẫu giáo lớn.',
        'age_group': '3-4 tuổi',
        'price': '3,000,000 VNĐ/tháng',
        'duration': 'Cả năm học',
        'featured_image': 'https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'is_active': True
    }
]

sample_news = [
    {
        'id': 1,
        'title': 'Khai giảng năm học mới 2024-2025',
        'content': 'Trường Mầm non Hoa Hướng Dương xin thông báo lễ khai giảng năm học mới...',
        'summary': 'Thông báo về lễ khai giảng năm học mới 2024-2025',
        'created_at': datetime.now(),
        'featured_image': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
    },
    {
        'id': 2,
        'title': 'Chương trình ngoại khóa tháng 10',
        'content': 'Trong tháng 10, trường sẽ tổ chức nhiều hoạt động ngoại khóa bổ ích...',
        'summary': 'Các hoạt động ngoại khóa phong phú trong tháng 10',
        'created_at': datetime.now(),
        'featured_image': 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
    }
]

sample_gallery = [
    {
        'id': 1,
        'title': 'Hoạt động học tập',
        'image_path': 'https://images.unsplash.com/photo-1544717297-fa95b6ee9643?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
        'is_featured': True
    },
    {
        'id': 2,
        'title': 'Vui chơi giải trí',
        'image_path': 'https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
        'is_featured': True
    },
    {
        'id': 3,
        'title': 'Các em học tập',
        'image_path': 'https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
        'is_featured': True
    },
    {
        'id': 4,
        'title': 'Hoạt động ngoại khóa',
        'image_path': 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
        'is_featured': True
    }
]

sample_events = [
    {
        'id': 1,
        'title': 'Lễ Trung Thu 2024',
        'description': 'Tổ chức đêm hội Trung Thu với nhiều hoạt động vui chơi...',
        'event_date': datetime(2024, 9, 17, 18, 0),
        'location': 'Sân trường Hoa Hướng Dương',
        'featured_image': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
    }
]

@app.route('/')
def index():
    return render_template('index.html', 
                         featured_programs=sample_programs[:3],
                         latest_news=sample_news,
                         gallery_images=sample_gallery,
                         upcoming_events=sample_events)

@app.route('/gioi-thieu')
def about():
    return render_template('about.html')

@app.route('/chuong-trinh')
def programs():
    return render_template('programs.html', programs=sample_programs)

@app.route('/chuong-trinh/<int:id>')
def program_detail(id):
    program = next((p for p in sample_programs if p['id'] == id), None)
    if not program:
        return "Không tìm thấy chương trình", 404
    return render_template('program_detail.html', program=program)

@app.route('/tin-tuc')
def news():
    return render_template('news.html', news={'items': sample_news, 'has_prev': False, 'has_next': False})

@app.route('/tin-tuc/<int:id>')
def news_detail(id):
    article = next((n for n in sample_news if n['id'] == id), None)
    if not article:
        return "Không tìm thấy tin tức", 404
    return render_template('news_detail.html', article=article, related_news=sample_news[:2])

@app.route('/thu-vien-anh')
def gallery():
    return render_template('gallery.html', images=sample_gallery, categories=['Hoạt động học tập', 'Vui chơi giải trí', 'Ngoại khóa'])

@app.route('/su-kien')
def events():
    return render_template('events.html', upcoming=sample_events, past=[])

@app.route('/lien-he', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Cảm ơn bạn đã liên hệ! Chúng tôi sẽ phản hồi sớm nhất có thể.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

# Routes cho admin (đơn giản)
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Đã đăng xuất', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    stats = {
        'posts': len(sample_news),
        'programs': len(sample_programs),
        'gallery': 0,
        'contacts': 0,
        'news': len(sample_news),
        'events': len(sample_events)
    }
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/news')
def admin_news():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin/news/list_simple.html', news_items=sample_news)

@app.route('/admin/news/create')
def admin_news_create():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin/news/create.html')

# Thêm các routes admin còn thiếu
@app.route('/admin/posts')
def admin_posts():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin/posts/list.html', posts=sample_news)

@app.route('/admin/programs')
def admin_programs():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin/programs/list.html', programs=sample_programs)

@app.route('/admin/programs/create')
def admin_programs_create():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin/programs/create.html')

@app.route('/admin/gallery')
def admin_gallery():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin/gallery/list.html', images={'items': []})

@app.route('/admin/gallery/create')
def admin_gallery_create():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin/gallery/create.html')

@app.route('/admin/events')
def admin_events():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin/events/list.html', events=sample_events)

@app.route('/admin/events/create')
def admin_events_create():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin/events/create.html')

@app.route('/admin/contacts')
def admin_contacts():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin/contacts/list.html', contacts=[])

@app.route('/admin/settings')
def admin_settings():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin/settings.html')

if __name__ == '__main__':
    # Tạo thư mục uploads
    os.makedirs('static/uploads', exist_ok=True)
    os.makedirs('static/uploads/news', exist_ok=True)
    os.makedirs('static/uploads/programs', exist_ok=True)
    os.makedirs('static/uploads/gallery', exist_ok=True)
    
    print("🌻 Website Trường Mầm non Hoa Hướng Dương - Phiên bản Demo")
    print("=" * 60)
    print("🚀 Server đang chạy tại: http://localhost:5000")
    print("🔧 Admin Panel: http://localhost:5000/admin")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n👋 Nhấn Ctrl+C để dừng server")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)