DROP USER IF EXISTS app@'%';
CREATE USER app@'%' IDENTIFIED BY '12345678';
GRANT SELECT, INSERT, UPDATE, DELETE ON Query1.* TO app@'%';

DROP DATABASE IF EXISTS Query1;
CREATE DATABASE Query1;
USE Query1;

CREATE TABLE filament(
id int primary key auto_increment,
proizvođač char(50),
boja char(50),
materijal char(50),
promjer decimal(3,2),
masa decimal(8,3),
datum_vrijeme_upisa datetime
);

CREATE TABLE korisnik(
id int primary key auto_increment,
email varchar(50),
password BINARY(50),
titula char(50)
); 

INSERT INTO filament(proizvođač, boja, materijal, promjer, masa, datum_vrijeme_upisa) VALUES
('Plastika Trček', 'plava', 'PLA', 1.75, 1000, NOW()),
('Devil Design', 'ljubičasta', 'PETG', 2.85, 500, NOW()),
('ESUN', 'žuta', 'ABS', 1.75, 250, NOW());

INSERT INTO korisnik(email, password, titula) VALUES
('marko.tesija@gmail.com', UNHEX(SHA2('marko', 256)), 'admin'),
('maja.benkovic@gmail.com', UNHEX(SHA2('maja', 256)), 'user'),
('marko.kljajic@gmial.com', UNHEX(SHA2('kljaja', 256)), 'user');


SELECT * from korisnik;