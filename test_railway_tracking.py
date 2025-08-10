#!/usr/bin/env python3
"""
Script để test tính năng tracking lượt truy cập trên Railway
"""

import os
import mysql.connector
import requests
from datetime import datetime, timedelta

# Thông tin kết nối Railway MySQL
RAILWAY_CONFIG = {
    'host': 'crossover.proxy.rlwy.net',
    'port': 29685,
    'user': 'root',
    'password': 'JUMlghRDGtVSaVSZoLgpelgXeTfNpAbp',
    'database': 'railway',
    'charset': 'utf8mb4'
}

# URL website trên Railway
WEBSITE_URL = 'https://mamnon.hoahuongduong.org'

def check_page_visit_stats():
    """Kiểm tra thống kê lượt truy cập"""
    try:
        print("📊 Đang kiểm tra thống kê lượt truy cập...")
        
        connection = mysql.connector.connect(**RAILWAY_CONFIG)
        cursor = connection.cursor()
        
        # Tổng lượt truy cập
        cursor.execute("SELECT COUNT(*) FROM page_visit")
        total_visits = cursor.fetchone()[0]
        
        # Lượt truy cập hôm nay
        today = datetime.now().date()
        cursor.execute("SELECT COUNT(*) FROM page_visit WHERE visit_date = %s", (today,))
        visits_today = cursor.fetchone()[0]
        
        # Unique visitors hôm nay
        cursor.execute("SELECT COUNT(*) FROM page_visit WHERE visit_date = %s AND is_unique = 1", (today,))
        unique_today = cursor.fetchone()[0]
        
        # Lượt truy cập 7 ngày qua
        week_ago = today - timedelta(days=7)
        cursor.execute("SELECT COUNT(*) FROM page_visit WHERE visit_date >= %s", (week_ago,))
        visits_week = cursor.fetchone()[0]
        
        # Top 5 trang được truy cập nhiều nhất
        cursor.execute("""
            SELECT page_url, COUNT(*) as visit_count 
            FROM page_visit 
            GROUP BY page_url 
            ORDER BY visit_count DESC 
            LIMIT 5
        """)
        top_pages = cursor.fetchall()
        
        # Hiển thị thống kê
        print("\n" + "="*60)
        print("📈 THỐNG KÊ LƯỢT TRUY CẬP WEBSITE")
        print("="*60)
        print(f"🌐 Tổng lượt truy cập:        {total_visits:,}")
        print(f"📅 Lượt truy cập hôm nay:    {visits_today:,}")
        print(f"👥 Khách duy nhất hôm nay:   {unique_today:,}")
        print(f"📊 Lượt truy cập 7 ngày:     {visits_week:,}")
        
        if top_pages:
            print(f"\n🔥 TOP 5 TRANG ĐƯỢC TRUY CẬP NHIỀU NHẤT:")
            print("-" * 60)
            for i, (url, count) in enumerate(top_pages, 1):
                # Rút gọn URL nếu quá dài
                display_url = url[:50] + "..." if len(url) > 50 else url
                print(f"{i}. {display_url:<53} ({count:,} lượt)")
        
        # Thống kê theo ngày (7 ngày gần nhất)
        print(f"\n📊 THỐNG KÊ THEO NGÀY (7 ngày gần nhất):")
        print("-" * 60)
        for i in range(7):
            check_date = today - timedelta(days=i)
            cursor.execute("SELECT COUNT(*) FROM page_visit WHERE visit_date = %s", (check_date,))
            day_visits = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM page_visit WHERE visit_date = %s AND is_unique = 1", (check_date,))
            day_unique = cursor.fetchone()[0]
            
            day_name = check_date.strftime("%A")[:3]  # Mon, Tue, etc.
            date_str = check_date.strftime("%d/%m")
            
            print(f"{day_name} {date_str}: {day_visits:>3} lượt ({day_unique:>2} unique)")
        
        cursor.close()
        connection.close()
        
        return {
            'total_visits': total_visits,
            'visits_today': visits_today,
            'unique_today': unique_today,
            'visits_week': visits_week
        }
        
    except Exception as e:
        print(f"❌ Lỗi khi kiểm tra thống kê: {e}")
        return None

