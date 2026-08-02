# app5.py
import streamlit as st
from dotenv import load_dotenv

from json_db5 import clear_messages, load_messages, save_message

from openai_service5 import (
    extract_text_from_pdf,
    build_rag_index,
    get_ai_response_with_rag,
)

load_dotenv()

st.set_page_config(page_title="PDF RAG Chat")

if "messages" not in st.session_state:
    st.session_state["messages"] = load_messages()

if "rag_index" not in st.session_state:
    st.session_state["rag_index"] = None

# 현재 업로드된 PDF 이름
if "source_name" not in st.session_state:
    st.session_state["source_name"] = None

st.title("PDF 업로드 RAG 챗봇")

with st.sidebar:
    st.subheader("PDF 업로드")

    # PDF 파일 업로드 (pdf만 허용)
    uploaded_file = st.file_uploader(
        "PDF 파일을 업로드하세요",
        type=["pdf"]
    )

    if uploaded_file is not None:
        # 이전에 업로드한 파일과 다른 경우에만 처리 (중복 인덱싱 방지)
        if st.session_state["source_name"] != uploaded_file.name:
            with st.spinner("PDF 텍스트 추출 및 RAG 인덱스 생성 중입니다..."):
                pdf_text = extract_text_from_pdf(uploaded_file)

                if not pdf_text.strip():
                    st.error("PDF에서 텍스트를 추출하지 못했습니다.")
                else:
                    st.session_state["rag_index"] = build_rag_index(pdf_text)
                    st.session_state["source_name"] = uploaded_file.name  # 현재 문서 이름 저장
                    st.success(f"{uploaded_file.name} 인덱싱 완료")         # 완료 메시지

    if st.session_state["source_name"]:
        st.caption(f"현재 문서: {st.session_state['source_name']}")

    if st.button("대화 초기화"):
        st.session_state["messages"] = []
        clear_messages()
        st.rerun()

st.write("업로드한 PDF 내용을 바탕으로 답변합니다.")

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("PDF에 대해 질문하세요"):
    st.session_state["messages"].append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    if st.session_state["rag_index"] is None:
        response = "먼저 PDF 파일을 업로드해 주세요."
    else:
        with st.spinner("응답을 생성 중입니다."):
            response = get_ai_response_with_rag(
                prompt=prompt,
                rag_index=st.session_state["rag_index"],
                chat_history=st.session_state["messages"]
            )

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state["messages"].append({
        "role": "assistant",
        "content": response
    })

    save_message("user", prompt)
    save_message("assistant", response)
