import sqlite3

try:
    conn = sqlite3.connect('feedback_analyzer.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("✓ SQLite Database Connected Successfully!")
    print(f"Database: feedback_analyzer.db")
    print(f"Tables found: {len(tables)}")
    
    if tables:
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"  - {table[0]}: {count} records")
    
    conn.close()
except Exception as e:
    print(f"✗ Error: {e}")