def test_website_access():
    """Test truy cập website để tạo dữ liệu tracking"""
    try:
        print(f"🌐 Đang test truy cập website: {WEBSITE_URL}")
        
        # Tạo một số request để test tracking
        test_pages = [
            '/',
            '/gioi-thieu',
            '/chuong-trinh',
            '/tin-tuc',
            '/lien-he'
        ]
        
        for page in test_pages:
            url = f"{WEBSITE_URL}{page}"
            try:
                response = requests.get(url, timeout=10)
                status = "✅" if response.status_code == 200 else "❌"
                print(f"  {status} {page:<15} - Status: {response.status_code}")
            except requests.RequestException as e:
                print(f"  ❌ {page:<15} - Error: {str(e)[:30]}...")
        
        print("⏳ Chờ 2 giây để tracking được xử lý...")
        import time
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ Lỗi khi test website: {e}")

def show_recent_visits():
    """Hiển thị các lượt truy cập gần nhất"""
    try:
        print("🕒 Đang lấy danh sách truy cập gần nhất...")
        
        connection = mysql.connector.connect(**RAILWAY_CONFIG)
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT ip_address, page_url, visit_time, is_unique
            FROM page_visit 
            ORDER BY visit_time DESC 
            LIMIT 10
        """)
        
        recent_visits = cursor.fetchall()
        
        if recent_visits:
            print(f"\n🕒 10 LƯỢT TRUY CẬP GẦN NHẤT:")
            print("-" * 80)
            print(f"{'IP Address':<15} {'Page':<30} {'Time':<20} {'Unique'}")
            print("-" * 80)
            
            for ip, page, visit_time, is_unique in recent_visits:
                # Rút gọn URL
                display_page = page.replace(WEBSITE_URL, '') if page else '/'
                display_page = display_page[:28] + ".." if len(display_page) > 30 else display_page
                
                # Ẩn một phần IP để bảo mật
                masked_ip = ip[:8] + "***" if ip and len(ip) > 8 else ip or "Unknown"
                
                unique_mark = "🆕" if is_unique else "🔄"
                time_str = visit_time.strftime("%d/%m %H:%M:%S") if visit_time else "Unknown"
                
                print(f"{masked_ip:<15} {display_page:<30} {time_str:<20} {unique_mark}")
        else:
            print("📭 Chưa có lượt truy cập nào được ghi nhận.")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Lỗi khi lấy danh sách truy cập: {e}")

if __name__ == "__main__":
    print("🧪 Railway Tracking Test Script")
    print("=" * 60)
    print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Website: {WEBSITE_URL}")
    print()
    
    # Kiểm tra thống kê hiện tại
    stats_before = check_page_visit_stats()
    
    if stats_before is not None:
        print("\n" + "="*60)
        
        # Test truy cập website (tùy chọn)
        user_input = input("🤔 Bạn có muốn test truy cập website không? (y/N): ").strip().lower()
        if user_input in ['y', 'yes']:
            test_website_access()
            
            # Kiểm tra thống kê sau khi test
            print("\n" + "="*60)
            print("📊 THỐNG KÊ SAU KHI TEST:")
            stats_after = check_page_visit_stats()
        
        # Hiển thị các lượt truy cập gần nhất
        print("\n" + "="*60)
        show_recent_visits()
        
        print("\n" + "="*60)
        print("✅ Test hoàn thành!")
        print("💡 Bạn có thể truy cập admin dashboard để xem thống kê chi tiết:")
        print(f"   {WEBSITE_URL}/admin")
    else:
        print("💥 Không thể kết nối đến database!")
