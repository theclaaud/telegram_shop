import sqlite3
def create():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id           INTEGER PRIMARY KEY
                         NOT NULL
                         UNIQUE,
    is_admin     BOOLEAN DEFAULT (0)
);
""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id    INTEGER PRIMARY KEY AUTOINCREMENT
                    NOT NULL,
        title TEXT    UNIQUE
                    NOT NULL
    );
""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS lots (
    id          INTEGER PRIMARY KEY AUTOINCREMENT
                        NOT NULL,
    title       TEXT    NOT NULL,
    description TEXT,
    price       INTEGER NOT NULL,
    image_id    INTEGER,
    category    TEXT    NOT NULL
                        REFERENCES categories (id) ON UPDATE CASCADE
    );
""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id       INTEGER PRIMARY KEY AUTOINCREMENT
                        NOT NULL
                        UNIQUE,
        buyer_id INTEGER REFERENCES users (id) 
                        NOT NULL,
        lot_id   INTEGER REFERENCES lots (id) 
                        NOT NULL,
        summ     INTEGER NOT NULL
    );
""")