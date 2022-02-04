import sqlite3
from sqlite3 import Error

def create_connection():
    db_file = "database.db"
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)    
    return conn


class TodosSQLite:
    def __init__(self):
        try:
            self.conn = create_connection()
            self.cur = self.conn.cursor()
            try:
                self.cur.execute("SELECT * FROM todos")
                self.todos_sqlite = self.cur.fetchall()
                self.conn.close()
            except Error:
                self.cur.execute('''CREATE TABLE IF NOT EXISTS todos (
                    id integer PRIMARY KEY, 
                    title VARCHAR(250) NOT NULL, 
                    description text NOT NULL,
                    done Boolean);''')
                self.todos_sqlite = []
        except FileNotFoundError:
            self.todos_sqlite = []

    def all(self):
        self.conn = create_connection()
        self.cur = self.conn.cursor()
        self.cur.execute(f"SELECT * FROM todos")
        self.todos_sqlite = self.cur.fetchall()
        self.conn.close()
        return self.todos_sqlite
    
    def get(self, id):
        self.conn = create_connection()
        self.cur = self.conn.cursor()
        self.cur.execute(f"SELECT * FROM todos WHERE id={id}")
        self.row = self.cur.fetchone()
        self.conn.close()
        self.dict = {"id": self.row[0], "title": self.row[1], "description": self.row[2], "done": self.row[3]}
        return self.dict
    
    def create(self, data):
        data.pop('csrf_token')
        self.conn = create_connection()
        self.cur = self.conn.cursor()
        sql = """INSERT INTO todos (title, description, done) VALUES (?,?,?)"""
        values = []
        for val in data.values():
            values.append(val)
        self.cur.execute(sql,values)
        self.conn.commit()
        self.conn.close()
        return self.cur.lastrowid

    def update(self, id, data):
        data.pop('csrf_token')
        self.parameters = [f"{k} = ?" for k in data.keys()]
        self.parameters = ", ".join(self.parameters)
        self.values = tuple(v for v in data.values())
        self.values += (id, )

        self.sql = f''' UPDATE todos
                    SET {self.parameters}
                    WHERE id = ?'''
        self.conn = create_connection()            
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(self.sql, self.values)
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print(e)

todos_sql = TodosSQLite()


"""
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

conn = create_connection()
cur = conn.cursor()
cur.execute('''INSERT INTO todos (title, description, done) VALUES ("test3","test test","True")''')
conn.commit()
conn.close()
"""