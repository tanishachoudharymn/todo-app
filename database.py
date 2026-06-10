import sqlite3

def init_db():
    conn = sqlite3.connect("tasks.db")
    conn.execute("DROP TABLE IF EXISTS tasks")
    conn.execute("""
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            done BOOLEAN DEFAULT 0,
            due_date TEXT DEFAULT NULL
        )
    """)
    conn.commit()
    conn.close()