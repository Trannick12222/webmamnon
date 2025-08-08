#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để sửa tất cả các lỗi template thiếu endblock
"""

import os
import re

def fix_template_endblock_issues():
    """Sửa các template thiếu endblock"""
    
    templates_to_fix = [
        'templates/admin/team/list.html',
        'templates/admin/mission/index.html', 
        'templates/admin/gallery/list.html',
        'templates/admin/faq/index.html',
        'templates/admin/about/index.html',
        'templates/admin/special_programs/index.html',
        'templates/admin/cta/index.html'
    ]
    
    print("🔧 Bắt đầu sửa các template thiếu endblock...")
    
    for template_path in templates_to_fix:
        if os.path.exists(template_path):
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Đếm số lượng {% block %} và {% endblock %}
                block_count = len(re.findall(r'{%\s*block\s+\w+\s*%}', content))
                endblock_count = len(re.findall(r'{%\s*endblock\s*%}', content))
                
                print(f"\n📄 {template_path}")
                print(f"   Blocks: {block_count}, Endblocks: {endblock_count}")
                
                if block_count > endblock_count:
                    missing_endblocks = block_count - endblock_count
                    print(f"   ⚠️ Thiếu {missing_endblocks} endblock(s)")
                    
                    # Tìm vị trí cuối cùng có {% block extra_js %}
                    if '{% block extra_js %}' in content:
                        # Nếu có extra_js block, thêm endblock trước nó
                        pattern = r'(\n\s*{% block extra_js %})'
                        replacement = r'\n{% endblock %}\1'
                        content = re.sub(pattern, replacement, content)
                        print(f"   ✅ Đã thêm endblock trước extra_js")
                    else:
                        # Nếu không có extra_js, thêm endblock ở cuối
                        content = content.rstrip() + '\n{% endblock %}\n'
                        print(f"   ✅ Đã thêm endblock ở cuối file")
                    
                    # Ghi lại file
                    with open(template_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"   💾 Đã lưu file")
                else:
                    print(f"   ✅ Template đã đúng")
                    
            except Exception as e:
                print(f"   ❌ Lỗi: {e}")
        else:
            print(f"❌ Không tìm thấy file: {template_path}")

def verify_templates():
    """Kiểm tra lại các template sau khi sửa"""
    print(f"\n🔍 KIỂM TRA LẠI CÁC TEMPLATE...")
    
    templates_to_check = [
        'templates/admin/team/list.html',
        'templates/admin/mission/index.html', 
        'templates/admin/gallery/list.html',
        'templates/admin/faq/index.html',
        'templates/admin/about/index.html',
        'templates/admin/special_programs/index.html',
        'templates/admin/cta/index.html'
    ]
    
    all_good = True
    
    for template_path in templates_to_check:
        if os.path.exists(template_path):
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                block_count = len(re.findall(r'{%\s*block\s+\w+\s*%}', content))
                endblock_count = len(re.findall(r'{%\s*endblock\s*%}', content))
                
                if block_count == endblock_count:
                    print(f"✅ {template_path} - OK ({block_count} blocks)")
                else:
                    print(f"❌ {template_path} - Vẫn lỗi ({block_count} blocks, {endblock_count} endblocks)")
                    all_good = False
                    
            except Exception as e:
                print(f"❌ {template_path} - Lỗi đọc file: {e}")
                all_good = False
    
    return all_good

if __name__ == "__main__":
    print("🚀 SỬA CÁC TEMPLATE THIẾU ENDBLOCK")
    print("=" * 50)
    
    fix_template_endblock_issues()
    
    print(f"\n" + "=" * 50)
    if verify_templates():
        print("🎉 TẤT CẢ TEMPLATE ĐÃ ĐƯỢC SỬA THÀNH CÔNG!")
        print(f"\n🔗 KIỂM TRA CÁC TRANG:")
        print(f"   - Team: http://127.0.0.1:5000/admin/team")
        print(f"   - Mission: http://127.0.0.1:5000/admin/mission")
        print(f"   - Gallery: http://127.0.0.1:5000/admin/gallery")
        print(f"   - FAQ: http://127.0.0.1:5000/admin/faq")
        print(f"   - About: http://127.0.0.1:5000/admin/about")
        print(f"   - Special Programs: http://127.0.0.1:5000/admin/special-programs")
        print(f"   - Call to Action: http://127.0.0.1:5000/admin/call-to-action")
    else:
        print("⚠️ VẪN CÒN MỘT SỐ TEMPLATE CÓ VẤN ĐỀ!")
