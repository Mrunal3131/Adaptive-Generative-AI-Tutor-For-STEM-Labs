import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "lab.db")

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT UNIQUE,
        password TEXT,
        class_group TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS reports(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT,
        subject TEXT,
        experiment TEXT,
        score INTEGER,
        hints_used INTEGER,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()
