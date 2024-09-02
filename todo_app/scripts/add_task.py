import sqlite3

def add_task(title, description, due_date, reminder_set=False, reminder_time=None):
    # Connect to the SQLite database
    conn = sqlite3.connect('../database/todo.db')
    cursor = conn.cursor()

    # Insert the task into the database
    cursor.execute('''
    INSERT INTO tasks (title, description, due_date, reminder_set, reminder_time, status)
    VALUES (?, ?, ?, ?, ?, 'Pending')
    ''', (title, description, due_date, reminder_set, reminder_time))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print(f"Task '{title}' added successfully.")
from datetime import datetime, timedelta

if __name__ == "__main__":
    # Set the reminder time to 2 minutes from now
    reminder_time = datetime.now() + timedelta(minutes=2)
    
    # Use the add_task function to add a test task
    add_task(
        title="Quick Test Reminder",
        description="This reminder is for testing purposes.",
        due_date=reminder_time.strftime("%Y-%m-%d %H:%M:%S"),
        reminder_set=True,
        reminder_time=reminder_time.strftime("%Y-%m-%d %H:%M:%S")
    )
