import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Kullanıcı tablosu oluşturuyoruz
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
