-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Gazda: localhost
-- Timp de generare: 20 Feb 2014 la 18:29
-- Versiune server: 5.5.35
-- Versiune PHP: 5.3.10-1ubuntu3.9

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Baza de date: `dexonline`
--

-- --------------------------------------------------------

--
-- Structură pentru vizualizare `LexemeOnly`
--

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `LexemeOnly` AS select `Lexem`.`id` AS `Id`,`Lexem`.`formUtf8General` AS `formUtf8General` from `Lexem`;

--
-- VIEW  `LexemeOnly`
-- Date: Nici unul(a)
--


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
