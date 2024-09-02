import sqlite3

def fetch_notes():
    # Connect to the SQLite database
    conn = sqlite3.connect('../database/todo.db')
    cursor = conn.cursor()

    # Fetch all notes from the database
    cursor.execute('SELECT * FROM notes')
    notes = cursor.fetchall()

    # Display the notes
    for note in notes:
        print(note)

    conn.close()

if __name__ == "__main__":
    fetch_notes()
