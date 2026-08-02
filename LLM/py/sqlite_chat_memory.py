import sqlite3
from pathlib import Path


LLM_DIR = Path(__file__).resolve().parent.parent
DB_DIR = LLM_DIR / "db"
DB_PATH = DB_DIR / "chat_memory.db"


def _connect() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_chat_messages_thread_id_id
            ON chat_messages (thread_id, id)
            """
        )


def load_messages(thread_id: str) -> list[dict[str, str]]:
    init_db()
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT role, content
            FROM chat_messages
            WHERE thread_id = ?
            ORDER BY id
            """,
            (thread_id,),
        ).fetchall()
    return [{"role": row["role"], "content": row["content"]} for row in rows]


def list_threads(limit: int = 30) -> list[dict[str, str | int]]:
    init_db()
    with _connect() as conn:
        rows = conn.execute(
            """
            WITH ranked_messages AS (
                SELECT
                    thread_id,
                    role,
                    content,
                    created_at,
                    id,
                    ROW_NUMBER() OVER (
                        PARTITION BY thread_id
                        ORDER BY id DESC
                    ) AS rn,
                    COUNT(*) OVER (
                        PARTITION BY thread_id
                    ) AS message_count
                FROM chat_messages
            )
            SELECT
                thread_id,
                role,
                content,
                created_at,
                message_count
            FROM ranked_messages
            WHERE rn = 1
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [
        {
            "thread_id": row["thread_id"],
            "role": row["role"],
            "content": row["content"],
            "created_at": row["created_at"],
            "message_count": row["message_count"],
        }
        for row in rows
    ]


def save_message(thread_id: str, role: str, content: str) -> None:
    init_db()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO chat_messages (thread_id, role, content)
            VALUES (?, ?, ?)
            """,
            (thread_id, role, content),
        )


def clear_messages(thread_id: str) -> None:
    init_db()
    with _connect() as conn:
        conn.execute(
            "DELETE FROM chat_messages WHERE thread_id = ?",
            (thread_id,),
        )
