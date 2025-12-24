# MySQL Database Setup Guide

This guide will help you set up MySQL for the Feedback Analyzer project.

## Prerequisites

1. **Install MySQL Server**
   - Download MySQL from [https://dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/)
   - Or install using package manager:
     - **Windows**: Download the installer or use Chocolatey: `choco install mysql`
     - **macOS**: `brew install mysql`
     - **Ubuntu/Debian**: `sudo apt install mysql-server`

2. **Install MySQL Workbench** (Optional but recommended)
   - Download from [https://dev.mysql.com/downloads/workbench/](https://dev.mysql.com/downloads/workbench/)

## Database Setup

### 1. Start MySQL Service

**Windows:**
```bash
net start mysql
```

**macOS/Linux:**
```bash
sudo systemctl start mysql
# or
brew services start mysql
```

### 2. Connect to MySQL

```bash
mysql -u root -p
```

### 3. Create Database and User

```sql
-- Create the database
CREATE DATABASE feedback_analyser CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create a dedicated user (recommended for production)
CREATE USER 'feedback_user'@'localhost' IDENTIFIED BY 'secure_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON feedback_analyser.* TO 'feedback_user'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;

-- Exit MySQL
EXIT;
```

### 4. Configure Environment Variables

Update the `.env` file in the Backend directory with your MySQL credentials:

```env
# Database Configuration
DB_HOST=localhost
DB_USER=feedback_user  # or 'root' if using root user
DB_PASSWORD=your_mysql_password
DB_NAME=feedback_analyser
DB_PORT=3306
```

## Application Setup

### 1. Install Python Dependencies

Navigate to the Backend directory and install dependencies:

```bash
cd Backend
pip install -r requirements.txt
```

### 2. Initialize Database Tables

The application will automatically create the required tables when you first run it. The tables include:

- `users` - User authentication and profile data
- `user_sessions` - JWT token management
- `user_analyses` - Stored feedback analyses

### 3. Run the Application

```bash
cd Backend
python app.py
```

The application will:
1. Connect to MySQL using the credentials in `.env`
2. Create the necessary tables if they don't exist
3. Start the Flask server on `http://localhost:5000`

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    name VARCHAR(255),
    provider VARCHAR(50) DEFAULT 'local',
    provider_id VARCHAR(255),
    avatar_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### User Sessions Table
```sql
CREATE TABLE user_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### User Analyses Table
```sql
CREATE TABLE user_analyses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    feedback TEXT NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## Troubleshooting

### Common Issues

1. **Connection Error**: Check if MySQL service is running
2. **Access Denied**: Verify username/password in `.env` file
3. **Database Not Found**: Ensure you've created the `feedback_analyser` database
4. **Port Issues**: Make sure port 3306 is available or change DB_PORT in `.env`

### Testing Connection

You can test your MySQL connection using this Python script:

```python
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

try:
    connection = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'feedback_analyser'),
        port=int(os.getenv('DB_PORT', 3306))
    )
    print("✅ MySQL connection successful!")
    connection.close()
except Exception as e:
    print(f"❌ MySQL connection failed: {e}")
```

## Security Recommendations

1. **Use a dedicated database user** instead of root
2. **Use strong passwords** for database users
3. **Keep your `.env` file secure** and never commit it to version control
4. **Enable SSL** for production deployments
5. **Regularly backup your database**

## Backup and Restore

### Backup
```bash
mysqldump -u feedback_user -p feedback_analyser > backup.sql
```

### Restore
```bash
mysql -u feedback_user -p feedback_analyser < backup.sql
```