import sqlite3
import sys

db_path = 'feedback_analyzer.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=" * 60)
print("SQLite Interactive Shell - Feedback Analyzer Database")
print("=" * 60)
print("Type SQL queries to execute. Type 'tables' to show all tables.")
print("Type '.schema TABLE_NAME' to show table structure.")
print("Type 'exit' or 'quit' to exit.\n")

while True:
    try:
        query = input("sqlite> ").strip()
        
        if not query:
            continue
        
        if query.lower() in ['exit', 'quit']:
            print("Exiting...")
            break
        
        if query.lower() == 'tables':
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = cursor.fetchall()
            print("\nTables in database:")
            for table in tables:
                print(f"  - {table[0]}")
            print()
            continue
        
        if query.lower().startswith('.schema'):
            parts = query.split()
            if len(parts) > 1:
                table_name = parts[1]
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                print(f"\nSchema for '{table_name}':")
                for col in columns:
                    print(f"  {col[1]}: {col[2]}")
                print()
            else:
                print("Usage: .schema TABLE_NAME")
            continue
        
        # Execute the query
        cursor.execute(query)
        
        # Check if it's a SELECT query
        if query.upper().startswith('SELECT'):
            results = cursor.fetchall()
            if results:
                # Get column names
                cols = [description[0] for description in cursor.description]
                print("\n" + " | ".join(cols))
                print("-" * 60)
                for row in results:
                    print(" | ".join(str(val) if val is not None else "NULL" for val in row))
                print(f"\n({len(results)} rows)\n")
            else:
                print("\nNo results\n")
        else:
            conn.commit()
            print(f"✓ Command executed successfully\n")
    
    except Exception as e:
        print(f"Error: {e}\n")

conn.close()
