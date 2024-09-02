# scripts/initialize_db.py
import sqlite3

def create_tables():
    # Connect to the SQLite database or create it if it doesn't exist
    conn = sqlite3.connect('../database/todo.db')
    cursor = conn.cursor()

    # Create a table for tasks
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        due_date TEXT,
        reminder_set BOOLEAN,
        reminder_time TEXT,
        status TEXT DEFAULT 'Pending'
    )
    ''')

    # Create a table for notes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT,
        created_at TEXT
    )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
