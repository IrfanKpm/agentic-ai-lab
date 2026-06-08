import sqlite3

conn = sqlite3.connect("company.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    created_at TEXT
)
""")

cursor.execute("""
INSERT INTO users (name,email,created_at)
VALUES
('John','john@test.com','2026-06-01'),
('Alice','alice@test.com','2026-06-03'),
('Bob','bob@test.com','2026-06-05')
""")

conn.commit()
conn.close()