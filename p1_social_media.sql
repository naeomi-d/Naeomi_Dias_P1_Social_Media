-- MySQL dump 10.13  Distrib 9.5.0, for macos15 (arm64)
--
-- Host: localhost    Database: p1_social_media
-- ------------------------------------------------------
-- Server version	9.6.0

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '5071b94e-4319-11f1-be12-bdf8a658c2c5:1-575';

--
-- Table structure for table `admin_audit_logs`
--

DROP TABLE IF EXISTS `admin_audit_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin_audit_logs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `admin_id` bigint NOT NULL,
  `action` varchar(50) NOT NULL,
  `entity_type` varchar(30) NOT NULL,
  `entity_id` bigint NOT NULL,
  `details` text,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_audit_admin_created` (`admin_id`,`created_at`),
  KEY `idx_audit_entity` (`entity_type`,`entity_id`),
  CONSTRAINT `admin_audit_logs_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_audit_logs`
--

LOCK TABLES `admin_audit_logs` WRITE;
/*!40000 ALTER TABLE `admin_audit_logs` DISABLE KEYS */;
INSERT INTO `admin_audit_logs` VALUES (1,3,'REVIEW_REPORT','REPORT',1,'Seed audit log for P1 API testing.','2026-08-20 15:45:55'),(2,6,'UPDATE_USER','USER',2,'Audit log entry #2','2026-08-21 16:55:06'),(3,3,'DELETE_POST','POST',3,'Audit log entry #3','2026-08-21 16:55:06'),(4,6,'BAN_USER','USER',4,'Audit log entry #4','2026-08-21 16:55:06'),(5,3,'REVIEW_REPORT','REPORT',5,'Audit log entry #5','2026-08-21 16:55:06'),(6,6,'UPDATE_USER','USER',6,'Audit log entry #6','2026-08-21 16:55:06'),(7,3,'DELETE_POST','POST',7,'Audit log entry #7','2026-08-21 16:55:06'),(8,6,'BAN_USER','USER',8,'Audit log entry #8','2026-08-21 16:55:06'),(9,3,'REVIEW_REPORT','REPORT',9,'Audit log entry #9','2026-08-21 16:55:06'),(10,6,'UPDATE_USER','USER',10,'Audit log entry #10','2026-08-21 16:55:06'),(11,3,'DELETE_POST','POST',1,'Audit log entry #11','2026-08-21 16:55:06'),(12,6,'BAN_USER','USER',2,'Audit log entry #12','2026-08-21 16:55:06'),(13,3,'REVIEW_REPORT','REPORT',3,'Audit log entry #13','2026-08-21 16:55:06'),(14,6,'UPDATE_USER','USER',4,'Audit log entry #14','2026-08-21 16:55:06'),(15,3,'DELETE_POST','POST',5,'Audit log entry #15','2026-08-21 16:55:06'),(16,6,'BAN_USER','USER',6,'Audit log entry #16','2026-08-21 16:55:06'),(17,3,'REVIEW_REPORT','REPORT',7,'Audit log entry #17','2026-08-21 16:55:06'),(18,6,'UPDATE_USER','USER',8,'Audit log entry #18','2026-08-21 16:55:06'),(19,3,'DELETE_POST','POST',9,'Audit log entry #19','2026-08-21 16:55:06'),(20,6,'BAN_USER','USER',10,'Audit log entry #20','2026-08-21 16:55:06'),(21,6,'REVIEW_REPORT','REPORT',29,'Report status set to REVIEWED.','2026-08-22 09:38:40'),(22,6,'REVIEW_REPORT','REPORT',26,'Report status set to REVIEWED.','2026-08-22 09:38:43'),(23,6,'DISMISS_REPORT','REPORT',5,'Report dismissed by moderator.','2026-08-23 05:56:11'),(24,6,'REMOVE_REPORTED_POST','POST',22,'Post removed after report #17.','2026-08-23 05:56:22'),(25,6,'REMOVE_REPORTED_POST','POST',25,'Post removed after report #20.','2026-08-23 05:56:32'),(26,6,'REMOVE_REPORTED_POST','POST',7,'Post removed after report #32.','2026-08-23 06:57:57'),(27,6,'REMOVE_REPORTED_POST','POST',13,'Post removed after report #8.','2026-08-23 06:59:09'),(28,6,'REMOVE_REPORTED_POST','POST',28,'Post removed after report #23.','2026-08-23 08:17:50'),(29,6,'REMOVE_REPORTED_POST','POST',19,'Post removed after report #14.','2026-08-23 08:21:20'),(30,6,'REMOVE_REPORTED_POST','POST',5,'Post removed after report #1.','2026-08-23 08:25:57'),(31,6,'REMOVE_REPORTED_POST','POST',16,'Post removed after report #11.','2026-08-23 08:26:08'),(32,6,'REMOVE_REPORTED_POST','POST',2,'Post removed after report #34. Resolved 1 pending report(s).','2026-08-23 08:49:29'),(33,3,'DEACTIVATE_USER','USER',13,'User @p1_user4 was deactivated.','2026-08-23 14:07:31'),(34,3,'DEACTIVATE_USER','USER',33,'User @p1_user24 was deactivated.','2026-08-23 14:09:24'),(35,3,'ACTIVATE_USER','USER',33,'User @p1_user24 was activated.','2026-08-23 14:34:21'),(36,36,'REVIEW_REPORT','REPORT',1,'Moderator reviewed a report concerning suspicious account information.','2026-08-23 14:52:47'),(37,37,'DISMISS_REPORT','REPORT',4,'Report dismissed because the reported content did not violate community guidelines.','2026-08-23 14:52:47'),(38,34,'UPDATE_USER','USER',38,'Administrator updated user account information.','2026-08-23 14:52:47'),(39,35,'UPDATE_USER','USER',39,'Administrator reviewed and updated user account.','2026-08-23 14:52:47'),(40,36,'REMOVE_REPORTED_POST','POST',57,'Post removed after report #41. Resolved 1 pending report(s).','2026-08-23 17:51:17'),(41,34,'REVIEW_REPORT','REPORT',38,'Report status set to REVIEWED.','2026-08-23 17:55:58'),(42,36,'REMOVE_REPORTED_POST','POST',54,'Post removed after report #43. Resolved 2 pending report(s).','2026-08-24 06:49:13');
/*!40000 ALTER TABLE `admin_audit_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookmarks`
--

DROP TABLE IF EXISTS `bookmarks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookmarks` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `post_id` bigint NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_bookmarks_user_post` (`user_id`,`post_id`),
  KEY `post_id` (`post_id`),
  KEY `idx_bookmarks_user` (`user_id`),
  CONSTRAINT `bookmarks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `bookmarks_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookmarks`
--

LOCK TABLES `bookmarks` WRITE;
/*!40000 ALTER TABLE `bookmarks` DISABLE KEYS */;
INSERT INTO `bookmarks` VALUES (2,1,2,'2026-08-20 03:44:20'),(3,1,3,'2026-08-20 03:44:51'),(4,4,5,'2026-08-20 15:45:55'),(5,8,7,'2026-08-21 16:55:06'),(6,9,8,'2026-08-21 16:55:06'),(7,4,9,'2026-08-21 16:55:06'),(8,5,10,'2026-08-21 16:55:06'),(9,10,11,'2026-08-21 16:55:06'),(10,11,12,'2026-08-21 16:55:06'),(11,12,13,'2026-08-21 16:55:06'),(12,13,14,'2026-08-21 16:55:06'),(13,14,15,'2026-08-21 16:55:06'),(14,15,16,'2026-08-21 16:55:06'),(15,16,17,'2026-08-21 16:55:06'),(16,17,18,'2026-08-21 16:55:06'),(17,18,19,'2026-08-21 16:55:06'),(18,19,20,'2026-08-21 16:55:06'),(19,20,21,'2026-08-21 16:55:06'),(20,21,22,'2026-08-21 16:55:06'),(21,22,23,'2026-08-21 16:55:06'),(22,23,24,'2026-08-21 16:55:06'),(23,24,25,'2026-08-21 16:55:06'),(24,25,26,'2026-08-21 16:55:06'),(25,26,27,'2026-08-21 16:55:06'),(26,27,28,'2026-08-21 16:55:06'),(27,28,29,'2026-08-21 16:55:06'),(28,29,30,'2026-08-21 16:55:06'),(29,30,31,'2026-08-21 16:55:06'),(30,31,32,'2026-08-21 16:55:06'),(31,32,33,'2026-08-21 16:55:06'),(32,33,34,'2026-08-21 16:55:06'),(33,3,35,'2026-08-21 16:55:06'),(34,7,36,'2026-08-21 16:55:06'),(35,1,9,'2026-08-22 09:26:43'),(36,4,19,'2026-08-22 15:13:06'),(37,38,40,'2026-08-23 14:52:47'),(38,40,41,'2026-08-23 14:52:47'),(39,41,42,'2026-08-23 14:52:47'),(40,42,43,'2026-08-23 14:52:47'),(41,43,44,'2026-08-23 14:52:47'),(42,44,45,'2026-08-23 14:52:47'),(43,46,47,'2026-08-23 14:52:47'),(44,48,49,'2026-08-23 14:52:47'),(45,51,52,'2026-08-23 14:52:47'),(47,40,56,'2026-08-24 06:46:07');
/*!40000 ALTER TABLE `bookmarks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `post_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_comments_user_id` (`user_id`),
  KEY `ix_comments_post_id` (`post_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE,
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (1,2,1,'Amazing','2026-08-19 16:28:26','2026-08-19 16:28:45','2026-08-19 16:28:45'),(2,2,1,'Very nice','2026-08-19 16:28:43','2026-08-19 16:28:43',NULL),(3,3,2,'Great','2026-08-20 09:47:57','2026-08-20 09:47:57',NULL),(4,5,4,'This is looking great!','2026-08-20 15:45:55','2026-08-20 15:45:55',NULL),(5,4,5,'Flask is really useful for API development.','2026-08-20 15:45:55','2026-08-20 15:45:55',NULL),(6,7,6,'This is looking great!','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(7,8,8,'Flask is really useful for API development.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(8,9,9,'Excellent architectural design!','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(9,10,4,'Great post, thanks for sharing.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(10,11,5,'Very informative article.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(11,12,10,'Subscribed for future updates!','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(12,13,11,'SQLAlchemy ORM makes queries so clean.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(13,14,12,'JWT claims handling is spot on.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(14,15,13,'Looking forward to the next update.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(15,16,14,'Solid implementation strategy.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(16,17,15,'This is looking great!','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(17,18,16,'Flask is really useful for API development.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(18,19,17,'Excellent architectural design!','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(19,20,18,'Great post, thanks for sharing.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(20,21,19,'Very informative article.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(21,22,20,'Subscribed for future updates!','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(22,23,21,'SQLAlchemy ORM makes queries so clean.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(23,24,22,'JWT claims handling is spot on.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(24,25,23,'Looking forward to the next update.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(25,26,24,'Solid implementation strategy.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(26,27,25,'This is looking great!','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(27,28,26,'Flask is really useful for API development.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(28,29,27,'Excellent architectural design!','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(29,30,28,'Great post, thanks for sharing.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(30,31,29,'Very informative article.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(31,32,30,'Subscribed for future updates!','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(32,33,31,'SQLAlchemy ORM makes queries so clean.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(33,34,32,'JWT claims handling is spot on.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(34,35,33,'Looking forward to the next update.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(35,36,3,'Solid implementation strategy.','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(36,40,38,'The SQLAlchemy relationships were one of the trickier parts for me too.','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(37,39,40,'Agreed. Flask makes it really easy to experiment with architecture.','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(38,43,41,'Absolutely. Testing early saves so much time.','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(39,45,43,'Security is definitely something I want to understand better.','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(40,53,46,'Consistency is probably the hardest part!','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(41,52,48,'Database optimization is surprisingly interesting.','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(42,41,45,'Layered architecture makes larger projects much easier to navigate.','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(43,50,47,'Keeping the workflow simple definitely helps.','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL);
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `follows`
--

DROP TABLE IF EXISTS `follows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `follows` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `follower_id` bigint NOT NULL,
  `following_id` bigint NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_follows_pair` (`follower_id`,`following_id`),
  KEY `idx_follows_following` (`following_id`),
  KEY `idx_follows_follower` (`follower_id`),
  CONSTRAINT `follows_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `follows_ibfk_2` FOREIGN KEY (`following_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `follows`
--

LOCK TABLES `follows` WRITE;
/*!40000 ALTER TABLE `follows` DISABLE KEYS */;
INSERT INTO `follows` VALUES (3,1,2,'2026-08-20 09:49:39'),(4,4,5,'2026-08-20 15:45:55'),(5,5,4,'2026-08-20 15:45:55'),(6,3,7,'2026-08-21 16:55:06'),(7,3,6,'2026-08-21 16:55:06'),(8,7,6,'2026-08-21 16:55:06'),(9,7,8,'2026-08-21 16:55:06'),(10,6,8,'2026-08-21 16:55:06'),(11,6,9,'2026-08-21 16:55:06'),(12,8,9,'2026-08-21 16:55:06'),(13,8,4,'2026-08-21 16:55:06'),(14,9,4,'2026-08-21 16:55:06'),(15,9,5,'2026-08-21 16:55:06'),(17,5,10,'2026-08-21 16:55:06'),(18,5,11,'2026-08-21 16:55:06'),(19,10,11,'2026-08-21 16:55:06'),(20,10,12,'2026-08-21 16:55:06'),(21,11,12,'2026-08-21 16:55:06'),(22,11,13,'2026-08-21 16:55:06'),(23,12,13,'2026-08-21 16:55:06'),(24,12,14,'2026-08-21 16:55:06'),(25,13,14,'2026-08-21 16:55:06'),(26,13,15,'2026-08-21 16:55:06'),(27,14,15,'2026-08-21 16:55:06'),(28,14,16,'2026-08-21 16:55:06'),(29,15,16,'2026-08-21 16:55:06'),(30,15,17,'2026-08-21 16:55:06'),(31,16,17,'2026-08-21 16:55:06'),(32,16,18,'2026-08-21 16:55:06'),(33,17,18,'2026-08-21 16:55:06'),(34,17,19,'2026-08-21 16:55:06'),(35,18,19,'2026-08-21 16:55:06'),(36,18,20,'2026-08-21 16:55:06'),(37,19,20,'2026-08-21 16:55:06'),(38,19,21,'2026-08-21 16:55:06'),(39,20,21,'2026-08-21 16:55:06'),(40,20,22,'2026-08-21 16:55:06'),(41,21,22,'2026-08-21 16:55:06'),(42,21,23,'2026-08-21 16:55:06'),(43,22,23,'2026-08-21 16:55:06'),(44,22,24,'2026-08-21 16:55:06'),(45,23,24,'2026-08-21 16:55:06'),(46,23,25,'2026-08-21 16:55:06'),(47,24,25,'2026-08-21 16:55:06'),(48,24,26,'2026-08-21 16:55:06'),(49,25,26,'2026-08-21 16:55:06'),(50,25,27,'2026-08-21 16:55:06'),(51,26,27,'2026-08-21 16:55:06'),(52,26,28,'2026-08-21 16:55:06'),(53,27,28,'2026-08-21 16:55:06'),(54,27,29,'2026-08-21 16:55:06'),(55,28,29,'2026-08-21 16:55:06'),(56,28,30,'2026-08-21 16:55:06'),(57,29,30,'2026-08-21 16:55:06'),(58,29,31,'2026-08-21 16:55:06'),(59,30,31,'2026-08-21 16:55:06'),(60,30,32,'2026-08-21 16:55:06'),(61,31,32,'2026-08-21 16:55:06'),(62,31,33,'2026-08-21 16:55:06'),(63,32,33,'2026-08-21 16:55:06'),(64,32,3,'2026-08-21 16:55:06'),(65,33,3,'2026-08-21 16:55:06'),(66,33,7,'2026-08-21 16:55:06'),(67,1,30,'2026-08-22 09:16:45'),(68,1,33,'2026-08-22 09:19:19'),(69,1,32,'2026-08-22 09:19:22'),(70,4,31,'2026-08-22 15:08:12'),(71,4,9,'2026-08-22 15:08:28'),(72,4,1,'2026-08-22 15:30:59'),(73,38,39,'2026-08-23 14:52:47'),(74,38,40,'2026-08-23 14:52:47'),(76,39,38,'2026-08-23 14:52:47'),(77,39,41,'2026-08-23 14:52:47'),(78,40,38,'2026-08-23 14:52:47'),(79,40,46,'2026-08-23 14:52:47'),(80,41,43,'2026-08-23 14:52:47'),(81,42,44,'2026-08-23 14:52:47'),(82,42,52,'2026-08-23 14:52:47'),(83,43,45,'2026-08-23 14:52:47'),(84,44,38,'2026-08-23 14:52:47'),(85,45,47,'2026-08-23 14:52:47'),(86,46,48,'2026-08-23 14:52:47'),(87,48,51,'2026-08-23 14:52:47'),(88,51,49,'2026-08-23 14:52:47'),(89,52,50,'2026-08-23 14:52:47'),(90,50,52,'2026-08-23 14:52:47'),(92,38,41,'2026-08-24 08:45:09'),(93,38,2,'2026-08-25 13:01:09');
/*!40000 ALTER TABLE `follows` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hashtags`
--

DROP TABLE IF EXISTS `hashtags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hashtags` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hashtags`
--

LOCK TABLES `hashtags` WRITE;
/*!40000 ALTER TABLE `hashtags` DISABLE KEYS */;
INSERT INTO `hashtags` VALUES (1,'flask','2026-08-20 01:55:02'),(2,'python','2026-08-20 01:55:02'),(4,'sqlalchemy','2026-08-20 01:58:14'),(5,'socialmedia','2026-08-20 15:45:55'),(6,'backend','2026-08-21 16:55:05'),(7,'api','2026-08-21 16:55:05'),(8,'webdev','2026-08-21 16:55:05'),(9,'developer','2026-08-21 16:55:05'),(10,'code','2026-08-21 16:55:05'),(11,'tech','2026-08-21 16:55:05'),(12,'database','2026-08-21 16:55:05'),(13,'mysql','2026-08-21 16:55:05'),(14,'jwt','2026-08-21 16:55:05'),(15,'security','2026-08-21 16:55:05'),(16,'pytest','2026-08-21 16:55:05'),(17,'testing','2026-08-21 16:55:05'),(18,'rest','2026-08-21 16:55:05'),(19,'architecture','2026-08-21 16:55:05'),(20,'design','2026-08-21 16:55:05'),(21,'software','2026-08-21 16:55:05'),(22,'engineering','2026-08-21 16:55:05'),(23,'computing','2026-08-21 16:55:05'),(24,'data','2026-08-21 16:55:05'),(25,'frontend','2026-08-21 16:55:05'),(26,'fullstack','2026-08-21 16:55:05'),(27,'opensource','2026-08-21 16:55:05'),(28,'git','2026-08-21 16:55:05'),(29,'docker','2026-08-21 16:55:05'),(30,'cloud','2026-08-21 16:55:05'),(31,'learning','2026-08-21 16:55:05'),(32,'webdevelopment','2026-08-23 14:52:47'),(33,'programming','2026-08-23 14:52:47'),(34,'technology','2026-08-23 14:52:47'),(35,'databases','2026-08-23 14:52:47'),(36,'career','2026-08-23 14:52:47'),(37,'softwareengineering','2026-08-23 14:52:47'),(38,'productivity','2026-08-23 14:52:47');
/*!40000 ALTER TABLE `hashtags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `likes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `post_id` bigint NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_likes_user_post` (`user_id`,`post_id`),
  KEY `idx_likes_post` (`post_id`),
  KEY `idx_likes_user` (`user_id`),
  CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
INSERT INTO `likes` VALUES (6,1,2,'2026-08-19 16:22:32'),(8,2,3,'2026-08-20 09:42:52'),(9,2,2,'2026-08-20 09:43:34'),(10,4,5,'2026-08-20 15:45:55'),(11,5,4,'2026-08-20 15:45:55'),(12,3,8,'2026-08-21 16:55:05'),(13,7,9,'2026-08-21 16:55:05'),(14,6,10,'2026-08-21 16:55:05'),(15,8,11,'2026-08-21 16:55:05'),(16,9,12,'2026-08-21 16:55:05'),(17,4,13,'2026-08-21 16:55:05'),(18,5,14,'2026-08-21 16:55:05'),(19,10,15,'2026-08-21 16:55:05'),(20,11,16,'2026-08-21 16:55:05'),(21,12,17,'2026-08-21 16:55:05'),(22,13,18,'2026-08-21 16:55:05'),(23,14,19,'2026-08-21 16:55:05'),(24,15,20,'2026-08-21 16:55:05'),(25,16,21,'2026-08-21 16:55:05'),(26,17,22,'2026-08-21 16:55:05'),(27,18,23,'2026-08-21 16:55:05'),(28,19,24,'2026-08-21 16:55:05'),(29,20,25,'2026-08-21 16:55:05'),(30,21,26,'2026-08-21 16:55:05'),(31,22,27,'2026-08-21 16:55:05'),(32,23,28,'2026-08-21 16:55:06'),(33,24,29,'2026-08-21 16:55:06'),(34,25,30,'2026-08-21 16:55:06'),(35,26,31,'2026-08-21 16:55:06'),(36,27,32,'2026-08-21 16:55:06'),(37,28,33,'2026-08-21 16:55:06'),(38,29,34,'2026-08-21 16:55:06'),(39,30,35,'2026-08-21 16:55:06'),(40,31,36,'2026-08-21 16:55:06'),(41,32,7,'2026-08-21 16:55:06'),(42,4,12,'2026-08-22 15:12:40'),(43,4,38,'2026-08-23 14:44:06'),(44,38,39,'2026-08-23 14:52:47'),(45,40,39,'2026-08-23 14:52:47'),(46,41,39,'2026-08-23 14:52:47'),(47,42,39,'2026-08-23 14:52:47'),(48,38,40,'2026-08-23 14:52:47'),(49,46,40,'2026-08-23 14:52:47'),(50,43,40,'2026-08-23 14:52:47'),(51,39,41,'2026-08-23 14:52:47'),(52,38,41,'2026-08-23 14:52:47'),(53,45,41,'2026-08-23 14:52:47'),(54,41,42,'2026-08-23 14:52:47'),(55,48,42,'2026-08-23 14:52:47'),(56,44,43,'2026-08-23 14:52:47'),(57,52,43,'2026-08-23 14:52:47'),(58,49,44,'2026-08-23 14:52:47'),(59,51,44,'2026-08-23 14:52:47'),(60,40,56,'2026-08-24 06:46:16'),(61,38,42,'2026-08-24 08:45:24');
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `recipient_id` bigint NOT NULL,
  `actor_id` bigint NOT NULL,
  `type` varchar(30) NOT NULL,
  `post_id` bigint DEFAULT NULL,
  `comment_id` bigint DEFAULT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `actor_id` (`actor_id`),
  KEY `post_id` (`post_id`),
  KEY `comment_id` (`comment_id`),
  KEY `idx_notifications_recipient` (`recipient_id`,`is_read`,`created_at`),
  KEY `ix_notifications_recipient_id` (`recipient_id`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`recipient_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `notifications_ibfk_2` FOREIGN KEY (`actor_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `notifications_ibfk_3` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE,
  CONSTRAINT `notifications_ibfk_4` FOREIGN KEY (`comment_id`) REFERENCES `comments` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (2,1,2,'LIKE',2,NULL,1,'2026-08-20 09:43:34'),(3,1,2,'COMMENT',3,3,1,'2026-08-20 09:47:57'),(4,2,1,'FOLLOW',NULL,NULL,1,'2026-08-20 09:49:39'),(5,5,4,'LIKE',5,NULL,0,'2026-08-20 15:45:55'),(6,5,4,'COMMENT',5,4,0,'2026-08-20 15:45:55'),(7,5,4,'FOLLOW',NULL,NULL,0,'2026-08-20 15:45:55'),(8,4,5,'LIKE',4,NULL,1,'2026-08-20 15:45:55'),(9,3,7,'LIKE',7,NULL,1,'2026-08-21 16:55:06'),(10,7,6,'COMMENT',8,7,0,'2026-08-21 16:55:06'),(11,6,8,'FOLLOW',NULL,NULL,0,'2026-08-21 16:55:06'),(12,8,9,'REPORT',NULL,NULL,0,'2026-08-21 16:55:06'),(13,9,4,'LIKE',11,NULL,0,'2026-08-21 16:55:06'),(14,4,5,'COMMENT',12,11,1,'2026-08-21 16:55:06'),(15,5,10,'FOLLOW',NULL,NULL,0,'2026-08-21 16:55:06'),(16,10,11,'REPORT',NULL,NULL,0,'2026-08-21 16:55:06'),(17,11,12,'LIKE',15,NULL,0,'2026-08-21 16:55:06'),(18,12,13,'COMMENT',16,15,0,'2026-08-21 16:55:06'),(19,13,14,'FOLLOW',NULL,NULL,0,'2026-08-21 16:55:06'),(20,14,15,'REPORT',NULL,NULL,0,'2026-08-21 16:55:06'),(21,15,16,'LIKE',19,NULL,0,'2026-08-21 16:55:06'),(22,16,17,'COMMENT',20,19,0,'2026-08-21 16:55:06'),(23,17,18,'FOLLOW',NULL,NULL,0,'2026-08-21 16:55:06'),(24,18,19,'REPORT',NULL,NULL,0,'2026-08-21 16:55:06'),(25,19,20,'LIKE',23,NULL,0,'2026-08-21 16:55:06'),(26,20,21,'COMMENT',24,23,0,'2026-08-21 16:55:06'),(27,21,22,'FOLLOW',NULL,NULL,0,'2026-08-21 16:55:06'),(28,22,23,'REPORT',NULL,NULL,0,'2026-08-21 16:55:06'),(29,23,24,'LIKE',27,NULL,0,'2026-08-21 16:55:06'),(30,24,25,'COMMENT',28,27,0,'2026-08-21 16:55:06'),(31,25,26,'FOLLOW',NULL,NULL,0,'2026-08-21 16:55:06'),(32,26,27,'REPORT',NULL,NULL,0,'2026-08-21 16:55:06'),(33,27,28,'LIKE',31,NULL,0,'2026-08-21 16:55:06'),(34,28,29,'COMMENT',32,31,0,'2026-08-21 16:55:06'),(35,29,30,'FOLLOW',NULL,NULL,0,'2026-08-21 16:55:06'),(36,30,31,'REPORT',NULL,NULL,0,'2026-08-21 16:55:06'),(37,31,32,'LIKE',35,NULL,0,'2026-08-21 16:55:06'),(38,32,33,'COMMENT',36,35,0,'2026-08-21 16:55:06'),(39,30,1,'FOLLOW',NULL,NULL,0,'2026-08-22 09:16:45'),(40,33,1,'FOLLOW',NULL,NULL,0,'2026-08-22 09:19:19'),(41,32,1,'FOLLOW',NULL,NULL,0,'2026-08-22 09:19:22'),(42,31,4,'FOLLOW',NULL,NULL,0,'2026-08-22 15:08:12'),(43,9,4,'FOLLOW',NULL,NULL,0,'2026-08-22 15:08:28'),(44,1,4,'FOLLOW',NULL,NULL,0,'2026-08-22 15:30:59'),(45,38,39,'FOLLOW',NULL,NULL,0,'2026-08-23 14:52:47'),(46,38,40,'LIKE',39,NULL,0,'2026-08-23 14:52:47'),(47,39,38,'COMMENT',40,NULL,0,'2026-08-23 14:52:47'),(48,40,41,'LIKE',41,NULL,0,'2026-08-23 14:52:47'),(49,42,44,'FOLLOW',NULL,NULL,0,'2026-08-23 14:52:47'),(50,46,48,'COMMENT',49,NULL,0,'2026-08-23 14:52:47'),(51,47,40,'LIKE',56,NULL,0,'2026-08-24 06:46:16'),(52,2,38,'FOLLOW',NULL,NULL,0,'2026-08-24 08:43:33'),(53,41,38,'FOLLOW',NULL,NULL,0,'2026-08-24 08:45:09'),(54,41,38,'LIKE',42,NULL,0,'2026-08-24 08:45:24'),(55,2,38,'FOLLOW',NULL,NULL,0,'2026-08-25 13:01:09');
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_hashtags`
--

DROP TABLE IF EXISTS `post_hashtags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post_hashtags` (
  `post_id` bigint NOT NULL,
  `hashtag_id` bigint NOT NULL,
  PRIMARY KEY (`post_id`,`hashtag_id`),
  KEY `hashtag_id` (`hashtag_id`),
  CONSTRAINT `post_hashtags_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE,
  CONSTRAINT `post_hashtags_ibfk_2` FOREIGN KEY (`hashtag_id`) REFERENCES `hashtags` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_hashtags`
--

LOCK TABLES `post_hashtags` WRITE;
/*!40000 ALTER TABLE `post_hashtags` DISABLE KEYS */;
INSERT INTO `post_hashtags` VALUES (4,1),(5,1),(7,1),(8,1),(39,1),(4,2),(7,2),(36,2),(39,2),(47,2),(3,4),(9,4),(10,4),(40,4),(49,4),(54,4),(5,5),(8,5),(9,5),(10,6),(11,6),(11,7),(12,7),(12,8),(13,8),(13,9),(14,9),(14,10),(15,10),(15,11),(16,11),(16,12),(17,12),(17,13),(18,13),(18,14),(19,14),(19,15),(20,15),(20,16),(21,16),(21,17),(22,17),(22,18),(23,18),(23,19),(24,19),(24,20),(25,20),(25,21),(26,21),(26,22),(27,22),(27,23),(28,23),(28,24),(29,24),(29,25),(30,25),(30,26),(31,26),(31,27),(32,27),(46,27),(55,27),(32,28),(33,28),(33,29),(34,29),(34,30),(35,30),(35,31),(36,31),(45,31),(47,31),(41,32),(44,32),(52,32),(57,32),(42,33),(46,33),(55,33),(44,34),(52,34),(57,34),(40,35),(49,35),(54,35),(41,37),(42,38),(45,38);
/*!40000 ALTER TABLE `post_hashtags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS `posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `posts` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `content` text,
  `image_path` varchar(500) DEFAULT NULL,
  `visibility` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_posts_user_id` (`user_id`),
  CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `posts`
--

LOCK TABLES `posts` WRITE;
/*!40000 ALTER TABLE `posts` DISABLE KEYS */;
INSERT INTO `posts` VALUES (1,1,'Hello P1',NULL,'PUBLIC','DELETED','2026-08-19 15:08:27','2026-08-19 15:17:49','2026-08-19 15:17:49'),(2,1,'Test post',NULL,'PUBLIC','DELETED','2026-08-19 16:21:00','2026-08-23 08:49:29','2026-08-23 08:49:29'),(3,1,'Learning #SQLAlchemy',NULL,'PUBLIC','ACTIVE','2026-08-20 01:55:02','2026-08-20 01:58:14',NULL),(4,4,'Learning Flask and building my P1 social media project!',NULL,'PUBLIC','ACTIVE','2026-08-20 15:45:55','2026-08-20 15:45:55',NULL),(5,5,'Building production-ready APIs with Flask and JWT.',NULL,'PUBLIC','DELETED','2026-08-20 15:45:55','2026-08-23 08:25:57','2026-08-23 08:25:57'),(6,4,'Python, SQLAlchemy and Flask are a great combination.',NULL,'PUBLIC','ACTIVE','2026-08-20 15:45:55','2026-08-20 15:45:55',NULL),(7,3,'Learning Flask and building my P1 social media project!',NULL,'PUBLIC','DELETED','2026-08-21 16:55:05','2026-08-23 06:57:56','2026-08-23 06:57:56'),(8,7,'Building production-ready APIs with Flask and JWT.',NULL,'PUBLIC','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(9,6,'Python, SQLAlchemy and Flask are a great combination.',NULL,'PUBLIC','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(10,8,'Exploring database relationships in SQLAlchemy ORM.',NULL,'PUBLIC','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(11,9,'Backend architecture design patterns for scalable web apps.',NULL,'PUBLIC','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(12,4,'Writing comprehensive pytest suites for REST APIs.',NULL,'PUBLIC','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(13,5,'Understanding JWT authentication and role-based access control.',NULL,'PUBLIC','DELETED','2026-08-21 16:55:05','2026-08-23 06:59:09','2026-08-23 06:59:09'),(14,10,'How to handle file uploads securely in Flask web applications.',NULL,'PUBLIC','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(15,11,'Database indexing techniques for MySQL performance optimization.',NULL,'PUBLIC','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(16,12,'Clean code principles and layered software architecture.',NULL,'PUBLIC','DELETED','2026-08-21 16:55:05','2026-08-23 08:26:08','2026-08-23 08:26:08'),(17,13,'Continuous integration pipelines for Python web projects.',NULL,'PUBLIC','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(18,14,'Frontend and backend integration using Flask and Jinja templates.',NULL,'PUBLIC','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(19,15,'Exploring Docker containerization for Flask microservices.',NULL,'PUBLIC','DELETED','2026-08-21 16:55:05','2026-08-23 08:21:20','2026-08-23 08:21:20'),(20,16,'Designing idempotent database seed scripts for production.',NULL,'PUBLIC','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(21,17,'Security best practices for web applications and API endpoints.',NULL,'PUBLIC','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(22,18,'Object-relational mapping vs raw SQL queries performance comparison.',NULL,'PUBLIC','DELETED','2026-08-21 16:55:05','2026-08-23 05:56:22','2026-08-23 05:56:22'),(23,19,'Building real-time notifications for social media platforms.',NULL,'PUBLIC','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(24,20,'Modular blueprint structure in large scale Flask codebases.',NULL,'PUBLIC','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(25,21,'Unit testing with mocks vs integration testing with real databases.',NULL,'PUBLIC','DELETED','2026-08-21 16:55:05','2026-08-23 05:56:32','2026-08-23 05:56:32'),(26,22,'RESTful API documentation using OpenAPI 3.0 specification.',NULL,'PUBLIC','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(27,23,'Exclusive updates for my followers only!',NULL,'FOLLOWERS','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(28,24,'Follower-only discussion on upcoming project architecture.',NULL,'FOLLOWERS','DELETED','2026-08-21 16:55:05','2026-08-23 08:17:50','2026-08-23 08:17:50'),(29,25,'Sneak peek of new features for followers.',NULL,'FOLLOWERS','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(30,26,'Special announcement for my connected network.',NULL,'FOLLOWERS','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(31,27,'Followers lounge: sharing development insights.',NULL,'FOLLOWERS','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(32,28,'My private development scratchpad and notes.',NULL,'PRIVATE','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(33,29,'Confidential draft post for internal review.',NULL,'PRIVATE','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(34,30,'Personal developer log entry - private thoughts.',NULL,'PRIVATE','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(35,31,'Private code snippets and configuration options.',NULL,'PRIVATE','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(36,32,'Private audit and system maintenance notes.',NULL,'PRIVATE','ACTIVE','2026-08-21 16:55:05','2026-08-21 16:55:05',NULL),(37,1,'REST and GraphQL handle data fetching differently: REST uses multiple URLs (endpoints) that return fixed data shapes, while GraphQL uses a single URL where the client explicitly states what data it needs.','/uploads/post_images/a77bd2708f6442849e986087963bf926.png','PUBLIC','DELETED','2026-08-22 09:06:47','2026-08-22 09:12:02','2026-08-22 09:12:02'),(38,4,'demo post edited','/uploads/post_images/2f7f3339f47f4129881eb8018ca817d8.jpeg','PUBLIC','ACTIVE','2026-08-23 14:43:34','2026-08-23 14:44:28',NULL),(39,38,'Spent the weekend building a small Flask application. Really enjoying how simple it is to structure APIs and services.',NULL,'PUBLIC','ACTIVE','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(40,39,'Finally finished my SQLAlchemy relationships today. Understanding how the models connect makes the rest of the application much easier.',NULL,'PUBLIC','ACTIVE','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(41,40,'Started learning more about backend architecture and how service and DAO layers help keep Flask applications maintainable.',NULL,'PUBLIC','ACTIVE','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(42,41,'A good reminder that writing tests early can save a lot of debugging time later.',NULL,'PUBLIC','ACTIVE','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(43,42,'Working on a personal productivity dashboard this week. Small projects are a great way to experiment with new ideas.',NULL,'PUBLIC','ACTIVE','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(44,43,'Reading about API security today. Authentication is only one part of building a secure application.',NULL,'PUBLIC','ACTIVE','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(45,44,'Coffee, code and a quiet afternoon. Sometimes that\'s all you need to make progress.',NULL,'PUBLIC','ACTIVE','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(46,45,'Exploring open-source projects and learning how experienced developers structure their repositories.',NULL,'PUBLIC','ACTIVE','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(47,46,'Just completed another Python practice session. Consistency really does make a difference.',NULL,'PUBLIC','ACTIVE','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(48,47,'Thinking about moving some of my older projects to a cleaner layered architecture.',NULL,'PUBLIC','ACTIVE','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(49,48,'Working through database indexing and query optimization. There is always something new to learn.',NULL,'PUBLIC','ACTIVE','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(50,49,'Trying out a new approach to organizing my development workflow. Keeping tasks small makes everything feel more manageable.',NULL,'PUBLIC','ACTIVE','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(51,50,'Sharing a few notes from my latest web development project. Documentation is definitely worth the extra effort.',NULL,'PUBLIC','ACTIVE','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(52,51,'Learning more about REST API design and how good endpoint structure improves the developer experience.',NULL,'PUBLIC','ACTIVE','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(53,52,'Taking some time this evening to review Python fundamentals and clean up some old code.',NULL,'PUBLIC','ACTIVE','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(54,39,'You are completely useless at programming. Stop pretending you know what you\'re doing.',NULL,'PUBLIC','DELETED','2026-08-23 14:52:47','2026-08-24 06:49:13','2026-08-24 06:49:13'),(55,45,'BUY NOW!!! Guaranteed money-making opportunity. Send me your details and I will show you how to double your income.',NULL,'PUBLIC','ACTIVE','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(56,47,'This community is full of idiots. Nobody here knows anything about software development.',NULL,'PUBLIC','ACTIVE','2026-08-23 14:52:47','2026-08-23 14:52:47',NULL),(57,43,'Free premium account available. Message me privately with your login information to activate it.',NULL,'PUBLIC','DELETED','2026-08-23 14:52:47','2026-08-23 17:51:17','2026-08-23 17:51:17');
/*!40000 ALTER TABLE `posts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports`
--

DROP TABLE IF EXISTS `reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reports` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `reporter_id` bigint NOT NULL,
  `reported_user_id` bigint DEFAULT NULL,
  `post_id` bigint DEFAULT NULL,
  `reason` varchar(100) NOT NULL,
  `description` text,
  `status` varchar(20) NOT NULL,
  `reviewed_by` bigint DEFAULT NULL,
  `reviewed_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reported_user_id` (`reported_user_id`),
  KEY `post_id` (`post_id`),
  KEY `reviewed_by` (`reviewed_by`),
  KEY `idx_reports_reporter` (`reporter_id`),
  KEY `idx_reports_status_created` (`status`,`created_at`),
  CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`reporter_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `reports_ibfk_2` FOREIGN KEY (`reported_user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `reports_ibfk_3` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE,
  CONSTRAINT `reports_ibfk_4` FOREIGN KEY (`reviewed_by`) REFERENCES `users` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports`
--

LOCK TABLES `reports` WRITE;
/*!40000 ALTER TABLE `reports` DISABLE KEYS */;
INSERT INTO `reports` VALUES (1,4,NULL,5,'SPAM','Test report for P1 API testing.','REVIEWED',6,'2026-08-23 08:25:57','2026-08-20 15:45:55'),(2,3,NULL,7,'SPAM','Automated seed report #1','REVIEWED',6,'2026-08-23 14:12:47','2026-08-21 16:55:06'),(3,7,NULL,8,'HARASSMENT','Automated seed report #2','REVIEWED',6,NULL,'2026-08-21 16:55:06'),(4,6,NULL,9,'INAPPROPRIATE','Automated seed report #3','REJECTED',6,NULL,'2026-08-21 16:55:06'),(5,8,NULL,10,'OFFENSIVE','Automated seed report #4','REJECTED',6,'2026-08-23 05:56:11','2026-08-21 16:55:06'),(6,9,NULL,11,'OTHER','Automated seed report #5','REVIEWED',6,NULL,'2026-08-21 16:55:06'),(7,4,NULL,12,'SPAM','Automated seed report #6','REJECTED',6,NULL,'2026-08-21 16:55:06'),(8,5,NULL,13,'HARASSMENT','Automated seed report #7','REVIEWED',6,'2026-08-23 06:59:09','2026-08-21 16:55:06'),(9,10,NULL,14,'INAPPROPRIATE','Automated seed report #8','REVIEWED',6,NULL,'2026-08-21 16:55:06'),(10,11,NULL,15,'OFFENSIVE','Automated seed report #9','REJECTED',6,NULL,'2026-08-21 16:55:06'),(11,12,NULL,16,'OTHER','Automated seed report #10','REVIEWED',6,'2026-08-23 08:26:08','2026-08-21 16:55:06'),(12,13,NULL,17,'SPAM','Automated seed report #11','REVIEWED',6,NULL,'2026-08-21 16:55:06'),(13,14,NULL,18,'HARASSMENT','Automated seed report #12','REJECTED',6,NULL,'2026-08-21 16:55:06'),(14,15,NULL,19,'INAPPROPRIATE','Automated seed report #13','REVIEWED',6,'2026-08-23 08:21:20','2026-08-21 16:55:06'),(15,16,NULL,20,'OFFENSIVE','Automated seed report #14','REVIEWED',6,NULL,'2026-08-21 16:55:06'),(16,17,NULL,21,'OTHER','Automated seed report #15','REJECTED',6,NULL,'2026-08-21 16:55:06'),(17,18,NULL,22,'SPAM','Automated seed report #16','REVIEWED',6,'2026-08-23 05:56:22','2026-08-21 16:55:06'),(18,19,NULL,23,'HARASSMENT','Automated seed report #17','REVIEWED',6,NULL,'2026-08-21 16:55:06'),(19,20,NULL,24,'INAPPROPRIATE','Automated seed report #18','REJECTED',6,NULL,'2026-08-21 16:55:06'),(20,21,NULL,25,'OFFENSIVE','Automated seed report #19','REVIEWED',6,'2026-08-23 05:56:32','2026-08-21 16:55:06'),(21,22,NULL,26,'OTHER','Automated seed report #20','REVIEWED',6,NULL,'2026-08-21 16:55:06'),(22,23,NULL,27,'SPAM','Automated seed report #21','REJECTED',6,NULL,'2026-08-21 16:55:06'),(23,24,NULL,28,'HARASSMENT','Automated seed report #22','REVIEWED',6,'2026-08-23 08:17:50','2026-08-21 16:55:06'),(24,25,NULL,29,'INAPPROPRIATE','Automated seed report #23','REVIEWED',6,NULL,'2026-08-21 16:55:06'),(25,26,NULL,30,'OFFENSIVE','Automated seed report #24','REJECTED',6,NULL,'2026-08-21 16:55:06'),(26,27,NULL,31,'OTHER','Automated seed report #25','REVIEWED',6,'2026-08-22 09:38:43','2026-08-21 16:55:06'),(27,28,NULL,32,'SPAM','Automated seed report #26','REVIEWED',6,NULL,'2026-08-21 16:55:06'),(28,29,NULL,33,'HARASSMENT','Automated seed report #27','REJECTED',6,NULL,'2026-08-21 16:55:06'),(29,30,NULL,34,'INAPPROPRIATE','Automated seed report #28','REVIEWED',6,'2026-08-22 09:38:40','2026-08-21 16:55:06'),(30,31,NULL,35,'OFFENSIVE','Automated seed report #29','REVIEWED',6,NULL,'2026-08-21 16:55:06'),(31,32,NULL,36,'OTHER','Automated seed report #30','REJECTED',6,NULL,'2026-08-21 16:55:06'),(32,4,NULL,7,'Inappropriate',NULL,'REVIEWED',6,'2026-08-23 06:57:56','2026-08-23 05:53:25'),(33,6,NULL,7,'hate',NULL,'REVIEWED',6,'2026-08-23 14:12:47','2026-08-23 06:28:41'),(34,6,NULL,2,'spam',NULL,'REVIEWED',6,'2026-08-23 08:49:29','2026-08-23 08:49:22'),(35,38,NULL,54,'HARASSMENT','The post contains insulting language directed at other members of the community.','REVIEWED',36,'2026-08-24 06:49:13','2026-08-23 14:52:47'),(36,40,NULL,55,'SPAM','The post appears to promote a suspicious money-making scheme.','PENDING',NULL,NULL,'2026-08-23 14:52:47'),(37,41,NULL,56,'OFFENSIVE','The post contains insulting and disrespectful language toward the community.','PENDING',NULL,NULL,'2026-08-23 14:52:47'),(38,42,43,NULL,'SPAM','This account repeatedly posts promotional content and suspicious offers.','REVIEWED',34,'2026-08-23 17:55:58','2026-08-23 14:52:47'),(39,44,NULL,57,'SPAM','The post requests sensitive account information.','REVIEWED',36,NULL,'2026-08-23 14:52:47'),(40,48,NULL,39,'OTHER','Reported because the content was considered unhelpful by the reporter.','REJECTED',37,NULL,'2026-08-23 14:52:47'),(41,38,NULL,57,'Fraud',NULL,'REVIEWED',36,'2026-08-23 17:51:17','2026-08-23 17:46:30'),(42,38,43,NULL,'Fraud',NULL,'PENDING',NULL,NULL,'2026-08-23 17:52:09'),(43,40,NULL,54,'hate',NULL,'REVIEWED',36,'2026-08-24 06:49:13','2026-08-24 06:47:01');
/*!40000 ALTER TABLE `reports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `bio` varchar(500) DEFAULT NULL,
  `profile_picture` varchar(500) DEFAULT NULL,
  `role` varchar(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'xena','xena@gmail.com','$2b$12$X.01e3zMEJDjvP3I6Ghsc.MV/iQkMvW.p6VGxeU88snQjLAf7NfSG','xena','pereira',NULL,'/uploads/profile_pictures/e24313a904eb4859a3607416931dc4d2.jpg','USER',1,'2026-08-19 14:37:31','2026-08-22 09:21:17'),(2,'naeomi','naeomi@gmail.com','$2b$12$GVsAtSzMS5tdgCLv7oEBw.42MdUbFl6XP0K0J3m9why7dRfJqC8ra','naeomi','dias',NULL,NULL,'USER',1,'2026-08-19 15:20:20','2026-08-19 15:20:20'),(3,'p1_admin','p1_admin@gmail.com','$2b$12$KAfFflJD9JPFI9wNmk2Et.K/35i5wOFjQWnXERe8H7oHrdVZr2RuO','P1','Admin',NULL,NULL,'ADMIN',1,'2026-08-20 15:45:55','2026-08-20 15:45:55'),(4,'p1_xena','p1_xena@gmail.com','$2b$12$OB1eRBOuTH.irwNV0Usl.e3TZP9y6Eb7QUSnQQpWvl2XxqQJItYbG','Xena','Pereira',NULL,'/uploads/profile_pictures/38be77f17b2842e5bf08910e9322b542.jpg','USER',1,'2026-08-20 15:45:55','2026-08-22 11:05:03'),(5,'p1_john','p1_john@gmail.com','$2b$12$4Vp1DnT642bFpZnUWwSizepQIgD83UyKvROyZK8ki.wLnse9E1AC2','John','Doe',NULL,NULL,'USER',1,'2026-08-20 15:45:55','2026-08-20 15:45:55'),(6,'p1_moderator','p1_moderator@gmail.com','$2b$12$AftFY8mvmBLrLL9CKaoCVOk4Dju02lV5is.NoxX9MLxQVqSkSlKo6','P1','Moderator',NULL,NULL,'MODERATOR',1,'2026-08-21 14:48:45','2026-08-21 14:48:45'),(7,'p1_admin2','p1_admin2@gmail.com','$2b$12$e/BScO9pim.IMo5N/152PenbeM5jWQRghJmSs2muzqGVrqiM48eBe','P1','SuperAdmin',NULL,NULL,'ADMIN',1,'2026-08-21 16:54:59','2026-08-21 16:54:59'),(8,'p1_mod2','p1_mod2@gmail.com','$2b$12$PhsVNfF/kxrMzQE6BIb8c.45vsVfsh2e4/eCdi2X.SR4kSKbPZEzC','Second','Moderator',NULL,NULL,'MODERATOR',1,'2026-08-21 16:54:59','2026-08-21 16:54:59'),(9,'p1_mod3','p1_mod3@gmail.com','$2b$12$VRp1YmfuqCNmYAR07yCHAOJfjE48slG3gco0GnnhSYNxVyuapVkQa','Third','Moderator',NULL,NULL,'MODERATOR',1,'2026-08-21 16:54:59','2026-08-21 16:54:59'),(10,'p1_user1','p1_user1@example.com','$2b$12$tb820oakPA7/sEV1u4/tKeVs2wbh1k4SlK054G/c4xJRwifL1grLi','UserFirstName1','UserLastName1',NULL,NULL,'USER',1,'2026-08-21 16:55:00','2026-08-21 16:55:00'),(11,'p1_user2','p1_user2@example.com','$2b$12$1F14Oefg2JlQ3NeAw1NHweYdHvh09CLuIcc7ekJV6y50Rl/T14dqq','UserFirstName2','UserLastName2',NULL,NULL,'USER',1,'2026-08-21 16:55:00','2026-08-21 16:55:00'),(12,'p1_user3','p1_user3@example.com','$2b$12$NNhWIBLhWdi85mDPZETYxO07kPBJ1vnBh2aeUefqoWJ7iXwIMrlTG','UserFirstName3','UserLastName3',NULL,NULL,'USER',1,'2026-08-21 16:55:00','2026-08-21 16:55:00'),(13,'p1_user4','p1_user4@example.com','$2b$12$0j5yn3Y64mgHXrgpNyio1OwItRl5Rioyf3c5fmIES66HA4MHzbbUm','UserFirstName4','UserLastName4',NULL,NULL,'USER',0,'2026-08-21 16:55:00','2026-08-23 14:07:31'),(14,'p1_user5','p1_user5@example.com','$2b$12$ZcFqldQv8hCHfvsV/vG87uIae6TT2BLeMNCvxdZQsmwGvozMojALG','UserFirstName5','UserLastName5',NULL,NULL,'USER',1,'2026-08-21 16:55:01','2026-08-21 16:55:01'),(15,'p1_user6','p1_user6@example.com','$2b$12$/GKDyLV2/w6DpkRyFgb/TO4FU3yiKZUek4NB1njX2wb0wgFKqYv9m','UserFirstName6','UserLastName6',NULL,NULL,'USER',1,'2026-08-21 16:55:01','2026-08-21 16:55:01'),(16,'p1_user7','p1_user7@example.com','$2b$12$wo8FeXoPepzg03N3JEE6GeEQtL/S/TTepbwPzlEKYiCGAVN76QRDi','UserFirstName7','UserLastName7',NULL,NULL,'USER',1,'2026-08-21 16:55:01','2026-08-21 16:55:01'),(17,'p1_user8','p1_user8@example.com','$2b$12$ifY15O9QS3eaQpcmxximy.48m6daklCubhKp8x5vKcLIlooT.rZE2','UserFirstName8','UserLastName8',NULL,NULL,'USER',1,'2026-08-21 16:55:01','2026-08-21 16:55:01'),(18,'p1_user9','p1_user9@example.com','$2b$12$//380NSvohfY9ZNo3ieRW.QuEnnSZvoRGpjPXBjmN1TJpup91YB6y','UserFirstName9','UserLastName9',NULL,NULL,'USER',1,'2026-08-21 16:55:02','2026-08-21 16:55:02'),(19,'p1_user10','p1_user10@example.com','$2b$12$0GIr7LcsDsR3XgBs1gbzuew7QR2BrSdtI9Ejr0YU1DhLlwUGQ9j96','UserFirstName10','UserLastName10',NULL,NULL,'USER',1,'2026-08-21 16:55:02','2026-08-21 16:55:02'),(20,'p1_user11','p1_user11@example.com','$2b$12$7XTS/8/YCONe/CNAXRd/pe3n3wFA6ragcF4NcZxA2rfjmeOjorheK','UserFirstName11','UserLastName11',NULL,NULL,'USER',1,'2026-08-21 16:55:02','2026-08-21 16:55:02'),(21,'p1_user12','p1_user12@example.com','$2b$12$fIoFk.aLalLB5scOLwa8De.qgI9jUSjU1hS.JD0I.sOHlX6168ppa','UserFirstName12','UserLastName12',NULL,NULL,'USER',1,'2026-08-21 16:55:02','2026-08-21 16:55:02'),(22,'p1_user13','p1_user13@example.com','$2b$12$a421av6LfxPStSx2C32kgOESaOeDh2Ew1f9sBwUIkeVw6.ai.9Lc2','UserFirstName13','UserLastName13',NULL,NULL,'USER',1,'2026-08-21 16:55:03','2026-08-21 16:55:03'),(23,'p1_user14','p1_user14@example.com','$2b$12$s05ocdwKOxZpc4Guid50Ee60ozHksiB6P5h5mQsSoSo8tcH7AgyPu','UserFirstName14','UserLastName14',NULL,NULL,'USER',1,'2026-08-21 16:55:03','2026-08-21 16:55:03'),(24,'p1_user15','p1_user15@example.com','$2b$12$uBq4GIkpQhatWA//ulXxieJmlqwaOM/EsVO08Y50yQ.PcWPdlJO4K','UserFirstName15','UserLastName15',NULL,NULL,'USER',1,'2026-08-21 16:55:03','2026-08-21 16:55:03'),(25,'p1_user16','p1_user16@example.com','$2b$12$SMOOC9bgDx6qsItQeXQnguwoAY7XKUZ/3tJthG/7W3.Mb2tvE86l2','UserFirstName16','UserLastName16',NULL,NULL,'USER',1,'2026-08-21 16:55:03','2026-08-21 16:55:03'),(26,'p1_user17','p1_user17@example.com','$2b$12$YMk45w/rpHv5ISZ4cHjI1Odwh79emUQSJWW5L82wwHr0EvH2t8EUy','UserFirstName17','UserLastName17',NULL,NULL,'USER',1,'2026-08-21 16:55:03','2026-08-21 16:55:03'),(27,'p1_user18','p1_user18@example.com','$2b$12$A6peaOPWWkkxw5w04dXvL.pl00qwzXcO.9CIxlLeFF6etxH/oI7Uq','UserFirstName18','UserLastName18',NULL,NULL,'USER',1,'2026-08-21 16:55:04','2026-08-21 16:55:04'),(28,'p1_user19','p1_user19@example.com','$2b$12$sY9H1XH07uUmKROtiB.W9uuc7JX9MC1Ibe/cON/YXqiWYz3nxYZ7C','UserFirstName19','UserLastName19',NULL,NULL,'USER',1,'2026-08-21 16:55:04','2026-08-21 16:55:04'),(29,'p1_user20','p1_user20@example.com','$2b$12$9VGnyKYC4bjhILQSYKT0rujLo6FKjAFet/63nDwnPsZezrwCXEete','UserFirstName20','UserLastName20',NULL,NULL,'USER',1,'2026-08-21 16:55:04','2026-08-21 16:55:04'),(30,'p1_user21','p1_user21@example.com','$2b$12$gXfG3x6Kb.p7kSyzlhNHAO2XmMeiKL1aVK//xKwpWc.WMTfCbw7l6','UserFirstName21','UserLastName21',NULL,NULL,'USER',1,'2026-08-21 16:55:04','2026-08-21 16:55:04'),(31,'p1_user22','p1_user22@example.com','$2b$12$VsUwU1ZbhdSUOyPpeE7BfepN5Bv5Mf56pj1DkjD2ueNZNs8oiQAya','UserFirstName22','UserLastName22',NULL,NULL,'USER',1,'2026-08-21 16:55:05','2026-08-21 16:55:05'),(32,'p1_user23','p1_user23@example.com','$2b$12$cHyVpFxe/6vF5fBlzDfNLekCLh2sccnwdJm3tvRXbjigqSAbzb3SG','UserFirstName23','UserLastName23',NULL,NULL,'USER',1,'2026-08-21 16:55:05','2026-08-21 16:55:05'),(33,'p1_user24','p1_user24@example.com','$2b$12$9JnCICn7K82Al42Q57w5AeGxDDuKA3xptpYJdMDA7KEa5vLy/OfBS','UserFirstName24','UserLastName24',NULL,NULL,'USER',1,'2026-08-21 16:55:05','2026-08-23 14:34:21'),(34,'alexandra_reed','alexandra.reed@example.com','$2b$12$9/bbmEPBRp/ZNplpo1M9N.bVhjD38Y/xxA7EjUiWcseglapzYPmv2','Alexandra','Reed',NULL,NULL,'ADMIN',1,'2026-08-23 14:52:43','2026-08-23 14:52:43'),(35,'daniel_carter','daniel.carter@example.com','$2b$12$isofwapI/OSLYnoYCeNaCuEqCHfZyX15/6ilPeE.zZ47soWISqzkC','Daniel','Carter',NULL,NULL,'ADMIN',1,'2026-08-23 14:52:43','2026-08-23 14:52:43'),(36,'sophia_morgan','sophia.morgan@example.com','$2b$12$nbrUcLEi7R4tWok1BIFOqu6dbL8Mr6t/q4pyvTG0Sj/xjQi5QHDoe','Sophia','Morgan',NULL,NULL,'MODERATOR',1,'2026-08-23 14:52:43','2026-08-23 14:52:43'),(37,'liam_bennett','liam.bennett@example.com','$2b$12$uP/g4aNX7Qbj0rVDdnYlLOIvgnyvpR4nmphfuCa4a8/nshNsmTqbi','Liam','Bennett',NULL,NULL,'MODERATOR',1,'2026-08-23 14:52:43','2026-08-23 14:52:43'),(38,'emma_wilson','emma.wilson@example.com','$2b$12$zkkUR4I3.cEoRg/2uvfHuuduwKB608QH43QPmUpgwVPsCL2H5nm5e','Emma','Wilson',NULL,'/uploads/profile_pictures/0fbba12b75f74584a585f8bb0b5f7355.jpg','USER',1,'2026-08-23 14:52:44','2026-08-23 17:43:57'),(39,'oliver_harris','oliver.harris@example.com','$2b$12$9McgoehhjoQRI2z8vY2JGOXr9t76n9J2iB0s8kUjA6kNrHt/hSWI2','Oliver','Harris',NULL,NULL,'USER',1,'2026-08-23 14:52:44','2026-08-23 14:52:44'),(40,'ava_thompson','ava.thompson@example.com','$2b$12$/Y6jwrD30jnucWwkpwdHau6CFqniC0mx8TONh6I9TAcF8y7D6sFZa','Ava','Thompson',NULL,NULL,'USER',1,'2026-08-23 14:52:44','2026-08-23 14:52:44'),(41,'noah_martin','noah.martin@example.com','$2b$12$xXCXYaihi4mqUYBe5a5ErudUuqDyRL8fjH0yGN/0ZKzsBYT5QLnpG','Noah','Martin',NULL,NULL,'USER',1,'2026-08-23 14:52:44','2026-08-23 14:52:44'),(42,'mia_clark','mia.clark@example.com','$2b$12$z6EhQUn3nbV0t.l4HNSuwunuDSGYPdUa2MLbrZvKnOf8I8/iGSYHW','Mia','Clark',NULL,NULL,'USER',1,'2026-08-23 14:52:45','2026-08-23 14:52:45'),(43,'ethan_lewis','ethan.lewis@example.com','$2b$12$Wa7qkKp/5PFYFUlEZG5Mtu4bNiT7xwdmNryPL5j0/TNZ.gCprEH0m','Ethan','Lewis',NULL,NULL,'USER',1,'2026-08-23 14:52:45','2026-08-23 14:52:45'),(44,'isabella_walker','isabella.walker@example.com','$2b$12$rCnlHz6yhwOhMpbbW2ygn.yr/VJHAMl0T6tURWHdOsOPoEVt0pdsa','Isabella','Walker',NULL,NULL,'USER',1,'2026-08-23 14:52:45','2026-08-23 14:52:45'),(45,'mason_hall','mason.hall@example.com','$2b$12$wr/Ndx3I6dg5vp9mVhZbEeNakB/hxdFUmikxGX8nA1TAEcrXc3So.','Mason','Hall',NULL,NULL,'USER',1,'2026-08-23 14:52:45','2026-08-23 14:52:45'),(46,'sophia_young','sophia.young@example.com','$2b$12$4CP9h1eRO7qvjefvrmiFHOgFyo5ooBh8qzraWc3MRm8oFr7lmXf/S','Sophia','Young',NULL,NULL,'USER',1,'2026-08-23 14:52:46','2026-08-23 14:52:46'),(47,'james_king','james.king@example.com','$2b$12$bzjLlDCfpDOIImr9wjCTh..UqUcHOdsjfgbcf5o7aGGfsA78mMqxS','James','King',NULL,NULL,'USER',1,'2026-08-23 14:52:46','2026-08-23 14:52:46'),(48,'charlotte_wright','charlotte.wright@example.com','$2b$12$kwrK5rtwRjYUDqgLWlnKLurfQTfNPpEs8N8MeOm0tAUEKla.pYtGS','Charlotte','Wright',NULL,NULL,'USER',1,'2026-08-23 14:52:46','2026-08-23 14:52:46'),(49,'benjamin_scott','benjamin.scott@example.com','$2b$12$Sq9cELchZW8.O/LooO1cB.4tAK6pzDa.rW3uc4nXJi0EwtWVjdqVO','Benjamin','Scott',NULL,NULL,'USER',1,'2026-08-23 14:52:46','2026-08-23 14:52:46'),(50,'amelia_green','amelia.green@example.com','$2b$12$wvDzBXSUWFm3MNuPxJE0Ve5mmyJneNyYqAMtEDCv2F5aEDaH8GfU6','Amelia','Green',NULL,NULL,'USER',1,'2026-08-23 14:52:46','2026-08-23 14:52:46'),(51,'henry_adams','henry.adams@example.com','$2b$12$8/WYWsnAmt8FIdTLZZOqSOEpX6Aou3XTBWBQtBfLnu.o1WHA56Bmm','Henry','Adams',NULL,NULL,'USER',1,'2026-08-23 14:52:47','2026-08-23 14:52:47'),(52,'grace_baker','grace.baker@example.com','$2b$12$pNXAdHAlcf1PY5Y072nSH.hkQ1Sfbjs.p/R5edb0HMiWNR9WV8O1a','Grace','Baker',NULL,'/uploads/profile_pictures/c790411905fc4ec2833428fd997f935a.jpg','USER',1,'2026-08-23 14:52:47','2026-08-26 02:36:50');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-31 18:43:35
