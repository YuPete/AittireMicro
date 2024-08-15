CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Aauth123';
--create actual user to access data table 

CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';
--auth.* grants all privileges to all data tables on auth database

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    --explanation
    --id: name of first column
    --INT: Data type of id column is int
    --NOT NULL id column cannot contain NULL values
    --id is auto incremented
    -- PRIMARY KEY: constraint on id column to ensure unique id's 
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user (email,password) VALUES ('pyu0919@gmail.com', 'Admin123'); 
--a user entry 
