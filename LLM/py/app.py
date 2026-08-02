import streamlit as st
from dotenv import load_dotenv
import os

from json_db import (
    load_messages,
    save_message,
    clear_messages,
    init_db,
    save_conversation_id,
    load_conversation_id
)
from openai_service import create_openai_client, get_ai_response, create_conversation

import truststore

# SSL 설정 및 환경 변수 로드
truststore.inject_into_ssl()
load_dotenv()

# 앱 시작 시 JSON 파일 초기화
init_db()

# ----------------------
# 사이드바
# ----------------------
with st.sidebar:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    st.write("### 설정")
    st.write("대화 내용은 JSON 파일에 저장됩니다")

    if st.button("대화 초기화"):
        clear_messages()
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        save_message("assistant", "How can I help you?")
        # 대화 초기화 시 conversation_id도 새로 생성하도록 삭제
        if "conversation_id" in st.session_state:
            del st.session_state["conversation_id"]
        save_conversation_id(None)
        st.rerun()

# ----------------------
# 제목 및 초기 대화 로드
# ----------------------
st.title("💬 Chatbot")
st.caption("🚀 2026 OpenAI Responses API Standard")

if "messages" not in st.session_state:
    db_messages = load_messages()
    if not db_messages:
        first_msg = {"role": "assistant", "content": "How can I help you?"}
        st.session_state["messages"] = [first_msg]
        save_message("assistant", "How can I help you?")
    else:
        st.session_state["messages"] = db_messages

# 대화 출력
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# ----------------------
# 사용자 입력 및 응답 처리
# ----------------------
if prompt := st.chat_input("메시지를 입력하세요"):
    if not openai_api_key:
        st.info("API Key를 설정해주세요.")
        st.stop()

    # 1. 사용자 메시지 저장 및 출력
    st.session_state["messages"].append({"role": "user", "content": prompt})
    save_message("user", prompt)
    st.chat_message("user").write(prompt)

    # 2. 클라이언트 및 Conversation ID 관리
    client = create_openai_client(openai_api_key)
    
    # ID 로직 최적화
    if "conversation_id" not in st.session_state or not st.session_state["conversation_id"]:
        cid = load_conversation_id()
        if not cid:
            cid = create_conversation(client)
            save_conversation_id(cid)
        st.session_state["conversation_id"] = cid

    # 3. AI 응답 생성
    with st.spinner("생각 중..."):
        try:
            assistant_text = get_ai_response(
                client=client,
                prompt=prompt,
                conversation_id=st.session_state["conversation_id"]
            )
        except Exception as e:
            assistant_text = f"연결 오류가 발생했습니다. 라이브러리 버전을 확인하세요: {e}"

    # 4. 응답 저장 및 출력
    st.session_state["messages"].append({"role": "assistant", "content": assistant_text})
    save_message("assistant", assistant_text)
    st.chat_message("assistant").write(assistant_text)