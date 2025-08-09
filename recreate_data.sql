SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- Xóa và tạo lại dữ liệu bảng news
DELETE FROM news;
INSERT INTO news (id, title, content, summary, featured_image, is_published, publish_date, created_at) VALUES 
(1, 'Khai giảng năm học mới 2024-2025', 'Trường Mầm non Hoa Hướng Dương xin thông báo lễ khai giảng năm học mới 2024-2025 sẽ được tổ chức vào ngày 05/09/2024. Chương trình gồm có các hoạt động như chào cờ, phát biểu của Ban Giám hiệu, giới thiệu đội ngũ giáo viên mới và các hoạt động vui chơi cho các em học sinh.', 'Thông báo về lễ khai giảng năm học mới 2024-2025 diễn ra vào ngày 05/09/2024', 'uploads/news/cf6e7bc9-7059-447d-b4ba-463d3e31100a_Screenshot_2023.11.29_06.49.43.584.png', 1, '2025-08-03 12:41:43', '2025-08-03 12:41:43'),
(2, 'Chương trình ngoại khóa tháng 10', 'Trong tháng 10, trường sẽ tổ chức nhiều hoạt động ngoại khóa bổ ích cho các em như: tham quan vườn bách thảo, học nấu ăn đơn giản, và các trò chơi tập thể. Các hoạt động này nhằm giúp trẻ phát triển toàn diện về thể chất lẫn tinh thần.', 'Các hoạt động ngoại khóa phong phú trong tháng 10 dành cho học sinh', NULL, 1, '2025-08-03 12:41:43', '2025-08-03 12:41:43'),
(3, 'Hội thảo nuôi dưỡng trẻ cho phụ huynh', 'Trường tổ chức hội thảo "Nuôi dưỡng và giáo dục trẻ mầm non" dành cho các bậc phụ huynh vào ngày 15/10/2024. Hội thảo do các chuyên gia tâm lý và dinh dưỡng trẻ em hàng đầu thực hiện, giúp cha mẹ hiểu rõ hơn về cách chăm sóc con trẻ ở độ tuổi mầm non.', 'Hội thảo bổ ích về nuôi dưỡng trẻ em dành cho phụ huynh', NULL, 1, '2025-08-03 12:41:43', '2025-08-03 12:41:43');

-- Xóa và tạo lại dữ liệu bảng category
DELETE FROM category;
INSERT INTO category (id, name, slug, created_at) VALUES 
(1, 'Hoạt động học tập', 'hoat-dong-hoc-tap', '2025-08-03 12:41:43'),
(2, 'Sự kiện trường', 'su-kien-truong', '2025-08-03 12:41:43'),
(3, 'Thông báo', 'thong-bao', '2025-08-03 12:41:43'),
(4, 'Tin tức chung', 'tin-tuc-chung', '2025-08-03 12:41:43');

-- Xóa và tạo lại dữ liệu bảng event
DELETE FROM event;
INSERT INTO event (id, title, description, event_date, location, featured_image, is_active, created_at) VALUES 
(1, 'Lễ Trung Thu 2024', 'Tổ chức đêm hội Trung Thu với nhiều hoạt động vui chơi, múa lân, thưởng thức bánh kẹo và đèn lồng cho các em học sinh.', '2024-09-17 18:00:00', 'Sân trường Hoa Hướng Dương', NULL, 1, '2025-08-03 12:41:43'),
(2, 'Ngày hội thể thao', 'Ngày hội thể thao năm 2024 với các môn thi đấu phù hợp lứa tuổi mầm non như chạy, nhảy bao bố, kéo co.', '2024-10-25 08:00:00', 'Sân vận động trường', NULL, 1, '2025-08-03 12:41:43'),
(3, 'Biểu diễn cuối năm', 'Chương trình biểu diễn văn nghệ cuối năm học với sự tham gia của tất cả các lớp, thể hiện những gì các em đã học được.', '2024-12-20 19:00:00', 'Hội trường trường học', NULL, 1, '2025-08-03 12:41:43');

-- Cập nhật bảng settings
UPDATE settings SET setting_value = 'Trường Mầm non Hoa Hướng Dương' WHERE setting_key = 'school_name';
UPDATE settings SET setting_value = '123 Đường Hoa Hướng Dương, Quận 1, TP.HCM' WHERE setting_key = 'school_address';
UPDATE settings SET setting_value = 'Thứ 2 - Thứ 6: 7:00 - 17:00' WHERE setting_key = 'school_hours';
UPDATE settings SET setting_value = 'Nuôi dưỡng tâm hồn - Phát triển tài năng' WHERE setting_key = 'school_motto';
