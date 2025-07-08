import sqlite3
from contextlib import closing

DB_NAME = 'slots.db'


def init_db():
    with closing(sqlite3.connect(DB_NAME)) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS slots (
            user_id INTEGER,
            business_center TEXT,
            date TEXT,
            time TEXT,
            link TEXT,
            UNIQUE(business_center, date, time)
            )"""
        )
        conn.commit()


def add_slot(user_id: int, business_center: str, date: str, time: str, link: str) -> bool:
    try:
        with closing(sqlite3.connect(DB_NAME)) as conn:
            conn.execute(
                "INSERT INTO slots (user_id, business_center, date, time, link) VALUES (?, ?, ?, ?, ?)",
                (user_id, business_center, date, time, link),
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def get_slots(business_center: str, date: str):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.execute(
            "SELECT user_id, time, link FROM slots WHERE business_center = ? AND date = ? ORDER BY time",
            (business_center, date),
        )
        return cur.fetchall()


def get_user_slots(user_id: int, business_center: str, date: str):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.execute(
            "SELECT time, link FROM slots WHERE user_id = ? AND business_center = ? AND date = ? ORDER BY time",
            (user_id, business_center, date),
        )
        return cur.fetchall()


def remove_slot(business_center: str, date: str, time: str):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        conn.execute(
            "DELETE FROM slots WHERE business_center = ? AND date = ? AND time = ?",
            (business_center, date, time),
        )
        conn.commit()

