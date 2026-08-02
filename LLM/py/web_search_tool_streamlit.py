import json
import os
from pathlib import Path

import streamlit as st
import truststore
from dotenv import load_dotenv
from openai import OpenAI

from tool_time_stock import get_current_time, get_yf_stock_info


truststore.inject_into_ssl()
load_dotenv()


LLM_DIR = Path(__file__).resolve().parent.parent
JSON_DIR = LLM_DIR / "json"
DB_FILE = JSON_DIR / "web_search_history.json"
DEFAULT_ASSISTANT_MESSAGE = (
    "검색, 현재 시각, 주식 가격이 필요한 질문을 입력해 주세요. "
    "필요하면 웹 검색과 도구를 함께 사용해 답변할게요."
)

WEB_SEARCH_TOOL = {"type": "web_search"}
TIME_TOOL = {
    "type": "function",
    "name": "get_current_time",
    "description": "사용자가 현재 시각이나 날짜를 물어보면 호출합니다.",
    "parameters": {
        "type": "object",
        "properties": {
            "timezone": {
                "type": "string",
                "description": "현재 날짜와 시간을 반환할 시간대입니다. 예: Asia/Seoul",
            }
        },
        "required": ["timezone"],
    },
}
STOCK_TOOL = {
    "type": "function",
    "name": "get_yf_stock_info",
    "description": (
        "사용자가 주식 가격이나 종목 정보를 물어보면 호출합니다. "
        "ticker에는 AAPL, TSLA 같은 티커나 Apple, Tesla, 애플, 삼성 같은 회사명을 넣을 수 있습니다."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "조회할 종목의 티커 또는 회사명입니다.",
            }
        },
        "required": ["ticker"],
    },
}
ALL_TOOLS = [WEB_SEARCH_TOOL, TIME_TOOL, STOCK_TOOL]


def init_db() -> None:
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    if not DB_FILE.exists():
        save_data({"messages": [], "conversation_id": None})


def load_data() -> dict:
    init_db()
    data = json.loads(DB_FILE.read_text(encoding="utf-8"))
    if "messages" not in data:
        data["messages"] = []
    if "conversation_id" not in data:
        data["conversation_id"] = None
    return data


def save_data(data: dict) -> None:
    DB_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_messages() -> list[dict]:
    return load_data()["messages"]


def save_messages(messages: list[dict]) -> None:
    data = load_data()
    data["messages"] = messages
    save_data(data)


def load_conversation_id() -> str | None:
    return load_data()["conversation_id"]


def save_conversation_id(conversation_id: str | None) -> None:
    data = load_data()
    data["conversation_id"] = conversation_id
    save_data(data)


def clear_history() -> None:
    save_data({"messages": [], "conversation_id": None})


@st.cache_resource
def create_openai_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key)


def create_conversation(client: OpenAI) -> str:
    conversation = client.conversations.create()
    return conversation.id


def is_time_prompt(prompt: str) -> bool:
    lowered = prompt.lower()
    keywords = ["현재 시각", "지금 몇 시", "몇시", "몇 시", "현재 시간", "지금 시간", "time in", "what time"]
    return any(keyword in lowered for keyword in keywords)


def is_stock_prompt(prompt: str) -> bool:
    lowered = prompt.lower()
    keywords = ["주가", "주식", "stock", "ticker", "시가총액", "가격", "삼성", "애플", "테슬라", "엔비디아"]
    return any(keyword in lowered for keyword in keywords)


def is_web_search_prompt(prompt: str) -> bool:
    lowered = prompt.lower()
    keywords = [
        "최신",
        "뉴스",
        "사건",
        "출시",
        "발표",
        "최근",
        "올해",
        "2026",
        "2025",
        "today",
        "latest",
        "news",
        "release",
        "event",
    ]
    return any(keyword in lowered for keyword in keywords)


def handle_function_call(name: str, arguments: str) -> str:
    parsed_arguments = json.loads(arguments) if arguments else {}

    if name == "get_current_time":
        return get_current_time(timezone=parsed_arguments.get("timezone", "Asia/Seoul"))

    if name == "get_yf_stock_info":
        return get_yf_stock_info(ticker=parsed_arguments.get("ticker", ""))

    return f"지원하지 않는 함수입니다: {name}"


