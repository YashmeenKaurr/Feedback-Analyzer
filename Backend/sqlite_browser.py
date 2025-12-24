import sqlite3
import sys

def sqlite_browser():
    """Interactive SQLite database browser"""
    db_path = 'feedback_analyzer.db'
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("\n" + "="*60)
        print("SQLite Database Browser - feedback_analyzer.db")
        print("="*60)
        
        # Show all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"\nTables ({len(tables)}):")
        for i, table in enumerate(tables, 1):
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  {i}. {table_name} ({count} rows)")
        
        print("\n" + "="*60)
        
        while True:
            print("\nCommands:")
            print("  1. View table schema")
            print("  2. View table data")
            print("  3. Run custom query")
            print("  4. Exit")
            
            choice = input("\nEnter command (1-4): ").strip()
            
            if choice == '1':
                print("\nAvailable tables:")
                for i, table in enumerate(tables, 1):
                    print(f"  {i}. {table[0]}")
                
                table_choice = input("Select table (number): ").strip()
                try:
                    table_idx = int(table_choice) - 1
                    if 0 <= table_idx < len(tables):
                        table_name = tables[table_idx][0]
                        cursor.execute(f"PRAGMA table_info({table_name})")
                        columns = cursor.fetchall()
                        print(f"\n{table_name} Schema:")
                        print("-" * 60)
                        for col in columns:
                            print(f"  {col[1]:<20} {col[2]:<15} (pk={col[5]})")
                except ValueError:
                    print("Invalid selection")
            
            elif choice == '2':
                print("\nAvailable tables:")
                for i, table in enumerate(tables, 1):
                    print(f"  {i}. {table[0]}")
                
                table_choice = input("Select table (number): ").strip()
                try:
                    table_idx = int(table_choice) - 1
                    if 0 <= table_idx < len(tables):
                        table_name = tables[table_idx][0]
                        cursor.execute(f"SELECT * FROM {table_name}")
                        rows = cursor.fetchall()
                        
                        if rows:
                            print(f"\n{table_name} Data:")
                            print("-" * 60)
                            cols = [description[0] for description in cursor.description]
                            print(" | ".join(f"{col:<15}" for col in cols))
                            print("-" * 60)
                            for row in rows:
                                print(" | ".join(f"{str(val):<15}" for val in row))
                        else:
                            print(f"No data in {table_name}")
                except ValueError:
                    print("Invalid selection")
            
            elif choice == '3':
                query = input("\nEnter SQL query: ").strip()
                try:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    
                    if rows:
                        cols = [description[0] for description in cursor.description]
                        print("\nResults:")
                        print("-" * 60)
                        print(" | ".join(f"{col:<15}" for col in cols))
                        print("-" * 60)
                        for row in rows:
                            print(" | ".join(f"{str(val):<15}" for val in row))
                    else:
                        print("No results")
                except Exception as e:
                    print(f"Error: {e}")
            
            elif choice == '4':
                print("Exiting...")
                break
            
            else:
                print("Invalid command")
        
        conn.close()
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    sqlite_browser()
