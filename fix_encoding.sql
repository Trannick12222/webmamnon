-- Fix encoding for news table
UPDATE news SET 
    title = 'Hội thảo nuôi dưỡng trẻ cho phụ huynh',
    content = 'Trường tổ chức hội thảo "Nuôi dưỡng và giáo dục trẻ mầm non" dành cho các bậc phụ huynh vào ngày 15/10/2024. Hội thảo do các chuyên gia tâm lý và dinh dưỡng trẻ em hàng đầu thực hiện, giúp cha mẹ hiểu rõ hơn về cách chăm sóc con trẻ ở độ tuổi mầm non.',
    summary = 'Hội thảo bổ ích về nuôi dưỡng trẻ em dành cho phụ huynh'
WHERE id = 3;

-- Fix other potential encoding issues
UPDATE category SET name = 'Hoạt động học tập' WHERE id = 1;
UPDATE category SET name = 'Sự kiện trường' WHERE id = 2;
UPDATE category SET name = 'Thông báo' WHERE id = 3;
UPDATE category SET name = 'Tin tức chung' WHERE id = 4;

UPDATE settings SET setting_value = 'Trường Mầm non Hoa Hướng Dương' WHERE setting_key = 'school_name';
UPDATE settings SET setting_value = '123 Đường Hoa Hướng Dương, Quận 1, TP.HCM' WHERE setting_key = 'school_address';
UPDATE settings SET setting_value = 'Thứ 2 - Thứ 6: 7:00 - 17:00' WHERE setting_key = 'school_hours';
UPDATE settings SET setting_value = 'Nuôi dưỡng tâm hồn - Phát triển tài năng' WHERE setting_key = 'school_motto';

-- Fix program names
UPDATE program SET name = 'Lớp Mầm (18-24 tháng)' WHERE id = 1;
UPDATE program SET name = 'Lớp Chồi (2-3 tuổi)' WHERE id = 2;
UPDATE program SET name = 'Lớp Lá (3-4 tuổi)' WHERE id = 3;
UPDATE program SET name = 'Lớp Lúa (4-5 tuổi)' WHERE id = 4;
UPDATE program SET name = 'Lớp Ngoại ngữ' WHERE id = 5;
UPDATE program SET name = 'Lớp Năng khiếu' WHERE id = 6;

-- Fix event titles
UPDATE event SET title = 'Lễ Trung Thu 2024' WHERE id = 1;
UPDATE event SET title = 'Ngày hội thể thao' WHERE id = 2;
UPDATE event SET title = 'Biểu diễn cuối năm' WHERE id = 3;
