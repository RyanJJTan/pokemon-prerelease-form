import sqlite3
import random

DB_NAME = "participants.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS participants(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        trainer_id TEXT,
        contact TEXT,
        lucky_number INTEGER
    )
    """)

    conn.commit()
    conn.close()


def add_participant(name, trainer_id, contact):
    lucky_number = random.randint(1, 999)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "INSERT INTO participants (name, trainer_id, contact, lucky_number) VALUES (?, ?, ?, ?)",
        (name, trainer_id, contact, lucky_number)
    )

    conn.commit()
    conn.close()

    return lucky_number