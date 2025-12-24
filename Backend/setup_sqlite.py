import sqlite3
import os
from datetime import datetime
import bcrypt

def init_sqlite_db():
    """Initialize SQLite database for testing"""
    db_path = 'feedback_analyzer.db'
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    
    # Create new database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable dict-like access
    cursor = conn.cursor()
    
    try:
        # Create users table
        cursor.execute("""
            CREATE TABLE users (
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
        
        # Create user_sessions table
        cursor.execute("""
            CREATE TABLE user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token_hash VARCHAR(255) NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Create user_analyses table
        cursor.execute("""
            CREATE TABLE user_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                feedback_text TEXT NOT NULL,
                sentiment VARCHAR(20) NOT NULL,
                confidence FLOAT DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Create test user
        password_hash = bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("""
            INSERT INTO users (email, password_hash, name, provider)
            VALUES ('test@example.com', ?, 'Test User', 'local')
        """, (password_hash,))
        
        conn.commit()
        
        # Show tables and counts
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("✅ SQLite Database created successfully!")
        print(f"📍 Database location: {os.path.abspath(db_path)}")
        print("📋 Created tables:")
        
        for table in tables:
            table_name = table['name']
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = cursor.fetchone()['count']
            print(f"  ✅ {table_name} ({count} records)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating SQLite database: {e}")
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    print("🚀 Setting up SQLite database for testing...")
    success = init_sqlite_db()
    if success:
        print("✅ Database setup complete!")
        print("👤 Test user created: test@example.com / password123")
    else:
        print("❌ Database setup failed!")