#!/usr/bin/env python3
"""
Test script to verify MySQL database connection
"""

import os
import sys

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

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_mysql_connection():
    """Test MySQL connection using mysql-connector-python"""
    try:
        import mysql.connector
        
        print("Testing MySQL connection with mysql-connector-python...")
        
        connection = mysql.connector.connect(
            host=os.environ.get('MYSQLHOST'),
            user=os.environ.get('MYSQLUSER'),
            password=os.environ.get('MYSQLPASSWORD'),
            port=int(os.environ.get('MYSQLPORT')),
            database=os.environ.get('MYSQLDATABASE')
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✓ MySQL connection successful!")
            print(f"✓ MySQL version: {version[0]}")
            
            # Test basic query
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"✓ Current tables in database: {len(tables)} tables")
            for table in tables:
                print(f"  - {table[0]}")
            
            cursor.close()
            connection.close()
            return True
            
    except Exception as e:
        print(f"❌ MySQL connection failed: {str(e)}")
        return False

def test_sqlalchemy_connection():
    """Test SQLAlchemy connection"""
    try:
        from app import app, db
        
        print("\nTesting SQLAlchemy connection...")
        print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        with app.app_context():
            # Test basic query
            from sqlalchemy import text
            result = db.session.execute(text('SELECT VERSION()'))
            version = result.fetchone()
            print(f"✓ SQLAlchemy connection successful!")
            print(f"✓ MySQL version: {version[0]}")
            
            # Check if tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✓ Tables accessible via SQLAlchemy: {len(tables)} tables")
            for table in tables:
                print(f"  - {table}")
            
            return True
            
    except Exception as e:
        print(f"❌ SQLAlchemy connection failed: {str(e)}")
        return False

def test_pymysql_connection():
    """Test PyMySQL connection"""
    try:
        import pymysql
        
        print("\nTesting PyMySQL connection...")
        
        connection = pymysql.connect(
            host=os.environ.get('MYSQLHOST'),
            user=os.environ.get('MYSQLUSER'),
            password=os.environ.get('MYSQLPASSWORD'),
            port=int(os.environ.get('MYSQLPORT')),
            database=os.environ.get('MYSQLDATABASE')
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✓ PyMySQL connection successful!")
            print(f"✓ MySQL version: {version[0]}")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ PyMySQL connection failed: {str(e)}")
        return False

if __name__ == '__main__':
    print("🔍 Testing database connections...\n")
    
    # Test different connection methods
    mysql_ok = test_mysql_connection()
    pymysql_ok = test_pymysql_connection()
    sqlalchemy_ok = test_sqlalchemy_connection()
    
    print(f"\n📊 Connection Test Results:")
    print(f"MySQL Connector: {'✓ PASS' if mysql_ok else '❌ FAIL'}")
    print(f"PyMySQL: {'✓ PASS' if pymysql_ok else '❌ FAIL'}")
    print(f"SQLAlchemy: {'✓ PASS' if sqlalchemy_ok else '❌ FAIL'}")
    
    if sqlalchemy_ok:
        print(f"\n🎉 Database is ready for your Flask application!")
    else:
        print(f"\n⚠️  Please check your database configuration.")
    
    sys.exit(0 if sqlalchemy_ok else 1)
