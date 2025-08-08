#!/usr/bin/env python3
"""
Database initialization script for Railway MySQL
This script will create all tables and initialize default data
"""

import os
import sys
from werkzeug.security import generate_password_hash

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment variables for Railway MySQL connection
# Use internal host if running on Railway, external proxy for local development
if os.environ.get('RAILWAY_ENVIRONMENT'):
    # Running on Railway - use internal connection
    os.environ['MYSQLHOST'] = 'mysql.railway.internal'
    os.environ['MYSQLPORT'] = '3306'
    os.environ['MYSQL_URL'] = 'mysql://root:JUMlghRDGtVSaVSZoLgpelgXeTfNpAbp@mysql.railway.internal:3306/railway'
else:
    # Running locally - use external proxy
    os.environ['MYSQLHOST'] = 'crossover.proxy.rlwy.net'
    os.environ['MYSQLPORT'] = '29685'
    os.environ['MYSQL_URL'] = 'mysql://root:JUMlghRDGtVSaVSZoLgpelgXeTfNpAbp@crossover.proxy.rlwy.net:29685/railway'

os.environ['MYSQLUSER'] = 'root'
os.environ['MYSQLPASSWORD'] = 'JUMlghRDGtVSaVSZoLgpelgXeTfNpAbp'
os.environ['MYSQLDATABASE'] = 'railway'

# Import the Flask app and database
from app import app, db, User, ContactSettings

def init_database():
    """Initialize the database with tables and default data"""
    print("Initializing MySQL database...")
    
    with app.app_context():
        try:
            # Test database connection
            print("Testing database connection...")
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            print("✓ Database connection successful!")
            
            # Create all tables
            print("Creating database tables...")
            db.create_all()
            print("✓ All tables created successfully!")
            
            # Create default admin user if not exists
            print("Creating default admin user...")
            if not User.query.first():
                admin = User(
                    username='admin',
                    email='admin@hoahuongduong.edu.vn',
                    password_hash=generate_password_hash('admin123')
                )
                db.session.add(admin)
                print("✓ Default admin user created (username: admin, password: admin123)")
            else:
                print("✓ Admin user already exists")
            
            # Create default contact settings if not exists
            print("Creating default contact settings...")
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
                print("✓ Default contact settings created")
            else:
                print("✓ Contact settings already exist")
            
            # Commit all changes
            db.session.commit()
            print("✓ All changes committed to database")
            
            print("\n🎉 Database initialization completed successfully!")
            print("\nDatabase connection details:")
            print(f"Host: {os.environ.get('MYSQLHOST')}")
            print(f"Database: {os.environ.get('MYSQLDATABASE')}")
            print(f"User: {os.environ.get('MYSQLUSER')}")
            print("\nAdmin login credentials:")
            print("Username: admin")
            print("Password: admin123")
            
        except Exception as e:
            print(f"❌ Error initializing database: {str(e)}")
            print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
            return False
    
    return True

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