def extract_response_data(response) -> dict:
    searched_query = ""
    citations: list[dict] = []
    seen_urls: set[str] = set()
    answer = ""
    function_outputs = []

    for item in getattr(response, "output", []):
        item_type = getattr(item, "type", "")

        if item_type == "web_search_call":
            action = getattr(item, "action", None)
            searched_query = getattr(action, "query", "") or searched_query

        elif item_type == "function_call":
            function_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": handle_function_call(item.name, item.arguments),
                }
            )

        elif item_type == "message":
            for content in getattr(item, "content", []):
                text = getattr(content, "text", "")
                if text:
                    answer = text

                for annotation in getattr(content, "annotations", []) or []:
                    url = getattr(annotation, "url", "")
                    if not url or url in seen_urls:
                        continue

                    seen_urls.add(url)
                    citations.append(
                        {
                            "title": getattr(annotation, "title", "출처"),
                            "url": url,
                        }
                    )

    return {
        "searched_query": searched_query,
        "citations": citations,
        "answer": answer,
        "function_outputs": function_outputs,
    }


def call_model(
    client: OpenAI,
    prompt: str,
    conversation_id: str,
    tools: list[dict],
    extra_instructions: str = "",
):
    return client.responses.create(
        model="gpt-4o",
        instructions=(
            "당신은 웹 검색, 현재 시각 조회, 주식 가격 조회를 도와주는 도우미입니다. "
            "최신 정보, 현재 상황, 연도 지정 질문, 사건, 출시, 뉴스, 일정, 가격처럼 "
            "시간에 따라 달라질 수 있는 정보는 web_search를 사용해 확인한 뒤 답하세요. "
            "현재 시각 질문은 get_current_time 함수를 사용하세요. "
            "주식 가격이나 종목 정보 질문은 get_yf_stock_info 함수를 사용하세요. "
            "도구를 쓸 수 있는 질문인데 추정으로 답하지 마세요. "
            f"{extra_instructions}"
        ),
        input=prompt,
        tools=tools,
        tool_choice="auto",
        include=["web_search_call.action.sources"],
        max_output_tokens=700,
        conversation=conversation_id,
    )


def get_ai_response(
    client: OpenAI,
    prompt: str,
    conversation_id: str,
) -> dict:
    answer = ""
    searched_query = ""
    citations: list[dict] = []

    wants_web_search = is_web_search_prompt(prompt) and not is_time_prompt(prompt) and not is_stock_prompt(prompt)
    wants_time = is_time_prompt(prompt) and not is_stock_prompt(prompt)
    wants_stock = is_stock_prompt(prompt) and not is_web_search_prompt(prompt)

    selected_tools = ALL_TOOLS
    extra_instructions = ""

    if wants_web_search:
        selected_tools = [WEB_SEARCH_TOOL]
        extra_instructions = (
            "이 질문은 최신 정보 또는 사건 질문입니다. "
            "반드시 web_search를 먼저 사용하고, 검색 결과를 바탕으로만 답하세요."
        )
    elif wants_time:
        selected_tools = [TIME_TOOL]
    elif wants_stock:
        selected_tools = [STOCK_TOOL]

    response = call_model(
        client=client,
        prompt=prompt,
        conversation_id=conversation_id,
        tools=selected_tools,
        extra_instructions=extra_instructions,
    )

    while True:
        parsed = extract_response_data(response)
        if parsed["searched_query"]:
            searched_query = parsed["searched_query"]
        if parsed["citations"]:
            citations = parsed["citations"]
        if parsed["answer"]:
            answer = parsed["answer"]

        if not parsed["function_outputs"]:
            break

        response = client.responses.create(
            model="gpt-4o",
            input=parsed["function_outputs"],
            conversation=conversation_id,
            tools=selected_tools,
            tool_choice="auto",
            include=["web_search_call.action.sources"],
            max_output_tokens=700,
        )

    if wants_web_search and not searched_query:
        response = call_model(
            client=client,
            prompt=f"반드시 웹 검색 후 답하세요: {prompt}",
            conversation_id=conversation_id,
            tools=[WEB_SEARCH_TOOL],
            extra_instructions=(
                "이 질문은 반드시 web_search를 사용해야 합니다. "
                "검색을 하지 않았다면 다시 검색해서 답하세요."
            ),
        )
        parsed = extract_response_data(response)
        searched_query = parsed["searched_query"]
        citations = parsed["citations"]
        answer = parsed["answer"] or answer

    if not answer:
        answer = getattr(response, "output_text", "") or "응답을 생성하지 못했습니다."

    return {
        "searched_query": searched_query,
        "answer": answer,
        "citations": citations,
    }


