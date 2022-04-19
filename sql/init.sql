CREATE DATABASE IF NOT EXISTS `webcalendar`;
USE `webcalendar`;

CREATE TABLE IF NOT EXISTS `accounts` (
	`userID` int NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(64) NOT NULL,
	  `backupphrase` varchar(64) NOT NULL,
    `holidays` BIT NULL,
    PRIMARY KEY (`userID`)
);

CREATE TABLE IF NOT EXISTS `events` (
  `eventID` INT NOT NULL AUTO_INCREMENT,
  `eventName` VARCHAR(128) NULL,
  `startTime` DATETIME NULL,
  `endTime` DATETIME NULL,
  `userID` INT NULL,
  `shareable` BIT NULL,
  `color` VARCHAR(20) NULL,
  PRIMARY KEY (`eventID`),
  INDEX `userID_idx` (`userID` ASC) VISIBLE,
  CONSTRAINT `userID`
    FOREIGN KEY (`userID`)
    REFERENCES `webcalendar`.`accounts` (`userID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
    );

CREATE TABLE IF NOT EXISTS `holidays` (
  `holidayID` INT NOT NULL AUTO_INCREMENT,
  `eventName` VARCHAR(128) NULL,
  `startTime` DATETIME NULL,
  `endTime` DATETIME NULL,
  `color` VARCHAR(20) NULL,
  PRIMARY KEY (`holidayID`)
);

INSERT INTO holidays VALUES (NULL, 'Veterans Day', '2022-11-11T00:00:00+00:00', '2022-11-11T00:00:00+00:00', 'black');
INSERT INTO holidays VALUES (NULL, 'Memorial Day', '2022-05-30T00:00:00+00:00', '2022-05-30T00:00:00+00:00', 'black');
INSERT INTO holidays VALUES (NULL, 'Labor Day', '2022-09-05T00:00:00+00:00', '2022-09-05T00:00:00+00:00', 'black');
INSERT INTO holidays VALUES (NULL, 'Columbus Day', '2022-10-10T00:00:00+00:00', '2022-10-10T00:00:00+00:00', 'black');
INSERT INTO holidays VALUES (NULL, 'New Year\'s Day', '2023-01-01T00:00:00+00:00', '2023-01-01T00:00:00+00:00', 'black');
INSERT INTO holidays VALUES (NULL, 'Christmas Day', '2022-12-25T00:00:00+00:00', '2022-12-25T00:00:00+00:00', 'black');
INSERT INTO holidays VALUES (NULL, 'Washington\'s Birthday', '2023-02-20T00:00:00+00:00', '2023-02-20T00:00:00+00:00', 'black');
INSERT INTO holidays VALUES (NULL, 'Thanksgiving Day', '2022-11-24T00:00:00+00:00', '2022-11-24T00:00:00+00:00', 'black');
INSERT INTO holidays VALUES (NULL, 'Independence Day', '2022-07-04T00:00:00+00:00', '2022-07-04T00:00:00+00:00', 'black');
INSERT INTO holidays VALUES (NULL, 'Martin Luther King, Jr. Day', '2023-01-16T00:00:00+00:00', '2023-01-16T00:00:00+00:00', 'black');