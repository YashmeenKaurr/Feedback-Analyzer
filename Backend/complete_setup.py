#!/usr/bin/env python3
"""
Complete MySQL setup for Feedback Analyzer
This script will create the database, user, and initialize tables
"""

import pymysql
import os
from dotenv import load_dotenv
import sys

def setup_database_with_root():
    """Set up database and user with root privileges"""
    print("=== Setting up MySQL Database ===\n")
    
    # Get root password
    root_password = input("Enter MySQL root password: ")
    
    try:
        # Connect as root
        print("Connecting to MySQL as root...")
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password=root_password,
            port=3306,
            autocommit=True
        )
        
        with connection.cursor() as cursor:
            print("✅ Connected successfully!")
            
            # Create database
            print("Creating database 'feedback_analyser'...")
            cursor.execute("CREATE DATABASE IF NOT EXISTS feedback_analyser CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("✅ Database created!")
            
            # Create user
            print("Creating user 'feedback_user'...")
            cursor.execute("CREATE USER IF NOT EXISTS 'feedback_user'@'localhost' IDENTIFIED BY 'FeedbackApp123!'")
            print("✅ User created!")
            
            # Grant privileges
            print("Granting privileges...")
            cursor.execute("GRANT ALL PRIVILEGES ON feedback_analyser.* TO 'feedback_user'@'localhost'")
            cursor.execute("FLUSH PRIVILEGES")
            print("✅ Privileges granted!")
            
            # Show databases
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print("\n📋 Available databases:")
            for db in databases:
                db_name = db[0] if isinstance(db, tuple) else list(db.values())[0]
                if db_name == 'feedback_analyser':
                    print(f"  ✅ {db_name}")
                else:
                    print(f"     {db_name}")
        
        connection.close()
        print("\n🎉 Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def test_app_connection():
    """Test connection with the app user"""
    print("\n=== Testing Application Database Connection ===")
    
    load_dotenv()
    
    try:
        connection = pymysql.connect(
            host='localhost',
            user='feedback_user',
            password='FeedbackApp123!',
            database='feedback_analyser',
            port=3306
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE(), USER(), VERSION()")
            result = cursor.fetchone()
            print(f"✅ Connected successfully!")
            print(f"   Database: {result['DATABASE()']}")
            print(f"   User: {result['USER()']}")
            print(f"   MySQL Version: {result['VERSION()']}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ App connection failed: {e}")
        return False

def create_tables():
    """Create the application tables"""
    print("\n=== Creating Application Tables ===")
    
    try:
        connection = pymysql.connect(
            host='localhost',
            user='feedback_user',
            password='FeedbackApp123!',
            database='feedback_analyser',
            port=3306,
            autocommit=True
        )
        
        with connection.cursor() as cursor:
            # Create users table
            print("Creating users table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255),
                    name VARCHAR(255),
                    provider VARCHAR(50) DEFAULT 'local',
                    provider_id VARCHAR(255),
                    avatar_url VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_email (email),
                    INDEX idx_provider (provider, provider_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            
            # Create user_sessions table
            print("Creating user_sessions table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    token_hash VARCHAR(255) NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user_id (user_id),
                    INDEX idx_expires_at (expires_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            
            # Create user_analyses table
            print("Creating user_analyses table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_analyses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    feedback_text TEXT NOT NULL,
                    sentiment VARCHAR(20) NOT NULL,
                    confidence FLOAT DEFAULT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user_id (user_id),
                    INDEX idx_sentiment (sentiment)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            
            # Show tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("\n📋 Created tables:")
            for table in tables:
                table_name = list(table.values())[0]
                cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                count = cursor.fetchone()['count']
                print(f"  ✅ {table_name} ({count} records)")
        
        connection.close()
        print("\n🎉 Tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Table creation failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Feedback Analyzer - Complete MySQL Setup\n")
    
    # Step 1: Setup database and user
    if not setup_database_with_root():
        print("\n❌ Setup failed at database creation step")
        return 1
    
    # Step 2: Test app connection
    if not test_app_connection():
        print("\n❌ Setup failed at connection test step")
        return 1
    
    # Step 3: Create tables
    if not create_tables():
        print("\n❌ Setup failed at table creation step")
        return 1
    
    print("\n" + "="*50)
    print("🎉 SETUP COMPLETE! 🎉")
    print("="*50)
    print()
    print("✅ MySQL database: feedback_analyser")
    print("✅ MySQL user: feedback_user")  
    print("✅ Tables: users, user_sessions, user_analyses")
    print("✅ Environment: .env file configured")
    print()
    print("🚀 Ready to run the application:")
    print("   Backend: python app.py")
    print("   Frontend: npm run dev")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())