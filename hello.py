import sqlite3


conn = sqlite3.connect("any.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
)
""")

conn.commit()

cursor.execute(
    "INSERT INTO users(name, age) VALUES(?, ?)",
    ("Laziz", 20)
)

conn.commit()

cursor.execute("SELECT * FROM users")

users = cursor.fetchall()

print("Users:")
for user in users:
    print(user)

cursor.execute(
    "UPDATE users SET age=? WHERE id=?",
    (25, 1)
)

conn.commit()

cursor.execute(
    "DELETE FROM users WHERE id=?",
    (1,)
)

conn.commit()

conn.close()