SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- Sửa bảng news (đầy đủ tất cả cột)
UPDATE news SET 
    title = 'Khai giảng năm học mới 2024-2025',
    content = 'Trường Mầm non Hoa Hướng Dương xin thông báo lễ khai giảng năm học mới 2024-2025 sẽ được tổ chức vào ngày 05/09/2024. Chương trình gồm có các hoạt động như chào cờ, phát biểu của Ban Giám hiệu, giới thiệu đội ngũ giáo viên mới và các hoạt động vui chơi cho các em học sinh.',
    summary = 'Thông báo về lễ khai giảng năm học mới 2024-2025 diễn ra vào ngày 05/09/2024'
WHERE id = 1;

UPDATE news SET 
    title = 'Chương trình ngoại khóa tháng 10',
    content = 'Trong tháng 10, trường sẽ tổ chức nhiều hoạt động ngoại khóa bổ ích cho các em như: tham quan vườn bách thảo, học nấu ăn đơn giản, và các trò chơi tập thể. Các hoạt động này nhằm giúp trẻ phát triển toàn diện về thể chất lẫn tinh thần.',
    summary = 'Các hoạt động ngoại khóa phong phú trong tháng 10 dành cho học sinh'
WHERE id = 2;

UPDATE news SET 
    title = 'Hội thảo nuôi dưỡng trẻ cho phụ huynh',
    content = 'Trường tổ chức hội thảo "Nuôi dưỡng và giáo dục trẻ mầm non" dành cho các bậc phụ huynh vào ngày 15/10/2024. Hội thảo do các chuyên gia tâm lý và dinh dưỡng trẻ em hàng đầu thực hiện, giúp cha mẹ hiểu rõ hơn về cách chăm sóc con trẻ ở độ tuổi mầm non.',
    summary = 'Hội thảo bổ ích về nuôi dưỡng trẻ em dành cho phụ huynh'
WHERE id = 3;

-- Sửa bảng category
UPDATE category SET name = 'Hoạt động học tập' WHERE id = 1;
UPDATE category SET name = 'Sự kiện trường' WHERE id = 2;
UPDATE category SET name = 'Thông báo' WHERE id = 3;
UPDATE category SET name = 'Tin tức chung' WHERE id = 4;

-- Sửa bảng event
UPDATE event SET 
    title = 'Lễ Trung Thu 2024',
    description = 'Tổ chức đêm hội Trung Thu với nhiều hoạt động vui chơi, múa lân, thưởng thức bánh kẹo và đèn lồng cho các em học sinh.',
    location = 'Sân trường Hoa Hướng Dương'
WHERE id = 1;

UPDATE event SET 
    title = 'Ngày hội thể thao',
    description = 'Ngày hội thể thao năm 2024 với các môn thi đấu phù hợp lứa tuổi mầm non như chạy, nhảy bao bố, kéo co.',
    location = 'Sân vận động trường'
WHERE id = 2;

UPDATE event SET 
    title = 'Biểu diễn cuối năm',
    description = 'Chương trình biểu diễn văn nghệ cuối năm học với sự tham gia của tất cả các lớp, thể hiện những gì các em đã học được.',
    location = 'Hội trường trường học'
WHERE id = 3;

-- Sửa bảng program
UPDATE program SET 
    name = 'Lớp Mầm (18-24 tháng)',
    description = 'Chương trình giáo dục cho trẻ 18-24 tháng tuổi, tập trung phát triển kỹ năng vận động thô, tinh và ngôn ngữ cơ bản.',
    age_group = '18-24 tháng',
    price = '2,500,000 VNĐ/tháng',
    duration = 'Cả năm học'
WHERE id = 1;

UPDATE program SET 
    name = 'Lớp Chồi (2-3 tuổi)',
    description = 'Chương trình giáo dục toàn diện cho trẻ 2-3 tuổi với các hoạt động vui chơi, học tập và phát triển tính cách.',
    age_group = '2-3 tuổi',
    price = '2,800,000 VNĐ/tháng',
    duration = 'Cả năm học'
