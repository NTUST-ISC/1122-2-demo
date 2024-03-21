from sqlite3 import *

conn = connect('attackMe.db')
cursor = conn.cursor()

def main():
    conn.execute('''Create table if not exists user(
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        account TEXT NOT NULL,
                        password TEXT NOT NULL
                    )''')
    conn.commit()
    conn.execute('''Create table if not exists post(
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        content TEXT NOT NULL,
                        user_id INTEGER,
                        FOREIGN KEY(user_id) REFERENCES user(id)
                    )''')
    conn.commit()

def exec(command):
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute(command)
    return cursor.fetchall()

def dict_factory(cursor, row):
    dict = {}
    for idx, col in enumerate(cursor.description):
        dict[col[0]] = row[idx]
    return dict

if __name__ == "__main__":
    main()