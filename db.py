import sqlite3

db_name = 'db.sqlite'

conn = None
cursor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()


def do(query):
    cursor.execute(query)
    conn.commit()

def create_tables():
    open()
    cursor.execute('PRAGMA foreign_keys=on')
    do('''CREATE TABLE IF NOT EXISTS users (
       id INTEGER PRIMARY KEY,
       login VARCHAR,
       password VARCHAR)
    ''')
    
    do('''CREATE TABLE IF NOT EXISTS categories (
       id INTEGER PRIMARY KEY,
       name VARCHAR )
    ''')

    do('''CREATE TABLE IF NOT EXISTS news (
              id INTEGER PRIMARY KEY,
              title VARCHAR,
              description VARCHAR,
              image VARCHAR,
              class_id INTEGER,
                author_id INTEGER,
        FOREIGN KEY (class_id) REFERENCES categories (id),
        FOREIGN KEY (author_id) REFERENCES users (id)
       )
    ''')
    close()

def drop_table():
    open()
    do('DROP TABLE IF EXISTS news')
    do('DROP TABLE IF EXISTS categories')
    do('DROP TABLE IF EXISTS users')
    close()

def insert_test_data():
    open()
    cursor.execute('''INSERT INTO users (login, password) VALUES (?,?)''', ['admin', 'admin'])
    conn.commit()

    cursor.execute('''INSERT INTO categories (name) VALUES (?)''', ['sport'])
    conn.commit()

    cursor.execute('''INSERT INTO news 
                   (title, description, image, class_id,author_id ) 
                   VALUES (?, ?,?,?,?)''', ['NEWS TITLE',
                                             "descrosakfokdsf", 
                                            '2asd', 
                                            '1',
                                            '1',
                                            ])
    conn.commit()

    close()

def show_tables():
    open()
    cursor.execute('''SELECT * FROM users''')
    print(cursor.fetchall())
    
    cursor.execute('''SELECT * FROM categories''')
    print(cursor.fetchall())

    cursor.execute('''SELECT * FROM news''')
    print(cursor.fetchall())
    close()

def get_all_news():
    open()
    cursor.execute('''SELECT news.id, news.title, news.description, categories.name, users.login, news.image
                   FROM news INNER JOIN categories 
                   ON news.class_id == categories.id
                INNER JOIN users ON news.author_id == users.id''')
    return cursor.fetchall()

def get_news_by_id(id):
    open()
    cursor.execute('''SELECT news.title, news.description, categories.name, users.login
                   FROM news INNER JOIN categories 
                   ON news.class_id == categories.id
                INNER JOIN users ON news.author_id == users.id WHERE news.id == (?)''', [id])
    return cursor.fetchall()

def add_news(title, description, image, class_id, author_id):
    open()
    cursor.execute('''INSERT INTO news 
                   (title, description, image, class_id,author_id ) 
                   VALUES (?, ?, ?, ?, ?)''', [title, description, image, class_id, author_id])
    conn.commit()
    close()

# drop_table()
# create_tables()
# insert_test_data()
# show_tables()
# add_news('12eawd', '123wd', '1asd21', '1', '1')
# news = get_all_news()
# print(news)