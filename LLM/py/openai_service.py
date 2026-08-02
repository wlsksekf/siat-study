from openai import OpenAI
import streamlit as st

@st.cache_resource
def create_openai_client(api_key):
    return OpenAI(api_key=api_key)

def create_conversation(client):
    """2026년형: 서버측 대화 세션 생성"""
    conversation = client.conversations.create()
    return conversation.id

def get_ai_response(client, prompt, conversation_id):
    """Responses API 사용: prompt 인자 이름을 일치시킴"""
    response = client.responses.create(
        model="gpt-4.1-nano",
        instructions="당신은 사용자를 도와주는 상담사입니다.",
        input=[
            {"role": "user", "content": prompt}
        ],
        conversation=conversation_id,
        max_output_tokens=500
    )
    return response.output_text