import sqlite3

def view_notes():
    conn = sqlite3.connect('../database/todo.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, title, content, created_at FROM notes')
    notes = cursor.fetchall()

    for note in notes:
        print(f"ID: {note[0]}\nTitle: {note[1]}\nContent: {note[2]}\nCreated At: {note[3]}\n")

    conn.close()

if __name__ == "__main__":
    view_notes()
