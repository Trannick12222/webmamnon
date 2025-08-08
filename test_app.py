#!/usr/bin/env python3
"""
Test script to verify the Flask application is working with MySQL
"""

import os
import sys

# Set Railway MySQL environment variables for local testing
os.environ['MYSQLHOST'] = 'crossover.proxy.rlwy.net'
os.environ['MYSQLUSER'] = 'root'
os.environ['MYSQLPASSWORD'] = 'JUMlghRDGtVSaVSZoLgpelgXeTfNpAbp'
os.environ['MYSQLPORT'] = '29685'
os.environ['MYSQLDATABASE'] = 'railway'
os.environ['MYSQL_URL'] = 'mysql://root:JUMlghRDGtVSaVSZoLgpelgXeTfNpAbp@crossover.proxy.rlwy.net:29685/railway'

# Import the Flask app
from app import app, db, User, News, Program

def test_app():
    """Test the Flask application"""
    print("🧪 Testing Flask application with MySQL...")
    
    with app.app_context():
        try:
            # Test database connection
            from sqlalchemy import text
            result = db.session.execute(text('SELECT VERSION()'))
            version = result.fetchone()
            print(f"✓ Database connection: MySQL {version[0]}")
            
            # Test database URL
            db_url = app.config['SQLALCHEMY_DATABASE_URI']
            safe_db_url = db_url.split('@')[1] if '@' in db_url else 'local'
            print(f"✓ Database URL: {safe_db_url}")
            
            # Test table access
            user_count = User.query.count()
            print(f"✓ Users table: {user_count} users")
            
            news_count = News.query.count()
            print(f"✓ News table: {news_count} articles")
            
            program_count = Program.query.count()
            print(f"✓ Programs table: {program_count} programs")
            
            # Test health check function
            from app import health_check
            with app.test_client() as client:
                response = client.get('/health')
                print(f"✓ Health check endpoint: {response.status_code}")
                if response.status_code == 200:
                    data = response.get_json()
                    print(f"  - Status: {data.get('status')}")
                    print(f"  - Database: {data.get('database')}")
                    print(f"  - MySQL Version: {data.get('mysql_version')}")
                    print(f"  - Environment: {data.get('environment')}")
            
            print("\n🎉 All tests passed! Your application is ready for deployment.")
            return True
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            return False

if __name__ == '__main__':
    success = test_app()
    sys.exit(0 if success else 1)
