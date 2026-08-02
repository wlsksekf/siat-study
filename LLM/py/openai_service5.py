from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st
import truststore
from langchain_community.vectorstores import FAISS
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import DefaultHttpxClient
from pypdf import PdfReader


truststore.inject_into_ssl()

BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_CERT_PATH = Path(r"C:\cert\cacert.pem")
CERTIFI_CERT_PATH = (
    BASE_DIR / "LLM" / "venv" / "Lib" / "site-packages" / "certifi" / "cacert.pem"
)
VECTOR_CACHE_DIR = BASE_DIR / "LLM" / "faiss_cache"
OPENAI_INSECURE_SSL = os.getenv("OPENAI_INSECURE_SSL", "0") == "1"
DEFAULT_MODEL = "gpt-4.1-nano"
EMBEDDING_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 900
CHUNK_OVERLAP = 150
TOP_K = 4


def resolve_cert_path() -> str | bool:
    if OPENAI_INSECURE_SSL:
        return False

    if CERTIFI_CERT_PATH.exists():
        cert_path = str(CERTIFI_CERT_PATH)
    elif DEFAULT_CERT_PATH.exists():
        cert_path = str(DEFAULT_CERT_PATH)
    else:
        return True

    os.environ["SSL_CERT_FILE"] = cert_path
    os.environ["REQUESTS_CA_BUNDLE"] = cert_path
    os.environ["CURL_CA_BUNDLE"] = cert_path
    return cert_path


@st.cache_resource
def create_http_client() -> DefaultHttpxClient:
    return DefaultHttpxClient(verify=resolve_cert_path(), timeout=30.0)


@st.cache_resource
def create_chat_llm(api_key: str) -> ChatOpenAI:
    return ChatOpenAI(
        model=DEFAULT_MODEL,
        api_key=api_key,
        temperature=0,
        timeout=30,
        max_retries=2,
        http_client=create_http_client(),
    )


@st.cache_resource
def create_embeddings(api_key: str) -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=api_key,
        http_client=create_http_client(),
    )


def extract_text_from_pdf(uploaded_file) -> str:
    reader = PdfReader(uploaded_file)
    page_texts: list[str] = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            page_texts.append(f"[Page {page_number}]\n{text}")

    uploaded_file.seek(0)
    return "\n\n".join(page_texts).strip()


def _build_text_splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )


def build_rag_index(pdf_text: str) -> dict[str, Any]:
    splitter = _build_text_splitter()
    chunks = splitter.split_text(pdf_text)
    indexed_at = datetime.now().isoformat(timespec="seconds")

    if not chunks:
        return {
            "chunks": [],
            "vectorstore": None,
            "indexed_at": indexed_at,
            "cache_dir": str(VECTOR_CACHE_DIR),
        }

    api_key = os.getenv("OPENAI_API_KEY")
    vectorstore = None

    if api_key:
        VECTOR_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        metadatas = [
            {
                "chunk_id": index,
                "indexed_at": indexed_at,
                "cache_dir": str(VECTOR_CACHE_DIR),
            }
            for index, _ in enumerate(chunks)
        ]
        vectorstore = FAISS.from_texts(
            texts=chunks,
            embedding=create_embeddings(api_key),
            metadatas=metadatas,
        )

    return {
        "chunks": chunks,
        "vectorstore": vectorstore,
        "indexed_at": indexed_at,
        "cache_dir": str(VECTOR_CACHE_DIR),
    }


def _convert_chat_history(chat_history: list[dict[str, str]] | None) -> list[HumanMessage | AIMessage]:
    if not chat_history:
        return []

    converted_messages: list[HumanMessage | AIMessage] = []
    for message in chat_history[-6:]:
        role = message.get("role")
        content = (message.get("content") or "").strip()
        if not content:
            continue
        if role == "user":
            converted_messages.append(HumanMessage(content=content))
        elif role == "assistant":
            converted_messages.append(AIMessage(content=content))
    return converted_messages


def _search_context(prompt: str, rag_index: dict[str, Any]) -> str:
    vectorstore = rag_index.get("vectorstore")
    if vectorstore is not None:
        docs = vectorstore.similarity_search(prompt, k=TOP_K)
        context_chunks = [doc.page_content for doc in docs if doc.page_content.strip()]
    else:
        context_chunks = rag_index.get("chunks", [])[:TOP_K]

    return "\n\n---\n\n".join(context_chunks).strip()


def get_ai_response_with_rag(
    prompt: str,
    rag_index: dict[str, Any],
    chat_history: list[dict[str, str]] | None = None,
) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "`.env` 파일에 `OPENAI_API_KEY`를 설정해 주세요."

    if not rag_index or not rag_index.get("chunks"):
        return "PDF에서 검색할 내용을 찾지 못했습니다."

    context_text = _search_context(prompt, rag_index)
    llm = create_chat_llm(api_key)
    messages = [
        SystemMessage(
            content=(
                "당신은 PDF 문서 기반 RAG 도우미입니다. "
                "반드시 제공된 문서 문맥을 우선 사용하세요. "
                "문맥에 없는 정보는 추측하지 말고 '문서에서 확인하지 못했습니다.'라고 답하세요. "
                "답변은 한국어로 작성하세요."
            )
        ),
        *_convert_chat_history(chat_history),
        HumanMessage(
            content=(
                f"[문서 문맥]\n{context_text}\n\n"
                f"[질문]\n{prompt}\n\n"
                f"[인덱싱 시각]\n{rag_index.get('indexed_at', 'unknown')}"
            )
        ),
    ]

    response = llm.invoke(messages)
    content = response.content

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            else:
                text = getattr(item, "text", None)
                if text:
                    parts.append(text)
        return "\n".join(parts).strip()

    return str(content).strip()
