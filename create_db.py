from backend.database import create_tables
import sqlite3

# 1️⃣ Create the existing students table
create_tables()
print("Students table created successfully")

# 2️⃣ Create the report table for storing experiment attempts
conn = sqlite3.connect("lab.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS report(
    student TEXT,
    experiment TEXT,
    score INTEGER
)
""")
conn.commit()
conn.close()
print("Report table created successfully")
