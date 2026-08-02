import json
from datetime import datetime
from pathlib import Path
from typing import Any


LLM_DIR = Path(__file__).resolve().parent.parent
JSON_DIR = LLM_DIR / "json"
DB_FILE = JSON_DIR / "pdf_analysis_history.json"


def init_pdf_db() -> None:
    # 기록 파일이 없으면 기본 구조로 생성합니다.
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    if not DB_FILE.exists():
        save_data({"analyses": []})


def load_data() -> dict[str, Any]:
    # 키가 빠진 오래된 파일도 현재 구조로 보정해서 읽습니다.
    init_pdf_db()
    text = DB_FILE.read_text(encoding="utf-8")
    data = json.loads(text)
    data.setdefault("analyses", [])
    return data


def save_data(data: dict[str, Any]) -> None:
    DB_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_analyses() -> list[dict[str, Any]]:
    return load_data()["analyses"]


def save_analysis(
    file_name: str,
    page_count: int,
    extracted_text: str,
    summary: str,
) -> None:
    # 분석 이력을 시간과 함께 누적 저장합니다.
    data = load_data()
    data["analyses"].append(
        {
            "file_name": file_name,
            "page_count": page_count,
            "extracted_text": extracted_text,
            "summary": summary,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
    )
    save_data(data)


def clear_analyses() -> None:
    # 앱에서 기록 초기화를 누르면 이 함수가 호출됩니다.
    save_data({"analyses": []})
