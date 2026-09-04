-- Original local MySQL schema
CREATE DATABASE IF NOT EXISTS attendance_db;
USE attendance_db;
CREATE TABLE IF NOT EXISTS attendance (id INT AUTO_INCREMENT PRIMARY KEY, student_name VARCHAR(100), subject VARCHAR(100), total_classes INT, attended_classes INT, percentage DECIMAL(5,2), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
