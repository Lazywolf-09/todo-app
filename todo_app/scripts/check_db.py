# scripts/check_db.py
import sqlite3

def check_tables():
    conn = sqlite3.connect('../database/todo.db')
    cursor = conn.cursor()

    # Check the tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Tables in the database:")
    for table in tables:
        print(table[0])

    conn.close()

if __name__ == "__main__":
    check_tables()
