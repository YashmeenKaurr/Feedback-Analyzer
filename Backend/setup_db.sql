-- Create database
CREATE DATABASE IF NOT EXISTS feedback_analyser 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user
CREATE USER IF NOT EXISTS 'feedback_user'@'localhost' IDENTIFIED BY 'FeedbackApp123!';

-- Grant privileges
GRANT ALL PRIVILEGES ON feedback_analyser.* TO 'feedback_user'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;

-- Show databases to confirm
SHOW DATABASES;