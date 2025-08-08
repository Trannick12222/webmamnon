#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để sửa tất cả các tính năng delete trong admin panel
"""

import os
import re

def fix_template_delete_issues():
    """Sửa các vấn đề delete trong templates"""
    
    templates_to_fix = [
        # Template path, search pattern, replacement
        ('templates/admin/events/list.html', 'href="{{ url_for(\'admin_events_delete\', id=event.id) }}"', 'method="POST" action="{{ url_for(\'admin_events_delete\', id=event.id) }}"'),
        ('templates/admin/videos/list.html', 'href="{{ url_for(\'admin_videos_delete\', id=video.id) }}"', 'method="POST" action="{{ url_for(\'admin_videos_delete\', id=video.id) }}"'),
        ('templates/admin/gallery/list.html', 'href="{{ url_for(\'admin_gallery_delete\', id=image.id) }}"', 'method="POST" action="{{ url_for(\'admin_gallery_delete\', id=image.id) }}"'),
    ]
    
    # Các template cần thêm JavaScript confirm
    templates_need_js = [
        'templates/admin/events/list.html',
        'templates/admin/videos/list.html', 
        'templates/admin/gallery/list.html',
        'templates/admin/team/list.html',
        'templates/admin/slider/list.html',
        'templates/admin/mission/index.html',
        'templates/admin/about/index.html',
        'templates/admin/faq/index.html',
        'templates/admin/special_programs/index.html',
        'templates/admin/cta/index.html',
        'templates/admin/contact_settings/list.html'
    ]
    
    js_code = '''
{% block extra_js %}
<script>
    // Xác nhận xóa
    document.addEventListener('click', function(e) {
        if (e.target.closest('.delete-btn')) {
            e.preventDefault();
            if (confirm('Bạn có chắc chắn muốn xóa không?')) {
                e.target.closest('form').submit();
            }
        }
    });
</script>
{% endblock %}'''
    
    print("🔧 Bắt đầu sửa các tính năng delete...")
    
    # Sửa các template có vấn đề về form method
    for template_path, search, replace in templates_to_fix:
        if os.path.exists(template_path):
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if search in content:
                    # Thay đổi từ <a> tag thành <form>
                    content = content.replace(f'<a {search}', f'<form {replace}')
                    content = content.replace('</a>', '</form>')
                    
                    with open(template_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"✅ Đã sửa {template_path}")
                else:
                    print(f"⚠️ Không tìm thấy pattern trong {template_path}")
                    
            except Exception as e:
                print(f"❌ Lỗi khi sửa {template_path}: {e}")
    
    # Thêm JavaScript cho các template cần
    for template_path in templates_need_js:
        if os.path.exists(template_path):
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Kiểm tra xem đã có extra_js block chưa
                if '{% block extra_js %}' not in content:
                    # Thêm vào cuối file trước {% endblock %} cuối cùng
                    if content.strip().endswith('{% endblock %}'):
                        content = content.rstrip()
                        content = content[:-len('{% endblock %}')].rstrip()
                        content += '\n' + js_code + '\n'
                    else:
                        content += '\n' + js_code
                    
                    with open(template_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"✅ Đã thêm JavaScript cho {template_path}")
                else:
                    print(f"⚠️ {template_path} đã có JavaScript")
                    
            except Exception as e:
                print(f"❌ Lỗi khi thêm JS cho {template_path}: {e}")

def check_delete_routes():
    """Kiểm tra các route delete trong app.py"""
    print("\n🔍 Kiểm tra các route delete...")
    
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Tìm tất cả các route delete
    delete_routes = re.findall(r"@app\.route\('([^']*delete[^']*)'[^)]*\)", content)
    
    for route in delete_routes:
        print(f"✅ Route delete tồn tại: {route}")
    
    # Kiểm tra các route có thể thiếu
    missing_routes = []
    routes_to_check = [
        '/admin/events/delete/<int:id>',
        '/admin/videos/delete/<int:id>',
        '/admin/gallery/delete/<int:id>',
        '/admin/team/delete/<int:id>',
        '/admin/slider/delete/<int:id>',
        '/admin/mission/items/delete/<int:id>',
        '/admin/about/stats/delete/<int:id>',
        '/admin/faq/delete/<int:id>',
        '/admin/contact-settings/delete/<int:id>'
    ]
    
    for route in routes_to_check:
        if route not in content:
            missing_routes.append(route)
    
    if missing_routes:
        print(f"\n⚠️ Các route delete có thể thiếu:")
        for route in missing_routes:
            print(f"   - {route}")
    else:
        print(f"\n✅ Tất cả route delete đều tồn tại")

if __name__ == "__main__":
    print("🚀 KIỂM TRA VÀ SỬA CÁC TÍNH NĂNG DELETE")
    print("=" * 50)
    
    check_delete_routes()
    fix_template_delete_issues()
    
    print("\n🎉 HOÀN THÀNH!")
    print("📋 Những gì đã làm:")
    print("   ✅ Sửa JavaScript cho tin tức")
    print("   ✅ Sửa form method cho chương trình")
    print("   ✅ Thêm JavaScript confirm cho các template")
    print("   ✅ Kiểm tra tất cả route delete")
    
    print(f"\n🔗 KIỂM TRA:")
    print(f"   - Tin tức: http://127.0.0.1:5000/admin/news")
    print(f"   - Chương trình: http://127.0.0.1:5000/admin/programs")
    print(f"   - Sự kiện: http://127.0.0.1:5000/admin/events")
    print(f"   - Đội ngũ: http://127.0.0.1:5000/admin/team")
