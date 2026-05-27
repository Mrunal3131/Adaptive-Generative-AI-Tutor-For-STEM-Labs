import sqlite3

def save_attempt(student, experiment, score):
    conn = sqlite3.connect("lab.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS report(
        student TEXT,
        experiment TEXT,
        score INTEGER
    )""")
    c.execute("INSERT INTO report VALUES (?,?,?)", (student, experiment, score))
    conn.commit()
    conn.close()
