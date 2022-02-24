CREATE DATABASE IF NOT EXISTS `webcalendar`;
USE `webcalendar`;

CREATE TABLE IF NOT EXISTS `accounts` (
	`userID` int NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(64) NOT NULL,
    PRIMARY KEY (`userID`)
)