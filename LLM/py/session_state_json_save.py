import json
from pathlib import Path
import streamlit as st

LLM_DIR = Path(__file__).resolve().parent.parent
JSON_DIR = LLM_DIR / "json"

# 저장할 JSON 파일의 경로를 지정합니다.
# count.json 파일을 LLM/json 폴더에서 사용합니다.
DATA_FILE = JSON_DIR / "count.json"

def load_count():
    JSON_DIR.mkdir(parents=True, exist_ok=True)

    # JSON 파일이 존재하는지 확인합니다.
    if DATA_FILE.exists():
        # 파일 내용을 문자열로 읽어옵니다.
        json_text = DATA_FILE.read_text(encoding="utf-8")

        # JSON 문자열을 Python 딕셔너리로 변환합니다.
        data = json.loads(json_text)

        # count 값이 있으면 반환하고, 없으면 0을 반환합니다.
        return data.get("count", 0)

    return 0

def save_count(count):
    data = {"count": count}

    # Python 딕셔너리를 JSON 문자열로 변환합니다.
    json_text = json.dumps(data, ensure_ascii=False, indent=2)

    # JSON 문자열을 파일에 저장합니다.
    DATA_FILE.write_text(json_text, encoding="utf-8")

# session_state의 count 값을 처음 한 번만 초기화합니다.
if "count" not in st.session_state:
    st.session_state.count = load_count()

st.title("JSON Count Save")

if st.button("증가"):
    st.session_state.count += 1
    save_count(st.session_state.count)

if st.button("초기화"):
    st.session_state.count = 0
    save_count(st.session_state.count)

st.write(f"현재 값: {st.session_state.count}")
