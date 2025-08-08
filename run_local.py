#!/usr/bin/env python3
"""
Local development server with Railway MySQL connection
"""

import os
import sys

# Set Railway MySQL environment variables for local testing
os.environ['MYSQLHOST'] = 'crossover.proxy.rlwy.net'  # Use public proxy for local testing
os.environ['MYSQLUSER'] = 'root'
os.environ['MYSQLPASSWORD'] = 'JUMlghRDGtVSaVSZoLgpelgXeTfNpAbp'
os.environ['MYSQLPORT'] = '29685'  # Use public proxy port
os.environ['MYSQLDATABASE'] = 'railway'
os.environ['MYSQL_URL'] = 'mysql://root:JUMlghRDGtVSaVSZoLgpelgXeTfNpAbp@crossover.proxy.rlwy.net:29685/railway'
os.environ['FLASK_ENV'] = 'development'

# Import and run the Flask app
from app import app

if __name__ == '__main__':
    print("🚀 Starting local development server with Railway MySQL...")
    print(f"Database: {os.environ.get('MYSQLHOST')}:{os.environ.get('MYSQLPORT')}")
    print(f"Environment: {os.environ.get('FLASK_ENV')}")
    print("\nAccess your application at: http://localhost:5000")
    print("Admin panel: http://localhost:5000/admin")
    print("Health check: http://localhost:5000/health")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
