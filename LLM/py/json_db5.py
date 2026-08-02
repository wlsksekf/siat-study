import json
from pathlib import Path


LLM_DIR = Path(__file__).resolve().parent.parent
JSON_DIR = LLM_DIR / "json"
DB_FILE = JSON_DIR / "chat_history5.json"


def init_db():
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    if not DB_FILE.exists():
        DB_FILE.write_text("[]", encoding="utf-8")


def load_messages():
    init_db()
    if not DB_FILE.exists():
        return []

    with DB_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_message(role, content):
    messages = load_messages()
    messages.append({"role": role, "content": content})

    with DB_FILE.open("w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


def clear_messages():
    init_db()
    DB_FILE.write_text("[]", encoding="utf-8")
