import os
import sqlite3

# Define the database file path
DATABASE_FILE = 'instance/database.db'

def add_column_if_not_exists(conn, table_name, column_name, column_type):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]
    if column_name not in columns:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
        print(f"Added column {column_name} to {table_name} table.")

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE_FILE)

    # Add 'is_selected' column to 'application' table if it doesn't exist
    add_column_if_not_exists(conn, 'application', 'is_selected', 'BOOLEAN DEFAULT FALSE')

    # Add 'num_students' column to 'event' table if it doesn't exist
    add_column_if_not_exists(conn, 'event', 'num_students', 'INTEGER')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print("Database updated successfully!")

if __name__ == '__main__':
    main()
