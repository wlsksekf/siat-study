# tools.py
from datetime import datetime
from pathlib import Path
import os
import ssl
from typing import Iterable

from curl_cffi import requests as curl_requests
from ddgs import DDGS
from dotenv import load_dotenv
from langchain_core.tools import tool
from openai import DefaultHttpxClient, OpenAI
import pytz
import truststore
import yfinance as yf


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_CERT_PATH = Path(r"C:\cert\cacert.pem")
CERTIFI_CERT_PATH = BASE_DIR / "LLM" / "venv" / "Lib" / "site-packages" / "certifi" / "cacert.pem"


COMPANY_TO_TICKER = {
    "apple": "AAPL",
    "aapl": "AAPL",
    "애플": "AAPL",
    "microsoft": "MSFT",
    "msft": "MSFT",
    "마이크로소프트": "MSFT",
    "tesla": "TSLA",
    "tsla": "TSLA",
    "테슬라": "TSLA",
    "nvidia": "NVDA",
    "nvda": "NVDA",
    "엔비디아": "NVDA",
    "alphabet": "GOOGL",
    "google": "GOOGL",
    "googl": "GOOGL",
    "구글": "GOOGL",
    "amazon": "AMZN",
    "amzn": "AMZN",
    "아마존": "AMZN",
    "meta": "META",
    "메타": "META",
    "samsung": "005930.KS",
    "samsung electronics": "005930.KS",
    "삼성": "005930.KS",
    "삼성전자": "005930.KS",
    "005930": "005930.KS",
    "005930.ks": "005930.KS",
}


def set_certificate_env(cert_path: str) -> str:
    os.environ["SSL_CERT_FILE"] = cert_path
    os.environ["REQUESTS_CA_BUNDLE"] = cert_path
    os.environ["CURL_CA_BUNDLE"] = cert_path
    return cert_path


def configure_ssl() -> str:
    truststore.inject_into_ssl()

    if CERTIFI_CERT_PATH.exists():
        return set_certificate_env(str(CERTIFI_CERT_PATH))

    if DEFAULT_CERT_PATH.exists():
        return set_certificate_env(str(DEFAULT_CERT_PATH))

    ssl._create_default_https_context = truststore.SSLContext
    return "truststore"


SSL_BACKEND = configure_ssl()
load_dotenv(BASE_DIR / "LLM" / ".env")

CACHE_DIR = BASE_DIR / "LLM" / ".cache" / "py-yfinance"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
yf.set_tz_cache_location(str(CACHE_DIR))

INSECURE_SSL = os.getenv("YF_INSECURE_SSL", "1") == "1"


def build_yfinance_session():
    return curl_requests.Session(
        impersonate="chrome",
        verify=not INSECURE_SSL,
    )


def build_openai_client() -> OpenAI | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    verify: str | bool = True
    if CERTIFI_CERT_PATH.exists():
        verify = str(CERTIFI_CERT_PATH)
    elif DEFAULT_CERT_PATH.exists():
        verify = str(DEFAULT_CERT_PATH)

    return OpenAI(
        api_key=api_key,
        http_client=DefaultHttpxClient(
            verify=verify,
            timeout=30.0,
        ),
    )


def normalize_ticker(ticker: str) -> str:
    normalized = ticker.strip()
    return COMPANY_TO_TICKER.get(normalized.lower(), normalized.upper())


def format_tool_error(tool_name: str, reason: str, details: str = "") -> str:
    base = f"[TOOL_ERROR] {tool_name}: {reason}"
    if details:
        return f"{base}\n상세: {details}"
    return base


def is_connection_error_message(message: str) -> bool:
    error_text = message.lower()
    keywords: Iterable[str] = (
        "connection error",
        "connecterror",
        "failed to establish a new connection",
        "tcp connect",
        "timed out",
        "timeout",
    )
    return any(keyword in error_text for keyword in keywords)


@tool
def get_current_time(timezone: str = "Asia/Seoul") -> str:
    """현재 날짜와 시간을 조회합니다. 예: Asia/Seoul"""
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"{now} {timezone}"
    except Exception as error:
        return f"시간 가져오기 오류: {error}"


@tool
def get_yf_stock_info(ticker: str) -> str:
    """
    주식 종목 코드나 회사명을 입력받아 Yahoo Finance 정보를 반환합니다.
    예: 삼성전자 -> 005930.KS, 마이크로소프트 -> MSFT
    """
    try:
        normalized_ticker = normalize_ticker(ticker)
        stock = yf.Ticker(normalized_ticker, session=build_yfinance_session())
        info = dict(stock.fast_info)

        if not info:
            return f"{normalized_ticker} 정보를 찾을 수 없습니다."

        info["requested_ticker"] = ticker
        info["resolved_ticker"] = normalized_ticker
        return str(info)
    except Exception as error:
        return f"주식 정보 조회 오류: {error}"


@tool
def web_search(query: str) -> str:
    """
    최신 뉴스, 웹 정보, 실시간 검색이 필요할 때 DuckDuckGo 검색 결과를 반환합니다.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        if not results:
            return "검색 결과가 없습니다."

        lines = []
        for idx, item in enumerate(results, start=1):
            title = item.get("title", "제목 없음")
            body = item.get("body", "")
            href = item.get("href", "")
            lines.append(f"{idx}. {title}\n{body}\n{href}")
        return "\n\n".join(lines)
    except Exception as error:
        client = build_openai_client()
        if client is None:
            reason = "웹 검색 차단"
            if is_connection_error_message(str(error)):
                reason = "웹 검색 연결 차단"
            return format_tool_error("web_search", reason, str(error))

        try:
            response = client.responses.create(
                model="gpt-4o",
                input=f"{query}\n최신 정보 3가지를 한국어로 간단히 정리해 주세요.",
                tools=[{"type": "web_search"}],
            )
            return response.output_text or "검색 결과를 가져오지 못했습니다."
        except Exception as fallback_error:
            web_reason = "웹 검색 차단"
            openai_reason = "OpenAI 연결 차단"
            if is_connection_error_message(str(error)):
                web_reason = "웹 검색 연결 차단"
            if not is_connection_error_message(str(fallback_error)):
                openai_reason = "OpenAI 검색 호출 오류"
            return (
                format_tool_error("web_search", web_reason, str(error))
                + "\n"
                + format_tool_error("openai_web_search", openai_reason, str(fallback_error))
            )


tools = [get_current_time, get_yf_stock_info, web_search]


if __name__ == "__main__":
    print(f"현재 시각: {get_current_time.invoke({'timezone': 'Asia/Seoul'})}")
    print("--- 삼성 주가 정보 예시 ---")
    print(get_yf_stock_info.invoke({"ticker": "삼성"}))
