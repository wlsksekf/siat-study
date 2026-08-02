import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

import truststore
from openai_service import create_conversation, create_openai_client, get_ai_response

# SSL 설정 및 환경 변수 로드
truststore.inject_into_ssl()
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# Whisper 전사용 기본 클라이언트
client = OpenAI()

st.title("오디오 전사 챗봇")
st.write("음성 파일을 업로드하고 채팅창에 전사를 요청해 보세요.")

with st.sidebar:
    st.header("파일 업로드")
    audio_file = st.file_uploader(
        "음성 파일을 선택해 주세요 (mp3, wav, m4a)",
        type=["mp3", "wav", "m4a"],
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("메시지를 입력하세요. 예: 한국어로 전사해줘"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if audio_file is not None and "전사" in prompt:
        with st.spinner("음성을 텍스트로 변환 중입니다. 잠시만 기다려 주세요."):
            try:
                target_language = "en" if "영어" in prompt else "ko"
                language_name = "영어" if target_language == "en" else "한국어"

                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text",
                    language=target_language,
                )

                response = f"**{language_name} 전사 결과입니다**\n\n> {transcription}"
            except Exception as e:
                response = f"오류가 발생했습니다: {e}"

    elif audio_file is None and "전사" in prompt:
        response = "먼저 왼쪽 사이드바에서 음성 파일을 업로드해 주세요."

    else:
        if not openai_api_key:
            response = "OPENAI_API_KEY를 .env에서 설정해 주세요."
        else:
            try:
                chat_client = create_openai_client(openai_api_key)

                if "conversation_id" not in st.session_state or not st.session_state["conversation_id"]:
                    st.session_state["conversation_id"] = create_conversation(chat_client)

                with st.spinner("생각 중..."):
                    response = get_ai_response(
                        client=chat_client,
                        prompt=prompt,
                        conversation_id=st.session_state["conversation_id"],
                    )
            except Exception as e:
                response = f"AI 응답 생성 중 오류가 발생했습니다: {e}"

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
