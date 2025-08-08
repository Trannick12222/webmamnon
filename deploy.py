#!/usr/bin/env python3
"""
Deployment script for Railway
This script handles database initialization and other deployment tasks
"""

import os
import sys
import subprocess

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("🔍 Testing database connection...")
    try:
        subprocess.run([sys.executable, 'test_db_connection.py'], check=True)
        print("✓ Database connection test passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def initialize_database():
    """Initialize database with tables and default data"""
    print("🗄️ Initializing database...")
    try:
        subprocess.run([sys.executable, 'init_mysql_db.py'], check=True)
        print("✓ Database initialized successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 Starting Railway deployment process...\n")
    
    # Check if we're in Railway environment
    is_railway = os.environ.get('RAILWAY_ENVIRONMENT') is not None
    print(f"Environment: {'Railway' if is_railway else 'Local'}")
    
    if is_railway:
        print("Railway environment variables:")
        for key in ['MYSQLHOST', 'MYSQLUSER', 'MYSQLDATABASE', 'RAILWAY_ENVIRONMENT']:
            value = os.environ.get(key, 'Not set')
            print(f"  {key}: {value}")
    
    print()
    
    # Step 1: Install dependencies (if needed)
    if not is_railway:  # Railway handles this automatically
        if not install_dependencies():
            sys.exit(1)
    
    # Step 2: Test database connection
    if not test_database_connection():
        print("⚠️  Database connection failed, but continuing with initialization...")
    
    # Step 3: Initialize database
    if not initialize_database():
        print("⚠️  Database initialization failed")
        sys.exit(1)
    
    print("\n🎉 Deployment completed successfully!")
    print("\nYour application is ready to use:")
    print("- Admin panel: /admin")
    print("- Health check: /health")
    print("- Default admin credentials: admin / admin123")

if __name__ == '__main__':
    main()
