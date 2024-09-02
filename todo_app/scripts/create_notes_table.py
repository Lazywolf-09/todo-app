import sqlite3

def create_notes_table():
    conn = sqlite3.connect('../database/todo.db')
    cursor = conn.cursor()

    # Create the notes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()
    print("Notes table created successfully.")

if __name__ == "__main__":
    create_notes_table()
