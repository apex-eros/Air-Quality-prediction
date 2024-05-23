import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    email TEXT,
                    password TEXT
                )''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
