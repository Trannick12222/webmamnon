"""
Image URL Handler - Xử lý URL hình ảnh từ các dịch vụ cloud storage
Hỗ trợ: Google Drive, OneDrive, Dropbox, Imgur, v.v.
"""
import re
import requests
from urllib.parse import urlparse, parse_qs

def convert_google_drive_url(url):
    """
    Chuyển đổi Google Drive share URL thành direct image URL
    Input: https://drive.google.com/file/d/FILE_ID/view?usp=sharing
    Output: https://drive.google.com/uc?export=view&id=FILE_ID
    """
    # Pattern cho Google Drive URLs
    patterns = [
        r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',
        r'https://drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)',
        r'https://drive\.google\.com/uc\?id=([a-zA-Z0-9_-]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            file_id = match.group(1)
            return f"https://drive.google.com/uc?export=view&id={file_id}"
    
    return url

def convert_onedrive_url(url):
    """
    Chuyển đổi OneDrive share URL thành direct image URL
    Input: https://1drv.ms/i/s!... hoặc https://onedrive.live.com/...
    """
    if '1drv.ms' in url or 'onedrive.live.com' in url:
        # OneDrive URLs có thể phức tạp, thường cần thêm &download=1
        if '?' in url:
            return url + '&download=1'
        else:
            return url + '?download=1'
    return url

def convert_dropbox_url(url):
    """
    Chuyển đổi Dropbox share URL thành direct image URL
    Input: https://www.dropbox.com/s/...?dl=0
    Output: https://www.dropbox.com/s/...?dl=1 (hoặc raw=1)
    """
    if 'dropbox.com' in url:
        # Thay dl=0 thành dl=1 hoặc thêm raw=1
        if 'dl=0' in url:
            return url.replace('dl=0', 'dl=1')
        elif '?' in url:
            return url + '&raw=1'
        else:
            return url + '?raw=1'
    return url

def convert_imgur_url(url):
    """
    Chuyển đổi Imgur URL thành direct image URL
    """
    if 'imgur.com' in url and not url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        # Thêm .jpg extension nếu chưa có
        if '/gallery/' in url:
            # Gallery URL cần xử lý khác
            return url
        else:
            return url + '.jpg'
    return url

def convert_google_photos_url(url):
    """
    Chuyển đổi Google Photos share URL thành direct image URL
    Input: https://photos.app.goo.gl/... hoặc https://photos.google.com/share/...
    """
    if 'photos.app.goo.gl' in url or 'photos.google.com' in url:
        # Google Photos URLs thường cần thêm =w2048 hoặc =s1600 để lấy direct image
        # Tuy nhiên, Google Photos có chính sách bảo mật nghiêm ngặt
        # Cần xử lý đặc biệt
        
        # Cách 1: Thêm parameter để lấy direct image
        if '=w' not in url and '=s' not in url:
            # Thêm parameter để lấy image với width 1600px
            separator = '&' if '?' in url else '?'
            return url + separator + 'w=1600'
        
        return url
    
    return url

def extract_google_photos_direct_url(share_url):
    """
    Trích xuất direct URL từ Google Photos share URL
    Lưu ý: Google Photos có thể yêu cầu authentication
    """
    try:
        import requests
        from urllib.parse import urlparse, parse_qs
        
        # Google Photos share URLs thường redirect
        response = requests.get(share_url, allow_redirects=True, timeout=10)
        
        # Tìm direct image URL trong HTML response
        if response.status_code == 200:
            content = response.text
            
            # Tìm các pattern phổ biến cho direct image URLs
            patterns = [
                r'"(https://lh3\.googleusercontent\.com/[^"]+)"',
                r'"(https://lh4\.googleusercontent\.com/[^"]+)"',
                r'"(https://lh5\.googleusercontent\.com/[^"]+)"',
                r'"(https://lh6\.googleusercontent\.com/[^"]+)"',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content)
                if matches:
                    # Lấy URL đầu tiên và thêm size parameter
                    direct_url = matches[0]
                    if '=w' not in direct_url and '=s' not in direct_url:
                        direct_url += '=s1600'
                    return direct_url
        
        return share_url
        
    except Exception as e:
        print(f"Error extracting Google Photos URL: {e}")
        return share_url

def process_external_image_url(url):
    """
    Xử lý URL hình ảnh từ các dịch vụ khác nhau
    """
    if not url:
        return None
    
    url = url.strip()
    
    # Google Drive
    if 'drive.google.com' in url:
        return convert_google_drive_url(url)
    
    # Google Photos
    elif 'photos.app.goo.gl' in url or 'photos.google.com' in url:
        # Thử extract direct URL trước
        try:
            direct_url = extract_google_photos_direct_url(url)
            if direct_url != url:
                return direct_url
        except:
            pass
        # Fallback to simple conversion
        return convert_google_photos_url(url)
    
    # OneDrive
    elif '1drv.ms' in url or 'onedrive.live.com' in url:
        return convert_onedrive_url(url)
    
    # Dropbox
    elif 'dropbox.com' in url:
        return convert_dropbox_url(url)
    
    # Imgur
    elif 'imgur.com' in url:
        return convert_imgur_url(url)
    
    # Direct image URLs
    elif url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')):
        return url
    
    # Other URLs - return as is
    return url

def validate_image_url(url, timeout=10):
    """
    Kiểm tra xem URL có phải là hình ảnh hợp lệ không
    """
    try:
        # Xử lý URL trước
        processed_url = process_external_image_url(url)
        
        # Gửi HEAD request để kiểm tra
        response = requests.head(processed_url, timeout=timeout, allow_redirects=True)
        
        # Kiểm tra status code
        if response.status_code != 200:
            return False, f"HTTP {response.status_code}"
        
        # Kiểm tra Content-Type
        content_type = response.headers.get('Content-Type', '').lower()
        if not content_type.startswith('image/'):
            return False, f"Not an image (Content-Type: {content_type})"
        
        # Kiểm tra kích thước file (nếu có)
        content_length = response.headers.get('Content-Length')
        if content_length:
            size_mb = int(content_length) / (1024 * 1024)
            if size_mb > 10:  # Giới hạn 10MB
                return False, f"File too large ({size_mb:.1f}MB)"
        
        return True, "Valid image URL"
        
    except requests.exceptions.Timeout:
        return False, "Request timeout"
    except requests.exceptions.RequestException as e:
        return False, f"Request error: {str(e)}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def get_supported_services():
    """
    Trả về danh sách các dịch vụ được hỗ trợ
    """
    return {
        'google_drive': {
            'name': 'Google Drive',
            'example': 'https://drive.google.com/file/d/FILE_ID/view?usp=sharing',
            'instructions': 'Chuột phải vào file → Get link → Copy link'
        },
        'google_photos': {
            'name': 'Google Photos',
            'example': 'https://photos.app.goo.gl/... hoặc https://photos.google.com/share/...',
            'instructions': 'Chọn ảnh → Share → Create link → Copy link (Lưu ý: cần public sharing)',
            'note': 'Có thể cần authentication, khuyến nghị dùng Google Drive thay thế'
        },
        'onedrive': {
            'name': 'OneDrive',
            'example': 'https://1drv.ms/i/s!...',
            'instructions': 'Chuột phải vào file → Share → Copy link'
        },
        'dropbox': {
            'name': 'Dropbox',
            'example': 'https://www.dropbox.com/s/...?dl=0',
            'instructions': 'Chuột phải vào file → Copy Dropbox link'
        },
        'imgur': {
            'name': 'Imgur',
            'example': 'https://imgur.com/IMAGE_ID',
            'instructions': 'Upload ảnh lên Imgur → Copy direct link'
        },
        'direct': {
            'name': 'Direct Image URL',
            'example': 'https://example.com/image.jpg',
            'instructions': 'URL trực tiếp đến file hình ảnh (.jpg, .png, .gif, ...)'
        }
    }
