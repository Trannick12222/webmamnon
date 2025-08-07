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
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/uploads/gallery', exist_ok=True)
os.makedirs('static/uploads/news', exist_ok=True)
os.makedirs('static/uploads/programs', exist_ok=True)
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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_unread_contacts():
    try:
        unread_contacts = Contact.query.filter_by(is_read=False).count()
        # Also inject contact settings for global use (header, footer)
        contact_settings = ContactSettings.query.filter_by(is_active=True).order_by(ContactSettings.order_index.asc()).all()
    except:
        unread_contacts = 0
        contact_settings = []
    return dict(unread_contacts=unread_contacts, global_contact_settings=contact_settings)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def save_image(file, folder='uploads'):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + '_' + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], folder, unique_filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)
        return f'uploads/{folder}/{unique_filename}'
    return None

@app.route('/')
def index():
    featured_programs = Program.query.filter_by(is_active=True, is_featured=True).limit(6).all()
    latest_news = News.query.filter_by(is_published=True).order_by(News.created_at.desc()).limit(3).all()
    gallery_images = Gallery.query.filter_by(is_featured=True).limit(8).all()
    upcoming_events = Event.query.filter_by(is_active=True).filter(Event.event_date > datetime.utcnow()).limit(3).all()
    slider_images = Slider.query.filter_by(is_active=True).order_by(Slider.order_index.asc()).all()
    
    # Get contact settings for social links
    contact_settings = ContactSettings.query.filter_by(is_active=True).order_by(ContactSettings.order_index.asc()).all()
    
    return render_template('index.html', 
                         featured_programs=featured_programs,
                         latest_news=latest_news,
                         gallery_images=gallery_images,
                         upcoming_events=upcoming_events,
                         slider_images=slider_images,
                         contact_settings=contact_settings)

@app.route('/gioi-thieu')
def about():
    return render_template('about.html')

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
    # Debug: Print program images
    for program in programs:
        if program.featured_image:
            print(f"Program {program.name} has image: {program.featured_image}")
            print(f"Full path: {os.path.join(app.config['UPLOAD_FOLDER'], program.featured_image.replace('uploads/', ''))}")
    return render_template('programs.html', programs=programs)

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
    return render_template('contact.html', contact_settings=contact_settings)

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
    stats = {
        'posts': Post.query.count(),
        'programs': Program.query.count(),
        'gallery': Gallery.query.count(),
        'contacts': Contact.query.filter_by(is_read=False).count(),
        'news': News.query.count(),
        'events': Event.query.count(),
        'slider': Slider.query.count()
    }
    unread_contacts = Contact.query.filter_by(is_read=False).count()
    return render_template('admin/dashboard.html', stats=stats, unread_contacts=unread_contacts)

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
            image_path = save_image(request.files['featured_image'], 'news')
            if image_path:
                news.featured_image = image_path
        
        db.session.commit()
        flash('Tin tức đã được cập nhật!', 'success')
        return redirect(url_for('admin_news'))
    
    return render_template('admin/news/edit.html', news=news)

@app.route('/admin/news/delete/<int:id>')
@login_required
def admin_news_delete(id):
    news = News.query.get_or_404(id)
    db.session.delete(news)
    db.session.commit()
    flash('Tin tức đã được xóa!', 'success')
    return redirect(url_for('admin_news'))

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
        
        if 'featured_image' in request.files:
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
        
        if 'featured_image' in request.files and request.files['featured_image'].filename:
            image_path = save_image(request.files['featured_image'], 'programs')
            if image_path:
                program.featured_image = image_path
        
        db.session.commit()
        flash('Chương trình đã được cập nhật!', 'success')
        return redirect(url_for('admin_programs'))
    
    return render_template('admin/programs/edit.html', program=program)

@app.route('/admin/programs/delete/<int:id>')
@login_required
def admin_programs_delete(id):
    program = Program.query.get_or_404(id)
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

@app.route('/admin/gallery/delete/<int:id>')
@login_required
def admin_gallery_delete(id):
    image = Gallery.query.get_or_404(id)
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
        event_date = datetime.strptime(
            f"{request.form['event_date']} {request.form['event_time']}", 
            '%Y-%m-%d %H:%M'
        )
        
        event.title = request.form['title']
        event.description = request.form['description']
        event.event_date = event_date
        event.location = request.form.get('location')
        event.is_active = bool(request.form.get('is_active'))
        
        if 'featured_image' in request.files and request.files['featured_image'].filename:
            image_path = save_image(request.files['featured_image'], 'events')
            if image_path:
                event.featured_image = image_path
        
        db.session.commit()
        flash('Sự kiện đã được cập nhật!', 'success')
        return redirect(url_for('admin_events'))
    
    return render_template('admin/events/edit.html', event=event)

@app.route('/admin/events/delete/<int:id>')
@login_required
def admin_events_delete(id):
    event = Event.query.get_or_404(id)
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

@app.route('/admin/contacts/delete/<int:id>')
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

@app.route('/admin/settings')
@login_required
def admin_settings():
    return render_template('admin/settings.html')

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
            image_path = save_image(request.files['image'], 'slider')
            if image_path:
                slider.image_path = image_path
        
        db.session.commit()
        flash('Slider đã được cập nhật!', 'success')
        return redirect(url_for('admin_slider'))
    
    return render_template('admin/slider/edit.html', slider=slider)

@app.route('/admin/slider/delete/<int:id>')
@login_required
def admin_slider_delete(id):
    slider = Slider.query.get_or_404(id)
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

@app.route('/admin/contact-settings/delete/<int:id>')
@login_required
def admin_contact_settings_delete(id):
    setting = ContactSettings.query.get_or_404(id)
    db.session.delete(setting)
    db.session.commit()
    flash('Thông tin liên hệ đã được xóa!', 'success')
    return redirect(url_for('admin_contact_settings'))

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
    
    app.run(debug=True, host='0.0.0.0', port=5000)