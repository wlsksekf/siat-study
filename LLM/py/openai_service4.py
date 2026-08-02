import os
from pathlib import Path

import streamlit as st
import truststore
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from openai import DefaultHttpxClient

from sqlite_checkpointer import SqliteCheckpointSaver
from tools import get_current_time, get_yf_stock_info, web_search


truststore.inject_into_ssl()

BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_CERT_PATH = Path(r"C:\cert\cacert.pem")
CERTIFI_CERT_PATH = (
    BASE_DIR / "LLM" / "venv" / "Lib" / "site-packages" / "certifi" / "cacert.pem"
)
OPENAI_INSECURE_SSL = os.getenv("OPENAI_INSECURE_SSL", "0") == "1"
SYSTEM_PROMPT = (
    "너는 친절한 AI 비서입니다. "
    "현재 시간이나 날짜를 물으면 get_current_time 도구를 사용하세요. "
    "주식 관련 질문은 get_yf_stock_info 도구를 사용하세요. "
    "최신 정보 검색이 필요하면 web_search 도구를 사용하세요. "
    "추측하지 말고 필요한 경우 도구를 사용하세요."
)


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
def create_agent_executor(api_key: str):
    llm = ChatOpenAI(
        model="gpt-4.1-nano",
        api_key=api_key,
        temperature=0,
        timeout=30,
        max_retries=2,
        http_client=DefaultHttpxClient(verify=resolve_cert_path(), timeout=30.0),
    )

    return create_agent(
        model=llm,
        tools=[get_current_time, get_yf_stock_info, web_search],
        checkpointer=SqliteCheckpointSaver(),
        system_prompt=SYSTEM_PROMPT,
    )


def _extract_text(content) -> str:
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text")
                if text:
                    parts.append(text)
            else:
                text = getattr(item, "text", None)
                if text:
                    parts.append(text)
        return "\n".join(parts).strip()

    return str(content)


def get_ai_response(agent, prompt: str, thread_id: str) -> str:
    """
    현재 사용자 입력 1개만 전달합니다.
    이전 대화는 thread_id 기준으로 checkpoint에서 복원됩니다.
    """
    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": prompt},
            ]
        },
        config={
            "configurable": {
                "thread_id": thread_id,
            }
        },
    )
    final_message = result["messages"][-1]
    return _extract_text(final_message.content)
