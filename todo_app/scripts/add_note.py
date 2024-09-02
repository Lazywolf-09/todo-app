import sqlite3
from datetime import datetime

def add_note(title, content):
    # Connect to the SQLite database
    conn = sqlite3.connect('../database/todo.db')
    cursor = conn.cursor()

    # Get the current date and time
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert the note into the database
    cursor.execute('''
    INSERT INTO notes (title, content, created_at)
    VALUES (?, ?, ?)
    ''', (title, content, created_at))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print(f"Note '{title}' added successfully.")

if __name__ == "__main__":
    # Example usage: Adding a note
    add_note(
        title="Meeting Notes",
        content="Discuss the new project requirements and deadlines."
    )

