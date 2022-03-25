CREATE DATABASE IF NOT EXISTS `webcalendar`;
USE `webcalendar`;

CREATE TABLE IF NOT EXISTS `accounts` (
	`userID` int NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(64) NOT NULL,
	`backupphrase` varchar(64) NOT NULL,
    PRIMARY KEY (`userID`)
)

CREATE TABLE IF NOT EXISTS `events` (
  `eventID` INT NOT NULL AUTO_INCREMENT,
  `eventName` VARCHAR(128) NULL,
  `startTime` DATETIME NULL,
  `endTime` DATETIME NULL,
  `userID` INT NULL,
  PRIMARY KEY (`eventID`),
  INDEX `userID_idx` (`userID` ASC) VISIBLE,
  CONSTRAINT `userID`
    FOREIGN KEY (`userID`)
    REFERENCES `webcalendar`.`accounts` (`userID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);
