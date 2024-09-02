
import sqlite3
from datetime import datetime

def trigger_alarm():
    print("Beep! Beep! Beep!")  # This is your alarm sound logic

def check_reminders():
    # Connect to the SQLite database
    conn = sqlite3.connect('../database/todo.db')
    cursor = conn.cursor()

    # Get the current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Checking reminders...\nCurrent time: {current_time}")

    # Check for reminders due at or before the current time and still pending
    cursor.execute('''
    SELECT title, reminder_time FROM tasks
    WHERE reminder_set = 1 AND reminder_time <= ? AND status = 'Pending'
    ''', (current_time,))
    
    reminders_due = cursor.fetchall()

    if reminders_due:
        for reminder in reminders_due:
            print(f"Reminder: {reminder[0]} is due now (at {reminder[1]})!")
            trigger_alarm()

            # Mark the task as 'Completed' or 'Reminded' to prevent further beeps
            cursor.execute('''
            UPDATE tasks
            SET status = 'Completed'
            WHERE title = ?
            ''', (reminder[0],))
            
            conn.commit()
    else:
        print("No reminders due at this time.")

    conn.close()

if __name__ == "__main__":
    check_reminders()
