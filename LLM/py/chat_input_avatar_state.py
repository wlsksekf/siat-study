# Streamlit 라이브러리를 st라는 이름으로 불러옵니다.
# Streamlit은 Python으로 웹 기반 인터페이스를 쉽게 만들 수 있게 해주는 도구입니다.
import streamlit as st

# 대화 기록 저장 공간 생성
# st.session_state는 Streamlit에서 페이지가 다시 실행되더라도
# 데이터를 유지하기 위한 저장 공간입니다.
if "messages" not in st.session_state:
    st.session_state.messages = []  # 대화 기록을 저장할 리스트 생성


# 기존 대화 기록 화면에 출력
# session_state에 저장된 메시지를 순서대로 화면에 다시 출력합니다.
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


# 사용자 입력 처리
# st.chat_input() : 화면 아래에 채팅 입력창을 생성합니다.
if prompt := st.chat_input("메시지를 입력하세요"):

    # 사용자 메시지를 session_state에 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # 사용자 메시지를 화면에 출력
    st.chat_message("user").write(prompt)

    # AI 응답 생성 (예제)
    response = "응답: " + prompt

    # AI 메시지를 session_state에 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    # AI 메시지를 화면이 출력
    st.chat_message("assistant").write(response)