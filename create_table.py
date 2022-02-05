import sqlite3
from sqlite3 import Error

def create_table():
    conn = None
    db_file = "database.db"
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS todos (
            id integer PRIMARY KEY, 
            title VARCHAR(250) NOT NULL, 
            description text NOT NULL,
            done Boolean);''')
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

create_table()