WHERE id = 2;

UPDATE program SET 
    name = 'Lớp Lá (3-4 tuổi)',
    description = 'Chuẩn bị cho trẻ 3-4 tuổi với các kỹ năng cần thiết trước khi vào mẫu giáo lớn.',
    age_group = '3-4 tuổi',
    price = '3,000,000 VNĐ/tháng',
    duration = 'Cả năm học'
WHERE id = 3;

UPDATE program SET 
    name = 'Lớp Lúa (4-5 tuổi)',
    description = 'Chương trình chuẩn bị vào lớp 1 cho trẻ 4-5 tuổi với các hoạt động học tập có hệ thống.',
    age_group = '4-5 tuổi',
    price = '3,200,000 VNĐ/tháng',
    duration = 'Cả năm học'
WHERE id = 4;

UPDATE program SET 
    name = 'Lớp Ngoại ngữ',
    description = 'Lớp học tiếng Anh cho trẻ em từ 3-5 tuổi với phương pháp giảng dạy sinh động, phù hợp lứa tuổi.',
    age_group = '3-5 tuổi',
    price = '1,500,000 VNĐ/tháng',
    duration = '3 buổi/tuần'
WHERE id = 5;

UPDATE program SET 
    name = 'Lớp Năng khiếu',
    description = 'Các lớp học năng khiếu như vẽ, múa, hát, đàn piano giúp phát triển tài năng của trẻ.',
    age_group = '3-5 tuổi',
    price = '1,000,000 VNĐ/tháng',
    duration = '2 buổi/tuần'
WHERE id = 6;

UPDATE program SET 
    name = 'Lớp Chồi Non',
    description = 'Chương trình đặc biệt dành cho trẻ em với phương pháp giáo dục hiện đại.',
    age_group = 'Đa tuổi',
    price = '1,000,000,000 VNĐ/tháng',
    duration = 'Cả năm học'
WHERE id = 7;

-- Sửa bảng settings
UPDATE settings SET setting_value = 'Trường Mầm non Hoa Hướng Dương' WHERE setting_key = 'school_name';
UPDATE settings SET setting_value = '123 Đường Hoa Hướng Dương, Quận 1, TP.HCM' WHERE setting_key = 'school_address';
UPDATE settings SET setting_value = 'Thứ 2 - Thứ 6: 7:00 - 17:00' WHERE setting_key = 'school_hours';
UPDATE settings SET setting_value = 'Nuôi dưỡng tâm hồn - Phát triển tài năng' WHERE setting_key = 'school_motto';

-- Sửa bảng contact_settings
UPDATE contact_settings SET 
    display_name = 'Số điện thoại chính',
    description = 'Hotline tư vấn và hỗ trợ'
WHERE setting_key = 'phone_main';

UPDATE contact_settings SET 
    display_name = 'Email chính',
    description = 'Email liên hệ chính thức'
WHERE setting_key = 'email_main';

UPDATE contact_settings SET 
    display_name = 'Facebook',
    description = 'Trang Facebook chính thức của trường'
WHERE setting_key = 'facebook';

UPDATE contact_settings SET 
    display_name = 'Zalo',
    description = 'Chat Zalo để tư vấn nhanh'
WHERE setting_key = 'zalo';

UPDATE contact_settings SET 
    display_name = 'YouTube',
    description = 'Kênh YouTube với các hoạt động của trường'
WHERE setting_key = 'youtube';

-- Sửa bảng location_settings
UPDATE location_settings SET 
    address = '123 Đường Hoa Hướng Dương, Quận 1, TP.HCM',
    marker_title = 'Trường Mầm non Hoa Hướng Dương',
    marker_info = 'Trường Mầm non Hoa Hướng Dương - Nuôi dưỡng tâm hồn, phát triển tài năng'
WHERE id = 1;

-- Sửa bảng intro_video
UPDATE intro_video SET 
    title = 'Giới thiệu trường',
    description = 'Video giới thiệu về Trường Mầm non Hoa Hướng Dương'
WHERE id = 2;
