import sqlite3

def fetch_tasks():
    # Connect to the SQLite database
    conn = sqlite3.connect('../database/todo.db')
    cursor = conn.cursor()

    # Fetch all tasks from the database
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()

    # Display the tasks
    for task in tasks:
        print(task)

    conn.close()

if __name__ == "__main__":
    fetch_tasks()
import sqlite3

def fetch_tasks():
    conn = sqlite3.connect('../database/todo.db')
    cursor = conn.cursor()

    cursor.execute('SELECT title, status FROM tasks')
    tasks = cursor.fetchall()

    for task in tasks:
        print(f"Task: {task[0]}, Status: {task[1]}")

    conn.close()

if __name__ == "__main__":
    fetch_tasks()
