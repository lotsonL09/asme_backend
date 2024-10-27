CREATE DATABASE asme;


USE asme;

CREATE TABLE grupos(
	id_group INT AUTO_INCREMENT,
    group_name VARCHAR(100) UNIQUE,
    coordinator VARCHAR(100),
    PRIMARY KEY(id_group)
);

CREATE TABLE teams(
	id_team INT AUTO_INCREMENT,
    team_name VARCHAR(100),
    PRIMARY KEY(id_team)
);

CREATE TABLE areas(
	id_area INT AUTO_INCREMENT,
    area_name VARCHAR(100),
    PRIMARY KEY(id_area)
);

CREATE TABLE users(
	id_user INT AUTO_INCREMENT,
	DNI VARCHAR(8),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    checkbooks VARCHAR(2), #TALONARIOS
	id_group INT,
    id_team INT,
	id_area INT,
    PRIMARY KEY(id_user),
    FOREIGN KEY(id_group) REFERENCES grupos(id_group),
    FOREIGN KEY(id_area) REFERENCES areas(id_area),
    FOREIGN KEY(id_team) REFERENCES teams(id_team)
);

CREATE TABLE buyers(
	id_buyer INT AUTO_INCREMENT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    DNI VARCHAR(8),
    email VARCHAR(100),
    cell_phone VARCHAR(20),
    PRIMARY KEY(id_buyer)
);

CREATE TABLE tickets(
	id_ticket INT AUTO_INCREMENT,
    number_ticket VARCHAR(4),
    booked BOOLEAN,
    booking_time DATETIME, #'1000-01-01 00:00:00' to '9999-12-31 23:59:59',
    evidence VARCHAR(200),
    id_user INT,
    id_buyer INT,
    PRIMARY KEY(id_ticket),
    FOREIGN KEY(id_user) REFERENCES users(id_user),
    FOREIGN KEY(id_buyer) REFERENCES buyers(id_buyer)
);




