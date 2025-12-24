import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Create and return a SQLite database connection"""
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'feedback_analyzer.db')
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row  # Enable dict-like access
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

def init_db():
    """Initialize the database with required tables"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255),
                name VARCHAR(255),
                provider VARCHAR(50) DEFAULT 'local',
                provider_id VARCHAR(255),
                avatar_url VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create user_sessions table for storing JWT tokens
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token_hash VARCHAR(255) NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Create user_analyses table to store user's feedback analyses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                feedback_text TEXT NOT NULL,
                sentiment VARCHAR(20) NOT NULL,
                confidence FLOAT DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        connection.commit()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
    finally:
        connection.close()