-- phpMyAdmin SQL Dump
-- version 4.3.5
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 08, 2015 at 06:49 PM
-- Server version: 5.5.38-0+wheezy1
-- PHP Version: 5.4.4-14+deb7u14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `donationbox`
--

-- --------------------------------------------------------

--
-- Table structure for table `moneyToProject`
--

CREATE TABLE IF NOT EXISTS `moneyToProject` (
  `IDmoneyToProject` int(11) NOT NULL,
  `BoxName` varchar(11) NOT NULL,
  `project` int(2) NOT NULL,
  `money` int(4) NOT NULL,
  `UpdateDateTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `moneyToProject`
--

INSERT INTO `moneyToProject` (`IDmoneyToProject`, `BoxName`, `project`, `money`, `UpdateDateTime`) VALUES
(1, 'D11111', 0, 0, '2015-01-06 16:55:51'),
(2, 'D11111', 1, 0, '2015-01-06 16:55:51'),
(3, 'D11111', 2, 0, '2015-01-06 16:55:51'),
(4, 'D11111', 3, 0, '2015-01-06 16:55:51'),
(5, 'D11111', 4, 0, '2015-01-06 16:55:51'),
(6, 'D11111', 5, 0, '2015-01-06 16:55:51');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `moneyToProject`
--
ALTER TABLE `moneyToProject`
  ADD PRIMARY KEY (`IDmoneyToProject`), ADD UNIQUE KEY `IDmoneyToProject_UNIQUE` (`IDmoneyToProject`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `moneyToProject`
--
ALTER TABLE `moneyToProject`
  MODIFY `IDmoneyToProject` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=7;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
