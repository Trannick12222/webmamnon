-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: hoa_huong_duong
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `about_section`
--

DROP TABLE IF EXISTS `about_section`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `about_section` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT NULL,
  `subtitle` text,
  `description_1` text,
  `description_2` text,
  `image_1` varchar(255) DEFAULT NULL,
  `image_2` varchar(255) DEFAULT NULL,
  `experience_years` varchar(10) DEFAULT NULL,
  `experience_text` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `about_section`
--

LOCK TABLES `about_section` WRITE;
/*!40000 ALTER TABLE `about_section` DISABLE KEYS */;
/*!40000 ALTER TABLE `about_section` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `about_stats`
--

DROP TABLE IF EXISTS `about_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `about_stats` (
  `id` int NOT NULL AUTO_INCREMENT,
  `stat_key` varchar(50) NOT NULL,
  `stat_value` varchar(20) NOT NULL,
  `stat_label` varchar(100) NOT NULL,
  `icon_class` varchar(100) DEFAULT NULL,
  `color_class` varchar(50) DEFAULT NULL,
  `order_index` int DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `stat_key` (`stat_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `about_stats`
--

LOCK TABLES `about_stats` WRITE;
/*!40000 ALTER TABLE `about_stats` DISABLE KEYS */;
/*!40000 ALTER TABLE `about_stats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `call_to_action`
--

DROP TABLE IF EXISTS `call_to_action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `call_to_action` (
  `id` int NOT NULL AUTO_INCREMENT,
  `section_name` varchar(100) NOT NULL,
  `main_title` varchar(255) NOT NULL,
  `subtitle` text NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `working_hours` varchar(100) DEFAULT NULL,
  `email_response_time` varchar(50) DEFAULT NULL,
  `visit_note` varchar(100) DEFAULT NULL,
  `promotion_title` varchar(255) DEFAULT NULL,
  `promotion_description` text,
  `promotion_note` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `section_name` (`section_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `call_to_action`
--

LOCK TABLES `call_to_action` WRITE;
/*!40000 ALTER TABLE `call_to_action` DISABLE KEYS */;
/*!40000 ALTER TABLE `call_to_action` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Hoạt động học tập','hoat-dong-hoc-tap','2025-08-03 12:41:43'),(2,'Sự kiện trường','su-kien-truong','2025-08-03 12:41:43'),(3,'Thông báo','thong-bao','2025-08-03 12:41:43'),(4,'Tin tức chung','tin-tuc-chung','2025-08-03 12:41:43');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `subject` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact`
--

LOCK TABLES `contact` WRITE;
/*!40000 ALTER TABLE `contact` DISABLE KEYS */;
/*!40000 ALTER TABLE `contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact_settings`
--

DROP TABLE IF EXISTS `contact_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact_settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `setting_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `setting_value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `setting_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `display_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `is_active` tinyint(1) DEFAULT NULL,
  `order_index` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `setting_key` (`setting_key`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_settings`
--

LOCK TABLES `contact_settings` WRITE;
/*!40000 ALTER TABLE `contact_settings` DISABLE KEYS */;
INSERT INTO `contact_settings` VALUES (1,'phone_main','028-3823-4567','phone','Số điện thoại chính','Hotline tư vấn và hỗ trợ',1,1,'2025-08-07 10:26:04','2025-08-07 10:26:04'),(2,'email_main','info@hoahuongduong.edu.vn','email','Email chính','Email liên hệ chính thức',1,2,'2025-08-07 10:26:04','2025-08-07 10:26:04'),(3,'facebook','https://facebook.com/truongmamnonhoahuongduong','url','Facebook','Trang Facebook chính thức của trường',1,3,'2025-08-07 10:26:04','2025-08-07 10:26:04'),(4,'zalo','https://zalo.me/0901234567','url','Zalo','Chat Zalo để tư vấn nhanh',1,4,'2025-08-07 10:26:04','2025-08-07 10:26:04'),(5,'youtube','https://youtube.com/@hoahuongduong','url','YouTube','Kênh YouTube với các hoạt động của trường',1,5,'2025-08-07 10:26:04','2025-08-07 10:26:04');
/*!40000 ALTER TABLE `contact_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `event_date` datetime NOT NULL,
  `location` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `featured_image` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (1,'Lễ Trung Thu 2024','Tổ chức đêm hội Trung Thu với nhiều hoạt động vui chơi, múa lân, thưởng thức bánh kẹo và đèn lồng cho các em học sinh.','2024-09-17 18:00:00','Sân trường Hoa Hướng Dương',NULL,1,'2025-08-03 12:41:43'),(2,'Ngày hội thể thao','Ngày hội thể thao năm 2024 với các môn thi đấu phù hợp lứa tuổi mầm non như chạy, nhảy bao bố, kéo co.','2024-10-25 08:00:00','Sân vận động trường',NULL,1,'2025-08-03 12:41:43'),(3,'Biểu diễn cuối năm','Chương trình biểu diễn văn nghệ cuối năm học với sự tham gia của tất cả các lớp, thể hiện những gì các em đã học được.','2024-12-20 19:00:00','Hội trường trường học',NULL,1,'2025-08-03 12:41:43');
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faq`
--

DROP TABLE IF EXISTS `faq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faq` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question` text NOT NULL,
  `answer` text NOT NULL,
  `order_index` int DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faq`
--

LOCK TABLES `faq` WRITE;
/*!40000 ALTER TABLE `faq` DISABLE KEYS */;
/*!40000 ALTER TABLE `faq` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gallery`
--

DROP TABLE IF EXISTS `gallery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gallery` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `image_path` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `category` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_featured` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gallery`
--

LOCK TABLES `gallery` WRITE;
/*!40000 ALTER TABLE `gallery` DISABLE KEYS */;
/*!40000 ALTER TABLE `gallery` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `history_event`
--

DROP TABLE IF EXISTS `history_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `history_event` (
  `id` int NOT NULL AUTO_INCREMENT,
  `year` varchar(10) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` text NOT NULL,
  `color` varchar(50) DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `order_index` int DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `history_event`
--

LOCK TABLES `history_event` WRITE;
/*!40000 ALTER TABLE `history_event` DISABLE KEYS */;
/*!40000 ALTER TABLE `history_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `history_section`
--

DROP TABLE IF EXISTS `history_section`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `history_section` (
  `id` int NOT NULL AUTO_INCREMENT,
  `main_title` varchar(200) DEFAULT NULL,
  `subtitle` text,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `history_section`
--

LOCK TABLES `history_section` WRITE;
/*!40000 ALTER TABLE `history_section` DISABLE KEYS */;
/*!40000 ALTER TABLE `history_section` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `intro_video`
--

DROP TABLE IF EXISTS `intro_video`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `intro_video` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` text,
  `video_url` varchar(500) NOT NULL,
  `thumbnail_image` varchar(200) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `order_index` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `intro_video`
--

LOCK TABLES `intro_video` WRITE;
/*!40000 ALTER TABLE `intro_video` DISABLE KEYS */;
INSERT INTO `intro_video` VALUES (2,'Giới thiệu','','<iframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed/dQw4w9WgXcQ?si=ZB4KLM3Fq5cnapYc\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share\" referrerpolicy=\"strict-origin-when-cross-origin\" allowfullscreen></iframe>','uploads/videos/11e2762c-2a39-42da-b75c-0fa30ebc7780_image_2025_03_11T11_36_06_322Z.png',1,1,'2025-08-09 03:57:33','2025-08-09 03:57:33');
/*!40000 ALTER TABLE `intro_video` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `location_settings`
--

DROP TABLE IF EXISTS `location_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `location_settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `address` text NOT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `google_maps_api_key` varchar(255) DEFAULT NULL,
  `map_zoom_level` int DEFAULT NULL,
  `map_style` varchar(50) DEFAULT NULL,
  `show_in_footer` tinyint(1) DEFAULT NULL,
  `map_height` varchar(20) DEFAULT NULL,
  `marker_title` varchar(200) DEFAULT NULL,
  `marker_info` text,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `google_maps_embed` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location_settings`
--

LOCK TABLES `location_settings` WRITE;
/*!40000 ALTER TABLE `location_settings` DISABLE KEYS */;
INSERT INTO `location_settings` VALUES (1,'123 Đường Hoa Hướng Dương, Quận 1, TP.HCM',11.7816,108.251,'None',15,'roadmap',1,'300px','Trường Mầm non Hoa Hướng Dương','Trường Mầm non Hoa Hướng Dương - Nuôi dưỡng tâm hồn, phát triển tài năng',1,'2025-08-08 23:34:28','2025-08-09 02:28:25','<iframe src=\"https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d3905.7648758091664!2d108.25073!3d11.7815988!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3171432684ca34b5%3A0x128c75a6d0607ad!2zVHLGsMahbmcgTeG6p20gTm9uIEhvYSBIxrDhu5tuZyBExrDGoW5n!5e0!3m2!1sen!2s!4v1754697967408!5m2!1sen!2s\" width=\"600\" height=\"450\" style=\"border:0;\" allowfullscreen=\"\" loading=\"lazy\" referrerpolicy=\"no-referrer-when-downgrade\"></iframe>');
/*!40000 ALTER TABLE `location_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mission_content`
--

DROP TABLE IF EXISTS `mission_content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mission_content` (
  `id` int NOT NULL AUTO_INCREMENT,
  `main_title` varchar(200) DEFAULT NULL,
  `main_image` varchar(255) DEFAULT NULL,
  `stats_number` varchar(10) DEFAULT NULL,
  `stats_text` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mission_content`
--

LOCK TABLES `mission_content` WRITE;
/*!40000 ALTER TABLE `mission_content` DISABLE KEYS */;
/*!40000 ALTER TABLE `mission_content` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mission_item`
--

DROP TABLE IF EXISTS `mission_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mission_item` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` text NOT NULL,
  `icon` varchar(100) DEFAULT NULL,
  `color` varchar(50) DEFAULT NULL,
  `order_index` int DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mission_item`
--

LOCK TABLES `mission_item` WRITE;
/*!40000 ALTER TABLE `mission_item` DISABLE KEYS */;
/*!40000 ALTER TABLE `mission_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news`
--

DROP TABLE IF EXISTS `news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `news` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `summary` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `featured_image` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_published` tinyint(1) DEFAULT '1',
  `publish_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news`
--

LOCK TABLES `news` WRITE;
/*!40000 ALTER TABLE `news` DISABLE KEYS */;
INSERT INTO `news` VALUES (1,'Khai giảng năm học mới 2024-2025','Trường Mầm non Hoa Hướng Dương xin thông báo lễ khai giảng năm học mới 2024-2025 sẽ được tổ chức vào ngày 05/09/2024. Chương trình gồm có các hoạt động như chào cờ, phát biểu của Ban Giám hiệu, giới thiệu đội ngũ giáo viên mới và các hoạt động vui chơi cho các em học sinh.','Thông báo về lễ khai giảng năm học mới 2024-2025 diễn ra vào ngày 05/09/2024','uploads/news/cf6e7bc9-7059-447d-b4ba-463d3e31100a_Screenshot_2023.11.29_06.49.43.584.png',1,'2025-08-03 12:41:43','2025-08-03 12:41:43'),(2,'Chương trình ngoại khóa tháng 10','Trong tháng 10, trường sẽ tổ chức nhiều hoạt động ngoại khóa bổ ích cho các em như: tham quan vườn bách thảo, học nấu ăn đơn giản, và các trò chơi tập thể. Các hoạt động này nhằm giúp trẻ phát triển toàn diện về thể chất lẫn tinh thần.','Các hoạt động ngoại khóa phong phú trong tháng 10 dành cho học sinh',NULL,1,'2025-08-03 12:41:43','2025-08-03 12:41:43'),(3,'Hội thảo nuôi dưỡng trẻ cho phụ huynh','Trường tổ chức hội thảo \"Nuôi dưỡng và giáo dục trẻ mầm non\" dành cho các bậc phụ huynh vào ngày 15/10/2024. Hội thảo do các chuyên gia tâm lý và dinh dưỡng trẻ em hàng đầu thực hiện, giúp cha mẹ hiểu rõ hơn về cách chăm sóc con trẻ ở độ tuổi mầm non.','Hội thảo bổ ích về nuôi dưỡng trẻ em dành cho phụ huynh',NULL,1,'2025-08-03 12:41:43','2025-08-03 12:41:43');
/*!40000 ALTER TABLE `news` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post`
--

DROP TABLE IF EXISTS `post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `excerpt` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `featured_image` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  `is_published` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
/*!40000 ALTER TABLE `post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program`
--

DROP TABLE IF EXISTS `program`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `program` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `age_group` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `featured_image` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `price` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `duration` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_featured` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program`
--

LOCK TABLES `program` WRITE;
/*!40000 ALTER TABLE `program` DISABLE KEYS */;
INSERT INTO `program` VALUES (1,'Lớp Mầm (18-24 tháng)','Chương trình giáo dục cho trẻ 18-24 tháng tuổi, tập trung phát triển kỹ năng vận động thô, tinh và ngôn ngữ cơ bản.','18-24 tháng',NULL,'2,500,000 VNĐ/tháng','Cả năm học',1,'2025-08-03 12:41:43',1),(2,'Lớp Chồi (2-3 tuổi)','Chương trình giáo dục toàn diện cho trẻ 2-3 tuổi với các hoạt động vui chơi, học tập và phát triển tính cách.','2-3 tuổi',NULL,'2,800,000 VNĐ/tháng','Cả năm học',1,'2025-08-03 12:41:43',1),(3,'Lớp Lá (3-4 tuổi)','Chuẩn bị cho trẻ 3-4 tuổi với các kỹ năng cần thiết trước khi vào mẫu giáo lớn.','3-4 tuổi',NULL,'3,000,000 VNĐ/tháng','Cả năm học',1,'2025-08-03 12:41:43',1),(4,'Lớp Lúa (4-5 tuổi)','Chương trình chuẩn bị vào lớp 1 cho trẻ 4-5 tuổi với các hoạt động học tập có hệ thống.','4-5 tuổi',NULL,'3,200,000 VNĐ/tháng','Cả năm học',1,'2025-08-03 12:41:43',1),(5,'Lớp Ngoại ngữ','Lớp học tiếng Anh cho trẻ em từ 3-5 tuổi với phương pháp giảng dạy sinh động, phù hợp lứa tuổi.','18-24 tháng',NULL,'1,500,000 VNĐ/tháng','3 buổi/tuần',1,'2025-08-03 12:41:43',1),(6,'Lớp Năng khiếu','Các lớp học năng khiếu như vẽ, múa, hát, đàn piano giúp phát triển tài năng của trẻ.','3-5 tuổi',NULL,'1,000,000 VNĐ/tháng','2 buổi/tuần',1,'2025-08-03 12:41:43',0),(7,'Lớp Chồi Non','Tuyệt vời nhưng siêu đắt','Đa tuổi','uploads/programs/25185b08-c16a-4374-b328-9a22e3082848_loi-thoi.jpg','1.000.000.000','Cả năm học',1,'2025-08-07 02:46:12',1);
/*!40000 ALTER TABLE `program` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seo_settings`
--

DROP TABLE IF EXISTS `seo_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seo_settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `page_type` varchar(50) NOT NULL,
  `page_id` int DEFAULT NULL,
  `meta_title` varchar(255) DEFAULT NULL,
  `meta_description` text,
  `meta_keywords` text,
  `og_title` varchar(255) DEFAULT NULL,
  `og_description` text,
  `og_image` varchar(255) DEFAULT NULL,
  `canonical_url` varchar(500) DEFAULT NULL,
  `robots_meta` varchar(100) DEFAULT NULL,
  `schema_markup` text,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seo_settings`
--

LOCK TABLES `seo_settings` WRITE;
/*!40000 ALTER TABLE `seo_settings` DISABLE KEYS */;
/*!40000 ALTER TABLE `seo_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `setting_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `setting_value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `setting_key` (`setting_key`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settings`
--

LOCK TABLES `settings` WRITE;
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;
INSERT INTO `settings` VALUES (1,'school_name','Trường Mầm non Hoa Hướng Dương','Tên trường','2025-08-03 12:41:43'),(2,'school_address','123 Đường Hoa Hướng Dương, Quận 1, TP.HCM','Địa chỉ trường','2025-08-03 12:41:43'),(3,'school_phone','028-3823-4567','Số điện thoại liên hệ','2025-08-03 12:41:43'),(4,'school_email','info@hoahuongduong.edu.vn','Email liên hệ','2025-08-03 12:41:43'),(5,'school_hours','Thứ 2 - Thứ 6: 7:00 - 17:00','Giờ làm việc','2025-08-03 12:41:43'),(6,'facebook_url','https://facebook.com/hoahuongduong','Trang Facebook','2025-08-03 12:41:43'),(7,'youtube_url','https://youtube.com/hoahuongduong','Kênh YouTube','2025-08-03 12:41:43'),(8,'school_motto','Nuôi dưỡng tâm hồn - Phát triển tài năng','Phương châm giáo dục','2025-08-03 12:41:43');
/*!40000 ALTER TABLE `settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `slider`
--

DROP TABLE IF EXISTS `slider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `slider` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `image_path` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `order_index` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `slider`
--

LOCK TABLES `slider` WRITE;
/*!40000 ALTER TABLE `slider` DISABLE KEYS */;
/*!40000 ALTER TABLE `slider` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `special_program`
--

DROP TABLE IF EXISTS `special_program`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `special_program` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` text NOT NULL,
  `icon_class` varchar(100) DEFAULT NULL,
  `background_gradient` varchar(100) DEFAULT NULL,
  `border_color` varchar(50) DEFAULT NULL,
  `icon_bg_color` varchar(50) DEFAULT NULL,
  `features` text,
  `image_path` varchar(255) DEFAULT NULL,
  `order_index` int DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `special_program`
--

LOCK TABLES `special_program` WRITE;
/*!40000 ALTER TABLE `special_program` DISABLE KEYS */;
/*!40000 ALTER TABLE `special_program` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team_member`
--

DROP TABLE IF EXISTS `team_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `team_member` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `position` varchar(200) NOT NULL,
  `description` text,
  `image_path` varchar(255) DEFAULT NULL,
  `order_index` int DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team_member`
--

LOCK TABLES `team_member` WRITE;
/*!40000 ALTER TABLE `team_member` DISABLE KEYS */;
/*!40000 ALTER TABLE `team_member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','admin@hoahuongduong.edu.vn','pbkdf2:sha256:600000$5nMCcRBXZ0XCR3pC$1f57c050daa7028f8971473db2f78818d0ea49ef92be64786b520a757ed6d58f','2025-08-03 12:44:36');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'hoa_huong_duong'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-09 11:35:45
