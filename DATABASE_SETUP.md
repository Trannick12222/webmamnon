# Database Configuration for Railway MySQL

This document explains how to configure and use the Railway MySQL database with your Flask application.

## 🗄️ Database Configuration

Your application is now configured to use Railway MySQL database with the following credentials:

- **Host**: `mysql.railway.internal` (internal) / `crossover.proxy.rlwy.net` (external)
- **Port**: `3306` (internal) / `29685` (external)
- **Database**: `railway`
- **User**: `root`
- **Password**: `JUMlghRDGtVSaVSZoLgpelgXeTfNpAbp`

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Test Database Connection

```bash
python test_db_connection.py
```

### 3. Initialize Database

```bash
python init_mysql_db.py
```

### 4. Run Application

For Railway deployment:
```bash
gunicorn --bind 0.0.0.0:$PORT app:app
```

For local development:
```bash
python run_local.py
```

## 🔧 Environment Variables

The application automatically detects Railway environment variables:

- `MYSQLHOST` - Database host
- `MYSQLUSER` - Database user
- `MYSQLPASSWORD` - Database password
- `MYSQLPORT` - Database port
- `MYSQLDATABASE` - Database name
- `MYSQL_URL` - Complete database URL

## 📋 Database Tables

The application will create the following tables:

- `user` - Admin users
- `category` - Content categories
- `post` - Blog posts
- `program` - Educational programs
- `gallery` - Image gallery
- `news` - News articles
- `event` - Events
- `contact` - Contact form submissions
- `slider` - Homepage slider images
- `contact_settings` - Contact information
- `team_member` - Team members
- `mission_item` - Mission items
- `mission_content` - Mission content
- `history_section` - History section
- `history_event` - History events
- `about_section` - About section
- `about_stats` - About statistics
- `faq` - Frequently asked questions
- `special_program` - Special programs
- `call_to_action` - Call-to-action sections
- `intro_video` - Introduction videos
- `seo_settings` - SEO settings

## 🔐 Default Admin Account

After initialization, you can log in with:

- **Username**: `admin`
- **Password**: `admin123`
- **Admin URL**: `/admin`

**⚠️ Important**: Change the default password after first login!

## 🌐 Health Check

The application includes a health check endpoint at `/health` that:

- Tests database connectivity
- Returns MySQL version
- Shows environment information
- Provides connection status

Example response:
```json
{
  "status": "healthy",
  "database": "connected",
  "mysql_version": "8.0.35",
  "database_host": "mysql.railway.internal:3306/railway",
  "environment": "production"
}
```

## 🛠️ Troubleshooting

### Connection Issues

1. **Check environment variables**:
   ```bash
   python -c "import os; print('MYSQL_URL:', os.environ.get('MYSQL_URL'))"
   ```

2. **Test connection manually**:
   ```bash
   python test_db_connection.py
   ```

3. **Check Railway service status**:
   - Go to Railway dashboard
   - Check MySQL service logs
   - Verify service is running

### Common Errors

**Error**: `Access denied for user 'root'@'...'`
- **Solution**: Verify password in environment variables

**Error**: `Can't connect to MySQL server`
- **Solution**: Check host and port configuration
- For local development, use external proxy: `crossover.proxy.rlwy.net:29685`
- For Railway deployment, use internal host: `mysql.railway.internal:3306`

**Error**: `Unknown database 'railway'`
- **Solution**: Database should be created automatically by Railway

### Database Reset

If you need to reset the database:

1. **Drop all tables** (⚠️ This will delete all data):
   ```python
   from app import app, db
   with app.app_context():
       db.drop_all()
       db.create_all()
   ```

2. **Re-initialize**:
   ```bash
   python init_mysql_db.py
   ```

## 📁 File Structure

```
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── init_mysql_db.py      # Database initialization script
├── test_db_connection.py # Connection test script
├── run_local.py          # Local development server
├── deploy.py             # Deployment script
├── railway.json          # Railway configuration
└── DATABASE_SETUP.md     # This documentation
```

## 🔄 Migration from SQLite

If you were previously using SQLite, your data will need to be migrated:

1. **Export SQLite data** (if needed):
   ```bash
   python -c "
   import sqlite3
   import json
   conn = sqlite3.connect('instance/hoa_huong_duong.db')
   # Export your data here
   "
   ```

2. **Import to MySQL**:
   - Use the admin panel to recreate content
   - Or create a custom migration script

## 📞 Support

If you encounter issues:

1. Check the health endpoint: `/health`
2. Review Railway service logs
3. Verify environment variables are set correctly
4. Test database connection with the provided scripts

## 🔒 Security Notes

- Never commit database credentials to version control
- Use Railway's environment variables for production
- Change default admin password immediately
- Consider using database connection pooling for high traffic
- Regularly backup your database

## 🚀 Deployment to Railway

1. **Push your code** to Railway
2. **Set environment variables** (should be automatic)
3. **Run initialization**:
   ```bash
   python deploy.py
   ```
4. **Access your application** at the Railway-provided URL

Your application should now be successfully connected to Railway MySQL! 🎉
