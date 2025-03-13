import sqlite3

def show_tables():
    conn = sqlite3.connect('labease.db')
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\nDatabase Tables:")
    print("-" * 50)
    
    # For each table, get its schema
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        print("-" * 50)
        
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        # Print column information
        for col in columns:
            cid, name, type_, notnull, dflt_value, pk = col
            nullable = "NOT NULL" if notnull else "NULL"
            primary = "PRIMARY KEY" if pk else ""
            print(f"{name:20} {type_:15} {nullable:10} {primary}")
    
    conn.close()

if __name__ == "__main__":
    show_tables()
