-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 27, 2021 at 07:39 PM
-- Server version: 5.7.31
-- PHP Version: 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pyfair`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `Email` varchar(100) NOT NULL,
  `First_Name` varchar(100) NOT NULL,
  `Last_Name` varchar(100) NOT NULL,
  `Password` varchar(100) NOT NULL,
  PRIMARY KEY (`Email`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`Email`, `First_Name`, `Last_Name`, `Password`) VALUES
('bilawal.hussain350@gmail.com', 'Bilawal', 'Hussain', 'pbkdf2:sha256:150000$BNnGwnXm$4790f34da3734a0108dec6a101e8d51a6a8e6913a340d9fcde464cf50f99a469'),
('bb.talpur@gmail.com', 'Bilal', 'Hussain', 'pbkdf2:sha256:150000$5W0Yhs4t$141a8a7fdd8be8ac5ad8aaf9d57f14c99cf499afd280c3364b2a598bf35903d6'),
('b_talpur@yahoo.com', 'Bilal', 'Hussain', 'pbkdf2:sha256:150000$A8by9W9e$9cb39f417dc11f97b40bc9616416e3ad04e7b45141e17e5235d3f4948c9e4700');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
