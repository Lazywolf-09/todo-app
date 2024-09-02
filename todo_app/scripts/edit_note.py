import sqlite3

def edit_note(note_id, new_title, new_content):
    conn = sqlite3.connect('../database/todo.db')
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE notes
    SET title = ?, content = ?
    WHERE id = ?
    ''', (new_title, new_content, note_id))

    conn.commit()
    conn.close()
    print(f"Note ID {note_id} updated successfully.")

if __name__ == "__main__":
    # Example usage: Editing a note
    edit_note(
        note_id=1,
        new_title="Updated Meeting Notes",
        new_content="Discussed updated project deadlines."
    )