def render_assistant_message(message: dict) -> None:
    with st.chat_message("assistant"):
        st.write(message["content"])

        searched_query = message.get("searched_query", "")
        citations = message.get("citations", [])

        if searched_query:
            st.caption(f"검색어: {searched_query}")

        if citations:
            with st.expander("출처 보기"):
                for index, citation in enumerate(citations, start=1):
                    title = citation.get("title", f"출처 {index}")
                    url = citation.get("url", "")
                    st.markdown(f"{index}. [{title}]({url})")


def build_default_messages() -> list[dict]:
    return [
        {
            "role": "assistant",
            "content": DEFAULT_ASSISTANT_MESSAGE,
            "searched_query": "",
            "citations": [],
        }
    ]


init_db()
st.set_page_config(page_title="Web Search Tool", page_icon="🌐", layout="wide")


with st.sidebar:
    st.header("설정")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    st.write("대화 내용과")
    st.write("conversation_id는")
    st.write("JSON 파일에 저장됩니다.")

    if st.button("대화 초기화"):
        clear_history()
        st.session_state["messages"] = build_default_messages()
        save_messages(st.session_state["messages"])
        if "conversation_id" in st.session_state:
            del st.session_state["conversation_id"]
        st.rerun()


st.title("웹 검색 챗봇")
st.caption("Streamlit + OpenAI Responses API + web_search + function tools")


if "messages" not in st.session_state:
    db_messages = load_messages()
    if not db_messages:
        st.session_state["messages"] = build_default_messages()
        save_messages(st.session_state["messages"])
    else:
        st.session_state["messages"] = db_messages


for message in st.session_state["messages"]:
    if message["role"] == "assistant":
        render_assistant_message(message)
    else:
        st.chat_message("user").write(message["content"])


if prompt := st.chat_input("예: 지금 런던 시간 알려줘 / 삼성 주가 알려줘 / 2026년 최신 사건 찾아줘"):
    if not openai_api_key:
        st.info("`.env`에 `OPENAI_API_KEY`를 설정해 주세요.")
        st.stop()

    user_message = {"role": "user", "content": prompt}
    st.session_state["messages"].append(user_message)
    save_messages(st.session_state["messages"])
    st.chat_message("user").write(prompt)

    client = create_openai_client(openai_api_key)

    if "conversation_id" not in st.session_state or not st.session_state["conversation_id"]:
        conversation_id = load_conversation_id()
        if not conversation_id:
            conversation_id = create_conversation(client)
            save_conversation_id(conversation_id)
        st.session_state["conversation_id"] = conversation_id

    with st.spinner("도구를 확인하고 답변을 만드는 중입니다..."):
        try:
            result = get_ai_response(
                client=client,
                prompt=prompt,
                conversation_id=st.session_state["conversation_id"],
            )
        except Exception as error:
            result = {
                "searched_query": "",
                "answer": f"오류가 발생했습니다: {error}",
                "citations": [],
            }

    assistant_message = {
        "role": "assistant",
        "content": result["answer"],
        "searched_query": result["searched_query"],
        "citations": result["citations"],
    }
    st.session_state["messages"].append(assistant_message)
    save_messages(st.session_state["messages"])
    render_assistant_message(assistant_message)
