from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os
import truststore

truststore.inject_into_ssl()

load_dotenv()

with st.sidebar:
    # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 대화 내용을 LLM으로 전달
    response = client.responses.create(
        model="gpt-4.1-nano",
        instructions="당신은 사용자를 도와주는 상담사입니다.",
        max_output_tokens=100,
        input=[
            {"role": "user", "content": prompt},
        ],
    )

    msg = response.output_text

    # LLM 응답을 대화 내용에 추가합니다.
    st.session_state.messages.append({"role": "assistant", "content": msg})

    # LLM 응답을 화면에 출력합니다.
    st.chat_message("assistant").write(msg)


