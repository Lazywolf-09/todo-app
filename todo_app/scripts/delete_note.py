import sqlite3

def delete_note(note_id):
    conn = sqlite3.connect('../database/todo.db')
    cursor = conn.cursor()

    cursor.execute('''
    DELETE FROM notes
    WHERE id = ?
    ''', (note_id,))

    conn.commit()
    conn.close()
    print(f"Note ID {note_id} deleted successfully.")

if __name__ == "__main__":
    # Example usage: Deleting a note
    delete_note(note_id=1)
