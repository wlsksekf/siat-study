# Streamlit 라이브러리를 st라는 이름으로 불러옵니다.
# Streamlit은 Python으로 웹 기반 인터페이스를 쉽게 만들 수 있게 해주는 도구입니다.
import streamlit as st

# st.chat_input("메시지를 입력하세요")
# 채팅 입력창을 화면 아래에 생성합니다.
# 사용자가 메시지를 입력하고 Enter를 누르면 입력 문자열이 반환됩니다.

if prompt := st.chat_input("메시지를 입력하세요"):

    # st.chat_message("user") : 사용자의 채팅 메시지 영역을 생성합니다.
    # write(prompt) : 사용자가 입력한 메시지를 화면에 출력합니다.
    st.chat_message("user").write(prompt)


    # st.chat_message("assistant") : AI(assistant)의 메시지 영역을 생성합니다.
    # 여기서는 간단한 예제로 사용자의 메시지 앞에 "응답: "을 붙여 출력합니다.
    st.chat_message("assistant").write("응답: " + prompt)