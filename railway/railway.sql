CREATE DATABASE railway_db;
USE railway_db;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100),
  gmail VARCHAR(100),
  phone VARCHAR(20),
  password VARCHAR(100)
);

CREATE TABLE tickets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100),
  train_id INT,
  class VARCHAR(20),
  people INT
);
