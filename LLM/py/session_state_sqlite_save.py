import sqlite3
from pathlib import Path

import streamlit as st


LLM_DIR = Path(__file__).resolve().parent.parent
DB_DIR = LLM_DIR / "db"
DB_PATH = DB_DIR / "count.db"


def init_db():
    DB_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS counter (
            id INTEGER PRIMARY KEY,
            count INTEGER
        )
        """
    )

    cursor.execute("SELECT count FROM counter WHERE id = 1")
    row = cursor.fetchone()

    if row is None:
        cursor.execute("INSERT INTO counter (id, count) VALUES (1, 0)")
        conn.commit()
        count = 0
    else:
        count = row[0]

    conn.close()
    return count


def save_count(count):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE counter SET count = ? WHERE id = 1", (count,))
    conn.commit()
    conn.close()


if "count" not in st.session_state:
    st.session_state.count = init_db()

st.title("SQLite Count Save")

if st.button("증가"):
    st.session_state.count += 1
    save_count(st.session_state.count)

st.write(f"현재 count: {st.session_state.count}")
