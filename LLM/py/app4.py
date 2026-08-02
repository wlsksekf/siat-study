import os
import uuid

import streamlit as st
from dotenv import load_dotenv

from openai_service4 import create_agent_executor, get_ai_response
from sqlite_chat_memory import clear_messages, list_threads, load_messages, save_message
from sqlite_checkpointer import SqliteCheckpointSaver


load_dotenv()

DEFAULT_THREAD_PREFIX = "app4-thread"


def extract_tool_errors(text: str) -> list[str]:
    if not text or "[TOOL_ERROR]" not in text:
        return []
    return [
        line.strip()
        for line in text.splitlines()
        if line.strip().startswith("[TOOL_ERROR]")
    ]


def make_thread_id() -> str:
    return f"{DEFAULT_THREAD_PREFIX}-{uuid.uuid4().hex[:8]}"


def summarize_thread(thread: dict[str, str | int]) -> str:
    content = str(thread["content"]).strip().replace("\n", " ")
    preview = content[:24] + "..." if len(content) > 24 else content
    role = "AI" if thread["role"] == "assistant" else "사용자"
    return f"{role}: {preview or '(빈 대화)'}"


def ensure_thread_state() -> None:
    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = make_thread_id()
    if "messages" not in st.session_state:
        st.session_state["messages"] = load_messages(st.session_state["thread_id"])


def switch_thread(thread_id: str) -> None:
    normalized = thread_id.strip()
    if not normalized or normalized == st.session_state["thread_id"]:
        return

    st.session_state["thread_id"] = normalized
    st.session_state["messages"] = load_messages(normalized)


def start_new_thread() -> None:
    st.session_state["thread_id"] = make_thread_id()
    st.session_state["messages"] = []


def clear_current_thread() -> None:
    thread_id = st.session_state["thread_id"]
    clear_messages(thread_id)
    SqliteCheckpointSaver().delete_thread(thread_id)
    st.session_state["messages"] = []


st.set_page_config(page_title="LangChain Agent Chat")
ensure_thread_state()

with st.sidebar:
    st.title("대화")
    thread_input = st.text_input("대화 ID", value=st.session_state["thread_id"])
    st.caption("같은 대화 ID를 쓰면 이전 대화가 이어집니다.")

    if thread_input != st.session_state["thread_id"]:
        switch_thread(thread_input)
        st.rerun()

    if st.button("새 대화 시작"):
        start_new_thread()
        st.rerun()

    if st.button("현재 대화 초기화"):
        clear_current_thread()
        st.rerun()

    st.divider()
    st.subheader("저장된 이전 대화")
    threads = list_threads()

    if not threads:
        st.caption("아직 저장된 대화가 없습니다.")
    else:
        for thread in threads:
            thread_id = str(thread["thread_id"])
            label = summarize_thread(thread)
            if thread_id == st.session_state["thread_id"]:
                label = f"[현재] {label}"

            help_text = (
                f"ID: {thread_id}\n"
                f"시간: {thread['created_at']}\n"
                f"메시지 수: {thread['message_count']}"
            )
            if st.button(label, key=f"thread-{thread_id}", help=help_text, use_container_width=True):
                switch_thread(thread_id)
                st.rerun()


api_key = os.getenv("OPENAI_API_KEY")
agent = create_agent_executor(api_key) if api_key else None

st.title("LangChain Agent Chat")

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


if prompt := st.chat_input("메시지를 입력하세요"):
    if not api_key:
        st.error("`.env`에 `OPENAI_API_KEY`를 설정해 주세요.")
        st.stop()

    thread_id = st.session_state["thread_id"]
    st.session_state["messages"].append({"role": "user", "content": prompt})
    save_message(thread_id, "user", prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner("AI가 답변을 생성하는 중입니다..."):
            response = get_ai_response(agent, prompt, thread_id)
    except Exception as error:
        response = f"오류가 발생했습니다: {error}"

    with st.chat_message("assistant"):
        st.markdown(response)
        tool_errors = extract_tool_errors(response)
        for error_text in tool_errors:
            st.error(error_text)

    st.session_state["messages"].append({"role": "assistant", "content": response})
    save_message(thread_id, "assistant", response)
