-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- 생성 시간: 22-02-22 18:26
-- 서버 버전: 10.5.9-MariaDB-1:10.5.9+maria~focal
-- PHP 버전: 7.4.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 데이터베이스: `wei_db`
--
CREATE DATABASE IF NOT EXISTS `wei_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `wei_db`;

-- --------------------------------------------------------

--
-- 테이블 구조 `serverlist`
--

DROP TABLE IF EXISTS `serverlist`;
CREATE TABLE IF NOT EXISTS `serverlist` (
  `server` varchar(50) NOT NULL,
  `url` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 삽입 전에 테이블 비우기 `serverlist`
--

TRUNCATE TABLE `serverlist`;
--
-- 테이블의 덤프 데이터 `serverlist`
--

INSERT INTO `serverlist` (`server`, `url`) VALUES
('아만', 'https://discord.com/channels/660684739056762891/724168359171719199'),
('루페온', 'https://discord.com/channels/660684739056762891/724168238300397618');

-- --------------------------------------------------------

--
-- 테이블 구조 `userinfo`
--

DROP TABLE IF EXISTS `userinfo`;
CREATE TABLE IF NOT EXISTS `userinfo` (
  `id` varchar(50) NOT NULL,
  `pwd` varchar(150) NOT NULL,
  `appnum` varchar(200) DEFAULT NULL,
  `server` varchar(30) NOT NULL,
  `keyword` varchar(20) DEFAULT NULL COMMENT 'keyword',
  `state` varchar(10) NOT NULL DEFAULT 'False',
  `signupDate` datetime NOT NULL DEFAULT current_timestamp(),
  `lastLoginDate` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 삽입 전에 테이블 비우기 `userinfo`
--

TRUNCATE TABLE `userinfo`;
--
-- 테이블의 덤프 데이터 `userinfo`
--

INSERT INTO `userinfo` (`id`, `pwd`, `appnum`, `server`, `keyword`, `state`, `signupDate`, `lastLoginDate`) VALUES
('test1234', 'pbkdf2:sha256:260000$a6CDAZiZPSbu4TSp$6abb20d9216c63bce98ebfc195e3b45686559d9cadfa3d05c410e4f9a6501bad', 'eOVQIi7DSW8:APA91bFOj1qpy0iKtUi0ZY8sNzCIB2YEbqBgSnGbP-D5w2PXHb7qpo705Vi-YP-6TGL8OzilGU5MvBLMd02Q0DnZpGwVdunotSQwtlJzMfhANEOUElg-fBimeJF-w9pC8rgEz8_sTTtc', '아만', '킬리언', 'False', '2022-02-14 21:16:29', '2022-02-22 15:10:55'),
('12345@', 'pbkdf2:sha256:260000$8nZytrCwgwk6EFi2$70cba689969007a95f8f7d637e3b9e3342d6d699763440cd3031f43cafe35982', NULL, '루페온', NULL, 'False', '2022-02-14 21:16:29', NULL),
('34123@', 'pbkdf2:sha256:260000$j0sfhBoI1HSpjEdi$0876bf5c6ec4519f4e3e753ee9e84ccb5f5bfc9fb15f77fb774f40fa914f92dc', NULL, '루페온', NULL, 'False', '2022-02-14 21:16:29', NULL),
('4123@', 'pbkdf2:sha256:260000$ez48vXowDNxKePiY$5385d5f25f45f95aabd0f76759cf7be6ee78c8b5d78ee90fc9f6315f04bb0ff6', NULL, '카제로스', NULL, 'False', '2022-02-14 21:16:29', NULL),
('abcde@', 'pbkdf2:sha256:260000$wwv3eJC6szBwcXun$16f9f4e5c1bda3f8f7aae4624d0dce067fd14864c3fa53342014aa1241bd640e', NULL, '루페온', NULL, 'False', '2022-02-14 21:16:29', NULL),
('123@4123', 'pbkdf2:sha256:260000$RXqwbxANdULaT2Fq$2d0b0d0ce77e382cf098c7eaf13b873f60a7d41e9c5738162248f7900bac0d5e', NULL, '루페온', NULL, 'False', '2022-02-14 21:16:29', NULL),
('asd@', 'pbkdf2:sha256:260000$PXjYIigCVeuqcxmj$c2777ee4381eab17185a67d17244712807895d6579185004fe5d3abab8cc824f', NULL, '루페온', NULL, 'False', '2022-02-14 21:16:29', NULL),
('12343@1', 'pbkdf2:sha256:260000$gpwDdpb3dZApcEPb$e0f51f9b3adc996c19c99bb2492856348609ea687e3bf0416f8deb93fa814c89', NULL, '루페온', NULL, 'False', '2022-02-14 21:16:29', NULL),
('test12345', 'pbkdf2:sha256:260000$Zbj9wYOJe4fpsOxt$b3e223709bcd53fcdb6d8ad38d66131e0a14e7c969b482d0e4ee1ac1f441ec57', NULL, '루페온', NULL, 'False', '2022-02-14 21:27:04', NULL),
('123@', 'pbkdf2:sha256:260000$857L2xWzPREeLM3m$d790aa987bca1a576ce11800091931d39a515638de522814e9d585a7e0d60ac7', NULL, '루페온', NULL, 'False', '2022-02-16 08:01:29', '2022-02-16 08:02:00'),
('12@', 'pbkdf2:sha256:260000$Kz8aF8MjcOIYrJPd$6c6071041217ab8353a6411525d0b64e3697368d80a6b3350e939f3e2c561f15', NULL, '루페온', NULL, 'False', '2022-02-17 15:35:36', NULL),
('12@2323', 'pbkdf2:sha256:260000$oGbYvNZPBuwK845o$15fc674c1b63fcd8e5cb15113efc22b4d31f38014b2aa60bcae17b21699a7388', NULL, '루페온', NULL, 'False', '2022-02-17 15:44:45', NULL),
('12@2323123', 'pbkdf2:sha256:260000$EAYVT5Y6E9WBuPnF$859be72d38a7201fd06b4b3f7f6b5c1add908d4430393ae05f82efc1f8d78025', NULL, '루페온', NULL, 'False', '2022-02-17 16:04:32', NULL),
('ysj97@naver.com', 'pbkdf2:sha256:260000$xu7g2O9SKmKil7MM$e3cb34020132f4bab17664a33157dbf4be752a381350eaf009a649c34cd23afa', 'eOVQIi7DSW8:APA91bFOj1qpy0iKtUi0ZY8sNzCIB2YEbqBgSnGbP-D5w2PXHb7qpo705Vi-YP-6TGL8OzilGU5MvBLMd02Q0DnZpGwVdunotSQwtlJzMfhANEOUElg-fBimeJF-w9pC8rgEz8_sTTtc', '루페온', '웨이', 'False', '2022-02-22 17:18:56', '2022-02-22 17:23:08');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
