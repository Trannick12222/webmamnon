#!/usr/bin/env python3
"""
Script to initialize themes in the database
Run this after creating the database tables
"""

from app import app, db, init_default_themes

def main():
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Initialize default themes
            init_default_themes()
            print("✅ Default themes initialized successfully")
            
            print("\n🎨 Available themes:")
            from app import ThemeSettings
            themes = ThemeSettings.query.all()
            for theme in themes:
                status = "🟢 ACTIVE" if theme.is_active else "⚪ INACTIVE"
                default = "⭐ DEFAULT" if theme.is_default else ""
                print(f"  - {theme.theme_name} ({theme.primary_color}) {status} {default}")
            
            print(f"\n✨ Total themes: {len(themes)}")
            print("🚀 Theme system is ready!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    return True

if __name__ == "__main__":
    main()
