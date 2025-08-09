SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

UPDATE news SET 
    title = 'Hội thảo nuôi dưỡng trẻ cho phụ huynh',
    content = 'Trường tổ chức hội thảo "Nuôi dưỡng và giáo dục trẻ mầm non" dành cho các bậc phụ huynh vào ngày 15/10/2024. Hội thảo do các chuyên gia tâm lý và dinh dưỡng trẻ em hàng đầu thực hiện, giúp cha mẹ hiểu rõ hơn về cách chăm sóc con trẻ ở độ tuổi mầm non.',
    summary = 'Hội thảo bổ ích về nuôi dưỡng trẻ em dành cho phụ huynh'
WHERE id = 3;

-- Cập nhật các bảng khác có thể bị lỗi charset
UPDATE category SET name = 'Hoạt động học tập' WHERE id = 1;
UPDATE category SET name = 'Sự kiện trường' WHERE id = 2;
UPDATE category SET name = 'Thông báo' WHERE id = 3;
UPDATE category SET name = 'Tin tức chung' WHERE id = 4;

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

UPDATE program SET 
    name = 'Lớp Mầm (18-24 tháng)',
    description = 'Chương trình giáo dục cho trẻ 18-24 tháng tuổi, tập trung phát triển kỹ năng vận động thô, tinh và ngôn ngữ cơ bản.'
WHERE id = 1;

UPDATE program SET 
    name = 'Lớp Chồi (2-3 tuổi)',
    description = 'Chương trình giáo dục toàn diện cho trẻ 2-3 tuổi với các hoạt động vui chơi, học tập và phát triển tính cách.'
WHERE id = 2;

UPDATE program SET 
    name = 'Lớp Lá (3-4 tuổi)',
    description = 'Chuẩn bị cho trẻ 3-4 tuổi với các kỹ năng cần thiết trước khi vào mẫu giáo lớn.'
WHERE id = 3;

UPDATE program SET 
    name = 'Lớp Lúa (4-5 tuổi)',
    description = 'Chương trình chuẩn bị vào lớp 1 cho trẻ 4-5 tuổi với các hoạt động học tập có hệ thống.'
WHERE id = 4;

UPDATE program SET 
    name = 'Lớp Ngoại ngữ',
    description = 'Lớp học tiếng Anh cho trẻ em từ 3-5 tuổi với phương pháp giảng dạy sinh động, phù hợp lứa tuổi.'
WHERE id = 5;

UPDATE program SET 
    name = 'Lớp Năng khiếu',
    description = 'Các lớp học năng khiếu như vẽ, múa, hát, đàn piano giúp phát triển tài năng của trẻ.'
WHERE id = 6;

UPDATE settings SET setting_value = 'Trường Mầm non Hoa Hướng Dương' WHERE setting_key = 'school_name';
UPDATE settings SET setting_value = '123 Đường Hoa Hướng Dương, Quận 1, TP.HCM' WHERE setting_key = 'school_address';
UPDATE settings SET setting_value = 'Thứ 2 - Thứ 6: 7:00 - 17:00' WHERE setting_key = 'school_hours';
UPDATE settings SET setting_value = 'Nuôi dưỡng tâm hồn - Phát triển tài năng' WHERE setting_key = 'school_motto';
