from datetime import datetime
from pathlib import Path
import os
import ssl

from curl_cffi import requests as curl_requests
import pytz
import truststore


BASE_DIR = Path(__file__).resolve().parents[2]


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


def configure_ssl_for_yfinance() -> str:
    truststore.inject_into_ssl()

    certifi_pem = BASE_DIR / ".venv" / "Lib" / "site-packages" / "certifi" / "cacert.pem"
    if certifi_pem.exists():
        cert_path = str(certifi_pem)
        os.environ["SSL_CERT_FILE"] = cert_path
        os.environ["REQUESTS_CA_BUNDLE"] = cert_path
        os.environ["CURL_CA_BUNDLE"] = cert_path
        return cert_path

    ssl._create_default_https_context = truststore.SSLContext
    return "truststore"


SSL_BACKEND = configure_ssl_for_yfinance()

import yfinance as yf  # noqa: E402


CACHE_DIR = BASE_DIR / "LLM" / ".cache" / "py-yfinance"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
yf.set_tz_cache_location(str(CACHE_DIR))

INSECURE_SSL = os.getenv("YF_INSECURE_SSL", "1") == "1"


def build_yfinance_session():
    return curl_requests.Session(
        impersonate="chrome",
        verify=not INSECURE_SSL,
    )


def normalize_ticker(ticker: str) -> str:
    normalized = ticker.strip()
    return COMPANY_TO_TICKER.get(normalized.lower(), normalized.upper())


def get_yf_stock_info(ticker: str):
    try:
        normalized_ticker = normalize_ticker(ticker)
        stock = yf.Ticker(normalized_ticker, session=build_yfinance_session())
        info_dict = dict(stock.fast_info)

        if not info_dict:
            return f"{normalized_ticker} 정보를 찾을 수 없습니다."

        info_dict["requested_ticker"] = ticker
        info_dict["resolved_ticker"] = normalized_ticker
        return str(info_dict)
    except Exception as error:
        return f"주식 정보 조회 오류: {error}"


def get_current_time(timezone: str = "Asia/Seoul"):
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"{now} {timezone}"
    except Exception as error:
        return f"시간 조회 오류: {error}"


tools = [
    {
        "type": "function",
        "name": "get_current_time",
        "description": "사용자가 현재 시각이나 날짜를 직접 물어보면 호출하세요.",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "현재 날짜와 시간을 반환할 시간대입니다. 예: Asia/Seoul",
                },
            },
            "required": ["timezone"],
        },
    },
    {
        "type": "function",
        "name": "get_yf_stock_info",
        "description": (
            "사용자가 주식 가격이나 종목 정보를 물어보면 호출하세요. "
            "ticker에는 AAPL, TSLA 같은 티커나 Apple, Tesla, 애플, 삼성 같은 회사명을 넣을 수 있습니다."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "조회할 종목의 티커 또는 회사명입니다. 예: MSFT, 애플, 삼성전자",
                },
            },
            "required": ["ticker"],
        },
    },
]


if __name__ == "__main__":
    print(f"현재 시각: {get_current_time('Asia/Seoul')}")
    print("--- 삼성 주가 정보 예시 ---")
    print(get_yf_stock_info("삼성"))
