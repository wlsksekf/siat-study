from pathlib import Path
import json

DB_FILE = Path("chat_history.json")


def load_messages():
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
    DB_FILE.write_text("[]", encoding="utf-8")