#!/usr/bin/env python3
"""
Database initialization script for Feedback Analyzer
Run this script to set up the MySQL database and tables
"""

import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import init_db, get_db_connection
from dotenv import load_dotenv

def test_connection():
    """Test the database connection"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ MySQL connection successful!")
            print(f"   MySQL version: {version['VERSION()']}")
            
            cursor.execute("SELECT DATABASE()")
            database = cursor.fetchone()
            print(f"   Connected to database: {database['DATABASE()']}")
        
        connection.close()
        return True
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        print("\nPlease check:")
        print("1. MySQL server is running")
        print("2. Database credentials in .env file are correct")
        print("3. Database 'feedback_analyser' exists")
        return False

def main():
    """Main function to initialize the database"""
    print("=== Feedback Analyzer Database Setup ===\n")
    
    # Load environment variables
    load_dotenv()
    
    # Test connection first
    print("Testing database connection...")
    if not test_connection():
        return 1
    
    print("\nInitializing database tables...")
    try:
        init_db()
        print("✅ Database tables created successfully!")
        print("\nTables created:")
        print("- users (user authentication and profiles)")
        print("- user_sessions (JWT token management)")
        print("- user_analyses (feedback analysis history)")
        
        # Verify tables were created
        print("\nVerifying tables...")
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"Found {len(tables)} tables:")
            for table in tables:
                table_name = list(table.values())[0]
                cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                count = cursor.fetchone()['count']
                print(f"  - {table_name} ({count} records)")
        
        connection.close()
        print("\n🎉 Database setup completed successfully!")
        print("\nYou can now run the application with: python app.py")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())