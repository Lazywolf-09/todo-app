import sqlite3

def create_db():
    conn = sqlite3.connect('database/todo.db')
    cursor = conn.cursor()

    # Create tasks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        due_date TEXT,
        reminder_set INTEGER DEFAULT 0,
        reminder_time TEXT,
        status TEXT DEFAULT 'Pending'
    )
    ''')

    # Create notes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT,
        created_at TEXT
    )
    ''')

    conn.commit()
    conn.close()
    print("Database and tables created successfully.")

if __name__ == "__main__":
    create_db()
