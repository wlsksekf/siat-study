# json_db.py

# JSON 파일 입출력을 위한 표준 라이브러리
import json

# 파일 경로를 객체 형태로 다루기 위한 라이브러리
from pathlib import Path

# Path는 파일 경로를 객체 형태로 다루기 위한 클래스입니다.
# JSON 파일의 경로를 Path 객체로 만들어 DB_FILE 변수에 저장합니다.
LLM_DIR = Path(__file__).resolve().parent.parent
JSON_DIR = LLM_DIR / "json"

# 저장할 JSON 파일의 경로를 지정합니다.
DB_FILE = JSON_DIR / "chat_history.json"

# JSON 파일 초기화 함수
def init_db():
    # 폴더가 없으면 생성하는 로직 추가
    if not JSON_DIR.exists():
        JSON_DIR.mkdir(parents=True, exist_ok=True)

    # DB_FILE이 존재하지 않으면 새 JSON 파일을 생성
    if not DB_FILE.exists():
        initial_data = {
            "messages": [],
            "conversation_id": None
        }
        DB_FILE.write_text(
            json.dumps(initial_data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

# 전체 JSON 데이터 불러오기 함수
def load_data():
    init_db()
    text = DB_FILE.read_text(encoding="utf-8")

    data = json.loads(text)

    if "conversation_id" not in data:
        data["conversation_id"] = None

    if "messages" not in data:
        data["messages"] = []

    return data


# 전체 JSON 데이터 저장 함수
def save_data(data):
    DB_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


# 전체 메시지 불러오기 함수
def load_messages():
    data = load_data()
    return data["messages"]


# 메시지 1개 저장 함수
def save_message(role, content):
    data = load_data()
    data["messages"].append({
        "role": role,
        "content": content
    })
    save_data(data)

# conversation_id 저장 함수
def save_conversation_id(conversation_id):
    data = load_data()
    data["conversation_id"] = conversation_id
    save_data(data)


# conversation_id 불러오기 함수
def load_conversation_id():
    data = load_data()
    return data["conversation_id"]


# 전체 대화 삭제 함수
def clear_messages():
    data = load_data()

    # conversation_id는 유지하고 messages만 초기화
    data["messages"] = []

    save_data(data)