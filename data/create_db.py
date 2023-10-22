import sqlite3
def create():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id           INTEGER PRIMARY KEY
                         NOT NULL
                         UNIQUE,
    phone_number TEXT,
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
        id       INTEGER PRIMARY KEY AUTOINCREMENT
                        NOT NULL,
        title    TEXT    NOT NULL,
        price    INTEGER NOT NULL,
        category TEXT    NOT NULL
                        REFERENCES categories (id) ON UPDATE CASCADE
    );
""")